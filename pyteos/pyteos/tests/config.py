import json
import pyteos.setup as setup
import pyteos.core.config as config

setup.CONFIG_JSON = "config.json"
print(config.config_file())
config_json = config.config_map()
print(json.dumps(config_json, indent=4))
print(json.dumps(config.current_config(
    "01_hello_world"), sort_keys=True, indent=4))