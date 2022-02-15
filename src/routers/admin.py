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

myclient = MongoClient("localhost",27017)
db = myclient["Yaya-Fever"]
plants = db["plants"]
users = db["users"]

@router.get('/admin/plant_info/{id}')
def get_plant_info(id :int, username=Depends(auth_handler.auth_wrapper)):
    result = plants.find_one({"ID":id} , {"_id":0,"plant_name":1,"humidity_soil_hard":1,"humidity_air_hard":1,"height_hard":1,"temp":1,"activate_auto":1})
    userpermission = users.find_one({"username": username})
    if (result != None) and (userpermission["permission"] == 1):
        return result
    elif (result != None) : 
        raise HTTPException(status_code=403, detail="Plant ID not found")
    else :
        raise HTTPException(status_code=401, detail='Permission denined')

@router.post("/admin/auto_mode")
def auto_mode(product : Product , username=Depends(auth_handler.auth_wrapper)):
    result = plants.find_one({"ID": product.ID} , {"_id":0})
    userpermission = users.find_one({"username": username},{"_id":0})
    if (result != None) and (username["permission"] == 1):
        query = {"ID": product.ID}
        new = {"$set" : {"activate_auto": product.activate_auto}}
        plants.update_one(query,new)
        return {
            "update success"
        }
    else :
        raise HTTPException(status_code=401, detail='Permission denined')
        
@router.post("/admin/humidity_front_want") # ส่ง ID มาด้วย
def humidity_front_want(product : Product , username=Depends(auth_handler.auth_wrapper)):
    result = plants.find_one({"ID": product.ID} , {"_id":0})
    resultname = users.find_one({"username": username},{"_id":0})
    if (result != None) and (resultname["permission"] == 1):
        query = {"ID": product.ID}
        new = {"$set" : {"humidity_soil_front": product.humidity_soil_front}}
        plants.update_one(query,new)
        return {
            "update success"
        }
    else:
        return {
            "failed"
        }

@router.post("/admin/new_plant") # เช็คว่าไอดี มีอยู่ไหม ถ้ามีใส่ใหม่ ไม่มีอัพเดท
def new_plant(product : Product , username=Depends(auth_handler.auth_wrapper)):
    result = plants.find_one({"ID": product.ID} , {"_id":0})
    resultname = users.find_one({"username": username},{"_id":0})
    if (result == None) and (resultname["permission"] == 1):
        x = jsonable_encoder(product)
        plants.insert_one(x)
        return {
            "added success"
        }
    elif (result != None):
        plants.update_one({"ID":product.ID},{"$set":{"plant_name":product.plant_name,"detail":product.detail,"price":product.price,"ID":product.ID}})
        #print({"plant_name":result["plant_name"],"detail":result["detail"],"price":result["price"],"ID":result["ID"]})
        return {
            "Updated success"
        }
        
@router.delete("/admin/delete_plant")
def delete_plant(product : Product , username=Depends(auth_handler.auth_wrapper)):
    result = plants.find_one({"ID": product.ID} , {"_id":0})
    resultname = users.find_one({"username": username},{"_id":0})
    if (result != None) and (resultname["permission"] == 1):
        query = {"ID": product.ID}
        plants.delete_one(query)
        return {
            "delete success"
        }
    else:
        return {
            "failed"
        }