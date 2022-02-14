from fastapi import FastAPI, Depends, HTTPException
from .auth import AuthHandler
from .schemas import AuthDetails
from fastapi.middleware.cors import CORSMiddleware
from fastapi.encoders import jsonable_encoder
from pymongo import MongoClient
from datetime import datetime

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