from pydantic import BaseModel
from typing import Optional

class AuthDetails(BaseModel):
    username: str
    password: str
    permission : Optional[int] = 0
    basketlist : Optional[list] = []
    
class Product(BaseModel):
    plant_name : Optional[str]
    detail : Optional[str] = " "
    price : Optional[int]
    ID : int
    humidity_soil_front : Optional[int] = -1
    humidity_soil_hard : Optional[int]
    humidity_air_hard : Optional[float]
    height_hard : Optional[int]
    temp : Optional[float]
    activate_auto : Optional[int] = 0
    booking : Optional[int] = 0
    username : Optional[str]
    duedate : Optional[int] = 3
    water_time : Optional[int] = 0