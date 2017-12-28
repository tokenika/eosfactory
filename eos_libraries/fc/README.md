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

add _CRT_SECURE_NO_WARNINGS

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

## secp256k1 library for Windows

```
git clone https://github.com/cryptonomex/secp256k1-zkp.git

```
Build steps
-----------

libsecp256k1 is built using autotools:

    $ ./autogen.sh
    $ ./configure
    $ make
    $ ./tests
    $ sudo make install  # optional

Build for Windows steps
-----------------------

### libsecp256k1 is built using autotools:

$ ./autogen.sh
$ ./configure --host=x86_64-w64-mingw32 --prefix=/mnt/hgfs/Workspaces/secp256k1-zkp/installWin
```
checking build system type... x86_64-pc-linux-gnu
checking host system type... x86_64-w64-mingw32
checking for a BSD-compatible install... /usr/bin/install -c
checking whether build environment is sane... yes
checking for x86_64-w64-mingw32-strip... x86_64-w64-mingw32-strip
checking for a thread-safe mkdir -p... /bin/mkdir -p
checking for gawk... no
checking for mawk... mawk
checking whether make sets $(MAKE)... yes
checking whether make supports nested variables... yes
checking how to print strings... printf
checking for style of include used by make... GNU
checking for x86_64-w64-mingw32-gcc... x86_64-w64-mingw32-gcc
checking whether the C compiler works... yes
checking for C compiler default output file name... a.exe
checking for suffix of executables... .exe
checking whether we are cross compiling... yes
checking for suffix of object files... o
checking whether we are using the GNU C compiler... yes
checking whether x86_64-w64-mingw32-gcc accepts -g... yes
checking for x86_64-w64-mingw32-gcc option to accept ISO C89... none needed
checking whether x86_64-w64-mingw32-gcc understands -c and -o together... yes
checking dependency style of x86_64-w64-mingw32-gcc... gcc3
checking for a sed that does not truncate output... /bin/sed
checking for grep that handles long lines and -e... /bin/grep
checking for egrep... /bin/grep -E
checking for fgrep... /bin/grep -F
checking for ld used by x86_64-w64-mingw32-gcc... /usr/bin/x86_64-w64-mingw32-ld
checking if the linker (/usr/bin/x86_64-w64-mingw32-ld) is GNU ld... yes
checking for BSD- or MS-compatible name lister (nm)... /usr/bin/x86_64-w64-mingw32-nm -B
checking the name lister (/usr/bin/x86_64-w64-mingw32-nm -B) interface... BSD nm
checking whether ln -s works... no, using cp -pR
checking the maximum length of command line arguments... 1572864
checking how to convert x86_64-pc-linux-gnu file names to x86_64-w64-mingw32 format... func_convert_file_nix_to_w32
checking how to convert x86_64-pc-linux-gnu file names to toolchain format... func_convert_file_noop
checking for /usr/bin/x86_64-w64-mingw32-ld option to reload object files... -r
checking for x86_64-w64-mingw32-objdump... x86_64-w64-mingw32-objdump
checking how to recognize dependent libraries... file_magic ^x86 archive import|^x86 DLL
checking for x86_64-w64-mingw32-dlltool... x86_64-w64-mingw32-dlltool
checking how to associate runtime and link libraries... func_cygming_dll_for_implib
checking for x86_64-w64-mingw32-ar... x86_64-w64-mingw32-ar
checking for archiver @FILE support... @
checking for x86_64-w64-mingw32-strip... (cached) x86_64-w64-mingw32-strip
checking for x86_64-w64-mingw32-ranlib... x86_64-w64-mingw32-ranlib
checking command to parse /usr/bin/x86_64-w64-mingw32-nm -B output from x86_64-w64-mingw32-gcc object... ok
checking for sysroot... no
checking for a working dd... /bin/dd
checking how to truncate binary pipes... /bin/dd bs=4096 count=1
checking for x86_64-w64-mingw32-mt... no
checking for mt... mt
configure: WARNING: using cross tools not prefixed with host triplet
checking if mt is a manifest tool... no
checking how to run the C preprocessor... x86_64-w64-mingw32-gcc -E
checking for ANSI C header files... yes
checking for sys/types.h... yes
checking for sys/stat.h... yes
checking for stdlib.h... yes
checking for string.h... yes
checking for memory.h... yes
checking for strings.h... yes
checking for inttypes.h... yes
checking for stdint.h... yes
checking for unistd.h... yes
checking for dlfcn.h... no
checking for objdir... .libs
checking if x86_64-w64-mingw32-gcc supports -fno-rtti -fno-exceptions... no
checking for x86_64-w64-mingw32-gcc option to produce PIC... -DDLL_EXPORT -DPIC
checking if x86_64-w64-mingw32-gcc PIC flag -DDLL_EXPORT -DPIC works... yes
checking if x86_64-w64-mingw32-gcc static flag -static works... yes
checking if x86_64-w64-mingw32-gcc supports -c -o file.o... yes
checking if x86_64-w64-mingw32-gcc supports -c -o file.o... (cached) yes
checking whether the x86_64-w64-mingw32-gcc linker (/usr/bin/x86_64-w64-mingw32-ld) supports shared libraries... yes
checking whether -lc should be explicitly linked in... yes
checking dynamic linker characteristics... Win32 ld.exe
checking how to hardcode library paths into programs... immediate
checking whether stripping libraries is possible... yes
checking if libtool supports shared libraries... yes
checking whether to build shared libraries... yes
checking whether to build static libraries... yes
checking whether make supports nested variables... (cached) yes
checking for x86_64-w64-mingw32-pkg-config... no
checking for pkg-config... /usr/bin/pkg-config
checking pkg-config is at least version 0.9.0... yes
checking for x86_64-w64-mingw32-ar... /usr/bin/x86_64-w64-mingw32-ar
checking for x86_64-w64-mingw32-ranlib... /usr/bin/x86_64-w64-mingw32-ranlib
checking for x86_64-w64-mingw32-strip... /usr/bin/x86_64-w64-mingw32-strip
checking for x86_64-w64-mingw32-gcc option to accept ISO C89... (cached) none needed
checking if x86_64-w64-mingw32-gcc supports -std=c89 -pedantic -Wall -Wextra -Wcast-align -Wnested-externs -Wshadow -Wstrict-prototypes -Wno-unused-function -Wno-long-long -Wno-overlength-strings... yes
checking for __int128... yes
checking for __builtin_expect... yes
checking for  __builtin_clzll... yes
checking for x86_64 assembly availability... yes
checking gmp.h usability... no
checking gmp.h presence... no
checking for gmp.h... no
checking openssl/crypto.h usability... no
checking openssl/crypto.h presence... no
checking for openssl/crypto.h... no
checking whether byte ordering is bigendian... no
configure: Using assembly optimizations: x86_64
configure: Using field implementation: 64bit
configure: Using bignum implementation: no
configure: Using scalar implementation: 64bit
configure: Using endomorphism optimizations: no
checking that generated files are newer than configure... done
configure: creating ./config.status
config.status: creating Makefile
config.status: creating libsecp256k1.pc
config.status: creating src/libsecp256k1-config.h
config.status: executing depfiles commands
config.status: executing libtool commands
```
$ make
```
CC       src/libsecp256k1_la-secp256k1.lo
CCLD     libsecp256k1.la
libtool: warning: undefined symbols not allowed in x86_64-w64-mingw32 shared libraries; building static only
/usr/bin/x86_64-w64-mingw32-ar: `u' modifier ignored since `D' is the default (see `U')
CC       src/tests-tests.o
CCLD     tests.exe
```
$ ./tests.exe
$ sudo make install  # optional
```
make[1]: Entering directory '/mnt/hgfs/Workspaces/secp256k1-zkp'
 /bin/mkdir -p '/mnt/hgfs/Workspaces/secp256k1-zkp/installWin/lib'
 /bin/bash ./libtool   --mode=install /usr/bin/install -c   libsecp256k1.la '/mnt/hgfs/Workspaces/secp256k1-zkp/installWin/lib'
libtool: install: /usr/bin/install -c .libs/libsecp256k1.lai /mnt/hgfs/Workspaces/secp256k1-zkp/installWin/lib/libsecp256k1.la
libtool: install: /usr/bin/install -c .libs/libsecp256k1.a /mnt/hgfs/Workspaces/secp256k1-zkp/installWin/lib/libsecp256k1.a
libtool: install: chmod 644 /mnt/hgfs/Workspaces/secp256k1-zkp/installWin/lib/libsecp256k1.a
libtool: install: /usr/bin/x86_64-w64-mingw32-ranlib /mnt/hgfs/Workspaces/secp256k1-zkp/installWin/lib/libsecp256k1.a
 /bin/mkdir -p '/mnt/hgfs/Workspaces/secp256k1-zkp/installWin/include'
 /usr/bin/install -c -m 644 include/secp256k1.h '/mnt/hgfs/Workspaces/secp256k1-zkp/installWin/include'
 /bin/mkdir -p '/mnt/hgfs/Workspaces/secp256k1-zkp/installWin/lib/pkgconfig'
 /usr/bin/install -c -m 644 libsecp256k1.pc '/mnt/hgfs/Workspaces/secp256k1-zkp/installWin/lib/pkgconfig'
make[1]: Leaving directory '/mnt/hgfs/Workspaces/secp256k1-zkp'
```
The library is libsecp256k1.a

## OpenSSL
$(C_INCLUDE)/openssl-1.0.1q-vs2015/lib/libeay32MT.lib

## Other
fc\src\filesystem.cpp
455  //BOOL success = GetUserProfileDirectoryW(access_token, user_profile_dir, &user_profile_dir_len);
       CloseHandle(access_token);
     //if (!success)
     //  FC_ASSERT(false, "Unable to get the user profile directory");

-----------------------
unresolved external symbol __imp_CertOpenStore referenced in function capi_open_store
