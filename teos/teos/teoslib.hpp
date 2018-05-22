#pragma once

#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include <boost/property_tree/ptree.hpp>

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

    bool list()
    {
      WalletList command;
      if(!command.printError())
      {
      cout << command.responseToString();      
      }
      return true;
    }
  
    bool keys()
    {
      WalletKeys command;
      if(!command.printError())
      {
        cout << command.responseToString(); 
      }
      return true;              
    }

  };

  class KeyEosio
  {
  public:
    string name_;
    string private_;
    string public_;      
    KeyEosio()
    {
      name_ = "eosio";
      private_ = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3";
      public_ = "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV";
    }
  };

  class AccountCreator
  {
  public:
    string name_;
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

  class Account : public CreateAccount, public AccountCreator
  {
  public:
    AccountCreator* permission_;
    GetCode* getCode_;
    SetContract* setContract_;

    Account(
        AccountCreator creator, string name,
        Key key_owner, Key key_active,
        AccountCreator* permission = nullptr,
        unsigned expiration_sec = 30, 
        bool skip_signature = false,
        bool dont_broadcast = false,
        bool force_unique = false,
        unsigned max_cpu_usage = 0,
        unsigned max_net_usage = 0) 
        :
        AccountCreator(name),
        CreateAccount(
          creator.name_, name,
          key_owner.public_, key_active.public_,
          permission ? permission->name_ : "",
          expiration_sec, 
          skip_signature,
          dont_broadcast,
          force_unique,
          max_cpu_usage,
          max_net_usage
        ), getCode_(nullptr), setContract_(nullptr)
    {
      permission_ = permission;
      printError();
    }

    ~Account()
    {
      if(getCode_) {
        delete getCode_;
      }

      if(setContract_) {
        delete setContract_;
      }
    }

    string code(string wast_file="", string abiFile="")
    {
      if(getCode_){
        delete getCode_;
      }      
      getCode_ = new GetCode(name_, wast_file, abiFile);
      if(getCode_->printError())
      {
        return "";
      }
      return getCode_->respJson_.get<string>("code_hash");
    }

    SetContract setContract(
        string contract_dir, string wast_file="", string abi_file="", 
        string permission="", 
        int expiration_sec=30, int force_unique=0,
        int max_cpu_usage=0, int max_net_usage=0)
    {
      setContract_ = new SetContract(
        name_,
        contract_dir, wast_file, abi_file, permission, 
        expiration_sec, force_unique, max_cpu_usage, max_cpu_usage);

      return *setContract_;
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

    PushAction* action_;
    SetContract* setContract_;
    GetTable* getTable_;
    string console_;
    
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
              max_cpu_usage_(max_cpu_usage), max_net_usage_(max_net_usage),
              setContract_(nullptr), console_(""), action_(nullptr)
    {}

    ~Contract()
    {
      if(setContract_)
      {
        delete setContract_;
      }
      if(action_)
      {
        delete action_;
      }
      // if(getTable_)
      // {
      //   delete getTable_;
      // }      
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
      if(action_)
      {
        delete action_;
      }
      action_ = new PushAction(
        account_.name_, action, data,
          permission ? permission->name_ : account_.name_, 
          expiration_sec, 
          skip_signature, dont_broadcast, force_unique,
          max_cpu_usage, max_net_usage
        );
      if(!action_->printError())
      {
        console_ 
          = action_->respJson_.get(
              "processed.action_traces..console", "");
        cout << console_ << endl;
        return true;        
      }
      return false;
    }

    // bool get_table(
    //   string table,
    //   AccountCreator* scope = nullptr
    // )
    // {
    //   getTable_ = GetTable(table, scope ? scope->name : account_.name_);
    //   if(!action_->printError())
    //   {
    //     return true;
    //   }
    //   return false;
    // }
  };

}