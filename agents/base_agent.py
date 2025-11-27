"""
Define a interface base para todos os agentes especialistas.
"""
from abc import ABC
from core.prompt_manager import prompt_manager

class BaseAgent(ABC):
    def __init__(self, generative_ai_client, agent_id: str):
        self.generative_ai_client = generative_ai_client
        self.agent_id = agent_id
        
        config = prompt_manager.load_prompt_config(agent_id)
        if not config:
            raise ValueError(f"Não foi possível carregar a configuração para o agente: {agent_id}")

        self.name = config.get("name")
        self.description = config.get("description")
        self.prompt_template = config.get("prompt")

    def get_response(self, user_query: str, **kwargs) -> str:
        """
        Formata o prompt com a consulta do usuário e o contexto adicional (histórico, etc.)
        e obtém uma resposta da IA.
        """
        if not self.prompt_template:
            raise ValueError(f"O template de prompt para o agente {self.name} não está definido.")

        # Prepara os argumentos para a formatação, garantindo que as chaves sempre existam.
        format_args = {
            "user_query": user_query,
            "conversation_history": kwargs.get("conversation_history", ""),
            "tool_result": kwargs.get("tool_result", "")
        }
        
        formatted_prompt = self.prompt_template.format(**format_args)
        
        response = self.generative_ai_client.generate(formatted_prompt)
        return response
