import json
import eosfactory.core.config as config

print('''
The current configuration of EOSFactory:
{}

You are free to overwrite the above settings with entries in the configuration file located here:
{}
'''.format(
        json.dumps(config.current_config(), sort_keys=True, indent=4),
        config.config_file())
)

not_defined = config.not_defined()
if not_defined:
    print('''
There are undefined setting:
{}
    '''.format(json.dumps(not_defined, sort_keys=True, indent=4)))

print('''
The current content of the configuration file is:
{}
'''.format(
        json.dumps(config.config_map(), sort_keys=True, indent=4))
)