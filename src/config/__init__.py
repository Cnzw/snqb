import yaml

def get_config(path='config.yml') -> dict:
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f.read())