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

@router.post("/update/soil")
def update_humid(product: Product):
    result = plants.find_one({"ID": product.ID})
    if (result is not None):
        query = {"ID": product.ID}
        new = {"$set" : {
            "humidity_soil_hard": product.humidity_soil_hard,
        }}
        plants.update_one(query,new)
        return {
            "update success"
        }
    else:
        raise HTTPException(status_code=403, detail="Plant ID not found")

@router.post("/update/air")
def update_humid(product: Product):
    result = plants.find_one({"ID": product.ID})
    if (result is not None):
        query = {"ID": product.ID}
        new = {"$set" : {
            "humidity_air_hard": product.humidity_air_hard,
            "temp": product.temp
        }}
        plants.update_one(query,new)
        return {
            "update success"
        }
    else:
        raise HTTPException(status_code=403, detail="Plant ID not found")

@router.post("/update_height")
def update_height(product: Product):
    result = plants.find_one({"ID": product.ID})
    if (result is not None):
        query = {"ID": product.ID}
        new = {"$set" : {"height_hard": product.height_hard}}
        plants.update_one(query,new)
        return {
            "update success"
        }
    else:
        raise HTTPException(status_code=403, detail="Plant ID not found")
        
@router.get("/auto_mode/{id}") # ใส่ไอดีมาด้วย
def auto_mode(id: int):
    detail = {"_id": 0,
        "humidity_soil_front": 1,
        "activate_auto": 1
    }
    result = plants.find_one({"ID": id}, detail)
    if (result is not None):
        return result
    else:
        raise HTTPException(status_code=403, detail="Plant ID not found")

@router.get("/exist_plant/{id}")
def exist_plant(id: int):
    result = plants.find_one({"ID": id})
    if (result is not None):
        return {
            "existed": 1
        }
    else:
        return {
            "existed": 0
        }