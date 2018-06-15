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
    static bool print_request;
    static bool print_response;

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
      od.add_options();
      od.add_options()
        ("address,a", value<string>(&(TeosCommand::httpAddress)),
          (string("The http address (host:port) of the EOSIO node. ")
           + "Default value is: " + TeosCommand::httpAddress).c_str())
        ("wallet,w", value<string>(&(TeosCommand::httpWalletAddress)),
          (string("The http address (host:port) where eos-wallet is running.")
          + " Default value is: " + TeosCommand::httpWalletAddress).c_str())
        ("print-request", value<bool>(&(TeosCommand::print_request)), 
          "Print HTTP request")
        ("print-response", value<bool>(&(TeosCommand::print_response)), 
          "Print HTTP response");
      od.add(ControlOptions::groupOptionDescription());
      return od;
    }

  public:
    CommandOptions(int argc, const char *argv[]) : ControlOptions(argc, argv) 
    {
      TeosCommand::httpAddress = TeosCommand::httpAddress.empty() 
          ? teos::control::getHttpWalletAddress(nullptr)
          : TeosCommand::httpAddress;
      TeosCommand::httpWalletAddress = TeosCommand::httpWalletAddress.empty()
          ? teos::control::getHttpWalletAddress(nullptr)
          : TeosCommand::httpWalletAddress;
    }
    static options_description httpOptions();
  };

  
}