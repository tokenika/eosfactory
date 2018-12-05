

from eosfactory.eosf import *
import eosfactory.core.cleos as cleos
import eosfactory.core.setup as setup

reset()
create_master_account("master")
create_account("Alice", master)
create_account("Jim", master)
Alice.info()



COMMENT("Set new key to a permission:")
key = cleos.CreateKey(is_verbose=False)
setup.is_print_command_line = True
Alice.set_account_permission(
    Permission.ACTIVE, key.key_public, Permission.OWNER, 
    (Alice, Permission.OWNER))
setup.is_print_command_line = False
Alice.info()



COMMENT("Set an account (instead of a key) as authority for a permission:")
create_account("Bob", master)
setup.is_print_command_line = True
Alice.set_account_permission(
    Permission.ACTIVE, Bob, Permission.OWNER, 
    (Alice, Permission.OWNER))
setup.is_print_command_line = False
Alice.info()



COMMENT("Weights and Threshold:")
create_account("Carol", master)
actors = [str(Bob), str(Carol)]
actors.sort()
Alice.set_account_permission(Permission.ACTIVE,
    {
        "threshold" : 100, 
        "keys" : [], 
        "accounts" : 
            [
                {
                    "permission":
                        {
                            "actor": actors[0],
                            "permission":"active"
                        },
                    "weight":25
                }, 
                {	
                    "permission":
                        {
                            "actor":actors[1],
                            "permission":"active"
                        },
                    "weight":75
                }
            ]
    },
    Permission.OWNER,
    (Alice, Permission.OWNER))
Alice.info()



COMMENT("Set two weighted keys:")
keys = [Bob.owner(), Carol.owner()]
keys.sort()

Alice.set_account_permission(Permission.ACTIVE,
    {
        "threshold" : 100, 
        "keys" : 
            [
                {
                    "key": keys[0],
                    "weight": 50
                },
                {
                    "key": keys[1],
                    "weight": 50
                }                    
            ]
    },
    Permission.OWNER,
    (Alice, Permission.OWNER)
)
Alice.info()

