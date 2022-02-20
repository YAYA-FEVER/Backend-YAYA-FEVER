from fastapi import APIRouter, Depends, HTTPException
from ..schemas import Product
from ..auth import AuthHandler
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient

auth_handler = AuthHandler()

router = APIRouter(
   prefix="/admin",
   tags=["Admin"],
   responses={404: {"message": "Not found"}}
)

myclient = MongoClient("localhost", 27017)
db = myclient["Yaya-Fever"]
plants = db["plants"]
users = db["users"]


def check_permission(username: str) -> bool:
    result = users.find_one({"username": username})
    return result["permission"] == 1


@router.get('/plant_info/{id}')
def get_plant_info(id: int, username=Depends(auth_handler.auth_wrapper)):
    """Show plant detail"""
    query = {"ID": id}
    detail = {
        "_id": 0,
        "plant_name": 1,
        "humidity_soil_hard": 1,
        "humidity_air_hard": 1,
        "height_hard": 1,
        "temp": 1,
        "activate_auto": 1,
        "img": 1
    }
    result = plants.find_one(query, detail)
    if (result is not None) and check_permission(username):
        return result
    elif (result is None) and check_permission(username):
        raise HTTPException(status_code=403, detail="Plant ID not found")
    elif not check_permission(username):
        raise HTTPException(status_code=401, detail='Permission denined')


@router.post("/auto_mode")
def auto_mode(product: Product, username=Depends(auth_handler.auth_wrapper)):
    """Auto mode on/off."""
    result = plants.find_one({"ID": product.ID})
    if (result is not None) and check_permission(username):
        query = {"ID": product.ID}
        new = {"$set": {
            "activate_auto": product.activate_auto,
            "humidity_soil_front":product.humidity_soil_front,
            "water_time":product.water_time
        }}
        plants.update_one(query, new)
        return {
           "success"
        }
    elif not check_permission(username):
        raise HTTPException(status_code=401, detail='Permission denined')


@router.post("/set_plant")
def new_plant(product: Product, username=Depends(auth_handler.auth_wrapper)):
    """If It's new ID add new plant If that ID already have update plant"""
    result = plants.find_one({"ID": product.ID})
    if (result is None) and check_permission(username):
        x = jsonable_encoder(product)
        plants.insert_one(x)
        return {
            "added success"
        }
    elif (result is not None) and check_permission(username):
        query = {"ID": product.ID}
        new = {"$set": {
            "plant_name": product.plant_name,
            "detail": product.detail,
            "price": product.price,
            "ID": product.ID,
            "img": product.img
        }}
        plants.update_one(query, new)
        return {
            "Updated success"
        }
    elif not check_permission(username):
        raise HTTPException(status_code=401, detail='Permission denined')


@router.post("/delete_plant")
def delete_plant(product: Product, username=Depends(auth_handler.auth_wrapper)):
    """Delete plants"""
    result = plants.find_one({"ID": product.ID})
    if (result is not None) and check_permission(username):
        query = {"ID": product.ID}
        plants.delete_one(query)
        return {
            "delete success"
        }
    elif not check_permission(username):
        raise HTTPException(status_code=401, detail='Permission denined')