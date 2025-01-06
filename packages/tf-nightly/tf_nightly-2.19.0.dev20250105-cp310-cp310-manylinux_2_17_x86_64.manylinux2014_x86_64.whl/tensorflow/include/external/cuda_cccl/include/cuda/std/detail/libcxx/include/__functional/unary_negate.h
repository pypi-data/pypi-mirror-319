// -*- C++ -*-
//===----------------------------------------------------------------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES.
//
//===----------------------------------------------------------------------===//

#ifndef _LIBCUDACXX___FUNCTIONAL_UNARY_NEGATE_H
#define _LIBCUDACXX___FUNCTIONAL_UNARY_NEGATE_H

#ifndef __cuda_std__
#include <__config>
#endif // __cuda_std__

#if defined(_CCCL_IMPLICIT_SYSTEM_HEADER_GCC)
#  pragma GCC system_header
#elif defined(_CCCL_IMPLICIT_SYSTEM_HEADER_CLANG)
#  pragma clang system_header
#elif defined(_CCCL_IMPLICIT_SYSTEM_HEADER_MSVC)
#  pragma system_header
#endif // no system header

#include "../__functional/unary_function.h"

_LIBCUDACXX_BEGIN_NAMESPACE_STD

#if _CCCL_STD_VER <= 2017 || defined(_LIBCUDACXX_ENABLE_CXX20_REMOVED_NEGATORS)

_CCCL_SUPPRESS_DEPRECATED_PUSH

template <class _Predicate>
class _LIBCUDACXX_TEMPLATE_VIS _LIBCUDACXX_DEPRECATED_IN_CXX17 unary_negate
    : public __unary_function<typename _Predicate::argument_type, bool>
{
    _Predicate __pred_;
public:
    _LIBCUDACXX_CONSTEXPR_AFTER_CXX11 _LIBCUDACXX_INLINE_VISIBILITY
    explicit unary_negate(const _Predicate& __pred)
        : __pred_(__pred) {}
    _CCCL_EXEC_CHECK_DISABLE
    _LIBCUDACXX_CONSTEXPR_AFTER_CXX11 _LIBCUDACXX_INLINE_VISIBILITY
    bool operator()(const typename _Predicate::argument_type& __x) const
        {return !__pred_(__x);}
};

template <class _Predicate>
_LIBCUDACXX_DEPRECATED_IN_CXX17 inline _LIBCUDACXX_CONSTEXPR_AFTER_CXX11 _LIBCUDACXX_INLINE_VISIBILITY
unary_negate<_Predicate>
not1(const _Predicate& __pred) {return unary_negate<_Predicate>(__pred);}

_CCCL_SUPPRESS_DEPRECATED_POP

#endif // _CCCL_STD_VER <= 2017 || defined(_LIBCUDACXX_ENABLE_CXX20_REMOVED_NEGATORS)

_LIBCUDACXX_END_NAMESPACE_STD

#endif // _LIBCUDACXX___FUNCTIONAL_UNARY_NEGATE_H
