/* Copyright 2022 The OpenXLA Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef XLA_PJRT_PJRT_FUTURE_H_
#define XLA_PJRT_PJRT_FUTURE_H_

#include <algorithm>
#include <atomic>
#include <cstdint>
#include <functional>
#include <memory>
#include <type_traits>
#include <utility>

#include "absl/status/status.h"
#include "absl/types/span.h"
#include "xla/tsl/concurrency/async_value.h"
#include "xla/tsl/concurrency/async_value_ref.h"
#include "xla/tsl/concurrency/ref_count.h"
#include "tsl/platform/logging.h"

namespace xla {

template <class T = void>
class PjRtFuture;

namespace internal {
template <class T, bool unique>
class PjRtFutureBase;
}

// Returns a `PjRtFuture` that will be successful if all `futures` complete
// successfully, or return a first encountered error.
PjRtFuture<> JoinFutures(absl::Span<const PjRtFuture<>> futures);

// An RAII event that a caller can use to tell the PjRtClient about asynchronous
// actions outside PjRt.
//
// A ScopedAsyncTrackingEvent can be generated by the caller by calling a method
// on PjRtDevice, and the creation of a ScopedAsyncTrackingEvent tells the
// PjRtClient that the client is creating some outstanding asynchronous work
// that depends on activities happening on the PjRtDevice.
//
// The caller can indicate that a ScopedAsyncTrackingEvent event cannot complete
// until after some PjRtFuture becomes ready, by calling
// future.AssertHappensBefore(event).
//
// The caller indicates that the work tracked by the ScopedAsyncTrackingEvent
// has completed by letting the event go out of scope.
//
// ScopedAsyncTrackingEvents are used by some PjRtClient implementations to
// monitor system-wide dependencies.
class ScopedAsyncTrackingEvent {
 public:
  virtual ~ScopedAsyncTrackingEvent() = default;

 private:
  template <class T, bool unique>
  friend class internal::PjRtFutureBase;

  // Indicates that the ScopedAsyncTrackingEvent won't complete until dependency
  // becomes available. Called only by PjRtFuture.
  virtual void AddDependency(tsl::RCReference<tsl::AsyncValue> dependency) = 0;
};

// Helpers for using PjRtFutures.
struct PjRtFutureHelpers {
 public:
  // Keys that are returned by an implementation-specific handler when a client
  // starts to block on a promise.
  //
  // For now, contains a single UID that can be used to identify a TraceMe, but
  // made extensible to allow support for other profilers such as endoscope.
  struct ProfilingKeys {
    uint64_t traceme_context_id = -1;
  };

  // Signature of handler called by the PjRtFuture class before it starts to
  // block a thread.
  using OnBlockStartFn = std::function<ProfilingKeys()>;

  // Signature of handler called by the PjRtFuture class after it finishes
  // blocking a thread.
  using OnBlockEndFn = std::function<void(ProfilingKeys)>;
};

namespace internal {

// Detects absl::StatusOr<T> specializations to disable them for PjRtFuture<T>.
template <typename T>
struct IsStatusOr : public std::false_type {};
template <typename T>
struct IsStatusOr<absl::StatusOr<T>> : public std::true_type {};

// A base class to conditionally disable copy constructor and assignment for a
// PjRtFuture<T> (by default we always disable copy constructor when `T` is not
// copyable), which makes PjRtFuture<T> an `std::unique_ptr`-like container for
// move-only types.
template <bool unique>
class PjRtFutureMoveControl;

template <>
class PjRtFutureMoveControl</*unique=*/true> {
 protected:
  PjRtFutureMoveControl() = default;

  PjRtFutureMoveControl(const PjRtFutureMoveControl&) = delete;
  PjRtFutureMoveControl& operator=(const PjRtFutureMoveControl&) = delete;

  PjRtFutureMoveControl(PjRtFutureMoveControl&&) = default;
  PjRtFutureMoveControl& operator=(PjRtFutureMoveControl&&) = default;
};

template <>
class PjRtFutureMoveControl</*unique=*/false> {
 protected:
  PjRtFutureMoveControl() = default;

  PjRtFutureMoveControl(const PjRtFutureMoveControl&) = default;
  PjRtFutureMoveControl& operator=(const PjRtFutureMoveControl&) = default;

