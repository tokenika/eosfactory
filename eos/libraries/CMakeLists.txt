add_subdirectory( fc )
add_subdirectory( chainbase )
add_subdirectory( wasm-jit )

add_subdirectory( types )
add_subdirectory( chain )

add_subdirectory( utilities )
add_subdirectory( appbase )

if( EOS_BUILD_RANGE STREQUAL all )
  #add_subdirectory( abi_generator ) compiler errors
  add_subdirectory( native_contract )
  # add_subdirectory( egenesis ) compiler errors
endif()

if( WIN32 )
  add_library(__iob_func __iob_func.cpp )
endif()