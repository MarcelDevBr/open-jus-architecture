"""
Implementa a ferramenta para acessar a Biblioteca de Recursos.
"""
from core.tools.base_tool import BaseTool
from services.resource_service import resource_service
from core.logger import logger

class ResourceLibraryTool(BaseTool):
    @property
    def name(self) -> str:
        return "resource_library_lookup"

    @property
    def description(self) -> str:
        return "Busca na Biblioteca de Recursos por modelos de documentos úteis (ex: notificação, cancelamento) usando uma palavra-chave. Use esta ferramenta se o usuário precisar de um modelo de documento para formalizar uma reclamação ou solicitação."

    def execute(self, params: dict) -> str:
        """
        Executa a busca por um documento na biblioteca de recursos.
        """
        keyword = params.get("keyword")
        if not keyword:
            return "Erro: Uma palavra-chave (ex: 'cancelamento', 'defeito') é necessária para buscar na biblioteca."

        logger.info(f"Executando a ferramenta 'resource_library_lookup' com a palavra-chave: {keyword}")
        
        document = resource_service.find_document_by_keyword(keyword)
        
        if document:
            return f"Documento encontrado: '{document['title']}'. Descrição: {document['description']}. Conteúdo: {document['content']}"
        else:
            return f"Nenhum modelo de documento encontrado para a palavra-chave '{keyword}'."
