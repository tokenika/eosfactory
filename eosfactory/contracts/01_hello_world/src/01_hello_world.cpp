#include <eosiolib/eosio.hpp>
#include <eosiolib/print.hpp>

#define DEBUG
#include "logger.hpp"

using namespace eosio;

class [[eosio::contract("01_hello_world")]] hello : public contract {
  public:
      using contract::contract;

      [[eosio::action]]
      void hi( name user ) {
         logger_info( "debug user name: ", name{user} );
         require_auth( user );
         print( "Hello, ", user);
      }
};

EOSIO_DISPATCH( hello, (hi))