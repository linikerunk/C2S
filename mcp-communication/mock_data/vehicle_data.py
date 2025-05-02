from app.core.database import SessionLocal
from app.models.vehicle import Vehicle
from typing import Dict, List
import random

class VehicleDataGenerator:
    def __init__(self):
        self.chinese_cars: Dict[str, Dict] = {
            'BYD': {
                'models': ['Dolphin', 'Seal', 'Tang', 'Han', 'Yuan Plus'],
                'base_prices': {
                    'Dolphin': 150000,
                    'Seal': 200000,
                    'Tang': 300000,
                    'Han': 250000,
                    'Yuan Plus': 180000
                },
                'power': {  # Potência em cv
                    'Dolphin': 204,
                    'Seal': 308,
                    'Tang': 517,
                    'Han': 494,
                    'Yuan Plus': 204
                },
                'battery': {  # Capacidade em kWh
                    'Dolphin': 44.9,
                    'Seal': 82.5,
                    'Tang': 86.4,
                    'Han': 85.4,
                    'Yuan Plus': 50.1
                }
            },
            'GWM': {
                'models': ['Haval H6', 'Tank 300', 'Ora 03', 'Poer', 'Haval H6 GT'],
                'base_prices': {
                    'Haval H6': 180000,
                    'Tank 300': 220000,
                    'Ora 03': 170000,
                    'Poer': 190000,
                    'Haval H6 GT': 210000
                },
                'power': {
                    'Haval H6': 243,
                    'Tank 300': 220,
                    'Ora 03': 171,
                    'Poer': 190,
                    'Haval H6 GT': 243
                },
                'battery': {
                    'Haval H6': 41.8,
                    'Tank 300': None,
                    'Ora 03': 47.8,
                    'Poer': None,
                    'Haval H6 GT': 41.8
                }
            },
            'JAC': {
                'models': ['E-JS1', 'E-JS4', 'T60', 'T80', 'iEV40'],
                'base_prices': {
                    'E-JS1': 150000,
                    'E-JS4': 180000,
                    'T60': 160000,
                    'T80': 200000,
                    'iEV40': 170000
                },
                'power': {
                    'E-JS1': 62,
                    'E-JS4': 150,
                    'T60': 136,
                    'T80': 190,
                    'iEV40': 115
                },
                'battery': {
                    'E-JS1': 30.2,
                    'E-JS4': 55.0,
                    'T60': None,
                    'T80': None,
                    'iEV40': 40.0
                }
            }
        }
        
        self.fuel_types = ['Elétrico', 'Híbrido', 'Plug-in Híbrido', 'Gasolina']
        self.colors = ['Branco Pérola', 'Preto Onix', 'Prata Lunar', 
                      'Azul Elétrico', 'Vermelho Imperial', 'Dourado Solar']
        self.transmissions = ['Automático', 'CVT', 'DCT', 'DSG']

    def generate_vehicle(self) -> Dict:
        brand = random.choice(list(self.chinese_cars.keys()))
        model = random.choice(self.chinese_cars[brand]['models'])
        base_price = self.chinese_cars[brand]['base_prices'][model]
        power = self.chinese_cars[brand]['power'][model]
        battery = self.chinese_cars[brand]['battery'][model]
        
        fuel_type = random.choice(self.fuel_types)
        
        # Se é elétrico ou híbrido, mantém a bateria, senão None
        if fuel_type not in ['Elétrico', 'Híbrido', 'Plug-in Híbrido']:
            battery = None

        return {
            'brand': brand,
            'model': model,
            'year': random.randint(2021, 2024),
            'fuel_type': fuel_type,
            'price': round(base_price * random.uniform(0.95, 1.15), 2),
            'mileage': round(random.uniform(0, 50000), 2),
            'color': random.choice(self.colors),
            'transmission': random.choice(self.transmissions),
            'is_available': random.choice([True, True, True, False]),  # 75% disponível
            'engine_power': power,
            'battery_capacity': battery
        }

def populate_mock_data(num_vehicles: int = 100):
    """Popula o banco com dados mock de veículos"""
    generator = VehicleDataGenerator()
    db = SessionLocal()
    
    try:
        print(f"\n🚗 Gerando {num_vehicles} veículos chineses...")
        for i in range(num_vehicles):
            vehicle_data = generator.generate_vehicle()
            vehicle = Vehicle(**vehicle_data)
            db.add(vehicle)
            
            if (i + 1) % 10 == 0:
                print(f"✓ {i + 1} veículos gerados")
        
        db.commit()
        print("\n✨ Mock data gerado com sucesso!")
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ Erro ao gerar mock data: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    populate_mock_data()