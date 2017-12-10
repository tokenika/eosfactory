## One by One
* chain_controller.cpp 276
* chain_controller.hpp 176 Not producing block because node didn't wake up within 500ms of the slot time.




* producer_plugin.cpp 194 Not producing block because node didn't wake up within 500ms of the slot time.



## Napping allowed

producer_plugin.cpp: 307
   if( llabs(((scheduled_time - now).count()) > fc::milliseconds( 500 ).count()) && !_napping_allowed )
   {
      capture("scheduled_time", scheduled_time)("now", now);
      return block_production_condition::lag;
   }

producer_plugin.cpp: 82
      producer_options.add_options()
         ("enable-stale-production", boost::program_options::bool_switch()->notifier([this](bool e){my->_production_enabled = e;}), "Enable block production, even if the chain is stale.")
         ("enable-napping-allowed", boost::program_options::bool_switch()->notifier([this](bool e){my->_napping_allowed = e;}), "Do not control time between blocks.") ////////////////////////////////////////Cartman addition
         ("required-participation", boost::program_options::bool_switch()->notifier([this](int e){my->_required_producer_participation = uint32_t(e*config::Percent1);}), "Percent of producers (0-99) that must be participating in order to produce blocks")
         ("producer-name,p", boost::program_options::value<vector<string>>()->composing()->multitoken(),
          ("ID of producer controlled by this node (e.g. inita; may specify multiple times)"))
         ("private-key", boost::program_options::value<vector<string>>()->composing()->multitoken()->default_value({fc::json::to_string(private_key_default)},
                                                                                                fc::json::to_string(private_key_default)),
          "Tuple of [PublicKey, WIF private key] (may specify multiple times)")
         ;


producer_plugin.cpp: 25
class producer_plugin_impl {
public:
   producer_plugin_impl(boost::asio::io_service& io)
      : _timer(io) {}
   void schedule_production_loop();
   block_production_condition::block_production_condition_enum block_production_loop();
   block_production_condition::block_production_condition_enum maybe_produce_block(fc::mutable_variant_object& capture);

   boost::program_options::variables_map _options;
   bool _production_enabled = false;
   bool _napping_allowed = false; ////////////////////////////////////////////////////Cartman addition
   
   (...)   

## Where is

```
workspaceDir="/mnt/hgfs/Workspaces/EOS/eoscBash/Contracts" &&\
contractSrcDir=${workspaceDir}/hello2 &&\
source /mnt/hgfs/Workspaces/EOS/eoscBash/eoscBash $EOSIO_INSTALL_DIR

eosc buildContract ${contractSrcDir}/hello2.cpp && \
eosc wallet create && \
eosc wallet import $initaPrivKey && \
eosc wallet unlock && \
eosc set contract \
  ${initaAccount} \
  ${contractSrcDir}/hello2.wast \
  ${contractSrcDir}/hello2.abi
##
## ls ${contractSrcDir}
## hello2.abi
## hello2.cpp
## hello2.wast
##
## eosc wallet create default:
## $defaultWalletPswd ...is stored in your safe.
##
## eosc wallet import $initaPrivKey:
## imported private key for $initaPublKey
##
## eosc wallet unlock default:
## Unlocked: default
##
## ${contractSet} ... set-contract json.
```
```
jq '.processed.messages' <<< "$contractSet"
[
  {
    "code": "eos",
    "type": "setcode",
    "authorization": [
      {
        "account": "inita",
        "permission": "active"
      }
    ],
    "data": (...)
  }
]
```

```
eosc push message ${initaAccount} transfer \
  '{"from":"currency","to":"inita","amount":50}' \
  --scope initc
1270028ms thread-0   main.cpp:1034                 operator()           ] Converting argument to binary...
##
## ${messagePushed} ... push-transaction json.
```
```
jq '.processed.messages' <<< "$messagePushed"
[
  {
    "code": "inita",
    "type": "transfer",
    "authorization": [],
    "data": {
      "from": "currency",
      "to": "inita",
      "amount": 50
    },
    "hex_data": "0000001e4d75af46000000000093dd743200000000000000"
  }
]
...



This example assumes a transfer operation. The refBlockNum and refBlockPrefix are provided as a result of /v1/chain/get_block.
```
curl  http://localhost:8888/v1/chain/push_transaction -X POST -d '
{   
   "refBlockNum": 63,
   "refBlockPrefix":"3452708124",
   "expiration":"2017-11-02T17:12:12",
   "scope":["eos","inita"],
   "messages":
   [
      {
         "code":"currency",
         "type":"transfer",
         "recipients":["initb","initc"],
         "authorization":[{"account":"initb","permission":"active"}],
         "data":"000000000041934b000000008041934be803000000000000"
      }
   ],
   "signatures":[],
   "authorizations":[]
}
'
```
```
msg="http://localhost:8888/v1/chain/push_transaction -X POST -d '
{   
   \"refBlockNum\":\"100\",
   \"refBlockPrefix\":\"137469861\",
   \"expiration\":\"2017-09-25T06:28:49\",
   \"scope\":[\"initc\"],
   \"messages\":
   [
      {
         \"code\":\"inita\",
         \"type\":\"transfer\",
         \"recipients\":[\"initb\",\"initc\"],
         \"authorization\":[],
         \"data\":{
            \"from\": \"currency\",
            \"to\": \"inita\",
            \"amount\": 50
         }
      }
   ],
   \"signatures\":[],
   \"authorizations\":[]
}
'"

