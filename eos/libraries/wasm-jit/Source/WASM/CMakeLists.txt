set(Sources WASMSerialization.cpp)
set(PublicHeaders ${WAVM_INCLUDE_DIR}/WASM/WASM.h)
include_directories(${WAVM_INCLUDE_DIR}/WASM)

add_library(WASM STATIC ${Sources} ${PublicHeaders})
### tokenika
#add_definitions(-DWEBASSEMBLY_API=DLL_EXPORT)
### tokenika
target_link_libraries(WASM Logging IR)

#<Tokenika>
install(
  TARGETS WASM 
  LIBRARY DESTINATION lib 
  ARCHIVE DESTINATION lib
)
#</Tokenika>
