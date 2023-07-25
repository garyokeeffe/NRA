import json

def save(data_object, name):
    with open(f'{name}.json', 'w') as f:
        json.dump(data_object, f)

def load(name):
    with open(f'{name}.json', 'r') as f:
        return json.load(f)