"""
Gerencia o registro e a execução de todas as ferramentas disponíveis.
"""
from core.tools.find_procon_tool import FindProconTool
from core.tools.resource_library_tool import ResourceLibraryTool
from core.logger import logger

class ToolManager:
    def __init__(self):
        self.tools = {}
        self._register_tools()

    def _register_tools(self):
        """Registra todas as instâncias de ferramentas disponíveis no sistema."""
        all_tools = [
            FindProconTool(),
            ResourceLibraryTool(),
            # Adicione outras ferramentas aqui
        ]
        for tool in all_tools:
            self.tools[tool.name] = tool
        logger.info(f"Ferramentas registradas: {list(self.tools.keys())}")

    def execute_tool(self, tool_name: str, params: dict) -> str:
        """Executa uma ferramenta específica pelo nome."""
        if tool_name in self.tools:
            try:
                return self.tools[tool_name].execute(params)
            except Exception as e:
                logger.error(f"Erro ao executar a ferramenta '{tool_name}': {e}", exc_info=True)
                return f"Erro: Falha ao executar a ferramenta {tool_name}."
        else:
            logger.warning(f"Tentativa de executar uma ferramenta desconhecida: {tool_name}")
            return f"Erro: Ferramenta '{tool_name}' não encontrada."

# Instância única para ser usada em toda a aplicação
tool_manager = ToolManager()
