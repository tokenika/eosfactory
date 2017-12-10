### CMake tuning
* CMake honors the environment variables CC and CXX upon detecting the C and C++ compiler to use:
```
export CC=/usr/bin/clang
export CXX=/usr/bin/clang++
## cmake ..
## -- The C compiler identification is Clang
## -- The CXX compiler identification is Clang

``
ERROR: 
/mnt/hgfs/Workspaces/EOS/EosContracts/eosContracts/main.cpp:50:27: warning: range-based for loop is a C++11 extension [-Wc++11-extensions]

With the following setting, the error remains!!!!!!!!!
```
SET (CMAKE_C_FLAGS_INIT                "-Wall -std=c++11")
SET (CMAKE_C_FLAGS_DEBUG_INIT          "-g")
SET (CMAKE_C_FLAGS_MINSIZEREL_INIT     "-Os -DNDEBUG")
SET (CMAKE_C_FLAGS_RELEASE_INIT        "-O4 -DNDEBUG")
SET (CMAKE_C_FLAGS_RELWITHDEBINFO_INIT "-O2 -g")

SET (CMAKE_CXX_FLAGS_INIT                "-Wall")
SET (CMAKE_CXX_FLAGS_DEBUG_INIT          "-g")
SET (CMAKE_CXX_FLAGS_MINSIZEREL_INIT     "-Os -DNDEBUG")
SET (CMAKE_CXX_FLAGS_RELEASE_INIT        "-O4 -DNDEBUG")
SET (CMAKE_CXX_FLAGS_RELWITHDEBINFO_INIT "-O2 -g")
```
* System wide C++ change on Ubuntu:
```
sudo update-alternatives --config c++
##   Selection    Path              Priority   Status
## ------------------------------------------------------------
## * 0            /usr/bin/g++       20        auto mode
##   1            /usr/bin/clang++   10        manual mode
##   2            /usr/bin/g++       20        manual mode

sudo update-alternatives --config cc
There are 2 choices for the alternative cc (providing /usr/bin/cc).

  Selection    Path            Priority   Status
------------------------------------------------------------
* 0            /usr/bin/gcc     20        auto mode
  1            /usr/bin/clang   10        manual mode
  2            /usr/bin/gcc     20        manual mode
```

## Compile errors

### types.h
```cpp
namespace eosio{ // originally, numerous conflicts with standard libraries.
   typedef long long            int64_t;
   typedef unsigned long long   uint64_t;
   typedef unsigned long        uint32_t;
   typedef unsigned short       uint16_t; 
   typedef long                 int32_t;
   typedef unsigned __int128    uint128_t;
   typedef __int128             int128_t;
   typedef unsigned char        uint8_t;
   typedef char                 int8_t;
   typedef short                int16_t;
   typedef unsigned int         size_t;
}
```


### body of constexpr function ... not a return-statement

/eos/contracts/eoslib/types.hpp:52:4: error: body of constexpr function ‘constexpr eosio::uint64_t eosio::string_to_name(const char*)’ not a return-statement
    }

```cpp
static constexpr char char_to_symbol( char c ) {
      if( c >= 'a' && c <= 'z' )
         return (c - 'a') + 6;
      if( c >= '1' && c <= '5' )
         return (c - '1') + 1;
      return 0;message
   }
```

From [cppreference](# http://en.cppreference.com/w/cpp/language/constexpr):

the function body must be either deleted or defaulted or contain only the following:
* null statements (plain semicolons)
* static_assert declarations
* typedef declarations and alias declarations that do not define classes or enumerations
* using declarations
* using directives
* **exactly one return statement**.

The same there:
```
   static constexpr eosio::uint64_t string_to_name( const char* str ) {

      eosio::uint32_t len = 0;
      while( str[len] ) ++len;

      eosio::uint64_t value = 0;

      for( eosio::uint32_t i = 0; i <= 12; ++i ) {
         eosio::uint64_t c = 0;
         if( i < len && i <= 12 ) c = char_to_symbol( str[i] );

         if( i < 12 ) {
            c &= 0x1f;
            c <<= 64-5*(i+1);
         }
         else {
            c &= 0x0f;
         }

         value |= c;
      }

      return value;
   }
