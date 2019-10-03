#!/usr/bin/env python3
"""Pretty print json received from a PushAction object."""

import eosfactory.core.str.actions as actions

#  HOST <= HOST::create         {"challenger":"ALICE","host":"CAROL"}
# executed transaction: 869173095f5ac4df477166eb285713e087eacac70395c7670148df3efaf043a4  112 bytes  1029 us
# warning: transaction executed locally, but may not be confirmed by the network yet    


example =\
{
    "transaction_id": "43b729c3b21bd83092da69631da14d6c1998717f6697c15139b61c29963190d7",
    "processed": {
        "id": "43b729c3b21bd83092da69631da14d6c1998717f6697c15139b61c29963190d7",
        "block_num": 17,
        "block_time": "2019-08-20T11:14:08.000",
        "producer_block_id": None,
        "receipt": {
            "status": "executed",
            "cpu_usage_us": 1064,
            "net_usage_words": 14
        },
        "elapsed": 7931,
        "net_usage": 112,
        "scheduled": False,
        "action_traces": [
            {
                "action_ordinal": 1,
                "creator_action_ordinal": 0,
                "closest_unnotified_ancestor_action_ordinal": 0,
                "receipt": {
                    "receiver": "l2plwqqlg54o",
                    "act_digest": "a59c7786adf5873922f446d9247acb1db31d3fbbe1a2e6998632a37475d8da71",
                    "global_sequence": 22,
                    "recv_sequence": 1,
                    "auth_sequence": [
                        [
                            "epbpalkj4rh5",
                            1
                        ]
                    ],
                    "code_sequence": 1,
                    "abi_sequence": 1
                },
                "receiver": "l2plwqqlg54o",
                "act": {
                    "account": "l2plwqqlg54o",
                    "name": "create",
                    "authorization": [
                        {
                            "actor": "epbpalkj4rh5",
                            "permission": "active"
                        }
                    ],
                    "data": {
                        "challenger": "i1k54odcmsrp",
                        "host": "epbpalkj4rh5"
                    },
                    "hex_data": "502f96285152607050da250f46534f55"
                },
                "context_free": False,
                "elapsed": 7730,
                "console": "",
                "trx_id": "43b729c3b21bd83092da69631da14d6c1998717f6697c15139b61c29963190d7",
                "block_num": 17,
                "block_time": "2019-08-20T11:14:08.000",
                "producer_block_id": None,
                "account_ram_deltas": [
                    {
                        "account": "epbpalkj4rh5",
                        "delta": 266
                    }
                ],
                "except": None,
                "error_code": None,
                "inline_traces": []
            }
        ],
        "account_ram_delta": None,
        "except": None,
        "error_code": None
    }
}

class Push():

    def __init__(self, received_json):
          
        self.info = ""
        def addln(msg=""):
            self.info = self.info + msg + "\n"

        addln(str(actions.Actions(received_json)))
        addln("# %25s: %d us" % ("cpu usage", received_json["processed"]["receipt"]["cpu_usage_us"]))
        addln("# %25s: %d words" % ("net usage", received_json["processed"]["receipt"]["net_usage_words"]))
        addln("# WARNING: transaction executed locally, but may not be confirmed by the network yet.")

    def __str__(self):
        return self.info

  
if __name__ == '__main__':
   print(Push(example))