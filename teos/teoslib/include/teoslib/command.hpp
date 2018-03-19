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
    void putError(string msg);
    void putError(string sender, string msg);
    void callEosd();
    virtual string normRequest(ptree& reqJson);
    virtual void normResponse(string response, ptree &respJson);
    virtual bool isWalletCommand() { return path_.find(walletCommandPath) != std::string::npos; };

  public:
    static ptree errorRespJson(string sender, string message);
    static string httpAddress;
    static string httpWalletAddress;

    TeosCommand(string path, ptree reqJson);
    TeosCommand(string path);
    TeosCommand(bool isError, ptree respJson);
    TeosCommand() {}

    void copy(TeosCommand teosCommand) {
      path_ = teosCommand.path_;
      reqJson_ = teosCommand.reqJson_;
      respJson_ = teosCommand.respJson_;
      isError_ = teosCommand.isError_;
    }

    ptree getResponse() const {
      return respJson_;
    }

  };

#define HTTP_SERVER_ADDRESS_DEFAULT "127.0.0.1:8888"
#define HTTP_SERVER_WALLET_ADDRESS_DEFAULT "127.0.0.1:8888"

  class CommandOptions : public ControlOptions
  {
  protected:

    options_description groupOptionDescription() {
      options_description od("");
      od.add(httpOptions());
      od.add_options()
        ("json,j", value<string>(&json_), "Json argument.")      
        ("received,v", "Print received json.")
        ("both,b", "For system use.")
        ("raw,r", "Raw print");
      return od;
    }

  public:
    CommandOptions(int argc, const char *argv[]) : ControlOptions(argc, argv) {}
    static options_description httpOptions();
  };
}