  PjRtFutureMoveControl(PjRtFutureMoveControl&&) = default;
  PjRtFutureMoveControl& operator=(PjRtFutureMoveControl&&) = default;
};

// A base class for a stateful future PjRtFuture<T> and a stateless future
// PjRtFuture<>. If `unique` is true, PjRtFuture derived from this class acts
// as a move-only type and the value can be passed to the caller only using move
// assignment (applied to Await and OnReady APIs).
template <typename T, bool unique = !std::is_copy_constructible_v<T>>
class PjRtFutureBase : public PjRtFutureMoveControl<unique> {
 protected:
  // A protected constructor that hides AsyncValueRef implementation detail
  // from the end users of PjRtFuture and Promise. Must not be made public!
  PjRtFutureBase(tsl::AsyncValueRef<T> promise,
                 PjRtFutureHelpers::OnBlockStartFn on_block_start,
                 PjRtFutureHelpers::OnBlockEndFn on_block_end)
      : promise_(std::move(promise)),
        on_block_start_(std::move(on_block_start)),
        on_block_end_(std::move(on_block_end)) {}

 public:
  PjRtFutureBase() = default;

  // Constructor for an already-available PjRtFuture.
  //
  // Typically used to eagerly return error values when async work will not
  // be enqueued, e.g., due to invalid arguments.
  explicit PjRtFutureBase(
      T t, PjRtFutureHelpers::OnBlockStartFn on_block_start = nullptr,
      PjRtFutureHelpers::OnBlockEndFn on_block_end = nullptr)
      : PjRtFutureBase(tsl::MakeAvailableAsyncValueRef<T>(std::move(t)),
                       std::move(on_block_start), std::move(on_block_end)) {}

  bool IsValid() const { return promise_ != nullptr; }

  // Two functions exist to know whether the future is ready, to accommodate
  // the fact some backends (e.g. distributed ones) could take a non-trivial
  // time to check the state of a future.
  //
  // `IsReady()` is guaranteed to return true if the future became ready
  // before `IsReady()` was called. `IsReady()` will return immediately if a
  // call to `Await()` has already returned, or any callback passed to
  // `OnReady` has already been triggered. Otherwise IsReady() may block for
  // the duration of a network message on some backends.
  bool IsReady() {
    CHECK(IsValid());
    return promise_.IsAvailable();
  }
  // `IsKnownReady()` is guaranteed to return immediately. `IsKnownReady()` will
  // always return true if a call to `Await()` has already returned, or any
  // callback passed to `OnReady` has already been triggered. Otherwise,
  // `IsKnownReady()` may return false in some cases in which the future was
  // ready before `IsKnownReady()` was called.
  bool IsKnownReady() {
    CHECK(IsValid());
    return promise_.IsAvailable();
  }

  // Indicates that event will not complete until after this becomes ready.
  //
  // May safely be called with event==nullptr in which case AssertHappensBefore
  // has no effect.
  void AssertHappensBefore(ScopedAsyncTrackingEvent* event) {
    CHECK(IsValid());
    if (event) event->AddDependency(promise_.CopyRCRef());
  }

 protected:
  static constexpr bool is_unique() { return unique; }

  // PjRtFuture<T>::Promise provides a facility to store a value or an error
  // that is later acquired asynchronously via a PjRtFuture<T> constructed from
  // the promise object. Note that the promise object is meant to be used only
  // once (set value or error).
  class Promise {
   public:
    Promise() = default;

    Promise(Promise&& other) = default;
    Promise& operator=(Promise&& other) = default;

    Promise(const Promise& other) = default;
    Promise& operator=(const Promise& other) = default;

    operator bool() const { return static_cast<bool>(promise_); }  // NOLINT

   protected:
    explicit Promise(tsl::AsyncValueRef<T> promise)
        : promise_(std::move(promise)) {}

    template <typename... Args>
    void emplace(Args&&... args) const {
      DCHECK(promise_) << "Promise must wrap an async value";
      promise_.template emplace<T>(std::forward<Args>(args)...);
    }

    // Releases the underlying AsyncValueRef container to the caller.
    tsl::AsyncValueRef<T> release() { return std::move(promise_); }

    // Returns a pointer to the underlying AsyncValue that can be used to
    // track completion of a promise. It is undefined behavior to access the
    // value stored in the AsyncValue.
    tsl::AsyncValue* async_value() const { return promise_.GetAsyncValue(); }

#ifndef NDEBUG
    int64_t AddFuture() { return num_futures_->fetch_add(1); }
#endif

