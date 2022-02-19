from imp import NullImporter
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
    duedate : Optional[int]
    water_time : Optional[int] = 0
    img : Optional[str] = "https://firebasestorage.googleapis.com/v0/b/test-fd80e.appspot.com/o/063780857652.295000000default_plant.jpeg?alt=media&token=28eef77b-7516-42af-b0a0-c0f2d9b7bcd4"