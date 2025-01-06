// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: tsl/profiler/protobuf/profiled_instructions.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_tsl_2fprofiler_2fprotobuf_2fprofiled_5finstructions_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_tsl_2fprofiler_2fprotobuf_2fprofiled_5finstructions_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021009 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_tsl_2fprofiler_2fprotobuf_2fprofiled_5finstructions_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_tsl_2fprofiler_2fprotobuf_2fprofiled_5finstructions_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_tsl_2fprofiler_2fprotobuf_2fprofiled_5finstructions_2eproto;
namespace tensorflow {
namespace profiler {
class ProfiledInstructionsProto;
struct ProfiledInstructionsProtoDefaultTypeInternal;
extern ProfiledInstructionsProtoDefaultTypeInternal _ProfiledInstructionsProto_default_instance_;
class ProfiledInstructionsProto_InstructionCost;
struct ProfiledInstructionsProto_InstructionCostDefaultTypeInternal;
extern ProfiledInstructionsProto_InstructionCostDefaultTypeInternal _ProfiledInstructionsProto_InstructionCost_default_instance_;
class ProfiledInstructionsProto_Latency;
struct ProfiledInstructionsProto_LatencyDefaultTypeInternal;
extern ProfiledInstructionsProto_LatencyDefaultTypeInternal _ProfiledInstructionsProto_Latency_default_instance_;
}  // namespace profiler
}  // namespace tensorflow
PROTOBUF_NAMESPACE_OPEN
template<> ::tensorflow::profiler::ProfiledInstructionsProto* Arena::CreateMaybeMessage<::tensorflow::profiler::ProfiledInstructionsProto>(Arena*);
template<> ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost* Arena::CreateMaybeMessage<::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost>(Arena*);
template<> ::tensorflow::profiler::ProfiledInstructionsProto_Latency* Arena::CreateMaybeMessage<::tensorflow::profiler::ProfiledInstructionsProto_Latency>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace tensorflow {
namespace profiler {

// ===================================================================

class ProfiledInstructionsProto_InstructionCost final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.profiler.ProfiledInstructionsProto.InstructionCost) */ {
 public:
  inline ProfiledInstructionsProto_InstructionCost() : ProfiledInstructionsProto_InstructionCost(nullptr) {}
  ~ProfiledInstructionsProto_InstructionCost() override;
  explicit PROTOBUF_CONSTEXPR ProfiledInstructionsProto_InstructionCost(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  ProfiledInstructionsProto_InstructionCost(const ProfiledInstructionsProto_InstructionCost& from);
  ProfiledInstructionsProto_InstructionCost(ProfiledInstructionsProto_InstructionCost&& from) noexcept
    : ProfiledInstructionsProto_InstructionCost() {
    *this = ::std::move(from);
  }

  inline ProfiledInstructionsProto_InstructionCost& operator=(const ProfiledInstructionsProto_InstructionCost& from) {
    CopyFrom(from);
    return *this;
  }
  inline ProfiledInstructionsProto_InstructionCost& operator=(ProfiledInstructionsProto_InstructionCost&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const ProfiledInstructionsProto_InstructionCost& default_instance() {
    return *internal_default_instance();
  }
  static inline const ProfiledInstructionsProto_InstructionCost* internal_default_instance() {
    return reinterpret_cast<const ProfiledInstructionsProto_InstructionCost*>(
               &_ProfiledInstructionsProto_InstructionCost_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(ProfiledInstructionsProto_InstructionCost& a, ProfiledInstructionsProto_InstructionCost& b) {
    a.Swap(&b);
  }
  inline void Swap(ProfiledInstructionsProto_InstructionCost* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(ProfiledInstructionsProto_InstructionCost* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  ProfiledInstructionsProto_InstructionCost* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<ProfiledInstructionsProto_InstructionCost>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const ProfiledInstructionsProto_InstructionCost& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const ProfiledInstructionsProto_InstructionCost& from) {
    ProfiledInstructionsProto_InstructionCost::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(ProfiledInstructionsProto_InstructionCost* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.profiler.ProfiledInstructionsProto.InstructionCost";
  }
  protected:
  explicit ProfiledInstructionsProto_InstructionCost(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kNameFieldNumber = 1,
    kCostUsFieldNumber = 2,
  };
  // string name = 1;
  void clear_name();
  const std::string& name() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_name(ArgT0&& arg0, ArgT... args);
  std::string* mutable_name();
  PROTOBUF_NODISCARD std::string* release_name();
  void set_allocated_name(std::string* name);
  private:
  const std::string& _internal_name() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_name(const std::string& value);
  std::string* _internal_mutable_name();
  public:

  // double cost_us = 2;
  void clear_cost_us();
  double cost_us() const;
  void set_cost_us(double value);
  private:
  double _internal_cost_us() const;
  void _internal_set_cost_us(double value);
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.profiler.ProfiledInstructionsProto.InstructionCost)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr name_;
    double cost_us_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tsl_2fprofiler_2fprotobuf_2fprofiled_5finstructions_2eproto;
};
// -------------------------------------------------------------------

class ProfiledInstructionsProto_Latency final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.profiler.ProfiledInstructionsProto.Latency) */ {
 public:
  inline ProfiledInstructionsProto_Latency() : ProfiledInstructionsProto_Latency(nullptr) {}
  ~ProfiledInstructionsProto_Latency() override;
  explicit PROTOBUF_CONSTEXPR ProfiledInstructionsProto_Latency(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  ProfiledInstructionsProto_Latency(const ProfiledInstructionsProto_Latency& from);
  ProfiledInstructionsProto_Latency(ProfiledInstructionsProto_Latency&& from) noexcept
    : ProfiledInstructionsProto_Latency() {
    *this = ::std::move(from);
  }

  inline ProfiledInstructionsProto_Latency& operator=(const ProfiledInstructionsProto_Latency& from) {
    CopyFrom(from);
    return *this;
  }
  inline ProfiledInstructionsProto_Latency& operator=(ProfiledInstructionsProto_Latency&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const ProfiledInstructionsProto_Latency& default_instance() {
    return *internal_default_instance();
  }
  static inline const ProfiledInstructionsProto_Latency* internal_default_instance() {
    return reinterpret_cast<const ProfiledInstructionsProto_Latency*>(
               &_ProfiledInstructionsProto_Latency_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(ProfiledInstructionsProto_Latency& a, ProfiledInstructionsProto_Latency& b) {
    a.Swap(&b);
  }
  inline void Swap(ProfiledInstructionsProto_Latency* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(ProfiledInstructionsProto_Latency* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  ProfiledInstructionsProto_Latency* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<ProfiledInstructionsProto_Latency>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const ProfiledInstructionsProto_Latency& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const ProfiledInstructionsProto_Latency& from) {
    ProfiledInstructionsProto_Latency::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(ProfiledInstructionsProto_Latency* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.profiler.ProfiledInstructionsProto.Latency";
  }
  protected:
  explicit ProfiledInstructionsProto_Latency(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kSourceFieldNumber = 1,
    kTargetFieldNumber = 2,
    kLatencyUsFieldNumber = 3,
  };
  // string source = 1;
  void clear_source();
  const std::string& source() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_source(ArgT0&& arg0, ArgT... args);
  std::string* mutable_source();
  PROTOBUF_NODISCARD std::string* release_source();
  void set_allocated_source(std::string* source);
  private:
  const std::string& _internal_source() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_source(const std::string& value);
  std::string* _internal_mutable_source();
  public:

  // string target = 2;
  void clear_target();
  const std::string& target() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_target(ArgT0&& arg0, ArgT... args);
  std::string* mutable_target();
  PROTOBUF_NODISCARD std::string* release_target();
  void set_allocated_target(std::string* target);
  private:
  const std::string& _internal_target() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_target(const std::string& value);
  std::string* _internal_mutable_target();
  public:

  // double latency_us = 3;
  void clear_latency_us();
  double latency_us() const;
  void set_latency_us(double value);
  private:
  double _internal_latency_us() const;
  void _internal_set_latency_us(double value);
  public:

  // @@protoc_insertion_point(class_scope:tensorflow.profiler.ProfiledInstructionsProto.Latency)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr source_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr target_;
    double latency_us_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tsl_2fprofiler_2fprotobuf_2fprofiled_5finstructions_2eproto;
};
// -------------------------------------------------------------------

class ProfiledInstructionsProto final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:tensorflow.profiler.ProfiledInstructionsProto) */ {
 public:
  inline ProfiledInstructionsProto() : ProfiledInstructionsProto(nullptr) {}
  ~ProfiledInstructionsProto() override;
  explicit PROTOBUF_CONSTEXPR ProfiledInstructionsProto(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  ProfiledInstructionsProto(const ProfiledInstructionsProto& from);
  ProfiledInstructionsProto(ProfiledInstructionsProto&& from) noexcept
    : ProfiledInstructionsProto() {
    *this = ::std::move(from);
  }

  inline ProfiledInstructionsProto& operator=(const ProfiledInstructionsProto& from) {
    CopyFrom(from);
    return *this;
  }
  inline ProfiledInstructionsProto& operator=(ProfiledInstructionsProto&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const ProfiledInstructionsProto& default_instance() {
    return *internal_default_instance();
  }
  static inline const ProfiledInstructionsProto* internal_default_instance() {
    return reinterpret_cast<const ProfiledInstructionsProto*>(
               &_ProfiledInstructionsProto_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    2;

  friend void swap(ProfiledInstructionsProto& a, ProfiledInstructionsProto& b) {
    a.Swap(&b);
  }
  inline void Swap(ProfiledInstructionsProto* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(ProfiledInstructionsProto* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  ProfiledInstructionsProto* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<ProfiledInstructionsProto>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const ProfiledInstructionsProto& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const ProfiledInstructionsProto& from) {
    ProfiledInstructionsProto::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(ProfiledInstructionsProto* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "tensorflow.profiler.ProfiledInstructionsProto";
  }
  protected:
  explicit ProfiledInstructionsProto(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  typedef ProfiledInstructionsProto_InstructionCost InstructionCost;
  typedef ProfiledInstructionsProto_Latency Latency;

  // accessors -------------------------------------------------------

  enum : int {
    kCostsFieldNumber = 1,
    kLatenciesFieldNumber = 2,
  };
  // repeated .tensorflow.profiler.ProfiledInstructionsProto.InstructionCost costs = 1;
  int costs_size() const;
  private:
  int _internal_costs_size() const;
  public:
  void clear_costs();
  ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost* mutable_costs(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost >*
      mutable_costs();
  private:
  const ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost& _internal_costs(int index) const;
  ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost* _internal_add_costs();
  public:
  const ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost& costs(int index) const;
  ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost* add_costs();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost >&
      costs() const;

  // repeated .tensorflow.profiler.ProfiledInstructionsProto.Latency latencies = 2;
  int latencies_size() const;
  private:
  int _internal_latencies_size() const;
  public:
  void clear_latencies();
  ::tensorflow::profiler::ProfiledInstructionsProto_Latency* mutable_latencies(int index);
  ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::profiler::ProfiledInstructionsProto_Latency >*
      mutable_latencies();
  private:
  const ::tensorflow::profiler::ProfiledInstructionsProto_Latency& _internal_latencies(int index) const;
  ::tensorflow::profiler::ProfiledInstructionsProto_Latency* _internal_add_latencies();
  public:
  const ::tensorflow::profiler::ProfiledInstructionsProto_Latency& latencies(int index) const;
  ::tensorflow::profiler::ProfiledInstructionsProto_Latency* add_latencies();
  const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::profiler::ProfiledInstructionsProto_Latency >&
      latencies() const;

  // @@protoc_insertion_point(class_scope:tensorflow.profiler.ProfiledInstructionsProto)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost > costs_;
    ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::profiler::ProfiledInstructionsProto_Latency > latencies_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_tsl_2fprofiler_2fprotobuf_2fprofiled_5finstructions_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// ProfiledInstructionsProto_InstructionCost

// string name = 1;
inline void ProfiledInstructionsProto_InstructionCost::clear_name() {
  _impl_.name_.ClearToEmpty();
}
inline const std::string& ProfiledInstructionsProto_InstructionCost::name() const {
  // @@protoc_insertion_point(field_get:tensorflow.profiler.ProfiledInstructionsProto.InstructionCost.name)
  return _internal_name();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void ProfiledInstructionsProto_InstructionCost::set_name(ArgT0&& arg0, ArgT... args) {
 
 _impl_.name_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.profiler.ProfiledInstructionsProto.InstructionCost.name)
}
inline std::string* ProfiledInstructionsProto_InstructionCost::mutable_name() {
  std::string* _s = _internal_mutable_name();
  // @@protoc_insertion_point(field_mutable:tensorflow.profiler.ProfiledInstructionsProto.InstructionCost.name)
  return _s;
}
inline const std::string& ProfiledInstructionsProto_InstructionCost::_internal_name() const {
  return _impl_.name_.Get();
}
inline void ProfiledInstructionsProto_InstructionCost::_internal_set_name(const std::string& value) {
  
  _impl_.name_.Set(value, GetArenaForAllocation());
}
inline std::string* ProfiledInstructionsProto_InstructionCost::_internal_mutable_name() {
  
  return _impl_.name_.Mutable(GetArenaForAllocation());
}
inline std::string* ProfiledInstructionsProto_InstructionCost::release_name() {
  // @@protoc_insertion_point(field_release:tensorflow.profiler.ProfiledInstructionsProto.InstructionCost.name)
  return _impl_.name_.Release();
}
inline void ProfiledInstructionsProto_InstructionCost::set_allocated_name(std::string* name) {
  if (name != nullptr) {
    
  } else {
    
  }
  _impl_.name_.SetAllocated(name, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.name_.IsDefault()) {
    _impl_.name_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.profiler.ProfiledInstructionsProto.InstructionCost.name)
}

// double cost_us = 2;
inline void ProfiledInstructionsProto_InstructionCost::clear_cost_us() {
  _impl_.cost_us_ = 0;
}
inline double ProfiledInstructionsProto_InstructionCost::_internal_cost_us() const {
  return _impl_.cost_us_;
}
inline double ProfiledInstructionsProto_InstructionCost::cost_us() const {
  // @@protoc_insertion_point(field_get:tensorflow.profiler.ProfiledInstructionsProto.InstructionCost.cost_us)
  return _internal_cost_us();
}
inline void ProfiledInstructionsProto_InstructionCost::_internal_set_cost_us(double value) {
  
  _impl_.cost_us_ = value;
}
inline void ProfiledInstructionsProto_InstructionCost::set_cost_us(double value) {
  _internal_set_cost_us(value);
  // @@protoc_insertion_point(field_set:tensorflow.profiler.ProfiledInstructionsProto.InstructionCost.cost_us)
}

// -------------------------------------------------------------------

// ProfiledInstructionsProto_Latency

// string source = 1;
inline void ProfiledInstructionsProto_Latency::clear_source() {
  _impl_.source_.ClearToEmpty();
}
inline const std::string& ProfiledInstructionsProto_Latency::source() const {
  // @@protoc_insertion_point(field_get:tensorflow.profiler.ProfiledInstructionsProto.Latency.source)
  return _internal_source();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void ProfiledInstructionsProto_Latency::set_source(ArgT0&& arg0, ArgT... args) {
 
 _impl_.source_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.profiler.ProfiledInstructionsProto.Latency.source)
}
inline std::string* ProfiledInstructionsProto_Latency::mutable_source() {
  std::string* _s = _internal_mutable_source();
  // @@protoc_insertion_point(field_mutable:tensorflow.profiler.ProfiledInstructionsProto.Latency.source)
  return _s;
}
inline const std::string& ProfiledInstructionsProto_Latency::_internal_source() const {
  return _impl_.source_.Get();
}
inline void ProfiledInstructionsProto_Latency::_internal_set_source(const std::string& value) {
  
  _impl_.source_.Set(value, GetArenaForAllocation());
}
inline std::string* ProfiledInstructionsProto_Latency::_internal_mutable_source() {
  
  return _impl_.source_.Mutable(GetArenaForAllocation());
}
inline std::string* ProfiledInstructionsProto_Latency::release_source() {
  // @@protoc_insertion_point(field_release:tensorflow.profiler.ProfiledInstructionsProto.Latency.source)
  return _impl_.source_.Release();
}
inline void ProfiledInstructionsProto_Latency::set_allocated_source(std::string* source) {
  if (source != nullptr) {
    
  } else {
    
  }
  _impl_.source_.SetAllocated(source, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.source_.IsDefault()) {
    _impl_.source_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.profiler.ProfiledInstructionsProto.Latency.source)
}

// string target = 2;
inline void ProfiledInstructionsProto_Latency::clear_target() {
  _impl_.target_.ClearToEmpty();
}
inline const std::string& ProfiledInstructionsProto_Latency::target() const {
  // @@protoc_insertion_point(field_get:tensorflow.profiler.ProfiledInstructionsProto.Latency.target)
  return _internal_target();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void ProfiledInstructionsProto_Latency::set_target(ArgT0&& arg0, ArgT... args) {
 
 _impl_.target_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:tensorflow.profiler.ProfiledInstructionsProto.Latency.target)
}
inline std::string* ProfiledInstructionsProto_Latency::mutable_target() {
  std::string* _s = _internal_mutable_target();
  // @@protoc_insertion_point(field_mutable:tensorflow.profiler.ProfiledInstructionsProto.Latency.target)
  return _s;
}
inline const std::string& ProfiledInstructionsProto_Latency::_internal_target() const {
  return _impl_.target_.Get();
}
inline void ProfiledInstructionsProto_Latency::_internal_set_target(const std::string& value) {
  
  _impl_.target_.Set(value, GetArenaForAllocation());
}
inline std::string* ProfiledInstructionsProto_Latency::_internal_mutable_target() {
  
  return _impl_.target_.Mutable(GetArenaForAllocation());
}
inline std::string* ProfiledInstructionsProto_Latency::release_target() {
  // @@protoc_insertion_point(field_release:tensorflow.profiler.ProfiledInstructionsProto.Latency.target)
  return _impl_.target_.Release();
}
inline void ProfiledInstructionsProto_Latency::set_allocated_target(std::string* target) {
  if (target != nullptr) {
    
  } else {
    
  }
  _impl_.target_.SetAllocated(target, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.target_.IsDefault()) {
    _impl_.target_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:tensorflow.profiler.ProfiledInstructionsProto.Latency.target)
}

// double latency_us = 3;
inline void ProfiledInstructionsProto_Latency::clear_latency_us() {
  _impl_.latency_us_ = 0;
}
inline double ProfiledInstructionsProto_Latency::_internal_latency_us() const {
  return _impl_.latency_us_;
}
inline double ProfiledInstructionsProto_Latency::latency_us() const {
  // @@protoc_insertion_point(field_get:tensorflow.profiler.ProfiledInstructionsProto.Latency.latency_us)
  return _internal_latency_us();
}
inline void ProfiledInstructionsProto_Latency::_internal_set_latency_us(double value) {
  
  _impl_.latency_us_ = value;
}
inline void ProfiledInstructionsProto_Latency::set_latency_us(double value) {
  _internal_set_latency_us(value);
  // @@protoc_insertion_point(field_set:tensorflow.profiler.ProfiledInstructionsProto.Latency.latency_us)
}

// -------------------------------------------------------------------

// ProfiledInstructionsProto

// repeated .tensorflow.profiler.ProfiledInstructionsProto.InstructionCost costs = 1;
inline int ProfiledInstructionsProto::_internal_costs_size() const {
  return _impl_.costs_.size();
}
inline int ProfiledInstructionsProto::costs_size() const {
  return _internal_costs_size();
}
inline void ProfiledInstructionsProto::clear_costs() {
  _impl_.costs_.Clear();
}
inline ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost* ProfiledInstructionsProto::mutable_costs(int index) {
  // @@protoc_insertion_point(field_mutable:tensorflow.profiler.ProfiledInstructionsProto.costs)
  return _impl_.costs_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost >*
ProfiledInstructionsProto::mutable_costs() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.profiler.ProfiledInstructionsProto.costs)
  return &_impl_.costs_;
}
inline const ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost& ProfiledInstructionsProto::_internal_costs(int index) const {
  return _impl_.costs_.Get(index);
}
inline const ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost& ProfiledInstructionsProto::costs(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.profiler.ProfiledInstructionsProto.costs)
  return _internal_costs(index);
}
inline ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost* ProfiledInstructionsProto::_internal_add_costs() {
  return _impl_.costs_.Add();
}
inline ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost* ProfiledInstructionsProto::add_costs() {
  ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost* _add = _internal_add_costs();
  // @@protoc_insertion_point(field_add:tensorflow.profiler.ProfiledInstructionsProto.costs)
  return _add;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::profiler::ProfiledInstructionsProto_InstructionCost >&
ProfiledInstructionsProto::costs() const {
  // @@protoc_insertion_point(field_list:tensorflow.profiler.ProfiledInstructionsProto.costs)
  return _impl_.costs_;
}

// repeated .tensorflow.profiler.ProfiledInstructionsProto.Latency latencies = 2;
inline int ProfiledInstructionsProto::_internal_latencies_size() const {
  return _impl_.latencies_.size();
}
inline int ProfiledInstructionsProto::latencies_size() const {
  return _internal_latencies_size();
}
inline void ProfiledInstructionsProto::clear_latencies() {
  _impl_.latencies_.Clear();
}
inline ::tensorflow::profiler::ProfiledInstructionsProto_Latency* ProfiledInstructionsProto::mutable_latencies(int index) {
  // @@protoc_insertion_point(field_mutable:tensorflow.profiler.ProfiledInstructionsProto.latencies)
  return _impl_.latencies_.Mutable(index);
}
inline ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::profiler::ProfiledInstructionsProto_Latency >*
ProfiledInstructionsProto::mutable_latencies() {
  // @@protoc_insertion_point(field_mutable_list:tensorflow.profiler.ProfiledInstructionsProto.latencies)
  return &_impl_.latencies_;
}
inline const ::tensorflow::profiler::ProfiledInstructionsProto_Latency& ProfiledInstructionsProto::_internal_latencies(int index) const {
  return _impl_.latencies_.Get(index);
}
inline const ::tensorflow::profiler::ProfiledInstructionsProto_Latency& ProfiledInstructionsProto::latencies(int index) const {
  // @@protoc_insertion_point(field_get:tensorflow.profiler.ProfiledInstructionsProto.latencies)
  return _internal_latencies(index);
}
inline ::tensorflow::profiler::ProfiledInstructionsProto_Latency* ProfiledInstructionsProto::_internal_add_latencies() {
  return _impl_.latencies_.Add();
}
inline ::tensorflow::profiler::ProfiledInstructionsProto_Latency* ProfiledInstructionsProto::add_latencies() {
  ::tensorflow::profiler::ProfiledInstructionsProto_Latency* _add = _internal_add_latencies();
  // @@protoc_insertion_point(field_add:tensorflow.profiler.ProfiledInstructionsProto.latencies)
  return _add;
}
inline const ::PROTOBUF_NAMESPACE_ID::RepeatedPtrField< ::tensorflow::profiler::ProfiledInstructionsProto_Latency >&
ProfiledInstructionsProto::latencies() const {
  // @@protoc_insertion_point(field_list:tensorflow.profiler.ProfiledInstructionsProto.latencies)
  return _impl_.latencies_;
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------

// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace profiler
}  // namespace tensorflow

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_tsl_2fprofiler_2fprotobuf_2fprofiled_5finstructions_2eproto
