from fastapi import FastAPI
from models import Resource
from logic import add_resource, get_resources, add_rating

app = FastAPI()

@app.post("/resource")
def create_resource(resource: Resource):
    add_resource(resource.dict())
    return {"message": "Resource added"}

@app.get("/resources")
def list_resources():
    return get_resources()

@app.post("/rate")
def rate_resource(resource_id: int, rating: int):
    add_rating(resource_id, rating)
    return {"message": "Rating added"}
