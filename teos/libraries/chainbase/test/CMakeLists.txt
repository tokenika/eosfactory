file(GLOB UNIT_TESTS "*.cpp")
add_executable( chainbase_test ${UNIT_TESTS} )

target_link_libraries( chainbase_test  
  PRIVATE
    chainbase ${PLATFORM_LIBRARIES} 
    ${Boost_LIBRARIES}
)

