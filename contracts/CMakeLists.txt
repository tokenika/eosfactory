cmake_minimum_required( VERSION 3.5 )

list(APPEND CMAKE_MODULE_PATH "CMakeModules")

# will be implictly used for any compilation unit if not overrided by SYSTEM_INCLUDE_FOLDERS parameter
# these directories go as -isystem <dir> to avoid warnings from code of third-party libraries
set(DEFAULT_SYSTEM_INCLUDE_FOLDERS ${CMAKE_SOURCE_DIR}/contracts/libc++/upstream/include ${CMAKE_SOURCE_DIR}/contracts/musl/upstream/include ${Boost_INCLUDE_DIR})

set(STANDARD_INCLUDE_FOLDERS ${CMAKE_SOURCE_DIR}/contracts ${CMAKE_SOURCE_DIR}/externals/magic_get/include)

add_subdirectory(currency)

file(GLOB SKELETONS RELATIVE ${CMAKE_SOURCE_DIR}/contracts "skeleton/*")

# Documented multiple output support is broken, so properly setting up the multiple
# dependencies in the custom target is not possible.  (CMake 3.5)
add_custom_command(OUTPUT share/eosio/skeleton/skeleton.cpp
                   COMMAND ${CMAKE_COMMAND} -E make_directory ../share/eosio/skeleton
                   COMMAND ${CMAKE_COMMAND} -E copy_directory ${CMAKE_CURRENT_SOURCE_DIR}/skeleton ../share/eosio/skeleton
                   DEPENDS ${SKELETONS}
                   COMMENT Copying skeleton contract...
                   VERBATIM)
add_custom_target(copy_skeleton_contract ALL DEPENDS share/eosio/skeleton/skeleton.cpp)

