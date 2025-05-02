from sqlalchemy import Boolean, Column, Integer, String, Float
from app.core.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False, index=True)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    fuel_type = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    mileage = Column(Float, nullable=True)
    color = Column(String, nullable=False)
     
    # Novas colunas
    transmission = Column(String(20), nullable=False, default="Automático")  # Tipo de transmissão
    is_available = Column(Boolean, default=True)  # Disponibilidade
    engine_power = Column(Float, nullable=True)  # Potência do motor (cv/hp)
    battery_capacity = Column(Float, nullable=True)  # Capacidade da bateria (kWh)
    def __repr__(self):
        return f"<Vehicle(brand={self.brand}, model={self.model}, year={self.year})>"