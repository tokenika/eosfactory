
#         eosio <= eosio::newaccount            {"creator":"yvngxrjzbf3w","name":"mnmsvtabluzl","owner":{"threshold":1,"keys":[{"key":"EOS663NVVFETZ...
#         eosio <= eosio::buyrambytes           {"payer":"yvngxrjzbf3w","receiver":"mnmsvtabluzl","bytes":8192}
#   eosio.token <= eosio.token::transfer        {"from":"yvngxrjzbf3w","to":"eosio.ram","quantity":"4.9469 EOS","memo":"buy ram"}
#  yvngxrjzbf3w <= eosio.token::transfer        {"from":"yvngxrjzbf3w","to":"eosio.ram","quantity":"4.9469 EOS","memo":"buy ram"}
#     eosio.ram <= eosio.token::transfer        {"from":"yvngxrjzbf3w","to":"eosio.ram","quantity":"4.9469 EOS","memo":"buy ram"}
#   eosio.token <= eosio.token::transfer        {"from":"yvngxrjzbf3w","to":"eosio.ramfee","quantity":"0.0249 EOS","memo":"ram fee"}
#  yvngxrjzbf3w <= eosio.token::transfer        {"from":"yvngxrjzbf3w","to":"eosio.ramfee","quantity":"0.0249 EOS","memo":"ram fee"}
#  eosio.ramfee <= eosio.token::transfer        {"from":"yvngxrjzbf3w","to":"eosio.ramfee","quantity":"0.0249 EOS","memo":"ram fee"}
#   eosio.token <= eosio.token::transfer        {"from":"eosio.ramfee","to":"eosio.rex","quantity":"0.0249 EOS","memo":"transfer from eosio.ramfee t...
#  eosio.ramfee <= eosio.token::transfer        {"from":"eosio.ramfee","to":"eosio.rex","quantity":"0.0249 EOS","memo":"transfer from eosio.ramfee t...
#     eosio.rex <= eosio.token::transfer        {"from":"eosio.ramfee","to":"eosio.rex","quantity":"0.0249 EOS","memo":"transfer from eosio.ramfee t...
#         eosio <= eosio::delegatebw            {"from":"yvngxrjzbf3w","receiver":"mnmsvtabluzl","stake_net_quantity":"3.0000 EOS","stake_cpu_quanti...
#   eosio.token <= eosio.token::transfer        {"from":"yvngxrjzbf3w","to":"eosio.stake","quantity":"6.0000 EOS","memo":"stake bandwidth"}
#  yvngxrjzbf3w <= eosio.token::transfer        {"from":"yvngxrjzbf3w","to":"eosio.stake","quantity":"6.0000 EOS","memo":"stake bandwidth"}
#   eosio.stake <= eosio.token::transfer        {"from":"yvngxrjzbf3w","to":"eosio.stake","quantity":"6.0000 EOS","memo":"stake bandwidth"}


