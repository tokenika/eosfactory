import json
import core.config as config

print('''
The current configuration of the EOSFactory is
{}

You may overwrite it with entries into the configuration file.

Configuration file is searched for in the following locations:
    * EOSFACTORY_DIR + CONFIG_DIR 
        where ``EOSFACTORY_DIR`` is a environment variable and 
        ``CONFIG_DIR`` is defined in the ``pyteos.setup`` module
    * <directory of the ``pyteos.setup`` module> + CONFIG_DIR
    * <../<directory of the ``pyteos.setup`` module>> + CONFIG_DIR
    * <../../<directory of the ``pyteos.setup`` module>> + CONFIG_DIR

The 'CONFIG_DIR' constant is defined in file
    '{}'

If not found, an empty file is created in the last location.

The current configuration json file is 
    '{}'

The contents of the configuration json file is 
{}
'''.format(
        json.dumps(config.current_config(), sort_keys=True, indent=4),
        __file__,
        config.config_file(),
        json.dumps(config.config_map(), sort_keys=True, indent=4))
)