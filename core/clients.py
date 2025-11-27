"""
Gerencia a configuração e instanciação dos clientes de LLM para o CrewAI.
"""
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

from core.logger import logger

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configuração do Cliente de LLM (OpenAI) ---
# Para o CrewAI, geralmente configuramos o LLM diretamente
# e o passamos para os Agents ou para o Crew.

# Pega a chave da API da OpenAI das variáveis de ambiente
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    logger.error("A chave de API da OpenAI (OPENAI_API_KEY) não foi encontrada. Verifique seu arquivo .env.")
    raise ValueError("OPENAI_API_KEY não configurada.")

# Instancia o modelo de linguagem que será usado pelos agentes
# Usamos o gpt-4-turbo por padrão, mas pode ser qualquer outro modelo da OpenAI
try:
    llm = ChatOpenAI(
        model="gpt-4-turbo",
        api_key=openai_api_key
    )
    logger.info("Cliente ChatOpenAI inicializado com sucesso.")
except Exception as e:
    logger.error(f"Falha ao inicializar o cliente ChatOpenAI: {e}", exc_info=True)
    raise

# --- Definição do Cliente de Áudio Falso (para manter a compatibilidade) ---

class FakeAudioAPIClient:
    """Cliente de Processamento de Áudio que simula conversões."""
    def convert_audio_to_text(self, audio_data) -> str:
        return "(Texto simulado) Meu produto veio com defeito e a loja quer que eu pague uma multa no contrato de serviço."

    def convert_text_to_audio(self, text: str):
        return b"dados_de_audio_simulados"

# --- Fábrica de Clientes ---

def get_audio_api_client():
    """Retorna uma instância do cliente de Áudio."""
    # A implementação do cliente de áudio real seguiria o mesmo padrão.
    return FakeAudioAPIClient()

# --- Instâncias Globais (para serem importadas por outros módulos) ---

# A instância 'llm' será importada diretamente pelos módulos que definem os agentes e a tripulação.
audio_api_client = get_audio_api_client()
