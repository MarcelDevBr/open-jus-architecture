"""
Define e agrupa as ferramentas (tools) que os agentes do CrewAI podem utilizar.

Este módulo centraliza a instanciação de todas as ferramentas e as agrupa em listas
específicas para cada tipo de agente, como 'consumer_tools'.
"""

from crewai_tools import tool

# Importa a ferramenta RAG e as ferramentas de utilidade
from core.rag_tool import knowledge_base_retriever
from core.tools.find_procon_tool import FindProconTool
from core.tools.resource_library_tool import ResourceLibraryTool

# Instancia as classes das ferramentas originais
find_procon_tool_instance = FindProconTool()
resource_library_tool_instance = ResourceLibraryTool()

# --- Definição das Ferramentas Adaptadas para CrewAI ---

@tool(find_procon_tool_instance.name)
def find_procon(location: str) -> str:
    """Busca o endereço e o telefone do Procon mais próximo de uma cidade ou CEP. Use esta ferramenta sempre que o usuário pedir o contato de um Procon."""
    return find_procon_tool_instance.execute({"location": location})

@tool(resource_library_tool_instance.name)
def resource_library_lookup(keyword: str) -> str:
    """Busca na Biblioteca de Recursos por modelos de documentos úteis (ex: 'notificação', 'cancelamento', 'defeito') usando uma palavra-chave. Use esta ferramenta se a situação do usuário puder ser resolvida com um documento formal."""
    return resource_library_tool_instance.execute({"keyword": keyword})


# --- Agrupamento de Ferramentas para Agentes Específicos ---

# Ferramentas para o Agente de Consumidor
consumer_tools = [knowledge_base_retriever, find_procon, resource_library_lookup]

# Lista de todas as ferramentas disponíveis (pode ser útil para outros agentes)
available_tools = [knowledge_base_retriever, find_procon, resource_library_lookup]