curl  http://localhost:8888/v1/chain/push_transaction -X POST -d '{"refBlockNum":"712","refBlockPrefix":"137469861", "expiration":"2017-11-03T07:50:50","scope":["initc"],"messages":[{"code":"inita","type":"transfer","recipients":["initb","initc"],"authorization":[],"data":{"from":"currency","to":"inita","amount":50}}],"signatures":[], "authorizations":[]}'


curl  http://localhost:8888/v1/chain/push_transaction -X POST -d '{"scope":["initc"],"messages":[{"code":"inita","type":"transfer","recipients":["initb","initc"],"authorization":[],"data":{"from":"currency","to":"inita","amount":50}}],"signatures":[], "authorizations":[]}'

xx=$(curl  http://localhost:8888/v1/account_history/get_transaction -X POST -d '{"transaction_id": "18cfb86e8e4b0f92c8ba00862bb856c71e294863989bda0e2d8fc7a8d9a72df4"}')jq <<< "$xx"
{
  "transaction_id": "18cfb86e8e4b0f92c8ba00862bb856c71e294863989bda0e2d8fc7a8d9a72df4",
  "transaction": {
    "refBlockNum": 2248,
    "refBlockPrefix": 2899029981,
    "expiration": "2017-11-05T18:37:42",
    "scope": [
      "initc"
    ],
    "signatures": [],
    "messages": [
      {
        "code": "inita",
        "type": "transfer",
        "authorization": [],
        "data": {
          "from": "currency",
          "to": "inita",
          "amount": 50
        },
        "hex_data": "0000001e4d75af46000000000093dd743200000000000000"
      }
    ],
    "output": [
      {
        "notify": [],
        "deferred_transactions": []
      }
    ]
  }
}

/mnt/hgfs/Workspaces/EOS/eos/programs/eosc/main.cpp:619
   // get transaction
   string transactionId;
   auto getTransaction = get->add_subcommand("transaction", localized("Retrieve a transaction from the blockchain"), false);
   getTransaction->add_option("id", transactionId, localized("ID of the transaction to retrieve"))->required();
   getTransaction->set_callback([&] {
      auto arg= fc::mutable_variant_object( "transaction_id", transactionId);
      std::cout << fc::json::to_pretty_string(call(get_transaction_func, arg)) << std::endl;
   });

























curl  http://localhost:8888/v1/chain/push_transaction -X POST -d '{"refBlockNum":"100","refBlockPrefix":"137469861","expiration":"2017-09-25T06:28:49","scope":["initb","initc"],"messages":[{"code":"currency","type":"transfer","recipients":["initb","initc"],"authorization":[{"account":"initb","permission":"active"}],"data":"000000000041934b000000008041934be803000000000000"}],"signatures":[],"authorizations":[]}'




curl  http://localhost:8888/v1/chain/push_transaction -X POST -d '\
{\   
   "refBlockNum":"100",\
   "refBlockPrefix":"137469861",\
   "expiration":"2017-09-25T06:28:49",\
   "scope":["initc"],\
   "messages":\
   [\
      {\
         "code":"inita",\
         "type":"transfer",\
         "recipients":["initb","initc"],\
         "authorization":[],\
         "data":{
            "from": "currency",
            "to": "inita",
            "amount": 50
         }\
      }\
   ],\
   "signatures":[],\
   "authorizations":[]
}\
'
```