from pydantic import BaseModel
from typing import Optional

class AuthDetails(BaseModel):
    username: str
    password: str
    permission : Optional[int] = 0
    
class Product(BaseModel):
    plant_name : str
    detail : str 
    price : int 
    ID : int 
    humidity_soil_front : Optional[int]
    humidity_soil_hard : Optional[int]
    humidity_air_hard : Optional[int]
    height_hard : Optional[int]
    activate_auto : Optional[int]=0
    booking : Optional[int]=0
    username : Optional[str]
    duedate : Optional[int] = 3