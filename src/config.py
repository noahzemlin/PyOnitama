import yaml

with open("config.yml", 'r') as raw_yaml:
    config = yaml.load(raw_yaml, Loader=yaml.FullLoader)