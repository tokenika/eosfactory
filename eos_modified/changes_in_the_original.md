CMakeLists.txt ///////////////////////////

@@ -38,7 +38,6 @@ elseif ("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang")
    endif()
endif()

-
set(CMAKE_EXPORT_COMPILE_COMMANDS "ON")
set(BUILD_DOXYGEN FALSE CACHE BOOL "Build doxygen documentation on every make")
set(BUILD_MONGO_DB_PLUGIN FALSE CACHE BOOL "Build mongo database plugin")
@ -152,6 +151,7 @@ else( WIN32 ) # Apple AND Linux
        set( CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -Wall -Wno-deprecated-declarations" )
    else( APPLE )
        # Linux Specific Options Here
+        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fPIC")
        message( STATUS "Configuring Eos on Linux" )
        set( CMAKE_CXX_FLAGS "${CMAKE_C_FLAGS} -Wall" )
        if ( FULL_STATIC_BUILD )

eosio_build.sh /////////////////////////////

@@ -100,8 +100,10 @@
			;;
			"Ubuntu")
				FILE=${WORK_DIR}/scripts/eosio_build_ubuntu.sh
-				CXX_COMPILER=clang++-4.0
-				C_COMPILER=clang-4.0
+				# CXX_COMPILER=clang++-4.0
+				# C_COMPILER=clang-4.0
+				CXX_COMPILER=g++
+				C_COMPILER=gcc			
				MONGOD_CONF=/etc/mongod.conf
			;;
			*)
@ -131,7 +133,7 @@

	COMPILE_EOS=1
	COMPILE_CONTRACTS=1
-	CMAKE_BUILD_TYPE=RelWithDebInfo
+	CMAKE_BUILD_TYPE=Debug

	cd ${WORK_DIR}
	mkdir -p ${BUILD_DIR}

libraries\chain\include\eosio\chain\wasm_eosio_injection.hpp ////////////////////////

@@ -319,8 +319,9 @@ namespace eosio { namespace chain { namespace wasm_injections {
         case wasm_ops::f64_convert_u_i64_code:
            return u8"_eosio_ui64_to_f64";

-         default:
-            FC_THROW_EXCEPTION( eosio::chain::wasm_execution_error, "Error, unknown opcode in injection ${op}", ("op", opcode));
+         // (g++, not LLVM) error: expression ‘<throw-expression>’ is not a constant-expression:
+         //default:
+         //   FC_THROW_EXCEPTION( eosio::chain::wasm_execution_error, "Error, unknown opcode in injection ${op}", ("op", opcode));
      }
   }

libraries\fc\CMakeLists.txt //////////////////////////////////

@@ -7,7 +7,8 @@ SET( DEFAULT_LIBRARY_INSTALL_DIR usr/lib )
SET( DEFAULT_EXECUTABLE_INSTALL_DIR usr/bin )
SET( CMAKE_DEBUG_POSTFIX _debug )
SET( BUILD_SHARED_LIBS NO )
- SET( ECC_IMPL secp256k1 CACHE STRING "secp256k1 or openssl or mixed" )
+ #SET( ECC_IMPL secp256k1 CACHE STRING "secp256k1 or openssl or mixed" )
+ SET( ECC_IMPL openssl CACHE STRING "secp256k1 or openssl or mixed" )

set(platformBitness 32)
if(CMAKE_SIZEOF_VOID_P EQUAL 8)
@ -19,6 +20,7 @@ SET (ORIGINAL_LIB_SUFFIXES ${CMAKE_FIND_LIBRARY_SUFFIXES})
find_package(Secp256k1 REQUIRED)
find_package(GMP REQUIRED)

+ MESSAGE(STATUS "ECC_IMPL: ${ECC_IMPL}")
IF( ECC_IMPL STREQUAL openssl )
  SET( ECC_REST src/crypto/elliptic_impl_pub.cpp )
ELSE( ECC_IMPL STREQUAL openssl )

libraries\fc\src\crypto\elliptic_openssl.cpp ////////////////////////////

@@ -186,7 +186,14 @@ namespace fc { namespace ecc {
      return buf;
    }

+ /*
+ <BlockOne>
+    compact_signature private_key::sign_compact( const fc::sha256& digest )const
+ </BlockOne>
+ */
+ //<Tokenika>
+     compact_signature private_key::sign_compact( const fc::sha256& digest, bool require_canonical)const
+ //</Tokenika>
    {
        try {
            FC_ASSERT( my->_key != nullptr );

libraries\wasm-jit\Include\Platform\Platform.h ////////////////////////////////

@@ -8,8 +8,18 @@

#ifdef _WIN32
	#define THREAD_LOCAL thread_local

+ /*
+ <BlockOne>
+ 	#define DLL_EXPORT __declspec(dllexport)
+ 	#define DLL_IMPORT __declspec(dllimport)
+ </BlockOne>
+ */
+ //<Tokenika>
+ #define DLL_EXPORT
+ #define DLL_IMPORT
+ //</Tokenika>
+ 
	#define FORCEINLINE __forceinline
	#define SUPPRESS_UNUSED(variable) (void)(variable);
	#include <intrin.h>    

programs\cleos\httpc.cpp ////////////////////////////////

  @@ -63,9 +63,22 @@ namespace eosio { namespace client { namespace http {
         request_stream << "Connection: close\r\n\r\n";
         request_stream << postjson;

         std::stringstream ss;
         ss << "POST " << path << " HTTP/1.0\r\n";
         ss << "Host: " << server << "\r\n";
         ss << "content-length: " << postjson.size() << "\r\n";
         ss << "Accept: */*\r\n";
         ss << "Connection: close\r\n\r\n";
         ss << postjson;
         std::string str = ss.str();
         std::cout << "REQUEST httc.cpp [66]" << std::endl; 
         std::cout << str << std::endl; 
         std::cout << "/REQUEST" << std::endl;           

         // Send the request.
         boost::asio::write(socket, request);


         // Read the response status line. The response streambuf will automatically
         // grow to accommodate the entire line. The growth may be limited by passing
         // a maximum size to the streambuf constructor.
@ -108,7 +121,7 @@ namespace eosio { namespace client { namespace http {
         if (error != boost::asio::error::eof)
            throw boost::system::system_error(error);

         //  std::cout << re.str() <<"\n";
         std::cout << re.str() <<"\n";
         const auto response_result = fc::json::from_string(re.str());
         if( status_code == 200 || status_code == 201 || status_code == 202 ) {
            return response_result;        