"""
Simula um serviço para acessar uma biblioteca de recursos, como modelos de documentos.
"""
from core.logger import logger

class ResourceService:
    def __init__(self):
        # Em uma aplicação real, isso se conectaria a um banco de dados (Firestore, S3, etc.)
        self.documents = {
            "notificacao_extrajudicial_produto_defeituoso": {
                "title": "Modelo de Notificação Extrajudicial por Produto Defeituoso",
                "description": "Um modelo de carta formal para notificar uma loja ou fabricante sobre um produto com defeito, solicitando reparo, troca ou reembolso.",
                "content": "Prezados, [Nome da Empresa],\n\nEu, [Seu Nome Completo], venho por meio desta notificar que o produto [Nome do Produto], adquirido em [Data da Compra], apresentou defeito..."
            },
            "solicitacao_cancelamento_servico": {
                "title": "Modelo de Solicitação de Cancelamento de Serviço",
                "description": "Um modelo de e-mail ou carta para solicitar o cancelamento de um serviço (telefonia, internet, academia) e questionar multas indevidas.",
                "content": "Assunto: Solicitação de Cancelamento de Contrato - [Seu Nome]\n\nA/C [Nome da Empresa],\n\nSolicito o cancelamento do meu contrato de [Tipo de Serviço]..."
            }
        }
        logger.info("ResourceService inicializado com documentos de exemplo.")

    def find_document_by_keyword(self, keyword: str) -> dict | None:
        """Busca um documento por uma palavra-chave no seu ID."""
        for doc_id, doc_data in self.documents.items():
            if keyword.lower() in doc_id.lower():
                return {"id": doc_id, **doc_data}
        return None

# Instância única
resource_service = ResourceService()
