#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/range/algorithm/find_if.hpp>
#include <boost/range/algorithm/sort.hpp>
#include <boost/range/adaptor/transformed.hpp>
#include <boost/algorithm/string/predicate.hpp>
#include <boost/algorithm/string/split.hpp>
#include <boost/range/algorithm/copy.hpp>
#include <boost/algorithm/string/classification.hpp>

#include <fc/crypto/private_key.hpp>
#include <fc/io/json.hpp>

#include <fc/variant.hpp>
#include <fc/io/fstream.hpp>
#include <eos/utilities/key_conversion.hpp>
#include <eosio/chain/authority.hpp>
#include <eosio/chain_plugin/chain_plugin.hpp>

#include <IR/Module.h>
#include <IR/Validate.h>
#include <WAST/WAST.h>
#include <WASM/WASM.h>
#include <Runtime/Runtime.h>

#include <teos/eos_interface.hpp>
#include <teos/command/get_commands.hpp>

using namespace std;

namespace teos {
  namespace command {

    KeyPair::KeyPair() {
      auto pk = fc::crypto::private_key::generate();
      publicKey = string(pk.get_public_key());
      privateKey = string(pk);
    }

    string KeyPair::privateK() {
      KeyPair kp;
      return kp.privateKey;
    }

    string KeyPair::prk = KeyPair::privateK();

    ////////////////////////////////////////

#define TEOS_ERROR true
#define CODE_PATH boost::str(boost::format("%1% (%2% [%3%]) ") % __func__ % __FILE__ % __LINE__)

