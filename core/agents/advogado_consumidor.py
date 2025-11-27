"""
Define o Agente 'Advogado' para Disputas de Consumidor.

Este módulo carrega as configurações do agente (role, goal, backstory) de arquivos de texto
e instancia o agente do CrewAI com as ferramentas necessárias.
"""

import os
from crewai import Agent
from core.clients import llm
from core.tools import consumer_tools

# --- Função para Carregar Prompts ---

def _load_prompt(file_name: str) -> str:
    """Carrega o conteúdo de um arquivo de prompt."""
    # Constrói o caminho relativo à localização deste arquivo
    # Isso torna o carregamento independente do diretório de trabalho atual
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # O caminho para os prompts é ../../prompts/agents/
    prompt_path = os.path.join(current_dir, "..", "..", "prompts", "agents", file_name)
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

# --- Carregamento das Configurações do Agente ---

advogado_consumidor_role = _load_prompt("advogado_consumidor_role.txt")
advogado_consumidor_goal = _load_prompt("advogado_consumidor_goal.txt")
advogado_consumidor_backstory = _load_prompt("advogado_consumidor_backstory.txt")

# --- Instanciação do Agente ---

advogado_consumidor_agent = Agent(
    role=advogado_consumidor_role,
    goal=advogado_consumidor_goal,
    backstory=advogado_consumidor_backstory,
    tools=consumer_tools,
    llm=llm,
    verbose=True,
    allow_delegation=False
)
