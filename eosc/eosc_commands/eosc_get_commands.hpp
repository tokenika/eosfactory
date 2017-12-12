/**
 * @file eosc_get_commands.hpp
 *
 * Definitions for get-type commands.
 *
 * Defines command line options.
 */

#pragma once

#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/property_tree/ptree.hpp>

#include "../eosc_config.h"
#include "eosc_command.hpp"

namespace tokenika
{
  namespace eosc
  {

    /**
     * @brief Get current blockchain information.
     *
     * Example:
     *
     * @verbatim
     * #include <stdio.h>
     * #include <stdlib.h>
     * #include <iostream>
     * #include <string>
     * #include <boost/property_tree/ptree.hpp>
     * #include "EoscCommands/eosc_get_commands.hpp"
     *
     * int main(int argc, char *argv[])
     * {
     * boost::property_tree::ptree postJson;
     * tokenika::eosc::GetInfo GetInfo(getInfoPostJson);
     * std::cout << GetInfo.get<int>("last_irreversible_block_num")) << std::endl;
     * boost::property_tree::ptree rcv_json = GetInfo.getRcvJson();
     * std::cout << GetBlock.toStringRcv() << std::endl; // Print the response json.
     *
     * return 0;
     * }
     * @endverbatim
     */
    class GetInfo : public EoscCommand
    {
    public:

      GetInfo(
        boost::property_tree::ptree postJson,
        bool raw = false)
        : EoscCommand(
          "/v1/chain/get_info",
          postJson,
          raw) {}
    };

    class GetInfoOptions : public CommandOptions
    {
    public:
      GetInfoOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Get current blockchain information
Usage: ./eosc get info [Options]
Usage: ./eosc get info [-j '{}'] [OPTIONS]
)EOF";
      }

      virtual bool setJson(boost::program_options::variables_map &vm) {
        return true;
      }

      virtual EoscCommand getCommand(bool is_raw) {
        return GetInfo(postJson, is_raw);
      }

      virtual void getOutput(tokenika::eosc::EoscCommand command) {
        output("head block", "%d", command.get<int>("head_block_num"));
        output("head block time", "%s", command.get<std::string>("head_block_time").c_str());
        output("last irreversible block", "%d", command.get<int>("last_irreversible_block_num"));
      }