    class CallChain : public teos::command::TeosCommand
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
            read_json(ss, reqJson_);
            stringstream ss1;
            json_parser::write_json(ss1, reqJson_, false);
            return true;
          }
          catch (exception& e) {
            putError(CODE_PATH, e.what());
          }
        }
        return true;
      }

      CallChain(std::string path, const fc::variant& postData = fc::variant())
        : TeosCommand(path)
      {
        if (fcaVariant2ptree(postData)) {
          callEosd();
        }
        //std::cout << path << std::endl;
        //std::cout << requestStr << std::endl;
        //std::cout << fc::json::to_pretty_string(fcVariant) << std::endl;
        if (isError_) {
          //std::cout << responseToString() << std::endl;
        }
      }

      std::string normRequest(ptree &regJson) { return requestStr; }
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
        putError(CODE_PATH, e.what());
      }
    }

    using namespace teos::command;
    using namespace eosio;
    //using namespace eosio::chain;
    //using namespace eosio::utilities;
    //using namespace boost::filesystem;

    const string getChainPath = "/v1/chain/";

    TeosCommand sign_transaction(chain::signed_transaction& trx)
    {
      CallChain callPublicKeys(std::string(walletCommandPath + "get_public_keys"));
      if (callPublicKeys.isError_) {
        return callPublicKeys;
      }
      const auto& public_keys = callPublicKeys.fcVariant;

      auto get_arg = fc::mutable_variant_object("transaction", trx)
        ("available_keys", public_keys);

      CallChain callRequiredKeys(string(getChainPath + "get_required_keys"), get_arg);
      if (callRequiredKeys.isError_) {
        return callRequiredKeys;
      }

      const auto& required_keys = callRequiredKeys.fcVariant;

      fc::variants sign_args = {
        fc::variant(trx), required_keys["required_keys"],
        fc::variant(chain::chain_id_type{})
      };

      CallChain callSignTransaction(std::string(walletCommandPath + "sign_transaction"),
        sign_args);
      if (callSignTransaction.isError_) {
        return callSignTransaction;
      }

      trx = callSignTransaction.fcVariant.as<chain::signed_transaction>();
      return callSignTransaction;
    }

    TeosCommand push_transaction(
      chain::signed_transaction& trx,
      bool sign,
      int expirationSec = 30)
    {
      //callGetInfo == call(host, port, get_info_func)  
      CallChain callGetInfo(string(getCommandPath + "get_info"));
      if (callGetInfo.isError_) {
        return callGetInfo;
      }

      auto info = callGetInfo.fcVariant.as<chain_apis::read_only::get_info_results>();
      trx.expiration = info.head_block_time + fc::seconds(expirationSec);
      trx.set_reference_block(info.head_block_id);

      if (sign) {
        TeosCommand respJson = sign_transaction(trx);
        if (respJson.isError_) {
          return respJson;
        }
      }

      CallChain callPushTransaction(string(getChainPath + "push_transaction"),
        fc::variant(trx));
      return callPushTransaction;
    }

    vector<chain::permission_level> get_account_permissions(const vector<string>& permissions) {
      auto fixedPermissions = permissions | boost::adaptors::transformed([](const string& p) {
        vector<string> pieces;
        split(pieces, p, boost::algorithm::is_any_of("@"));
        //EOSC_ASSERT(pieces.size() == 2, "Invalid permission: ${p}", ("p", p));
        return chain::permission_level{ .actor = pieces[0], .permission = pieces[1] };
      });
      vector<chain::permission_level> accountPermissions;
      boost::range::copy(fixedPermissions, back_inserter(accountPermissions));
      return accountPermissions;
    }


    TeosCommand assemble_wast(const std::string& wast, vector<uint8_t>& wasm)
    {
      IR::Module module;
      std::vector<WAST::Error> parseErrors;
      WAST::parseModule(wast.c_str(), wast.size(), module, parseErrors);
      if (parseErrors.size())
      {
        stringstream  msg;
        msg << "Error parsing WebAssembly text file:" << std::endl;
        for (auto& error : parseErrors)
        {
          msg << ":" << error.locus.describe() << ": " << error.message.c_str() << std::endl;
          msg << error.locus.sourceLine << std::endl;
          msg << std::setw(error.locus.column(8)) << "^" << std::endl;
        }
        return TeosCommand(TEOS_ERROR, TeosCommand::errorRespJson(CODE_PATH, msg.str()));
      }

      try
      {
        // Serialize the WebAssembly module.
        Serialization::ArrayOutputStream stream;
        WASM::serialize(stream, module);
        wasm = stream.getBytes();
      }
      catch (Serialization::FatalSerializationException exception)
      {
        stringstream  msg;
        msg << "Error serializing WebAssembly binary file:" << std::endl;
        msg << exception.message << std::endl;

        return TeosCommand(TEOS_ERROR, TeosCommand::errorRespJson(CODE_PATH,msg.str()));
      }
      return TeosCommand(CODE_PATH);
    }

    TeosCommand createAccount(string creatorStr, string nameStr,
      string ownerKey, string activeKey,  uint64_t staked_deposit,
      bool skipSignature, int expiration)
    {
      try {
        chain::name creator = creatorStr;
        chain::name newaccount = nameStr;

        auto owner_auth = chain::authority{ 1,{ { chain::public_key_type(ownerKey), 1 } },{} };
        auto active_auth = chain::authority{ 1,{ { chain::public_key_type(activeKey), 1 } },{} };
        auto recovery_auth = chain::authority{ 1,{},{ { { creator, "active" }, 1 } } };

        chain::signed_transaction trx;
        trx.actions.emplace_back( vector<chain::permission_level>{{creator,"active"}},
          chain::contracts::newaccount{creator, newaccount, owner_auth, active_auth, recovery_auth, 
          staked_deposit });

        return push_transaction(trx, !skipSignature, expiration);
      }
      catch (const std::exception& e) {
        return TeosCommand(TEOS_ERROR, TeosCommand::errorRespJson(CODE_PATH, e.what()));
      }
    }

    TeosCommand setContract(string account, string wastPath, string abiPath,
      bool skipSignature, int expiration)
    {
      try {
        if (!boost::filesystem::exists(wastPath)) {
          return TeosCommand(TEOS_ERROR,
            TeosCommand::errorRespJson(CODE_PATH, boost::str(boost::format(
              "Cannot find the wast file:\n %1%\n does not exist!\n") % wastPath)));
        }

        std::string wast;
        fc::read_file_contents(wastPath, wast);
        vector<uint8_t> wasm;

        const string binary_wasm_header = "\x00\x61\x73\x6d";
        if(wast.compare(0, 4, binary_wasm_header) == 0) {
          wasm = vector<uint8_t>(wast.begin(), wast.end());
        }
        else {
          TeosCommand status = assemble_wast(wast, wasm);
          if (status.isError_) {
            return status;
          }          
        }

        chain::contracts::setcode handler;
        handler.account = account;
        handler.code.assign(wasm.begin(), wasm.end());

        chain::signed_transaction trx;
        trx.actions.emplace_back( vector<chain::permission_level>{{account,"active"}}, handler);

        if (abiPath.length() > 0) {
          if (!boost::filesystem::exists(abiPath)) {
            return TeosCommand(TEOS_ERROR,
              TeosCommand::errorRespJson(CODE_PATH, boost::str(boost::format(
                "Cannot find the abi file:\n %1%\n does not exist!\n") % abiPath)));
          }
          chain::contracts::setabi handler;
          handler.account = account;
          handler.abi = fc::json::from_file(abiPath).as<chain::contracts::abi_def>();
          trx.actions.emplace_back( vector<chain::permission_level>{{account,"active"}}, handler);
        }
        //std::cout << "Publishing contract..." << std::endl;
        return push_transaction(trx, !skipSignature, expiration);
      }
      catch (const std::exception& e) {
        return TeosCommand(TEOS_ERROR,
          TeosCommand::errorRespJson(CODE_PATH, e.what()));
      }
    }

    TeosCommand getCode(string accountName, string wastPath, string abiPath) {
      //auto result = call(get_code_func, fc::mutable_variant_object("account_name", accountName));
      CallChain callGetCode(string(getCommandPath + "get_code"), 
        fc::mutable_variant_object("account_name", accountName));
      auto result = callGetCode.fcVariant;

      if (wastPath.size()) {
        auto code = result["wast"].as_string();
        std::ofstream out(wastPath.c_str());
        if (out.is_open()) {
          out << code;
        }
        else {
          return TeosCommand(TEOS_ERROR,
            TeosCommand::errorRespJson(CODE_PATH, boost::str(boost::format(
              "Cannot open the wast file:\n %1%\n") % wastPath)));
        }
      }

      if (abiPath.size()) {
        auto abi = fc::json::to_pretty_string(result["abi"]);
        std::ofstream out(abiPath.c_str());
        if (out.is_open()) {
          out << abi;
        }
        else {
          return TeosCommand(TEOS_ERROR,
            TeosCommand::errorRespJson(CODE_PATH, boost::str(boost::format(
              "Cannot open the abi file:\n %1%\n") % abiPath)));
        } 
      }
      return callGetCode;
    }

    uint64_t generate_nonce_value() {
      return fc::time_point::now().time_since_epoch().count();
    }

    chain::action generate_nonce() {
      return chain::action( {}, chain::contracts::nonce{.value = generate_nonce_value()} ); 
    }

    TeosCommand pushAction(string contract, string action, string data, 
      const vector<string> scopes, const vector<string> permissions, 
      bool skipSignature, int expiration, 
      bool tx_force_unique)
    {
      try {
        auto arg = fc::mutable_variant_object ("code", contract) ("action", action)
          ("args", fc::json::from_string(data));

        //auto result = call(json_to_bin_func, arg);
        CallChain call("/v1/chain/abi_json_to_bin", arg);
        auto result = call.fcVariant;

        auto accountPermissions = get_account_permissions(permissions);

        chain::signed_transaction trx;
        trx.actions.emplace_back(accountPermissions, contract, action, result.get_object()["binargs"]
          .as<chain::bytes>());

        if (tx_force_unique) {
          trx.actions.emplace_back( generate_nonce() );
        }

        return push_transaction(trx, !skipSignature, expiration);
      }
      catch (const std::exception& e) {
        return TeosCommand(TEOS_ERROR, TeosCommand::errorRespJson(CODE_PATH, e.what()));
      }
    }

  }
}