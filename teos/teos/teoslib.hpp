#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/property_tree/ptree.hpp>
#include <boost/foreach.hpp>

#include <teoslib/control/build_contract.hpp>
#include <teoslib/command/get_commands.hpp>
#include <teoslib/command/create_commands.hpp>
#include <teoslib/command/set_commands.hpp>
#include <teoslib/command/wallet_commands.hpp>
#include <teoslib/command/push_commands.hpp>

using namespace std;
using namespace boost::property_tree;


namespace teoslib
{    
  using namespace teos::control;
  using namespace teos::command;

  class Key : public CreateKey
  {
  public:
    string name_;
    string private_;
    string public_;

    Key(string name) : CreateKey(name)
    {
      name_ = name;
      if(!printError())
      {
        private_ = respJson_.get<string>("privateKey");
        public_ = respJson_.get<string>("publicKey");         
      }
    }
  };

  class Wallet : public WalletCreate
  {
  public:
    string name_;
    string password_;

    Wallet(string name = "default") : WalletCreate(name)
    {
      if(!printError())
      {
        name_ = name;
        password_ = respJson_.get<string>("password");
      }
    }

    vector<string> list(bool& isError)
    {
      WalletList command;
      vector<string> retval;

      isError = false;
      if(command.printError())
      {
        isError = true;
        return retval;        
      }

      BOOST_FOREACH(ptree::value_type &v
        , command.respJson_.get_child("wallets"))
      {
        retval.push_back(v.second.data());
      }
    }

    vector<string> list()
    {
      bool isError;
      return list(isError);
    }

    bool open()
    {
      WalletOpen command(name_);
      return !command.printError();
    }

    bool lock()
    {
      WalletLock command(name_);
      return !command.printError();
    }

    bool unlock()
    {
      WalletUnlock command(name_, password_);
      return !command.printError();
    }

    bool import_key(Key key)
    {
      WalletImport command(name_, key.private_);
      return !command.printError();
    }
  
    vector<string> keys(bool& isError)
    {
      WalletKeys command;
      vector<string> retval;

      isError = false;
      if(command.printError())
      {
        isError = true;
        return retval;
      }
      
      BOOST_FOREACH(ptree::value_type &v
        , command.respJson_.get_child("wallet keys"))
      {
        retval.push_back(v.second.data());
      }        
    }

    vector<string> keys()
    {
      bool isError;
      return keys(isError);
    }
  };

  class KeyEosio
  {
  public:
    string name_;
    string private_;
    string public_;
    ptree respJson_;      
    KeyEosio()
    {
      name_ = "eosio";
      private_ = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3";
      public_ = "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV";
      respJson_.put("privateKey", private_);
      respJson_.put("publicKey", public_);
    }
  };

  class AccountCreator
  {
  public:
    string name_;
    ptree respJson_;
    AccountCreator(string name)
    {
      name_ = name;
    }    
  };

  class AccountEosio : public AccountCreator
  {
  public:
    AccountEosio() : AccountCreator("eosio"){}      
  };

  class Account : public AccountCreator, CreateAccount
  {
  public:
    string permission_;
    ptree getCode_;
    ptree setContract_;

    Account(
        AccountCreator creator, string name,
        Key owner_key, Key active_key,
        string permission = "",
        unsigned expiration_sec = 30, 
        bool skip_signature = false,
        bool dont_broadcast = false,
        bool force_unique = false,
        unsigned max_cpu_usage = 0,
        unsigned max_net_usage = 0) 
        :
        AccountCreator(creator.name_),
        CreateAccount(
          creator.name_, name,
          owner_key.public_, active_key.public_,
          permission,
          expiration_sec, 
          skip_signature,
          dont_broadcast,
          force_unique,
          max_cpu_usage,
          max_net_usage
        )
    {
      name_ = name;
      permission_ = permission;
      printError();
    }

    string code(string wast_file="", string abiFile="")
    {
        GetCode getCode = GetCode(name_, wast_file, abiFile);
        getCode_ = getCode.respJson_;
        return getCode_.get("code", "");
    }

    ptree setContract(
        string contract_dir, string wast_file="", string abi_file="", 
        string permission="", 
        int expiration_sec=30, int force_unique=0,
        int max_cpu_usage=0, int max_net_usage=0)
    {
      SetContract setContract = SetContract(
        name_,
        contract_dir, wast_file, abi_file, permission, 
        expiration_sec, force_unique, max_cpu_usage, max_cpu_usage);

      setContract_ = setContract.respJson_;
      return setContract_;
    }

  };

  class Contract
  {
  public:
    AccountCreator account_;
    string contract_dir_;
    string wast_file_;
    string abi_file_;
    AccountCreator* permission_;
    int expiration_sec_;
    bool skip_signature_;
    bool dont_broadcast_;
    bool force_unique_;
    int max_cpu_usage_;
    int max_net_usage_;

    ptree action_;
    string console_;
    SetContract* setContract_;

    Contract(
          AccountCreator account, string contract_dir,
          AccountCreator* permission = nullptr,            
          string wast_file="", string abi_file="", 
          int expiration_sec=30, 
          bool skip_signature=0, bool dont_broadcast=0, bool force_unique=0,
          int max_cpu_usage=0, int max_net_usage=0) 
            : 
              account_(account), contract_dir_(contract_dir),
              wast_file_(wast_file), abi_file_(abi_file),
              permission_(permission),
              expiration_sec_(expiration_sec),
              skip_signature_(skip_signature), dont_broadcast_(dont_broadcast), 
              force_unique_(force_unique),
              max_cpu_usage_(max_cpu_usage), max_net_usage_(max_net_usage)
    {}

    ~Contract()
    {
      if(setContract_)
      {
        delete setContract_;
      }
    }

    bool deploy()
    {
      setContract_ = new SetContract(
          account_.name_, contract_dir_, 
          wast_file_, abi_file_, 
          permission_ ? permission_->name_ : "", 
          expiration_sec_, 
          skip_signature_, dont_broadcast_, force_unique_,
          max_cpu_usage_, max_net_usage_
        );
      return !setContract_->printError();
    }

    bool wast()
    {
      BuildContract buildContract(contract_dir_);
      return !buildContract.printError();
    }

    bool abi()
    {
      GenerateAbi generateAbi(contract_dir_);
      return !generateAbi.printError();
    }

    bool build()
    {
      if(!wast())
      {
        return false;
      }
      if(!abi())
      {
        return false;
      }
      return true;
    }

    bool push_action(
        string action, string data,
        AccountCreator* permission = nullptr, 
        int expiration_sec=30, 
        bool skip_signature=false, bool dont_broadcast=false, 
        bool force_unique=false,
        int max_cpu_usage=0, int max_net_usage=0
    )
    {
      PushAction command(
        account_.name_, action, data,
          permission_ ? permission_->name_ : "", 
          expiration_sec, 
          skip_signature, dont_broadcast, force_unique,
          max_cpu_usage, max_net_usage
        );

      action_ = command.respJson_;
      console_ = action_.get("processed.action_traces.0.console", "");
      return !command.printError();
    }
  };

}