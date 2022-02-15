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
    plant_list = []
    for i in plants.find({},{"_id":0 ,"ID":1 , "booking": 1}):
        plant_list.append(i)
    return {
        "plant_list": plant_list
    }
        

@router.get("/customer/plant_detail")
def plant_detail(product : Product):
    result = plants.find_one({"ID": product.ID},{"_id":0,"plant_name":1 , "detail": 1 , "price": 1 , "ID" : 1})
    if (result != None):
        return {
            "detail" : result
        }
    elif (result != None) : 
        raise HTTPException(status_code=403, detail="Plant ID not found")
    else :
        raise HTTPException(status_code=401, detail='Permission denined')

@router.post("/customer/reserve")
def reserve(product : Product , username=Depends(auth_handler.auth_wrapper)):
    resultproduct = plants.find_one({"ID":product.ID},{"_id":0})
    user = users.find_one({"username": username},{"_id":0})
    if (resultproduct != None) and resultproduct["booking"] == 0:
        users.update_one({"username" : username},{"$set" : {"basketlist": user["basketlist"]+[{"ID":product.ID,"duedate":datetime.today()+timedelta(days=2),"plant_name":resultproduct["plant_name"]}]}})
        plants.update_one({"ID":product.ID},{"$set": {"booking":1}})
        return {
            "update success"
        }
    elif (resultproduct == None) :
        return {
            "plant does not exist"
        }
    else:
        return {
            "already reserve"
        }
    # return "Updated"

@router.get("/customer/basket_list")
def basket_list(username=Depends(auth_handler.auth_wrapper)):
    userpermission = users.find_one({"username": username},{"_id":0})
    if (userpermission["basketlist"] != None):
        return {"basketlist": userpermission["basketlist"]}
    else:
        return "not reserve"