   private:
    tsl::AsyncValueRef<T> promise_;

#ifndef NDEBUG
    // In debug builds we track the number of futures created from a promise to
    // detect when a promise for a move-only type can be accidentally shared by
    // multiple futures. We wrap the counter into shared pointer because promise
    // for a unique future is still copyable, but only one future can be created
    // from all the copies.
    std::shared_ptr<std::atomic<int64_t>> num_futures_ =
        std::make_shared<std::atomic<int64_t>>(0);
#endif
  };

  PjRtFutureHelpers::ProfilingKeys OnBlockStart() const {
    return on_block_start_ ? on_block_start_()
                           : PjRtFutureHelpers::ProfilingKeys();
  }

  void OnBlockEnd(PjRtFutureHelpers::ProfilingKeys keys) const {
    if (on_block_end_) on_block_end_(std::move(keys));
  }

  // Blocks the calling thread until the future is ready.
  void BlockUntilReady() const {
    CHECK(IsValid());
    if (!promise_.IsAvailable()) {
      PjRtFutureHelpers::ProfilingKeys keys = OnBlockStart();
      tsl::BlockUntilReady(promise_);
      OnBlockEnd(std::move(keys));
    }
    DCHECK(promise_.IsConcrete());
  }

  // Blocks the calling thread until the future is ready, then returns the
  // final value.
  const T& Await() const& {
    BlockUntilReady();
    return *promise_;
  }

  // Blocks the calling thread until the future is ready, then returns the
  // final value.
  std::conditional_t<unique, T, const T&> Await() && {
    BlockUntilReady();

    if constexpr (unique) {
      return std::move(*promise_);
    } else {
      // We can't move from the promise to the caller because for non-unique
      // futures we can have multiple copies of the PjRtFuture sharing the
      // same underlying promise object.
      return *promise_;
    }
  }

  // Registers callback to be called once the promise is ready, with the final
  // value.
  //
  // callback may be called on an internal system thread or the calling thread.
  // The client should avoid any potentially re-entrant API calls within the
  // callback, for example by using the callback to enqueue work on a
  // client-owned threadpool.
  template <typename F, std::enable_if_t<std::is_invocable_v<F, const T&> &&
                                         !unique>* = nullptr>
  void OnReady(F&& f) const& {
    CHECK(IsValid());
    promise_.AndThen(
        [promise = promise_.AsPtr(), f = std::forward<F>(f)]() mutable {
          DCHECK(promise.IsConcrete());
          f(*promise);
        });
  }

  // Registers callback to be called once the promise is ready, with the final
  // value.
  //
  // callback may be called on an internal system thread or the calling thread.
  // The client should avoid any potentially re-entrant API calls within the
  // callback, for example by using the callback to enqueue work on a
  // client-owned threadpool.
  template <
      typename F,
      std::enable_if_t<unique ? std::is_invocable_v<F, T>
                              : std::is_invocable_v<F, const T&>>* = nullptr>
  void OnReady(F&& f) && {
    CHECK(IsValid());
    promise_.AndThen(
        [promise = promise_.AsPtr(), f = std::forward<F>(f)]() mutable {
          DCHECK(promise.IsConcrete());
          if constexpr (unique) {
            f(std::move(*promise));
          } else {
            // We can't move from the promise to the caller because for
            // non-unique futures we can have multiple copies of the PjRtFuture
            // sharing the same underlying promise object.
            f(*promise);
          }
        });
  }

 private:
  tsl::AsyncValueRef<T> promise_;

  // Function that is called before a thread starts blocking on the promise.
  PjRtFutureHelpers::OnBlockStartFn on_block_start_;
  // Function that is called after a thread finishes blocking on the promise.
  PjRtFutureHelpers::OnBlockEndFn on_block_end_;
};

}  // namespace internal

