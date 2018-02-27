set(Sources
	POSIX.cpp
	Windows.cpp)
set(PublicHeaders
	${WAVM_INCLUDE_DIR}/Platform/Platform.h)
include_directories(${WAVM_INCLUDE_DIR}/Platform)

### tokenika:
#add_definitions(-DPLATFORM_API=DLL_EXPORT)
### tokenika

add_library(Platform STATIC ${Sources} ${PublicHeaders})

# Link with dl on Linux for dladdr.
if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
	target_link_libraries(Platform dl pthread rt)
endif()

#<Tokenika>
install(
  TARGETS Platform 
  LIBRARY DESTINATION lib 
  ARCHIVE DESTINATION lib
)
#</Tokenika>