      virtual void getExample() {
        boost::property_tree::ptree postJson;
        GetInfo GetInfo(postJson);
        std::cout << R"EOF(
Invoke 'GetInfo' command:
GetInfo GetInfo;
)EOF" << std::endl;
        std::cout << GetInfo.toStringRcv() << std::endl;
      }
    };

    /**
     * @brief Retrieve a full block from a blockchain.
     *
     * Given a `boost::property_tree::ptree json`, conforms ([after eosjs-json]
     * (#https://github.com/EOSIO/eosjs-json/blob/master/api/v1/chain.json)) this
     * pattern:
     * @verbatim
     * {"block_num_or_id":"uint32 | string"}.
     * @endverbatim
     *
     * the constructor posts it to
     * an EOS block socket, specified in the `eosc_config.json` file. The responce
     * of the blockchain is, again, a `boost::property_tree::ptree json`. On error,
     * the reaponce json is `{"error":"error message"}`, otherwise it conforms
     * ([after eosjs-json]
     * (#https://github.com/EOSIO/eosjs-json/blob/master/api/v1/chain.json)) this
     * pattern:
     * @verbatim
     * {
     * "previous":"uint32",
     * "timestamp":"2017-07-18T20:16:36",
     * "transaction_merkle_root":"uint32",
     * "producer":"uint16",
     * "producer_changes":"map<account_name, account_name>[]",
     * "producer_signature":"signature",
     * "cycles":"thread[]",
     * "id":"fixed_bytes33",
     * "block_num":"uint32",
     * "refBlockPrefix":"uint32"
     * }
     * @endverbatim
     *
     * It is available with the \ref tokenika::eosc::EoscCommand::getRcvJson() method.
     *
     * Note that time is a string. For processing, it has to be expressed as a
     * structure and afterwords back to a string. Helper functions, namely
     * ::strToTime(const std::string)
     *
     * Example:
     *
     * @verbatim
     * #include <stdio.h>
     * #include <stdlib.h>
     * #include <iostream>
     * #include <string>
     *
     * #include <boost/property_tree/ptree.hpp>
     * #include "boost/date_time/posix_time/posix_time.hpp"
     *
     * #include "EoscCommands/eosc_get_commands.hpp"
     *
     * int main(int argc, char *argv[])
     * {
     * boost::property_tree::ptree postJson;
     * postJson.put("block_num_or_id", 25);
     * tokenika::eosc::GetBlock getBlock(getInfoPostJson);
     * if(!getBlock.isError())
     * {
     *    std::cout << getBlock.get<int>("last_irreversible_block_num")) << std::endl;
     *    boost::posix_time::ptime time = GetInfo.get<boost::posix_time::ptime>("timestamp");
     *    std::cout << time << std::endl;
     *    boost::posix_time::ptime t1 = time + boost::posix_time::seconds(900);
     *    cout << (boost::posix_time::to_iso_extended_string)(t1) << endl;
     * } else
     * {
     *    std::cerr << getBlock.get<string>("error")) << std::endl;
     * }
     *
     * return 0;
     * }
     * @endverbatim
     */
    class GetBlock : public EoscCommand
    {
    public:

      GetBlock(boost::property_tree::ptree postJson, bool raw = false)
        : EoscCommand(
          "/v1/chain/get_block",
          postJson,
          raw) {}
    };

    class GetBlockOptions : public CommandOptions
    {
    public:
      GetBlockOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Retrieve a full block from the blockchain
Usage: ./eosc get block [block_num] [Options]
Usage: ./eosc get block [-j '{"block_num_or_id":"int | string"}'] [OPTIONS]
)EOF";
      }

      int n;
      std::string id;

      virtual boost::program_options::options_description options() {
        boost::program_options::options_description special("");
        special.add_options()
          ("block_num,n",
            boost::program_options::value<int>(&n),
            "Block number")
            ("block_id,i",
              boost::program_options::value<std::string>(&id),
              "Block id");
        return special;
      }

      virtual void
        setPosDesc(boost::program_options::positional_options_description&
          pos_desc) {
        pos_desc.add("block_num", 1);
      }

      virtual bool setJson(boost::program_options::variables_map &vm) {
        bool ok = false;
        if (vm.count("block_num")) {
          postJson.put("block_num_or_id", n);
          ok = true;
        }
        else if (vm.count("block_id")) {
          postJson.put("block_num_or_id", id);
          ok = true;
        }
        return ok;
      }

      virtual EoscCommand getCommand(bool is_raw) {
        return GetBlock(postJson, is_raw);
      }

      virtual void getOutput(EoscCommand command) {
        output("block number", "%d", command.get<int>("block_num"));
        output("timestamp", "%s", command.get<std::string>("timestamp").c_str());
        output("ref block prefix", "%s", command.get<std::string>("ref_block_prefix").c_str());
      }

      virtual void getExample() {
        boost::property_tree::ptree getInfoPostJson;
        GetInfo GetInfo(getInfoPostJson);
        std::cout << R"EOF(
Invoke 'GetInfo' command:
GetInfo getInfo;
)EOF" << std::endl;

        std::cout << GetInfo.toStringRcv() << std::endl;
        boost::property_tree::ptree GetBlock_post_json;
        GetBlock_post_json.put("block_num_or_id", 25);
        GetBlock GetBlock(GetBlock_post_json);
        std::cout << R"EOF(
Use reference to the last block:
GetBlock GetBlock(
  GetInfo.get<int>("last_irreversible_block_num"));
)EOF" << std::endl;
        std::cout << GetBlock.toStringRcv() << std::endl;
      }
    };
  }
}