from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import router
from app.core.database import engine
from app.models.vehicle import Base

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# Inicializa o FastAPI
app = FastAPI(
    title="API de Veículos",
    description="Sistema de gerenciamento de veículos chineses premium",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(router, prefix="/api/v1", tags=["vehicles"])

# Rota de teste
@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Bem-vindo à API de Veículos!"}