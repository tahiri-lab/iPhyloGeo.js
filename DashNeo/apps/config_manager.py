import yaml


def read_config():
    with open('config/config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    return config


def update_config(new_config):
    with open('config/config.yaml', 'w') as f:
        yaml.dump(new_config, f)
