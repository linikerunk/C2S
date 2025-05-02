from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse

router = APIRouter()

@router.post("/vehicles/", response_model=VehicleResponse)
async def create_vehicle(vehicle: VehicleCreate, db: Session = Depends(get_db)):
    """Cria um novo veículo no banco de dados"""
    db_vehicle = Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    try:
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/vehicles/", response_model=List[VehicleResponse])
async def read_vehicles(
    skip: int = 0,
    limit: int = 100,
    brand: str = None,
    fuel_type: str = None,
    max_price: float = None,
    db: Session = Depends(get_db)
):
    """Lista veículos com filtros opcionais"""
    query = db.query(Vehicle) 
    
    if brand:
        query = query.filter(Vehicle.brand == brand)
    if fuel_type:
        query = query.filter(Vehicle.fuel_type == fuel_type)
    if max_price:
        query = query.filter(Vehicle.price <= max_price)
    
    vehicles = query.offset(skip).limit(limit).all()
    return vehicles

@router.get("/vehicles/{vehicle_id}", response_model=VehicleResponse)
async def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Busca um veículo específico por ID"""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    return vehicle

@router.delete("/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    """Remove um veículo do banco de dados"""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail="Veículo não encontrado")
    
    db.delete(vehicle)
    db.commit()
    return {"message": "Veículo removido com sucesso"}