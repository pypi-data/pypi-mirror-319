/*******************************************************************************
 * Copyright 2022-2023 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *******************************************************************************/
static const int majorVersion = 1;
static const int minorVersion = 0;
static const int patchVersion = 0;
static int getVersion() { return (majorVersion << 16) + (minorVersion << 8) + patchVersion; }
static const char *getVersionString() { return "1.0.0"; }
