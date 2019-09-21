import importlib
import eosfactory.core.setup as setup
setup.set_is_eosjs()

import eosfactory.shell.wallet as wallet_module
import eosfactory.core.logger as logger

# logger.verbosity([logger.Verbosity.OUT])
url = None#"http://xxx.xxx.xxx:8888"
setup.set_nodeos_address(url)
wallet = wallet_module.create_wallet(save_password=True)
keys = wallet.private_keys().json
for key in keys:
    print(key)
