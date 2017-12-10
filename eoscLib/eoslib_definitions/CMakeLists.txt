
include_directories("${CMAKE_INSTALL_PREFIX}/include")
include_directories("${EOSIO_INSTALL_DIR}/contracts")
add_library(print print.cpp)
add_library(message message.cpp)
add_library(system system.cpp)
add_library(db db.cpp)

install(TARGETS print DESTINATION lib)
install(TARGETS message DESTINATION lib)
install(TARGETS system DESTINATION lib)
install(TARGETS db DESTINATION lib)