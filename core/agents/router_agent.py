"""
Define o Agente Roteador.

Este módulo carrega as configurações do agente (role, goal, backstory) de arquivos de texto
e instancia o agente do CrewAI.
"""

import os
from crewai import Agent
from core.clients import llm

# --- Função para Carregar Prompts ---

def _load_prompt(file_name: str) -> str:
    """Carrega o conteúdo de um arquivo de prompt."""
    current_dir = os.path.dirname(os.path.realpath(__file__))
    prompt_path = os.path.join(current_dir, "..", "..", "prompts", "agents", file_name)
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

# --- Carregamento das Configurações do Agente ---

router_agent_role = _load_prompt("router_agent_role.txt")
router_agent_goal = _load_prompt("router_agent_goal.txt")
router_agent_backstory = _load_prompt("router_agent_backstory.txt")

# --- Instanciação do Agente ---

router_agent = Agent(
    role=router_agent_role,
    goal=router_agent_goal,
    backstory=router_agent_backstory,
    tools=[],  # Este agente não possui ferramentas
    llm=llm,
    verbose=True,
    allow_delegation=False
)
