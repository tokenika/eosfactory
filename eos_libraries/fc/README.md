### In E:\Workspaces\EOS\eos_fc\fc\CMakeModules\FindSecp256k1.cmake:
```
find_path(Secp256k1_ROOT_DIR
    NAMES include/secp256k1.h
	HINTS $ENV{Secp256k1_ROOT_DIR}
)

find_path(Secp256k1_INCLUDE_DIR
    NAMES secp256k1.h
    HINTS ${Secp256k1_ROOT_DIR}/include  $ENV{Secp256k1_ROOT_DIR}/incl
)

find_library(Secp256k1_LIBRARY
    NAMES libsecp256k1.a secp256k1.lib secp256k1
    HINTS ${Secp256k1_ROOT_DIR}/lib $ENV{Secp256k1_ROOT_DIR}/lib
)
```

### In E:\Workspaces\EOS\eos_fc\fc\include\fc\uint128.hpp:

The type __int128 is not any standard in windows. Instead, use 
#include <boost/multiprecision/cpp_int.hpp>

For example:

// explicit uint128( unsigned __int128 i ):hi( i >> 64 ), lo(i){ }
explicit uint128(boost::multiprecision::uint128_t i ):hi( i >> 64 ), lo(i){ }

### crypto

exclusions that do not compile:
* pke.cpp
* elliptic_openssl.cpp
* base32.cpp
* equihash.cpp

* set x-64 Debug VS

### logger

fc\include\fc\log\appender.hpp
[6] // namespace boost { namespace asio { class io_service; } }

fc\include\fc\log\gelf_appender.hpp
[7] // namespace boost { namespace asio { class io_service; } }

fc\include\fc\log\appender.hpp
[5] #include <boost/asio.hpp>

### secp256k1 library for Windows
