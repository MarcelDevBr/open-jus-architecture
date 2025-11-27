"""
Gerencia o carregamento de configurações de agentes e prompts a partir de arquivos YAML.
"""
import yaml
from pathlib import Path
from config import BASE_DIR
from core.logger import logger

class PromptManager:
    def __init__(self, prompts_directory="prompts"):
        self.prompts_path = BASE_DIR / prompts_directory
        self.prompts_config = {}

    def load_prompt_config(self, agent_id: str) -> dict | None:
        """Carrega a configuração de um agente (nome, descrição, prompt) de um arquivo YAML."""
        if agent_id in self.prompts_config:
            return self.prompts_config[agent_id]

        # O agent_id corresponde ao caminho do arquivo, ex: 'specialists/consumer_law_agent'
        file_path = self.prompts_path / f"{agent_id}.yaml"
        
        if not file_path.is_file():
            logger.error(f"Arquivo de prompt não encontrado: {file_path}")
            return None

        try:
            with file_path.open('r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
                self.prompts_config[agent_id] = config
                logger.info(f"Configuração de prompt para '{agent_id}' carregada com sucesso.")
                return config
        except yaml.YAMLError as e:
            logger.error(f"Erro de sintaxe no arquivo YAML {file_path}: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao carregar o arquivo de prompt {file_path}: {e}", exc_info=True)
            return None

prompt_manager = PromptManager()
