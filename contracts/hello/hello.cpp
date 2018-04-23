#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>
/* 
Could not find bits/endian.h
There is one 
  E:\Workspaces\EOS\eos\contracts\musl\upstream\include
hence, I have copied it to 
  E:\Workspaces\EOS\eos\contracts\musl\upstream\include\bits
*/
using namespace eosio;

class hello : public eosio::contract {
  public:
      using contract::contract;

      /// @abi action 
      void hi( account_name user ) {
         print( "Hello, ", name{user} );
      }

      
};

EOSIO_ABI( hello, (hi) )