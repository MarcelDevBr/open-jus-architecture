"""
Contém a lógica de orquestração para executar planos com múltiplos agentes,
permitindo o uso de ferramentas e sintetizando as respostas.
"""
import json
from typing import Any, Dict

from agents.base_agent import BaseAgent
from core.agent_manager import get_agent_by_name
from core.clients import generative_ai_client
from core.tools.tool_manager import tool_manager
from core.synthesizer import Synthesizer
from core.logger import logger

def _parse_tool_call(response: str) -> Dict[str, Any] | None:
    """Tenta parsear a resposta de um agente como uma chamada de ferramenta JSON de forma segura."""
    try:
        # A resposta deve ser um JSON bem-formado para ser uma chamada de ferramenta
        tool_call = json.loads(response)
        if isinstance(tool_call, dict) and "tool_name" in tool_call:
            return tool_call
    except (json.JSONDecodeError, TypeError):
        # Não é um JSON ou não é um dicionário, então é uma resposta de texto.
        return None
    return None

class Orchestrator:
    def __init__(self, user_query: str, conversation_history: str = ""):
        self.user_query = user_query
        self.conversation_history = conversation_history
        self.synthesizer = Synthesizer(generative_ai_client)

    def _execute_agent_turn(self, agent: BaseAgent) -> str:
        """Executa um único turno de um agente, implementando o ciclo de Raciocínio e Ação (ReAct)."""
        response = agent.get_response(
            self.user_query, 
            conversation_history=self.conversation_history
        )

        tool_call = _parse_tool_call(response)
        if not tool_call:
            return response  # Resposta final, sem uso de ferramenta.

        # Ciclo ReAct: Execução da ferramenta
        tool_name = tool_call.get("tool_name")
        params = tool_call.get("parameters", {})
        logger.info(f"Agente '{agent.name}' solicitou a ferramenta '{tool_name}' com parâmetros: {params}")
        
        tool_result = tool_manager.execute_tool(tool_name, params)
        logger.info(f"Resultado da ferramenta '{tool_name}': {tool_result}")

        # Segunda chamada ao agente com o resultado da ferramenta para a resposta final
        logger.info(f"Chamando o agente '{agent.name}' novamente com o resultado da ferramenta.")
        return agent.get_response(
            self.user_query,
            conversation_history=self.conversation_history,
            tool_result=tool_result
        )

    def execute_plan(self, plan: list[str]) -> str:
        """Executa um plano, consulta os agentes necessários e sintetiza a resposta."""
        # Utiliza list comprehension e o operador walrus (:=) para um código mais conciso e pythonico.
        expert_responses = [
            {"agent_name": agent.name, "response": self._execute_agent_turn(agent)}
            for agent_name in plan
            if (agent := get_agent_by_name(agent_name))
        ]

        if not expert_responses:
            logger.warning(f"Nenhum agente do plano '{plan}' pôde ser executado.")
            return "Desculpe, não foi possível processar sua solicitação com os especialistas disponíveis."
        
        return self.synthesizer.synthesize(self.user_query, expert_responses)
