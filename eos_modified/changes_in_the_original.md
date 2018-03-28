##build.sh 

@@ -74,7 +74,7 @@ COMPILE_EOS=1
COMPILE_CONTRACTS=1

# Define default arguments.
- CMAKE_BUILD_TYPE=RelWithDebugInfo
+ CMAKE_BUILD_TYPE=Debug

# Install dependencies
if [ ${INSTALL_DEPS} == "1" ]; then
@ -89,8 +89,8 @@ cd ${WORK_DIR}
mkdir -p ${BUILD_DIR}
cd ${BUILD_DIR}

- CXX_COMPILER=clang++-4.0
- C_COMPILER=clang-4.0
+ CXX_COMPILER=c++ #clang++-4.0
+ C_COMPILER=cc #clang-4.0

if [ $ARCH == "darwin" ]; then
  CXX_COMPILER=clang++

## libraries/fc/CMAKEList.txt 

@@ -7,7 +7,7 @@ SET( DEFAULT_LIBRARY_INSTALL_DIR lib/ )
SET( DEFAULT_EXECUTABLE_INSTALL_DIR bin/ )
SET( CMAKE_DEBUG_POSTFIX _debug )
SET( BUILD_SHARED_LIBS NO )
- SET( ECC_IMPL secp256k1 CACHE STRING "secp256k1 or openssl or mixed" )
+ SET( ECC_IMPL openssl CACHE STRING "secp256k1 or openssl or mixed" )

set(platformBitness 32)
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
@ -19,6 +19,7 @@ SET (ORIGINAL_LIB_SUFFIXES ${CMAKE_FIND_LIBRARY_SUFFIXES})
find_package(Secp256k1 REQUIRED)
find_package(GMP REQUIRED)

+ MESSAGE(STATUS "ECC_IMPL: ${ECC_IMPL}")
IF( ECC_IMPL STREQUAL openssl )
  SET( ECC_REST src/crypto/elliptic_impl_pub.cpp )
ELSE( ECC_IMPL STREQUAL openssl )

## llibraries/fc/src/crypto/elliptic_openssl.cpp 

@@ -186,7 +186,14 @@ namespace fc { namespace ecc {
      return buf;
    }

+ /*
+ <BlockOne>
    compact_signature private_key::sign_compact( const fc::sha256& digest )const
+ </BlockOne>
+ */
+ //<Tokenika>
+   compact_signature private_key::sign_compact( const fc::sha256& digest, bool require_canonical)const
+ //</Tokenika>
    {
        try {
            FC_ASSERT( my->_key != nullptr );

## libraries/wasm-jit/include/Platform/Platform.h 
@@ -8,8 +8,18 @@

#ifdef _WIN32
	#define THREAD_LOCAL thread_local
+	
+ /*
+ <BlockOne>
	#define DLL_EXPORT __declspec(dllexport)
	#define DLL_IMPORT __declspec(dllimport)
+ </BlockOne>
+ */
+ //<Tokenika>
+	#define DLL_EXPORT
+	#define DLL_IMPORT
+ //</Tokenika>
+
	#define FORCEINLINE __forceinline
	#define SUPPRESS_UNUSED(variable) (void)(variable);
	#include <intrin.h>

## programs/eosioc/http.cpp 

@@ -60,6 +60,19 @@ fc::variant call( const std::string& server, uint16_t port,
       request_stream << "Connection: close\r\n\r\n";
       request_stream << postjson;
+
+      std::stringstream ss;
+      ss << "POST " << path << " HTTP/1.0\r\n";
+      ss << "Host: " << server << "\r\n";
+      ss << "content-length: " << postjson.size() << "\r\n";
+      ss << "Accept: */*\r\n";
+      ss << "Connection: close\r\n\r\n";
+      ss << postjson;
+      std::string str = ss.str();
+      std::cout << "REQUEST httc.cpp [66]" << std::endl; 
+      std::cout << str << std::endl; 
+      std::cout << "/REQUEST" << std::endl;       
+
       // Send the request.
       boost::asio::write(socket, request);

@ -70,7 +83,8 @@ fc::variant call( const std::string& server, uint16_t port,
       boost::asio::read_until(socket, response, "\r\n");

       // Check that response is OK.
-       std::istream response_stream(&response);
+       std::istream response_stream(&response);  

       std::string http_version;
       response_stream >> http_version;
       unsigned int status_code;
@ -88,13 +102,14 @@ fc::variant call( const std::string& server, uint16_t port,
       {
//         std::cout << header << "\n";
       }
- //      std::cout << "\n";
+ //      std::cout << "\n";          return fc::json::from_string(re.str());

       std::stringstream re;
       // Write whatever content we already have to output.
       if (response.size() > 0)
      //   std::cout << &response;
      
+      if (response.size() > 0) {
         re << &response;
+       }

       // Read until EOF, writing data to output as we go.
       boost::system::error_code error;
@ -105,7 +120,10 @@ fc::variant call( const std::string& server, uint16_t port,
       if (error != boost::asio::error::eof)
         throw boost::system::system_error(error);

-     //  std::cout << re.str() <<"\n";
+     std::cout << "RESPONSE  httc.cpp [123]" << std::endl;
+     std::cout << re.str();
+     std::cout << "/RESPONSE" << std::endl;
+
       if( status_code == 200 || status_code == 201 || status_code == 202 ) {
          return fc::json::from_string(re.str());
       }