"""
Define o Agente de Adaptação de Comunicação.
"""
from core.prompt_manager import prompt_manager

class CommunicationAdapterAgent:
    def __init__(self, generative_ai_client):
        self.generative_ai_client = generative_ai_client
        config = prompt_manager.load_prompt_config("utility/communication_adapter_agent")
        if not config or "prompt" not in config:
            raise ValueError("Não foi possível carregar a configuração do CommunicationAdapterAgent.")
        self.prompt_template = config["prompt"]

    def adapt_style(self, original_user_query: str, expert_response: str) -> str:
        """
        Adapta o estilo da resposta do especialista com base na consulta do usuário.
        """
        formatted_prompt = self.prompt_template.format(
            original_user_query=original_user_query,
            expert_response=expert_response
        )
        return self.generative_ai_client.generate(formatted_prompt)
