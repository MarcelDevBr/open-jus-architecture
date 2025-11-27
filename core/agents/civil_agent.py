"""
Define o Agente Especialista em Direito Civil.

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

civil_agent_role = _load_prompt("civil_agent_role.txt")
civil_agent_goal = _load_prompt("civil_agent_goal.txt")
civil_agent_backstory = _load_prompt("civil_agent_backstory.txt")

# --- Instanciação do Agente ---

civil_agent = Agent(
    role=civil_agent_role,
    goal=civil_agent_goal,
    backstory=civil_agent_backstory,
    tools=[],  # Este agente não possui ferramentas
    llm=llm,
    verbose=True,
    allow_delegation=False
)
