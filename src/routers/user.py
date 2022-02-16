from fastapi import APIRouter, Depends, HTTPException
from ..auth import AuthHandler
from ..schemas import AuthDetails
from pymongo import MongoClient

myclient = MongoClient("localhost",27017)
db = myclient["Yaya-Fever"]
users = db["users"]

auth_handler = AuthHandler()

router = APIRouter(
   prefix="/users",
   tags=["Users"],
   responses={404: {"message": "Not found"}}
)

#Register User
@router.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    #Find that user already use or not.
    result = users.find_one({"username":auth_details.username},{"_id":0})
    if (result):
        print(auth_details.username)
        raise HTTPException(status_code=400, detail='Username is taken')
    #Register newuser.
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.insert_one({
        'username': auth_details.username,
        'password': hashed_password,
        'permission':auth_details.permission
    })
    return {"detail": "Register SUCCESS"}

#Login 
@router.post('/login')
def login(auth_details: AuthDetails):
    result = users.find_one({"username":auth_details.username},{"_id":0})
    #Check username and password.
    if (result is None) or (not auth_handler.verify_password(auth_details.password, result['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(result['username'])
    return { 'token': token }

#Check permistion
@router.get('/getpermission')
def protected(username = Depends(auth_handler.auth_wrapper)):
    result = users.find_one({"username" : username},{"_id":0})
    if result["permission"] == 1:
        return {'name': username}
    else:
        raise HTTPException(status_code=401, detail='Permission denined')