/*
 *  Copyright 2008-2013 NVIDIA Corporation
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

#pragma once

// Internal config header that is only included through thrust/detail/config/config.h

#if defined(_CCCL_IMPLICIT_SYSTEM_HEADER_GCC)
#  pragma GCC system_header
#elif defined(_CCCL_IMPLICIT_SYSTEM_HEADER_CLANG)
#  pragma clang system_header
#elif defined(_CCCL_IMPLICIT_SYSTEM_HEADER_MSVC)
#  pragma system_header
#endif // no system header

#ifndef THRUST_DEBUG
#  ifndef NDEBUG
#    if defined(DEBUG) || defined(_DEBUG)
#      define THRUST_DEBUG 1
#    endif // (DEBUG || _DEBUG)
#  endif // NDEBUG
#endif // THRUST_DEBUG

#if THRUST_DEBUG
#  ifndef __THRUST_SYNCHRONOUS
#    define __THRUST_SYNCHRONOUS 1
#  endif // __THRUST_SYNCHRONOUS
#endif // THRUST_DEBUG

