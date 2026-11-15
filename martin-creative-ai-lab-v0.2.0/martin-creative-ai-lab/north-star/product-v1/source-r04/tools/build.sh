#!/bin/sh
# Production-target fixture has ONE gameplay owner, world.cpp. The prior product.cpp
# remains a separate legacy binary for regression only; it is NOT linked into the client.
set -eu
cd "$(dirname "$0")/.."
mkdir -p artifacts site
${CXX:-g++} -std=c++20 -Wall -Wextra -Werror -O2 -fPIC -shared -DNS_BUILD_DLL core/world.cpp -o artifacts/libns_world.so
${CXX:-g++} -std=c++20 -Wall -Wextra -Werror -O2 -fPIC -shared -DNS_BUILD_DLL core/world_r02.cpp -o artifacts/libns_world_r02.so
${CXX:-g++} -std=c++20 -Wall -Wextra -Werror -O2 -fPIC -shared -DNS_BUILD_DLL core/product.cpp -o artifacts/libns_product.so
clang++ --target=wasm32 -std=c++20 -O2 -fno-exceptions -fno-rtti -nostdlib -DNS_PRODUCT_WASM \
 -Wl,--no-entry -Wl,--export-all -Wl,--strip-debug -Wl,--initial-memory=131072 core/world_r02.cpp -o site/product.wasm
clang++ --target=wasm32 -std=c++20 -O2 -fno-exceptions -fno-rtti -nostdlib -DNS_PRODUCT_WASM \
 -Wl,--no-entry -Wl,--export-all -Wl,--strip-debug -Wl,--initial-memory=131072 core/world.cpp -o artifacts/world_r01.wasm
clang++ --target=wasm32 -std=c++20 -O2 -fno-exceptions -fno-rtti -nostdlib -DNS_PRODUCT_WASM \
 -Wl,--no-entry -Wl,--export-all -Wl,--strip-debug -Wl,--initial-memory=131072 core/product.cpp -o artifacts/product_legacy.wasm
${CXX:-g++} -std=c++20 -Wall -Wextra -Werror -O2 -fPIC -shared -DNS_BUILD_DLL core/world_r03.cpp -o artifacts/libns_world_r03.so
clang++ --target=wasm32 -std=c++20 -O2 -fno-exceptions -fno-rtti -nostdlib -DNS_PRODUCT_WASM \
 -Wl,--no-entry -Wl,--export-all -Wl,--strip-debug -Wl,--initial-memory=131072 core/world_r03.cpp -o site/product.wasm

# R04 authoritative world. R03 remains archived in an explicit old WASM binary.
clang++ --target=wasm32 -std=c++20 -O2 -fno-exceptions -fno-rtti -nostdlib -DNS_PRODUCT_WASM \
 -Wl,--no-entry -Wl,--export-all -Wl,--strip-debug -Wl,--initial-memory=131072 core/world_r03.cpp -o artifacts/world_r03.wasm
${CXX:-g++} -std=c++20 -Wall -Wextra -Werror -O2 -fPIC -shared -DNS_BUILD_DLL core/world_r04.cpp -o artifacts/libns_world_r04.so
clang++ --target=wasm32 -std=c++20 -O2 -fno-exceptions -fno-rtti -nostdlib -DNS_PRODUCT_WASM \
 -Wl,--no-entry -Wl,--export-all -Wl,--strip-debug -Wl,--initial-memory=131072 core/world_r04.cpp -o site/product.wasm
