from fastapi import APIRouter, Depends, HTTPException
from ..schemas import Product
from ..auth import AuthHandler
from pymongo import MongoClient
from datetime import datetime,timedelta

router = APIRouter(
   prefix="/customer",
   tags=["Customer"],
   responses={404: {"message": "Not found"}}
)

auth_handler = AuthHandler()

myclient = MongoClient("localhost",27017)
db = myclient["Yaya-Fever"]
plants = db["plants"]
users = db["users"]

@router.get("/shelf/plant")
def shelf_plant():
    """Get all plant list"""
    plant_list = []
    plant_list3 = []
    result = list(plants.find({},{"_id":0 , "ID":1 , "booking":1}))
    print(list(result))
    for i in range(len(result)):
        if ((i+1)%3 == 0):
            plant_list3.append(result[i])
            plant_list.append(plant_list3)
            plant_list3 = []
        else:
            plant_list3.append(result[i])
            if ((i+1) == len(result)):
                plant_list.append(plant_list3)
        
        
    return plant_list
    

@router.get("/plant_detail/{id}")
def plant_detail(id: int):
    """Show plant detail for custome"""
    query = {"ID": id}
    detail = {
        "_id": 0,
        "plant_name": 1,
        "detail": 1,
        "price": 1,
        "ID": 1,
        "img": 1
    }
    result = plants.find_one(query, detail)
    if (result is not None):
        return result
    else : 
        raise HTTPException(status_code=403, detail="Plant ID not found")


@router.post("/reserve")
def reserve(product: Product, username=Depends(auth_handler.auth_wrapper)):
    """Reserve plant"""
    resultproduct = plants.find_one({"ID": product.ID})
    user = users.find_one({"username" : username})
    if (resultproduct is not None) and resultproduct["booking"] == 0:
        userquery = {"username" : username}
        usernew = {"$set": {
                "basketlist": user["basketlist"] + [{
                "ID": product.ID,
                "duedate": datetime.today()+timedelta(days=2),
                "plant_name": resultproduct["plant_name"]
            }]}
        }
        users.update_one(userquery, usernew)
        plantquery = {"ID": product.ID}
        plantnew = {"$set": {
                "booking": 1,
                "duedate": datetime.today()+timedelta(days=2),
                "username": username
        }}
        plants.update_one(plantquery, plantnew)
        return {
            "update success"
        }
    else:
        return {
            "already reserve"
        }


@router.post("/unreserve")
def update_reserve(product: Product, username=Depends(auth_handler.auth_wrapper)):
    """Update reserve status"""
    plant = plants.find_one({"ID": product.ID})
    user = users.find_one({"username": username})
    if (plant is not None) and (plant["booking"] == 1):
        newbasket = list(user["basketlist"])
        for item in newbasket:
            if item["ID"] == product.ID:
                newbasket.remove(item)
        query = {"username": username}
        new = {"$set": {
            "basketlist": newbasket
        }}
        users.update_one(query, new)
        plantquery = {"ID": product.ID}
        plantnew = {"$set": {
                "booking": 0,
                "duedate": None,
                "username": None
        }}
        plants.update_one(plantquery, plantnew)
        return {
            "update success"
        }
    else:
        return {
            "Plant not reserve"
        }


@router.get("/basket_list")
def basket_list(username=Depends(auth_handler.auth_wrapper)):
    """Return item in basket"""
    user = users.find_one({"username": username})
    if (user["basketlist"] is not None):
        return user["basketlist"]
    else:
        return "No plant in basket"