#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/range/algorithm/sort.hpp>

#include <fc/variant.hpp>
#include <fc/io/json.hpp>
#include <eos/chain_plugin/chain_plugin.hpp>

#include <teos_command.hpp>
#include <teos_get_commands.hpp>
#include <teos_wallet_commands.hpp>

namespace tokenika
{
  namespace teos
  {
    class CallChain : public TeosCommand
    {
      std::string requestStr;
    public:
      fc::variant fcVariant;
    
      bool fcaVariant2ptree(const fc::variant& postData) {
        if (!postData.is_null()) {
          requestStr = fc::json::to_string(postData);
          stringstream ss;
          ss << requestStr;
          try {
            read_json(ss, reqJson);
            stringstream ss1;
            json_parser::write_json(ss1, reqJson, false);
            return true;
          }
          catch (exception& e) {
            reqJson.put(teos_ERROR, e.what());
            return false;
          }
        }
        return true;
      }

      CallChain(std::string path, const fc::variant& postData = fc::variant()) : TeosCommand( path, true) {
        if (fcaVariant2ptree(postData)) {
          callEosd();
        }
        //std::cout << path << std::endl;
        //std::cout << requestStr << std::endl;
        //std::cout << fc::json::to_pretty_string(fcVariant) << std::endl;
        if(isError()) {
          //std::cout << toStringRcv() << std::endl;
        }
      }

      std::string normRequest(ptree &regJson){ return requestStr; }
      void normResponse(std::string response, ptree &respJson);
    };

    void CallChain::normResponse(std::string response, ptree &respJson) {
      fcVariant = fc::json::from_string(response);
      stringstream ss;
      ss << response;
      try {
        read_json(ss, respJson);
        stringstream ss1; // Try to write respJson, in order to check it.
        json_parser::write_json(ss1, respJson, false);
      }
      catch (exception& e) {
        respJson.put(teos_ERROR, e.what());
      }
    }
  }
}

using namespace tokenika::teos;
using namespace eosio;

const string getChainPath = "/v1/chain/";

chain::signed_transaction sign_transaction(chain::signed_transaction& trx) 
{
  CallChain callPublicKeys(std::string(walletCommandPath + "get_public_keys"));
  const auto& public_keys = callPublicKeys.fcVariant;

  auto get_arg = fc::mutable_variant_object("transaction", trx)
    ("available_keys", public_keys);

  CallChain callRequiredKeys(string(getChainPath + "get_required_keys"), get_arg);
  const auto& required_keys = callRequiredKeys.fcVariant;
    
  fc::variants sign_args = {
    fc::variant(trx), required_keys["required_keys"], 
    fc::variant(chain::chain_id_type{})
  };

  CallChain callSignTransaction(std::string(walletCommandPath + "sign_transaction"), sign_args);
  return callSignTransaction.fcVariant.as<chain::signed_transaction>();
}

CallChain push_transaction(
  chain::signed_transaction& trx, 
  bool sign, 
  int expirationSec = 30) 
{
  CallChain callGetInfo(std::string(getCommandPath + "get_info"));
  //callGetInfo == call(host, port, get_info_func)
  auto info = callGetInfo.fcVariant.as<chain_apis::read_only::get_info_results>();

  trx.expiration = info.head_block_time + fc::seconds(expirationSec);
  transaction_set_reference_block(trx, info.head_block_id);
  boost::sort(trx.scope);

  if (sign) {
    trx = sign_transaction(trx);
  }

  CallChain callPushTransaction(string(getChainPath + "push_transaction"), fc::variant(trx));
  return callPushTransaction;
}

std::vector<types::name> sort_names(std::vector<types::name>&& names) {
  std::sort(names.begin(), names.end());
  auto itr = std::unique(names.begin(), names.end());
  names.erase(itr, names.end());
  return names;
}

CallChain createAccount(const ptree reqJson) {
  types::name creator = reqJson.get<string>("creator");
  types::name newaccount = reqJson.get<string>("name");

  auto owner_auth = chain::authority{ 1, { { types::public_key(reqJson.get<string>("ownerKey")), 1 } }, {} };
  auto active_auth = chain::authority{ 1, { { types::public_key(reqJson.get<string>("activeKey")), 1 } }, {} };
  auto recovery_auth = chain::authority{ 1, {}, { { { creator, "active" }, 1 } } };

  chain::signed_transaction trx;
  trx.scope = sort_names({ creator, config::eos_contract_name });
  transaction_emplace_message(trx, config::eos_contract_name, 
    vector<types::account_permission>{ {creator, "active"}}, "newaccount",
    types::newaccount{ creator, newaccount, owner_auth,
    active_auth, recovery_auth,  reqJson.get<int>("deposit") });
  return push_transaction(trx, !reqJson.get<bool>("skipSignature"), reqJson.get<int>("expiration"));
}

#ifdef WIN32
extern "C" FILE*  __cdecl __iob_func(void);
#endif // WIN32

int main(int argc, const char *argv[]) {
#ifdef WIN32
  __iob_func();
#endif // WIN32
  ptree reqJson;
  reqJson.put("creator", argv[3]);
  reqJson.put("name", argv[4]);
  reqJson.put("ownerKey", argv[5]);
  reqJson.put("activeKey", argv[6]);
  reqJson.put("skipSignature", false);
  reqJson.put("expiration", 90);
  reqJson.put("deposit", 1);

  CallChain create = createAccount(reqJson);
  std::cout << create.toStringRcv(false) << std::endl;

  return 0;
}
