"""
Gerencia o registro e o acesso aos agentes especialistas de forma declarativa.
"""

from agents.base_agent import BaseAgent
from agents.specialists.consumer_law_agent import ConsumerLawAgent
from agents.specialists.criminal_law_agent import CriminalLawAgent
from agents.specialists.civil_law_agent import CivilLawAgent
from core.clients import generative_ai_client
from core.logger import logger

# --- Registro Declarativo de Agentes ---
# Mapeia um ID de agente (que corresponde ao seu arquivo de prompt) à sua classe.
# Para adicionar um novo especialista, basta adicionar uma linha a este dicionário.
AGENT_REGISTRY = {
    "specialists/consumer_law_agent": ConsumerLawAgent,
    "specialists/criminal_law_agent": CriminalLawAgent,
    "specialists/civil_law_agent": CivilLawAgent,
}

# --- Inicialização dos Agentes ---
# Itera sobre o registro para instanciar cada agente com seu ID e o cliente de IA.
specialist_agents: list[BaseAgent] = [
    agent_class(generative_ai_client, agent_id=agent_id)
    for agent_id, agent_class in AGENT_REGISTRY.items()
]

# Mapeia nomes de agentes (carregados do YAML) às suas instâncias para acesso rápido.
agents_map: dict[str, BaseAgent] = {agent.name: agent for agent in specialist_agents}

logger.info(f"Agentes especialistas carregados e prontos: {list(agents_map.keys())}")

# --- Funções de Acesso ---

def get_specialist_agents() -> list[BaseAgent]:
    """Retorna a lista de todas as instâncias de agentes especialistas."""
    return specialist_agents

def get_agent_by_name(name: str) -> BaseAgent | None:
    """Busca um agente especialista pelo nome de forma eficiente."""
    return agents_map.get(name)
