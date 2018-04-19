/**
 * @file command.hpp
 * @copyright defined in resources/LICENSE.txt
 * @brief Tool for sending transactions and querying state from EOS blockchain
 *
 * @brief Base definitions.
 *
 * Defines base classes of the project, and helper methods.
 */

#pragma once

#include <stdlib.h>
#include <string>
#include <iostream>
#include <boost/property_tree/ptree.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/program_options.hpp>
#include <teoslib/utilities.hpp>
#include <teoslib/control.hpp>
#include <teoslib/control/config.hpp>

#define TOKENIKA_WALLET "tokenikaWallet"

using namespace std;
using namespace boost::program_options;
using namespace boost::property_tree;

extern const string walletCommandPath;

namespace teos 
{
  class TeosCommand : public TeosControl
  {
  protected:
    string path_;
    void callEosd();
    virtual string normRequest(ptree& reqJson);
    virtual void normResponse(string response, ptree &respJson);
    virtual bool isWalletCommand() { return path_.find(walletCommandPath) != std::string::npos; };

  public:
    static string httpAddress;
    static string httpWalletAddress;

    TeosCommand(string path, ptree reqJson);
    TeosCommand(string path);
    TeosCommand(string errorMsg, string errorSender){
      errorRespJson(errorSender, errorMsg);
    }

    TeosCommand() {}

    void copy(TeosCommand teosCommand) {
      path_ = teosCommand.path_;
      reqJson_ = teosCommand.reqJson_;
      respJson_ = teosCommand.respJson_;
      isError_ = teosCommand.isError_;
    }
  };

  class CommandOptions : public ControlOptions
  {
  protected:

    options_description groupOptionDescription() {
      namespace control = teos::control;
      
      options_description od("");
      od.add_options()
        ("address,a", value<string>(&(TeosCommand::httpAddress))
            ->default_value(TeosCommand::httpAddress.empty() 
          ? teos::control::getHttpWalletAddress(nullptr)
          : TeosCommand::httpAddress),
          "The http address (host:port) of the EOSIO daemon.")
        ("wallet,w", value<string>(&(TeosCommand::httpWalletAddress))
            ->default_value(TeosCommand::httpWalletAddress.empty()
          ? teos::control::getHttpWalletAddress(nullptr)
          : TeosCommand::httpWalletAddress),
        "The http address (host:port) where eos-wallet is running.");
      od.add(ControlOptions::groupOptionDescription());
      return od;
    }

  public:
    CommandOptions(int argc, const char *argv[]) : ControlOptions(argc, argv) {}
    static options_description httpOptions();
  };
}