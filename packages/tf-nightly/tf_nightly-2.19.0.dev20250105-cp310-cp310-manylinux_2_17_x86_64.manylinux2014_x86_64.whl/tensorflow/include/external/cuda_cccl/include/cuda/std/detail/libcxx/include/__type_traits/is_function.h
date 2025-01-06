//===----------------------------------------------------------------------===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
// SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES.
//
//===----------------------------------------------------------------------===//

#ifndef _LIBCUDACXX___TYPE_TRAITS_IS_FUNCTIONAL_H
#define _LIBCUDACXX___TYPE_TRAITS_IS_FUNCTIONAL_H

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
#include "../__type_traits/is_const.h"
#include "../__type_traits/is_reference.h"

_LIBCUDACXX_BEGIN_NAMESPACE_STD

#if defined(_LIBCUDACXX_IS_FUNCTION) && !defined(_LIBCUDACXX_USE_IS_FUNCTION_FALLBACK)

template <class _Tp>
struct _LIBCUDACXX_TEMPLATE_VIS is_function : integral_constant<bool, _LIBCUDACXX_IS_FUNCTION(_Tp)> {};

#if _CCCL_STD_VER > 2011 && !defined(_LIBCUDACXX_HAS_NO_VARIABLE_TEMPLATES)
template <class _Tp>
_LIBCUDACXX_INLINE_VAR constexpr bool is_function_v = _LIBCUDACXX_IS_FUNCTION(_Tp);
#endif

#else

template <class _Tp>
struct _LIBCUDACXX_TEMPLATE_VIS is_function
    : public integral_constant<bool, !(is_reference<_Tp>::value || is_const<const _Tp>::value)> {};

#if _CCCL_STD_VER > 2011 && !defined(_LIBCUDACXX_HAS_NO_VARIABLE_TEMPLATES)
template <class _Tp>
_LIBCUDACXX_INLINE_VAR constexpr bool is_function_v = is_function<_Tp>::value;
#endif

#endif // defined(_LIBCUDACXX_IS_FUNCTION) && !defined(_LIBCUDACXX_USE_IS_FUNCTION_FALLBACK)

_LIBCUDACXX_END_NAMESPACE_STD

#endif // _LIBCUDACXX___TYPE_TRAITS_IS_FUNCTIONAL_H
