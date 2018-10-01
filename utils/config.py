import json
import core.config as config

print('''
The current configuration of the EOSFactory is
{}

You may overwrite it with entries into a configuration file.

The configuration file named '{}' is expected for in the repository directory 
of the EOSFactory. If it is not found, an empty file is created there.

The contents of the configuration json file is 
{}
'''.format(
        json.dumps(config.current_config(), sort_keys=True, indent=4),
        config.CONFIG_JSON,
        json.dumps(config.config_map(), sort_keys=True, indent=4))
)