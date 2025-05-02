from pydantic import BaseModel
from typing import Optional

class VehicleBase(BaseModel):
    brand: str
    model: str
    year: int
    fuel_type: str
    price: float
    mileage: float
    color: str

class VehicleCreate(VehicleBase):
    pass

class VehicleResponse(VehicleBase):
    id: int

    class Config:
        orm_mode = True