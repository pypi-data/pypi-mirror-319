//===- RuntimeOpVerification.h - Op Verification ----------------*- C++ -*-===//
//
// Part of the LLVM Project, under the Apache License v2.0 with LLVM Exceptions.
// See https://llvm.org/LICENSE.txt for license information.
// SPDX-License-Identifier: Apache-2.0 WITH LLVM-exception
//
//===----------------------------------------------------------------------===//

#ifndef MLIR_DIALECT_LINALG_RUNTIMEOPVERIFICATION_H
#define MLIR_DIALECT_LINALG_RUNTIMEOPVERIFICATION_H

namespace mlir {
class DialectRegistry;

namespace linalg {
void registerRuntimeVerifiableOpInterfaceExternalModels(
    DialectRegistry &registry);
} // namespace linalg
} // namespace mlir

#endif // MLIR_DIALECT_LINALG_RUNTIMEOPVERIFICATION_H
