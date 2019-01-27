from ruamel.yaml import YAML

yaml = YAML()

config_path = "fbmcliconfig.txt"

config_defaults = {"fbmcli_version": "v0.1.031",
                   "username": "username@example.com",
                   "password": "password",
                   "cookies_path": "fbmcli.cookies",
                   "prompt": " > ",
                   "n_threads": 10}


def save_configs(_config: dict = config_defaults, _config_path: str = config_path) -> bool:
    """Try to save the config and return a bool showing if the attempt was successful."""
    try:
        with open(_config_path, "w") as handle:
            yaml.dump(_config, handle)
    except:
        print(f"Config file could not be saved.")
        return False
    else:
        print(f"Configs saved to '{_config_path}'.")
        return True


def load_configs(_config_path: str = config_path) -> dict:
    try:
        print("Opening config file.")
        with open(_config_path) as handle:
            _config = yaml.load(handle)
    except FileNotFoundError:
        print("Config file not found, creating one.")
        _config = config_defaults
        if save_configs(_config):
            return _config
        else:
            return None
    else:
        for config_name in config_defaults:
            if config_name not in _config:
                print(f"Config '{config_name}' not found.")
                _config[config_name] = config_defaults[config_name]
        if _config["fbmcli_version"] != config_defaults["fbmcli_version"]:
            print(f"Updating to {config_defaults['fbmcli_version']}.")
            _config["fbmcli_version"] = config_defaults["fbmcli_version"]
        save_configs(_config)
        return _config


config = load_configs()
if config is None:
    quit()
