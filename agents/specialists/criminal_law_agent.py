"""
Agente especialista em Direito Penal.

A lógica e o prompt deste agente são carregados dinamicamente a partir de:
/prompts/specialists/criminal_law_agent.yaml
"""
from agents.base_agent import BaseAgent

class CriminalLawAgent(BaseAgent):
    def __init__(self, generative_ai_client):
        super().__init__(generative_ai_client, agent_id="specialists/criminal_law_agent")
