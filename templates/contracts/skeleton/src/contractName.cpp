#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>

#define DEBUG
#include "logger.hpp"
#include "@contractName@.hpp" 

using namespace eosio;

class hello : public eosio::contract {
  public:
      using contract::contract; 

      /// @abi action 
      void hi( account_name user ) {
        logger_info("account name: ", user);
        print( "Hello, ", name{user} );
      }
};

EOSIO_ABI( hello, (hi) )