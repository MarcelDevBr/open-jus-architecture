"""
Gerencia a criação, configuração e execução da tripulação (Crew) de agentes da CrewAI.

Este módulo importa todos os agentes, define a sequência de tarefas de 3 etapas
(Roteamento -> Análise Técnica -> Comunicação) e executa a tripulação.
"""

from crewai import Task, Crew, Process
from core.logger import logger

# --- Importação de todos os Agentes Modulares ---
from core.agents.router_agent import router_agent
from core.agents.advogado_consumidor import advogado_consumidor_agent
from core.agents.criminal_agent import criminal_agent
from core.agents.civil_agent import civil_agent
from core.agents.communication_agent import communication_agent # Novo agente!

# --- Definição das Tarefas em 3 Etapas ---

def create_crew_tasks(user_query: str) -> list[Task]:
    """Cria as tarefas para a tripulação com base na consulta do usuário."""

    # Tarefa 1: Roteamento
    # O router_agent analisa a consulta e decide qual especialista é o mais adequado.
    routing_task = Task(
        description=f"Analise a seguinte consulta do usuário e decida qual especialista é o mais qualificado para respondê-la. Consulta: '{user_query}'",
        expected_output="O nome do cargo (role) do agente especialista mais adequado para a tarefa. Apenas o nome do cargo.",
        agent=router_agent
    )

    # Tarefa 2: Análise Técnica
    # O agente especialista escolhido (via contexto) executa a análise aprofundada.
    # A resposta desta tarefa será a matéria-prima para a próxima etapa.
    technical_analysis_task = Task(
        description=f"Com base na consulta do usuário, forneça uma análise técnica completa e uma orientação clara, seguindo estritamente suas diretrizes de atuação. Use suas ferramentas para embasar a resposta. Consulta: '{user_query}'",
        expected_output="A análise técnica e detalhada, incluindo referências legais ou de ferramentas, para ser usada pelo Especialista em Comunicação.",
        context=[routing_task], # O resultado do roteamento determina o agente
    )

    # Tarefa 3: Comunicação com o Usuário
    # O communication_agent "traduz" a análise técnica para uma linguagem simples.
    communication_task = Task(
        description="Reescreva a análise técnica a seguir em uma linguagem simples, clara, empática e acionável para um usuário leigo. Elimine jargões e foque em orientações práticas.",
        expected_output="A resposta final, formatada e pronta para ser entregue ao usuário, escrita em linguagem totalmente compreensível.",
        agent=communication_agent,
        context=[technical_analysis_task] # Usa a saída da análise técnica como entrada
    )

    return [routing_task, technical_analysis_task, communication_task]

# --- Montagem e Execução da Tripulação ---

def run_crew(user_query: str) -> str:
    """
    Monta e executa a tripulação para processar a consulta do usuário.
    """
    logger.info(f"Iniciando a execução da tripulação para a consulta: {user_query}")

    tasks = create_crew_tasks(user_query)

    # A lista de agentes inclui todos os nossos especialistas. O CrewAI selecionará
    # dinamicamente os agentes corretos para cada tarefa com base no contexto.
    crew = Crew(
        agents=[
            router_agent, 
            advogado_consumidor_agent, 
            criminal_agent, 
            civil_agent, 
            communication_agent
        ],
        tasks=tasks,
        process=Process.sequential, # As 3 tarefas são executadas em sequência
        verbose=2
    )

    result = crew.kickoff()

    logger.info(f"Execução da tripulação concluída. Resultado: {result}")
    return result
