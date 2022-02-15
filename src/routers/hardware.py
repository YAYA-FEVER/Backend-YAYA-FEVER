from fastapi import APIRouter, Depends, HTTPException
from ..schemas import Product
from pymongo import MongoClient

router = APIRouter(
   prefix="/hardware",
   tags=["Hardware"],
   responses={404: {"message": "Not found"}}
)

myclient = MongoClient("localhost",27017)
db = myclient["Yaya-Fever"]
plants = db["plants"]

@router.post("/hardware/update_humid")
def update_humid(product : Product):
    result = plants.find_one({"ID": product.ID},{"_id":0})
    if (result != None):
        query = {"ID": product.ID}
        new = {"$set" : {"humidity_soil_hard": product.humidity_soil_hard , "humidity_air_hard":product.humidity_air_hard , "temp":product.temp}}
        plants.update_one(query,new)
        return {
            "update success"
        }
    else:
        return {
            "product not found"
        }

@router.post("/hardware/update_height")
def update_height(product : Product):
    result = plants.find_one({"ID": product.ID},{"_id":0})
    if (result != None):
        query = {"ID": product.ID}
        new = {"$set" : {"height_hard": product.height_hard}}
        plants.update_one(query,new)
        return {
            "update success"
        }
    else:
        return {
            "product not found"
        }
        
@router.get("/hardware/auto_mode/{id}") # ใส่ไอดีมาด้วย
def auto_mode(id : int):
    result = plants.find_one({"ID": id},{"_id":0,"humidity_soil_front":1,"activate_auto": 1})
    if (result != None):
        return result
    else:
        return {
            "product not found"
        }

@router.get("/hardware/exist_plant/{id}")
def exist_plant(id :int):
    result = plants.find_one({"ID": id},{"_id":0})
    if (result != None):
        return "found plant"
    else:
        return "not found plant"