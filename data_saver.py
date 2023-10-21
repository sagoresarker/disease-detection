import json
import hashlib
import os

DATA_DIRECTORY = "/app/data"

def generate_unique_filename(data):
    json_data = json.dumps(data)
    hash_object = hashlib.sha256(json_data.encode())
    filename = hash_object.hexdigest()
    return filename

def save_data(data):
    if not os.path.exists(DATA_DIRECTORY):
        os.makedirs(DATA_DIRECTORY)

    filename = generate_unique_filename(data)

    file_path = os.path.join(DATA_DIRECTORY, f"{filename}.json")

    with open(file_path, "w") as file:
        json.dump(data, file)

    return file_path
