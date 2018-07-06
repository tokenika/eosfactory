#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>

#define DEBUG
#include "logger.hpp"
#include "@CONTRACT_NAME@.hpp" 

using namespace eosio;

class hello : public eosio::contract {
  public:
      using contract::contract; 

      /// @abi action 
      void hi( account_name user ) {
        logger_info( "user: ", name{user} );
        require_auth( user );
        print( "Hello, XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ", name{user} );
      }
};

EOSIO_ABI( hello, (hi) )
