"""
Agente especialista em Direito do Consumidor.

A lógica e o prompt deste agente são carregados dinamicamente a partir de:
/prompts/specialists/consumer_law_agent.yaml
"""
from agents.base_agent import BaseAgent

class ConsumerLawAgent(BaseAgent):
    def __init__(self, generative_ai_client):
        # O agent_id corresponde ao caminho do arquivo de prompt, sem a extensão .yaml
        super().__init__(generative_ai_client, agent_id="specialists/consumer_law_agent")
