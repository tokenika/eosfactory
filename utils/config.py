import json
import core.config as config

print('''
The current configuration of EOSFactory:
{}

You are free to overwrite the above settings with entries in the configuration file located here:
{}

The current content of the configuration file is:
{}
'''.format(
        json.dumps(config.current_config(), sort_keys=True, indent=4),
        config.config_file(),
        json.dumps(config.config_map(), sort_keys=True, indent=4))
)