// PjRtFuture<T> is a simple future that is returned by PjRt APIs that
// enqueue asynchronous work, reporting a value of type T when the work is
// complete.
//
// PjRtFuture can be used by the client to wait for work to complete, either via
// a blocking call or a callback.
//
// The implementation wraps a tsl::AsyncValueRef<T>, but we prefer to
// encapsulate the AVR rather than returning it directly for three reasons.
//
// First, in contrast to AsyncValueRef which has a smart-pointer semantics,
// future has more of a value semantics, i.e. future of a move-only type also
// is a move-only type. You can think of a move-only (unique) future as a box to
// pass a value of type T between asynchronous producer/consumer: you can open
// the box once to put the value into it and you can open the box only once to
// take the value out of it. For copyable types PjRtFuture<T> is a copyable
// type, although all copies share the same underlying value.
//
// Second, we want to retain portability in case a future implementation moves
// away from AsyncValueRef ---- we don't want clients to call arbitrary
// AsyncValueRef APIs.
//
// Third, we want to export different semantics, for example we support
// integration between blocking and profiling (e.g., TraceMe).
template <class T>
class PjRtFuture : public internal::PjRtFutureBase<absl::StatusOr<T>> {
  using Base = internal::PjRtFutureBase<absl::StatusOr<T>>;

  static_assert(!std::is_same_v<T, absl::Status>,
                "Use PjRtFuture<> specialization for stateless futures");

  static_assert(
      !internal::IsStatusOr<T>::value,
      "PjRtFuture<T> already has an implicit absl::StatusOr<T> semantics");

 public:
  class Promise : public Base::Promise {
   public:
    using Base::Promise::Promise;

    // Sets the value of the promise. Must be called at most once.
    //
    // After Set is called, value will be delivered to waiters on the PjRtFuture
    // constructed from a promise, via blocking or callbacks.
    void Set(absl::StatusOr<T> value) {
      Base::Promise::emplace(std::move(value));
    }

   private:
    friend class PjRtFuture<T>;
  };

  // Returns a Promise that can be used to construct a PjRtFuture, and then Set
  // later.
  static Promise CreatePromise() {
    return Promise(tsl::MakeUnconstructedAsyncValueRef<absl::StatusOr<T>>());
  }

  // Bring PjRtFutureBase constructors in scope.
  using Base::Base;

  // Constructor for unavailable future that will be fulfilled later via the
  // promise object.
  //
  // - on_block_start is called before Await starts to block.
  //  - on_block_end is called after Await finishes blocking.
  explicit PjRtFuture(
      Promise promise,
      PjRtFutureHelpers::OnBlockStartFn on_block_start = nullptr,
      PjRtFutureHelpers::OnBlockEndFn on_block_end = nullptr)
      : Base(promise.release(), std::move(on_block_start),
             std::move(on_block_end)) {
#ifndef NDEBUG
    if constexpr (Base::is_unique()) {
      DCHECK_EQ(promise.AddFuture(), 0)
          << "Unique PjRtFuture cannot share a promise object";
    }
#endif
  }

  using Base::Await;
  using Base::OnReady;
};

// PjRtFuture<void> specialization for communicating stateless events.
//
// See PjRtFuture<T> documentation above for more details.
template <>
class PjRtFuture<void> : public internal::PjRtFutureBase<absl::Status> {
  using Base = internal::PjRtFutureBase<absl::Status>;

 public:
  class Promise : public Base::Promise {
   public:
    using Base::Promise::async_value;
    using Base::Promise::Promise;

    // Sets the promise completed with a given status. Must be called at most
    // once.
    //
    // After Set is called, completion event will be delivered to waiters on the
    // PjRtFuture constructed from a promise, via blocking or callbacks.
    void Set(absl::Status status = absl::OkStatus()) {
      Base::Promise::emplace(std::move(status));
    }

   private:
    friend class PjRtFuture<void>;
  };

  // Returns a Promise that can be used to construct a PjRtFuture, and then Set
  // later.
  static Promise CreatePromise() {
    return Promise(tsl::MakeUnconstructedAsyncValueRef<absl::Status>());
  }

  // Bring PjRtFutureBase constructors in scope.
  using Base::Base;

  // Constructor for unavailable future that will be fulfilled later via the
  // promise object.
  //
  // - on_block_start is called before Await starts to block.
  //  - on_block_end is called after Await finishes blocking.
  explicit PjRtFuture(
      Promise promise,
      PjRtFutureHelpers::OnBlockStartFn on_block_start = nullptr,
      PjRtFutureHelpers::OnBlockEndFn on_block_end = nullptr)
      : Base(promise.release(), std::move(on_block_start),
             std::move(on_block_end)) {}

  using Base::Await;
  using Base::OnReady;
};

}  // namespace xla

#endif  // XLA_PJRT_PJRT_FUTURE_H_
