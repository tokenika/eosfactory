project (EosLib)
include(../config.cmake)

set(Boost_USE_STATIC_LIBS ON)
set(Boost_USE_MULTITHREADED ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost 1.64.0 REQUIRED COMPONENTS program_options)

include_directories(${Boost_INCLUDE_DIRS})
add_subdirectory (eoslib_definitions)
include_directories ("${PROJECT_SOURCE_DIR}/eoslib_definitions")
include_directories("${EOSIO_INSTALL_DIR}//contracts")