```
I remove the constexpr declaration.

### types.h typedef eosio::uint32_t time;

eos/contracts/eoslib/types.h:35:25: error: ‘typedef eosio::uint32_t time’ 
redeclared as different kind of symbol
 typedef eosio::uint32_t time;

In file included from /usr/include/pthread.h:24:0,



## Letter

We are interested in building a development tool for EOS contracts that could be comparable to the Truffle device.

Our effort could be much easer if you would approve the following formal changes in the code of the *contracts* part:

* There are type definitions in *eoslib/types.h* that conflict with some standard libraries, for example:

```
eos/contracts/eoslib/types.h:27:33: error: conflicting declaration ‘typedef unsigned int size_t’
    typedef unsigned int         size_t;
                                 ^~~~~~
/usr/lib/gcc/x86_64-linux-gnu/7/include/stddef.h:216:23: note: previous declaration as ‘typedef long unsigned int size_t’
 typedef __SIZE_TYPE__ size_t;
                       ^~~~~~

//////////////////////////////////////
eos/contracts/eoslib/types.h:27:33: error: ‘typedef uint32_t time’ redeclared as different kind of symbol
    typedef uint32_t             time;
                                 ^~~~
/usr/include/time.h:75:15: note: previous declaration ‘time_t time(time_t*)’
 extern time_t time (time_t *__timer) __THROW;                       

///////////////////////////////////////
eos/contracts/eoslib/types.h:25:33: error: conflicting declaration ‘typedef char int8_t’
    typedef char                 int8_t;
                                 ^~~~~~
/usr/include/x86_64-linux-gnu/bits/stdint-intn.h:24:18: note: previous declaration as ‘typedef __int8_t int8_t’
 typedef __int8_t int8_t;
```

Could not they be put into a namespace?
```
namespace eosio{
   typedef long long            int64_t;
   typedef unsigned long long   uint64_t;
   typedef unsigned long        uint32_t;
   typedef unsigned short       uint16_t; 
   typedef long                 int32_t;
   typedef unsigned __int128    uint128_t;
   typedef __int128             int128_t;
   typedef unsigned char        uint8_t;
   typedef char                 int8_t;
   typedef short                int16_t;
   typedef unsigned int         size_t;
   typedef eosio::uint32_t      time;
}
```
* The same with two functions in *system.h*, namely *assert* and *now*.

* The formal definition of the *constexpr* function From :

In *eoslib/types.hpp* there are *constexpr* functions that do not adhere to the formal definition [cppreference](#http://en.cppreference.com/w/cpp/language/constexpr), and therefore the cause compile errors like this:
```
/eos/contracts/eoslib/types.hpp:52:4: error: body of constexpr function ‘constexpr eosio::uint64_t eosio::string_to_name(const char*)’ not a return-statement
    }
```
Could you consider replacing them with regular functions?

## Cleaning, starting, killing eosd

Extracted from /mnt/hgfs/Workspaces/EOS/eos/tests/eosd_run_test.sh

```
cd ${EOSIO_INSTALL_DIR}/build

function cleanup()
{
  rm -rf tn_data_0
  rm -rf test_wallet_0
}

verifyErrorCode()
{
  rc=$?
  if [[ $rc != 0 ]]; then
    error "FAILURE - $1 returned error code $rc"
  fi
}

SERVER="localhost"

programs/launcher/launcher
//verifyErrorCode "launcher"
sleep 7
count=`grep -c "generated block" tn_data_0/stderr.txt`
if [[ $count == 0 ]]; then
error "FAILURE - no blocks produced"
fi
```

