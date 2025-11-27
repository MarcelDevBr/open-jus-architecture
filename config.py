"""
Carrega e valida as configurações da aplicação de forma moderna e segura.
"""
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Define o diretório raiz do projeto de forma robusta
BASE_DIR = Path(__file__).resolve().parent

# Carrega as variáveis de ambiente do arquivo .env na raiz do projeto
load_dotenv(BASE_DIR / ".env")

class Settings(BaseSettings):
    # --- Configurações Gerais ---
    APP_MODE: str = "prod"  # Mude para 'dev' para usar clientes falsos, se implementado

    # --- Chaves de API ---
    GOOGLE_API_KEY: str | None = None
    MESSAGING_API_TOKEN: str = "SEU_TOKEN_DE_API_AQUI"

# Cria uma instância única das configurações para ser usada em toda a aplicação
settings = Settings()
