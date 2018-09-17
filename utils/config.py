import json
import pyteos.core.config as config

print('''
The current configuration of the EOSFactory is
{}

You may overwrite it with entries into the configuration file.

Configuration file is look for in the following locations:
    * EOSIO_EOSFACTORY_DIR + setup.CONFIG_DIR 
        where ``EOSIO_EOSFACTORY_DIR`` is a environment variable and 
        ``setup.CONFIG_DIR`` is defined in the ``pyteos.setup`` module
    * <directory of the ``pyteos.setup`` module> + setup.CONFIG_DIR
    * <../<directory of the ``pyteos.setup`` module>> + setup.CONFIG_DIR
    * <../../<directory of the ``pyteos.setup`` module>> + setup.CONFIG_DIR

If not found, an empty file is created in the last location.

The current configuration json file is 
    {}

The contents of the configuration json file is 
{}
'''.format(
        json.dumps(config.current_config(), sort_keys=True, indent=4),
        config.config_file(),
        json.dumps(config.config_map(), sort_keys=True, indent=4))
)