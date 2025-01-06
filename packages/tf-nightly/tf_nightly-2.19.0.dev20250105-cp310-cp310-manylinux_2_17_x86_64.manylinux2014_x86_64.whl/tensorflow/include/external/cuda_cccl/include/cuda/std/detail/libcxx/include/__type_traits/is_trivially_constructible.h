//===----------------------------------------------------------------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES.
//
//===----------------------------------------------------------------------===//

#ifndef _LIBCUDACXX___TYPE_TRAITS_IS_TRIVIALLY_CONSTRUCTIBLE_H
#define _LIBCUDACXX___TYPE_TRAITS_IS_TRIVIALLY_CONSTRUCTIBLE_H

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

#include "../__type_traits/integral_constant.h"
#include "../__type_traits/is_scalar.h"

_LIBCUDACXX_BEGIN_NAMESPACE_STD

#if defined(_LIBCUDACXX_IS_TRIVIALLY_CONSTRUCTIBLE) && !defined(_LIBCUDACXX_USE_IS_TRIVIALLY_CONSTRUCTIBLE_FALLBACK)

template <class _Tp, class... _Args>
struct _LIBCUDACXX_TEMPLATE_VIS is_trivially_constructible
    : public integral_constant<bool, _LIBCUDACXX_IS_TRIVIALLY_CONSTRUCTIBLE(_Tp, _Args...)>
    {};

#if _CCCL_STD_VER > 2011 && !defined(_LIBCUDACXX_HAS_NO_VARIABLE_TEMPLATES)
template <class _Tp, class... _Args>
_LIBCUDACXX_INLINE_VAR constexpr bool is_trivially_constructible_v =
    _LIBCUDACXX_IS_TRIVIALLY_CONSTRUCTIBLE(_Tp, _Args...);
#endif

#else

template <class _Tp, class... _Args>
struct _LIBCUDACXX_TEMPLATE_VIS is_trivially_constructible
    : false_type
{
};

_CCCL_SUPPRESS_DEPRECATED_PUSH
template <class _Tp>
struct _LIBCUDACXX_TEMPLATE_VIS is_trivially_constructible<_Tp>
#if defined(_LIBCUDACXX_HAS_TRIVIAL_CONSTRUCTOR) && !defined(_LIBCUDACXX_USE_HAS_TRIVIAL_CONSTRUCTOR_FALLBACK)
    : integral_constant<bool, _LIBCUDACXX_HAS_TRIVIAL_CONSTRUCTOR(_Tp)>
#else
    : integral_constant<bool, is_scalar<_Tp>::value>
#endif // defined(_LIBCUDACXX_HAS_TRIVIAL_CONSTRUCTOR) && !defined(_LIBCUDACXX_USE_HAS_TRIVIAL_CONSTRUCTOR_FALLBACK)
{
};
_CCCL_SUPPRESS_DEPRECATED_POP

template <class _Tp>
struct _LIBCUDACXX_TEMPLATE_VIS is_trivially_constructible<_Tp, _Tp&&>
    : integral_constant<bool, is_scalar<_Tp>::value>
{
};

template <class _Tp>
struct _LIBCUDACXX_TEMPLATE_VIS is_trivially_constructible<_Tp, const _Tp&>
    : integral_constant<bool, is_scalar<_Tp>::value>
{
};

template <class _Tp>
struct _LIBCUDACXX_TEMPLATE_VIS is_trivially_constructible<_Tp, _Tp&>
    : integral_constant<bool, is_scalar<_Tp>::value>
{
};

#if _CCCL_STD_VER > 2011 && !defined(_LIBCUDACXX_HAS_NO_VARIABLE_TEMPLATES)
template <class _Tp, class... _Args>
_LIBCUDACXX_INLINE_VAR constexpr bool is_trivially_constructible_v
    = is_trivially_constructible<_Tp, _Args...>::value;
#endif

#endif // defined(_LIBCUDACXX_IS_TRIVIALLY_CONSTRUCTIBLE) && !defined(_LIBCUDACXX_USE_IS_TRIVIALLY_CONSTRUCTIBLE_FALLBACK)

_LIBCUDACXX_END_NAMESPACE_STD

#endif // _LIBCUDACXX___TYPE_TRAITS_IS_TRIVIALLY_CONSTRUCTIBLE_H
