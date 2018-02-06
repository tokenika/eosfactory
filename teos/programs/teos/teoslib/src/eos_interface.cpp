#include <eos/types/types.hpp>
#include <eos/types/public_key.hpp>
#include <fc/crypto/base58.hpp>

#include <fc/io/raw.hpp>
#include <fc/crypto/hmac.hpp>
#include <fc/crypto/openssl.hpp>
#include <fc/crypto/ripemd160.hpp>

#include <eos/utilities/key_conversion.hpp>
#include <fc/crypto/base58.hpp>
#include <fc/variant.hpp>

#include <eos_interface.hpp>

#include <boost/range/algorithm/sort.hpp>

#include <fc/variant.hpp>
#include <fc/io/json.hpp>
#include <eos/chain_plugin/chain_plugin.hpp>

using namespace std;

namespace tokenika {
  namespace teos {

    KeyPair::KeyPair() {
      fc::ecc::private_key pk = fc::ecc::private_key::generate();
      publicKey = string(eosio::types::public_key(pk.get_public_key()));
      privateKey = eosio::utilities::key_to_wif(pk.get_secret());
    }

    string KeyPair::privateK() {
      KeyPair kp;
      return kp.privateKey;
    }
    
    string KeyPair::prk = KeyPair::privateK();

////////////////////////////////////////

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

CallChain createAccount(string creatorStr, string nameStr,
  string ownerKey, string activeKey,
  bool skipSignature, int expiration, int deposit) 
{
  types::name creator = creatorStr;
  types::name newaccount = nameStr;

  auto owner_auth = chain::authority{ 1,{ { types::public_key(ownerKey), 1 } },{} };
  auto active_auth = chain::authority{ 1,{ { types::public_key(activeKey), 1 } },{} };
  auto recovery_auth = chain::authority{ 1,{},{ { { creator, "active" }, 1 } } };

  chain::signed_transaction trx;
  trx.scope = sort_names({ creator, config::eos_contract_name });
  transaction_emplace_message(trx, config::eos_contract_name,
    vector<types::account_permission>{ {creator, "active"}}, "newaccount",
    types::newaccount{ creator, newaccount, owner_auth,
    active_auth, recovery_auth,  deposit });
  return push_transaction(trx, !skipSignature, expiration);
}
