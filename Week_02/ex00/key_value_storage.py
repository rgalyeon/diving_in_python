import os
import tempfile
import json
import argparse

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')


def read_data():
    dictionary = dict()
    if not os.path.exists(storage_path):
        return dictionary
    with open(storage_path, 'r') as read_file:
        tmp = read_file.read()
        if tmp:
            dictionary = dict(json.loads(tmp))
    return dictionary


def get_data(key):
    storage = read_data()
    tmp = storage.get(key)
    if tmp:
        return storage.get(key)
    return [""]


def save_data(key, value):
    storage = read_data()
    if key in storage:
        storage[key] += value
    else:
        storage[key] = value
    with open(storage_path, 'w') as f:
        f.write(json.dumps(storage))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--key', action='store', nargs=1, dest='key', required=True, type=str)
    parser.add_argument('--val', action='store', nargs=1, dest='val', required=False, type=str)
    data = parser.parse_args()
    if data.val:
        save_data(*data.key, data.val)
    elif data.key:
        print(', '.join(get_data(*data.key)))
