import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(BASE_DIR, "storage.json")


def load_data():
    with open(DB, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=2)

def add_resource(resource):
    data = load_data()
    data.append(resource)
    save_data(data)

def get_resources():
    return load_data()

def add_rating(resource_id, rating):
    data = load_data()
    for r in data:
        if r["id"] == resource_id:
            total = r["avg_rating"] * r["rating_count"]
            r["rating_count"] += 1
            r["avg_rating"] = (total + rating) / r["rating_count"]
    save_data(data)
