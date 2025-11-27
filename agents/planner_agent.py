"""
Este módulo define o Agente Planejador (PlannerAgent).
"""
from core.prompt_manager import prompt_manager

class PlannerAgent:
    def __init__(self, generative_ai_client):
        self.generative_ai_client = generative_ai_client
        config = prompt_manager.load_prompt_config("planner_agent")
        if not config or "prompt" not in config:
            raise ValueError("Não foi possível carregar a configuração do PlannerAgent.")
        self.prompt_template = config["prompt"]

    def create_plan(self, user_query: str, available_agents: list) -> list[str]:
        """
        Cria um plano de execução listando os agentes necessários.
        """
        agent_descriptions = "\n".join(
            [f"- {agent.name}: {agent.description}" for agent in available_agents]
        )

        formatted_prompt = self.prompt_template.format(
            user_query=user_query, 
            agent_descriptions=agent_descriptions
        )

        response = self.generative_ai_client.generate(formatted_prompt).strip()
        selected_agents = [name.strip() for name in response.split(',') if name.strip()]
        return selected_agents