EXAMPLE =\
{
  "transaction_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
  "processed": {
    "id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
    "block_num": 44861211,
    "block_time": "2019-08-17T17:37:40.500",
    "producer_block_id": null,
    "receipt": {
      "status": "executed",
      "cpu_usage_us": 882,
      "net_usage_words": 42
    },
    "elapsed": 882,
    "net_usage": 336,
    "scheduled": false,
    "action_traces": [{
        "action_ordinal": 1,
        "creator_action_ordinal": 0,
        "closest_unnotified_ancestor_action_ordinal": 0,
        "receipt": {
          "receiver": "eosio",
          "act_digest": "e31655dc57c536c1b5e820111e47e6a27e18b9747de43daaa8007b6c82dac758",
          "global_sequence": 468007328,
          "recv_sequence": 49156871,
          "auth_sequence": [[
              "yvngxrjzbf3w",
              140
            ]
          ],
          "code_sequence": 9,
          "abi_sequence": 11
        },
        "receiver": "eosio",
        "act": {
          "account": "eosio",
          "name": "newaccount",
          "authorization": [{
              "actor": "yvngxrjzbf3w",
              "permission": "active"
            }
          ],
          "data": {
            "creator": "yvngxrjzbf3w",
            "name": "moyqjj2eqwli",
            "owner": {
              "threshold": 1,
              "keys": [{
                  "key": "EOS5piYU9RJdkrEjjDiH2qyfXEAAE8sVF8dNtSFSxbSFwphDJ2FZS",
                  "weight": 1
                }
              ],
              "accounts": [],
              "waits": []
            },
            "active": {
              "threshold": 1,
              "keys": [{
                  "key": "EOS7a33GqsRf6eoDNPLabcc4jRJhJdYrvM5uwv7YvGfPUWs92ymGh",
                  "weight": 1
                }
              ],
              "accounts": [],
              "waits": []
            }
          },
          "hex_data": "c0c73affddcee6f6e022b74abc673d95010000000100027b2145770cbe0be6068e0db31e88092b0095754b7f3ffd4228a9f962837003640100000001000000010003612fdb55afa82a4a5bb820b8895cc786255da4aa64ec403c6415ef125948f73001000000"
        },
        "context_free": false,
        "elapsed": 233,
        "console": "",
        "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
        "block_num": 44861211,
        "block_time": "2019-08-17T17:37:40.500",
        "producer_block_id": null,
        "account_ram_deltas": [{
            "account": "moyqjj2eqwli",
            "delta": 2996
          }
        ],
        "except": null,
        "error_code": null,
        "inline_traces": []
      },{
        "action_ordinal": 2,
        "creator_action_ordinal": 0,
        "closest_unnotified_ancestor_action_ordinal": 0,
        "receipt": {
          "receiver": "eosio",
          "act_digest": "73c943cbd256f07d9f966756af90a37d000e8762d13c4c8d3450215646f60fca",
          "global_sequence": 468007329,
          "recv_sequence": 49156872,
          "auth_sequence": [[
              "yvngxrjzbf3w",
              141
            ]
          ],
          "code_sequence": 9,
          "abi_sequence": 11
        },
        "receiver": "eosio",
        "act": {
          "account": "eosio",
          "name": "buyrambytes",
          "authorization": [{
              "actor": "yvngxrjzbf3w",
              "permission": "active"
            }
          ],
          "data": {
            "payer": "yvngxrjzbf3w",
            "receiver": "moyqjj2eqwli",
            "bytes": 8192
          },
          "hex_data": "c0c73affddcee6f6e022b74abc673d9500200000"
        },
        "context_free": false,
        "elapsed": 195,
        "console": "",
        "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
        "block_num": 44861211,
        "block_time": "2019-08-17T17:37:40.500",
        "producer_block_id": null,
        "account_ram_deltas": [],
        "except": null,
        "error_code": null,
        "inline_traces": [{
            "action_ordinal": 4,
            "creator_action_ordinal": 2,
            "closest_unnotified_ancestor_action_ordinal": 2,
            "receipt": {
              "receiver": "eosio.token",
              "act_digest": "f402a10ac3827f7a7b24827bd33aabc1628176d622f6ccba6eefa8012297e6ca",
              "global_sequence": 468007330,
              "recv_sequence": 76005808,
              "auth_sequence": [[
                  "eosio.ram",
                  298707
                ],[
                  "yvngxrjzbf3w",
                  142
                ]
              ],
              "code_sequence": 5,
              "abi_sequence": 4
            },
            "receiver": "eosio.token",
            "act": {
              "account": "eosio.token",
              "name": "transfer",
              "authorization": [{
                  "actor": "yvngxrjzbf3w",
                  "permission": "active"
                },{
                  "actor": "eosio.ram",
                  "permission": "active"
                }
              ],
              "data": {
                "from": "yvngxrjzbf3w",
                "to": "eosio.ram",
                "quantity": "4.9469 EOS",
                "memo": "buy ram"
              },
              "hex_data": "c0c73affddcee6f6000090e602ea30553dc100000000000004454f5300000000076275792072616d"
            },
            "context_free": false,
            "elapsed": 57,
            "console": "",
            "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
            "block_num": 44861211,
            "block_time": "2019-08-17T17:37:40.500",
            "producer_block_id": null,
            "account_ram_deltas": [],
            "except": null,
            "error_code": null,
            "inline_traces": [{
                "action_ordinal": 7,
                "creator_action_ordinal": 4,
                "closest_unnotified_ancestor_action_ordinal": 4,
                "receipt": {
                  "receiver": "yvngxrjzbf3w",
                  "act_digest": "f402a10ac3827f7a7b24827bd33aabc1628176d622f6ccba6eefa8012297e6ca",
                  "global_sequence": 468007331,
                  "recv_sequence": 40,
                  "auth_sequence": [[
                      "eosio.ram",
                      298708
                    ],[
                      "yvngxrjzbf3w",
                      143
                    ]
                  ],
                  "code_sequence": 5,
                  "abi_sequence": 4
                },
                "receiver": "yvngxrjzbf3w",
                "act": {
                  "account": "eosio.token",
                  "name": "transfer",
                  "authorization": [{
                      "actor": "yvngxrjzbf3w",
                      "permission": "active"
                    },{
                      "actor": "eosio.ram",
                      "permission": "active"
                    }
                  ],
                  "data": {
                    "from": "yvngxrjzbf3w",
                    "to": "eosio.ram",
                    "quantity": "4.9469 EOS",
                    "memo": "buy ram"
                  },
                  "hex_data": "c0c73affddcee6f6000090e602ea30553dc100000000000004454f5300000000076275792072616d"
                },
                "context_free": false,
                "elapsed": 3,
                "console": "",
                "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
                "block_num": 44861211,
                "block_time": "2019-08-17T17:37:40.500",
                "producer_block_id": null,
                "account_ram_deltas": [],
                "except": null,
                "error_code": null,
                "inline_traces": []
              },{
                "action_ordinal": 8,
                "creator_action_ordinal": 4,
                "closest_unnotified_ancestor_action_ordinal": 4,
                "receipt": {
                  "receiver": "eosio.ram",
                  "act_digest": "f402a10ac3827f7a7b24827bd33aabc1628176d622f6ccba6eefa8012297e6ca",
                  "global_sequence": 468007332,
                  "recv_sequence": 263532,
                  "auth_sequence": [[
                      "eosio.ram",
                      298709
                    ],[
                      "yvngxrjzbf3w",
                      144
                    ]
                  ],
                  "code_sequence": 5,
                  "abi_sequence": 4
                },
                "receiver": "eosio.ram",
                "act": {
                  "account": "eosio.token",
                  "name": "transfer",
                  "authorization": [{
                      "actor": "yvngxrjzbf3w",
                      "permission": "active"
                    },{
                      "actor": "eosio.ram",
                      "permission": "active"
                    }
                  ],
                  "data": {
                    "from": "yvngxrjzbf3w",
                    "to": "eosio.ram",
                    "quantity": "4.9469 EOS",
                    "memo": "buy ram"
                  },
                  "hex_data": "c0c73affddcee6f6000090e602ea30553dc100000000000004454f5300000000076275792072616d"
                },
                "context_free": false,
                "elapsed": 2,
                "console": "",
                "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
                "block_num": 44861211,
                "block_time": "2019-08-17T17:37:40.500",
                "producer_block_id": null,
                "account_ram_deltas": [],
                "except": null,
                "error_code": null,
                "inline_traces": []
              }
            ]
          },{
            "action_ordinal": 5,
            "creator_action_ordinal": 2,
            "closest_unnotified_ancestor_action_ordinal": 2,
            "receipt": {
              "receiver": "eosio.token",
              "act_digest": "35bfcf83109b6c9f7ed79b6b62b4709145e7e9a6f92c712d873c0b3dc7d024c8",
              "global_sequence": 468007333,
              "recv_sequence": 76005809,
              "auth_sequence": [[
                  "yvngxrjzbf3w",
                  145
                ]
              ],
              "code_sequence": 5,
              "abi_sequence": 4
            },
            "receiver": "eosio.token",
            "act": {
              "account": "eosio.token",
              "name": "transfer",
              "authorization": [{
                  "actor": "yvngxrjzbf3w",
                  "permission": "active"
                }
              ],
              "data": {
                "from": "yvngxrjzbf3w",
                "to": "eosio.ramfee",
                "quantity": "0.0249 EOS",
                "memo": "ram fee"
              },
              "hex_data": "c0c73affddcee6f6a0d492e602ea3055f90000000000000004454f53000000000772616d20666565"
            },
            "context_free": false,
            "elapsed": 38,
            "console": "",
            "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
            "block_num": 44861211,
            "block_time": "2019-08-17T17:37:40.500",
            "producer_block_id": null,
            "account_ram_deltas": [],
            "except": null,
            "error_code": null,
            "inline_traces": [{
                "action_ordinal": 9,
                "creator_action_ordinal": 5,
                "closest_unnotified_ancestor_action_ordinal": 5,
                "receipt": {
                  "receiver": "yvngxrjzbf3w",
                  "act_digest": "35bfcf83109b6c9f7ed79b6b62b4709145e7e9a6f92c712d873c0b3dc7d024c8",
                  "global_sequence": 468007334,
                  "recv_sequence": 41,
                  "auth_sequence": [[
                      "yvngxrjzbf3w",
                      146
                    ]
                  ],
                  "code_sequence": 5,
                  "abi_sequence": 4
                },
                "receiver": "yvngxrjzbf3w",
                "act": {
                  "account": "eosio.token",
                  "name": "transfer",
                  "authorization": [{
                      "actor": "yvngxrjzbf3w",
                      "permission": "active"
                    }
                  ],
                  "data": {
                    "from": "yvngxrjzbf3w",
                    "to": "eosio.ramfee",
                    "quantity": "0.0249 EOS",
                    "memo": "ram fee"
                  },
                  "hex_data": "c0c73affddcee6f6a0d492e602ea3055f90000000000000004454f53000000000772616d20666565"
                },
                "context_free": false,
                "elapsed": 3,
                "console": "",
                "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
                "block_num": 44861211,
                "block_time": "2019-08-17T17:37:40.500",
                "producer_block_id": null,
                "account_ram_deltas": [],
                "except": null,
                "error_code": null,
                "inline_traces": []
              },{
                "action_ordinal": 10,
                "creator_action_ordinal": 5,
                "closest_unnotified_ancestor_action_ordinal": 5,
                "receipt": {
                  "receiver": "eosio.ramfee",
                  "act_digest": "35bfcf83109b6c9f7ed79b6b62b4709145e7e9a6f92c712d873c0b3dc7d024c8",
                  "global_sequence": 468007335,
                  "recv_sequence": 354953,
                  "auth_sequence": [[
                      "yvngxrjzbf3w",
                      147
                    ]
                  ],
                  "code_sequence": 5,
                  "abi_sequence": 4
                },
                "receiver": "eosio.ramfee",
                "act": {
                  "account": "eosio.token",
                  "name": "transfer",
                  "authorization": [{
                      "actor": "yvngxrjzbf3w",
                      "permission": "active"
                    }
                  ],
                  "data": {
                    "from": "yvngxrjzbf3w",
                    "to": "eosio.ramfee",
                    "quantity": "0.0249 EOS",
                    "memo": "ram fee"
                  },
                  "hex_data": "c0c73affddcee6f6a0d492e602ea3055f90000000000000004454f53000000000772616d20666565"
                },
                "context_free": false,
                "elapsed": 2,
                "console": "",
                "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
                "block_num": 44861211,
                "block_time": "2019-08-17T17:37:40.500",
                "producer_block_id": null,
                "account_ram_deltas": [],
                "except": null,
                "error_code": null,
                "inline_traces": []
              }
            ]
          },{
            "action_ordinal": 6,
            "creator_action_ordinal": 2,
            "closest_unnotified_ancestor_action_ordinal": 2,
            "receipt": {
              "receiver": "eosio.token",
              "act_digest": "c6a048c01516c6487debbb7504deda397fa0ac1b11198c3e4a14ce2daee69625",
              "global_sequence": 468007336,
              "recv_sequence": 76005810,
              "auth_sequence": [[
                  "eosio.ramfee",
                  274269
                ]
              ],
              "code_sequence": 5,
              "abi_sequence": 4
            },
            "receiver": "eosio.token",
            "act": {
              "account": "eosio.token",
              "name": "transfer",
              "authorization": [{
                  "actor": "eosio.ramfee",
                  "permission": "active"
                }
              ],
              "data": {
                "from": "eosio.ramfee",
                "to": "eosio.rex",
                "quantity": "0.0249 EOS",
                "memo": "transfer from eosio.ramfee to eosio.rex"
              },
              "hex_data": "a0d492e602ea30550000e8ea02ea3055f90000000000000004454f5300000000277472616e736665722066726f6d20656f73696f2e72616d66656520746f20656f73696f2e726578"
            },
            "context_free": false,
            "elapsed": 44,
            "console": "",
            "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
            "block_num": 44861211,
            "block_time": "2019-08-17T17:37:40.500",
            "producer_block_id": null,
            "account_ram_deltas": [],
            "except": null,
            "error_code": null,
            "inline_traces": [{
                "action_ordinal": 11,
                "creator_action_ordinal": 6,
                "closest_unnotified_ancestor_action_ordinal": 6,
                "receipt": {
                  "receiver": "eosio.ramfee",
                  "act_digest": "c6a048c01516c6487debbb7504deda397fa0ac1b11198c3e4a14ce2daee69625",
                  "global_sequence": 468007337,
                  "recv_sequence": 354954,
                  "auth_sequence": [[
                      "eosio.ramfee",
                      274270
                    ]
                  ],
                  "code_sequence": 5,
                  "abi_sequence": 4
                },
                "receiver": "eosio.ramfee",
                "act": {
                  "account": "eosio.token",
                  "name": "transfer",
                  "authorization": [{
                      "actor": "eosio.ramfee",
                      "permission": "active"
                    }
                  ],
                  "data": {
                    "from": "eosio.ramfee",
                    "to": "eosio.rex",
                    "quantity": "0.0249 EOS",
                    "memo": "transfer from eosio.ramfee to eosio.rex"
                  },
                  "hex_data": "a0d492e602ea30550000e8ea02ea3055f90000000000000004454f5300000000277472616e736665722066726f6d20656f73696f2e72616d66656520746f20656f73696f2e726578"
                },
                "context_free": false,
                "elapsed": 1,
                "console": "",
                "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
                "block_num": 44861211,
                "block_time": "2019-08-17T17:37:40.500",
                "producer_block_id": null,
                "account_ram_deltas": [],
                "except": null,
                "error_code": null,
                "inline_traces": []
              },{
                "action_ordinal": 12,
                "creator_action_ordinal": 6,
                "closest_unnotified_ancestor_action_ordinal": 6,
                "receipt": {
                  "receiver": "eosio.rex",
                  "act_digest": "c6a048c01516c6487debbb7504deda397fa0ac1b11198c3e4a14ce2daee69625",
                  "global_sequence": 468007338,
                  "recv_sequence": 98105,
                  "auth_sequence": [[
                      "eosio.ramfee",
                      274271
                    ]
                  ],
                  "code_sequence": 5,
                  "abi_sequence": 4
                },
                "receiver": "eosio.rex",
                "act": {
                  "account": "eosio.token",
                  "name": "transfer",
                  "authorization": [{
                      "actor": "eosio.ramfee",
                      "permission": "active"
                    }
                  ],
                  "data": {
                    "from": "eosio.ramfee",
                    "to": "eosio.rex",
                    "quantity": "0.0249 EOS",
                    "memo": "transfer from eosio.ramfee to eosio.rex"
                  },
                  "hex_data": "a0d492e602ea30550000e8ea02ea3055f90000000000000004454f5300000000277472616e736665722066726f6d20656f73696f2e72616d66656520746f20656f73696f2e726578"
                },
                "context_free": false,
                "elapsed": 3,
                "console": "",
                "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
                "block_num": 44861211,
                "block_time": "2019-08-17T17:37:40.500",
                "producer_block_id": null,
                "account_ram_deltas": [],
                "except": null,
                "error_code": null,
                "inline_traces": []
              }
            ]
          }
        ]
      },{
        "action_ordinal": 3,
        "creator_action_ordinal": 0,
        "closest_unnotified_ancestor_action_ordinal": 0,
        "receipt": {
          "receiver": "eosio",
          "act_digest": "fa12d817f97b8fd25b2a4cba431fccfe77a0590d00b0aac750a24678f34aac9b",
          "global_sequence": 468007339,
          "recv_sequence": 49156873,
          "auth_sequence": [[
              "yvngxrjzbf3w",
              148
            ]
          ],
          "code_sequence": 9,
          "abi_sequence": 11
        },
        "receiver": "eosio",
        "act": {
          "account": "eosio",
          "name": "delegatebw",
          "authorization": [{
              "actor": "yvngxrjzbf3w",
              "permission": "active"
            }
          ],
          "data": {
            "from": "yvngxrjzbf3w",
            "receiver": "moyqjj2eqwli",
            "stake_net_quantity": "3.0000 EOS",
            "stake_cpu_quantity": "3.0000 EOS",
            "transfer": 0
          },
          "hex_data": "c0c73affddcee6f6e022b74abc673d95307500000000000004454f5300000000307500000000000004454f530000000000"
        },
        "context_free": false,
        "elapsed": 142,
        "console": "",
        "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
        "block_num": 44861211,
        "block_time": "2019-08-17T17:37:40.500",
        "producer_block_id": null,
        "account_ram_deltas": [{
            "account": "yvngxrjzbf3w",
            "delta": 160
          }
        ],
        "except": null,
        "error_code": null,
        "inline_traces": [{
            "action_ordinal": 13,
            "creator_action_ordinal": 3,
            "closest_unnotified_ancestor_action_ordinal": 3,
            "receipt": {
              "receiver": "eosio.token",
              "act_digest": "0027f9d74738a5d9d3569a755f568852a638957439ffc85554bee452de4c8014",
              "global_sequence": 468007340,
              "recv_sequence": 76005811,
              "auth_sequence": [[
                  "yvngxrjzbf3w",
                  149
                ]
              ],
              "code_sequence": 5,
              "abi_sequence": 4
            },
            "receiver": "eosio.token",
            "act": {
              "account": "eosio.token",
              "name": "transfer",
              "authorization": [{
                  "actor": "yvngxrjzbf3w",
                  "permission": "active"
                }
              ],
              "data": {
                "from": "yvngxrjzbf3w",
                "to": "eosio.stake",
                "quantity": "6.0000 EOS",
                "memo": "stake bandwidth"
              },
              "hex_data": "c0c73affddcee6f60014341903ea305560ea00000000000004454f53000000000f7374616b652062616e647769647468"
            },
            "context_free": false,
            "elapsed": 42,
            "console": "",
            "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
            "block_num": 44861211,
            "block_time": "2019-08-17T17:37:40.500",
            "producer_block_id": null,
            "account_ram_deltas": [],
            "except": null,
            "error_code": null,
            "inline_traces": [{
                "action_ordinal": 14,
                "creator_action_ordinal": 13,
                "closest_unnotified_ancestor_action_ordinal": 13,
                "receipt": {
                  "receiver": "yvngxrjzbf3w",
                  "act_digest": "0027f9d74738a5d9d3569a755f568852a638957439ffc85554bee452de4c8014",
                  "global_sequence": 468007341,
                  "recv_sequence": 42,
                  "auth_sequence": [[
                      "yvngxrjzbf3w",
                      150
                    ]
                  ],
                  "code_sequence": 5,
                  "abi_sequence": 4
                },
                "receiver": "yvngxrjzbf3w",
                "act": {
                  "account": "eosio.token",
                  "name": "transfer",
                  "authorization": [{
                      "actor": "yvngxrjzbf3w",
                      "permission": "active"
                    }
                  ],
                  "data": {
                    "from": "yvngxrjzbf3w",
                    "to": "eosio.stake",
                    "quantity": "6.0000 EOS",
                    "memo": "stake bandwidth"
                  },
                  "hex_data": "c0c73affddcee6f60014341903ea305560ea00000000000004454f53000000000f7374616b652062616e647769647468"
                },
                "context_free": false,
                "elapsed": 2,
                "console": "",
                "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
                "block_num": 44861211,
                "block_time": "2019-08-17T17:37:40.500",
                "producer_block_id": null,
                "account_ram_deltas": [],
                "except": null,
                "error_code": null,
                "inline_traces": []
              },{
                "action_ordinal": 15,
                "creator_action_ordinal": 13,
                "closest_unnotified_ancestor_action_ordinal": 13,
                "receipt": {
                  "receiver": "eosio.stake",
                  "act_digest": "0027f9d74738a5d9d3569a755f568852a638957439ffc85554bee452de4c8014",
                  "global_sequence": 468007342,
                  "recv_sequence": 340141,
                  "auth_sequence": [[
                      "yvngxrjzbf3w",
                      151
                    ]
                  ],
                  "code_sequence": 5,
                  "abi_sequence": 4
                },
                "receiver": "eosio.stake",
                "act": {
                  "account": "eosio.token",
                  "name": "transfer",
                  "authorization": [{
                      "actor": "yvngxrjzbf3w",
                      "permission": "active"
                    }
                  ],
                  "data": {
                    "from": "yvngxrjzbf3w",
                    "to": "eosio.stake",
                    "quantity": "6.0000 EOS",
                    "memo": "stake bandwidth"
                  },
                  "hex_data": "c0c73affddcee6f60014341903ea305560ea00000000000004454f53000000000f7374616b652062616e647769647468"
                },
                "context_free": false,
                "elapsed": 2,
                "console": "",
                "trx_id": "4e6e12e84991582eaea834e174a1ee86046e8a0ce027129b50b6f8d5ed7a4b34",
                "block_num": 44861211,
                "block_time": "2019-08-17T17:37:40.500",
                "producer_block_id": null,
                "account_ram_deltas": [],
                "except": null,
                "error_code": null,
                "inline_traces": []
              }
            ]
          }
        ]
      }
    ],
    "account_ram_delta": null,
    "except": null,
    "error_code": null
  }
}
