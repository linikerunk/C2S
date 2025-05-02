from app.core.database import Base, engine
from app.models.vehicle import Vehicle
from mock_data.vehicle_data import populate_mock_data  # Corrigindo o caminho da importação

def migrate_database():
    """Migra e popula o banco C2S com dados mock"""
    try:
        # Remove tabelas existentes e recria
        print("\n🔧 Recriando tabelas no banco C2S...")
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas recriadas com sucesso!")
        
        # Popula com os dados mock usando o VehicleDataGenerator
        print("\n📝 Populando banco com dados mock...")
        populate_mock_data(num_vehicles=100)
        
    except Exception as e:
        print(f"\n❌ Erro durante migração: {str(e)}")
        print(f"Detalhes: {e.__class__.__name__}")
        return False
        
    return True

if __name__ == "__main__":
    migrate_database()