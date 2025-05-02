import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 500
    TEMPERATURE = 0.7
    
    SYSTEM_PROMPT = """
    Você é um assistente especializado em veículos chineses premium.
    Base suas respostas em dados reais sobre BYD, GWM, JAC e outras marcas.
    Seja preciso com especificações técnicas e preços.
    Mantenha um tom profissional mas amigável.
    """