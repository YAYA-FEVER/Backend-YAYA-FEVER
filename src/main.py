from fastapi import FastAPI, Depends, HTTPException
from .auth import AuthHandler
from .schemas import AuthDetails , Product
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from datetime import datetime,timedelta

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

myclient = MongoClient("localhost",27017)
db = myclient["Project"]
colproduct = db["Product"]
users = db["Users"]


#login system
auth_handler = AuthHandler()
# users = []

@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    result = users.find_one({"username":auth_details.username},{"_id":0})
    if (result):
        print(auth_details.username)
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.insert_one({
        'username': auth_details.username,
        'password': hashed_password,
        'permission':auth_details.permission
    })
    return


@app.post('/login')
def login(auth_details: AuthDetails):
    result = users.find_one({"username":auth_details.username},{"_id":0})
    if (result is None) or (not auth_handler.verify_password(auth_details.password, result['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(result['username'])
    return { 'token': token }


@app.get('/unprotected')
def unprotected():
    return { 'hello': 'world' }


@app.get('/getpermission')
def protected(username=Depends(auth_handler.auth_wrapper)):
    result = users.find_one({"username" : username},{"_id":0})
    if result["permission"] == 1:
        return {'name': username}
    else:
        raise HTTPException(status_code=401, detail='Permission denined')
    
#product
#admin
@app.get('/admin/plant_info/{id}')
def get_plant_info(id :int, username=Depends(auth_handler.auth_wrapper)):
    result = colproduct.find_one({"ID":id} , {"_id":0,"plant_name":1,"humidity_soil_hard":1,"humidity_air_hard":1,"height_hard":1,"temp":1,"activate_auto":1})
    resultname = users.find_one({"username": username},{"_id":0})
    if (result != None) and (resultname["permission"] == 1):
        return result
    else : 
        return {
            "failed"
        }

# @app.get('/admin/plant_info/')
# def get_plant_info(product : Product, username=Depends(auth_handler.auth_wrapper)):
#     result = colproduct.find_one({"ID" : product["ID"]} , {"_id":0})
#     resultname = users.find_one({"username": username},{"_id":0})
#     if (result != None) and (resultname["permission"] == 1):
#         return result
#     else : 
#         return {
#             "failed"
#         }

@app.post("/admin/auto_mode")
def auto_mode(product : Product , username=Depends(auth_handler.auth_wrapper)):
    result = colproduct.find_one({"ID": product.ID} , {"_id":0})
    resultname = users.find_one({"username": username},{"_id":0})
    if (result != None) and (resultname["permission"] == 1):
        query = {"ID": product.ID}
        new = {"$set" : {"activate_auto": product.activate_auto}}
        colproduct.update_one(query,new)
        return {
            "update success"
        }
    else:
        return {
            "failed"
        }
        
@app.post("/admin/humidity_front_want") # ส่ง ID มาด้วย
def humidity_front_want(product : Product , username=Depends(auth_handler.auth_wrapper)):
    result = colproduct.find_one({"ID": product.ID} , {"_id":0})
    resultname = users.find_one({"username": username},{"_id":0})
    if (result != None) and (resultname["permission"] == 1):
        query = {"ID": product.ID}
        new = {"$set" : {"humidity_soil_front": product.humidity_soil_front}}
        colproduct.update_one(query,new)
        return {
            "update success"
        }
    else:
        return {
            "failed"
        }

@app.post("/admin/new_plant") # เช็คว่าไอดี มีอยู่ไหม ถ้ามีใส่ใหม่ ไม่มีอัพเดท
def new_plant(product : Product , username=Depends(auth_handler.auth_wrapper)):
    result = colproduct.find_one({"ID": product.ID} , {"_id":0})
    resultname = users.find_one({"username": username},{"_id":0})
    if (result == None) and (resultname["permission"] == 1):
        x = jsonable_encoder(product)
        colproduct.insert_one(x)
        return {
            "added success"
        }
    elif (result != None):
        colproduct.update_one({"ID":product.ID},{"$set":{"plant_name":product.plant_name,"detail":product.detail,"price":product.price,"ID":product.ID}})
        #print({"plant_name":result["plant_name"],"detail":result["detail"],"price":result["price"],"ID":result["ID"]})
        return {
            "Updated success"
        }

# @app.put("/admin/update_plant")
# def update_plant(product : Product , username=Depends(auth_handler.auth_wrapper)):
#     result = colproduct.find_one({"ID": product.ID} , {"_id":0})
#     resultname = users.find_one({"username": username},{"_id":0})
#     if (result != None) and (resultname["permission"] == 1):
#         query = {"ID": product.ID}
#         new = {"$set" : {"detail": product.detail}}
#         colproduct.update_one(query,new)
#         return {
#             "update success"
#         }
#     else:
#         return {
#             "failed"
#         }
        
@app.delete("/admin/delete_plant")
def delete_plant(product : Product , username=Depends(auth_handler.auth_wrapper)):
    result = colproduct.find_one({"ID": product.ID} , {"_id":0})
    resultname = users.find_one({"username": username},{"_id":0})
    if (result != None) and (resultname["permission"] == 1):
        query = {"ID": product.ID}
        colproduct.delete_one(query)
        return {
            "delete success"
        }
    else:
        return {
            "failed"
        }
# customer

@app.get("/shelf/plant")
def shelf_plant():
    plant_list = []
    for i in colproduct.find({},{"_id":0 ,"ID":1 , "booking": 1}):
        plant_list.append(i)
    return {
        "plant_list": plant_list
    }
        

@app.get("/customer/plant_detail")
def plant_detail(product : Product):
    result = colproduct.find_one({"ID": product.ID},{"_id":0,"plant_name":1 , "detail": 1 , "price": 1 , "ID" : 1})
    if (result != None):
        return {
            "detail" : result
        }
    else:
        return {
            "detail" : "plant does not exist"
        }

@app.post("/customer/reserve")
def reserve(product : Product , username=Depends(auth_handler.auth_wrapper)):
    resultproduct = colproduct.find_one({"ID":product.ID},{"_id":0})
    resultname = users.find_one({"username": username},{"_id":0})
    #print(resultname)
    if (resultproduct != None) and resultproduct["booking"] == 0:
        users.update_one({"username" : username},{"$set" : {"basketlist": resultname["basketlist"]+[{"ID":product.ID,"duedate":datetime.today()+timedelta(days=2),"plant_name":resultproduct["plant_name"]}]}})
        colproduct.update_one({"ID":product.ID},{"$set": {"booking":1}})
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

@app.get("/customer/basket_list")
def basket_list(username=Depends(auth_handler.auth_wrapper)):
    resultname = users.find_one({"username": username},{"_id":0})
    if (resultname["basketlist"] != None):
        return {"basketlist": resultname["basketlist"]}
    else:
        return "not reserve"

#hardware
@app.post("/hardware/update_humid")
def update_humid(product : Product):
    result = colproduct.find_one({"ID": product.ID},{"_id":0})
    if (result != None):
        query = {"ID": product.ID}
        new = {"$set" : {"humidity_soil_hard": product.humidity_soil_hard , "humidity_air_hard":product.humidity_air_hard , "temp":product.temp}}
        colproduct.update_one(query,new)
        return {
            "update success"
        }
    else:
        return {
            "product not found"
        }

@app.post("/hardware/update_height")
def update_height(product : Product):
    result = colproduct.find_one({"ID": product.ID},{"_id":0})
    if (result != None):
        query = {"ID": product.ID}
        new = {"$set" : {"height_hard": product.height_hard}}
        colproduct.update_one(query,new)
        return {
            "update success"
        }
    else:
        return {
            "product not found"
        }
        
@app.get("/hardware/auto_mode/{id}") # ใส่ไอดีมาด้วย
def auto_mode(id : int):
    result = colproduct.find_one({"ID": id},{"_id":0,"humidity_soil_front":1,"activate_auto": 1})
    if (result != None):
        return result
    else:
        return {
            "product not found"
        }

@app.get("/hardware/exist_plant/{id}")
def exist_plant(id :int):
    result = colproduct.find_one({"ID": id},{"_id":0})
    if (result != None):
        return {
            "existed": 1 
        }
    else:
        return {
            "existed": 0
        }
                