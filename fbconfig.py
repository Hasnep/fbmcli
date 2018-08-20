from ruamel.yaml import YAML

config_path = "fbmcliconfig.txt"


def load_configs(_config_path=config_path):
    yaml = YAML()
    try:
        print("Opening config file.")
        with open(_config_path) as handle:
            _config = yaml.load(handle)
    except FileNotFoundError:
        print("Config file not found, creating one.")
        _config = {"username": "username@example.com",
                   "password": "password",
                   "cookies_path": "fbmcli.cookies",
                   "prompt": " > ",
                   "n_threads": 10}
        try:
            with open(_config_path, "w") as handle:
                yaml.dump(_config, handle)
            print("Config file %s created." % _config_path)
            return _config
        except:
            print("Config file could not be created.")
            return None
    else:
        print("Configs loaded.")
        return _config


config = load_configs()
