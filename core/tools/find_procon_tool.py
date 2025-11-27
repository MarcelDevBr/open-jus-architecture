"""
Implementa a ferramenta para encontrar Procons locais, alinhada com a funcionalidade 'CONECTE' do MVP.
"""
from core.tools.base_tool import BaseTool
from core.logger import logger

class FindProconTool(BaseTool):
    @property
    def name(self) -> str:
        return "find_procon"

    @property
    def description(self) -> str:
        return "Busca o endereço e o telefone do Procon mais próximo de uma cidade ou CEP fornecido pelo usuário. Use esta ferramenta sempre que o usuário pedir o contato de um Procon."

    def execute(self, params: dict) -> str:
        """
        Simula a busca por um Procon. Em uma implementação real, isso chamaria
        as APIs do Google Maps, possivelmente orquestrado via Make.com como no plano do MVP.
        """
        location = params.get("location")
        if not location:
            return "Erro: A localização (cidade ou CEP) não foi fornecida para a busca."

        logger.info(f"Executando a ferramenta 'find_procon' para a localização: {location}")
        
        # Simulação de uma chamada de API para o Webhook
        # No seu MVP, isso seria uma chamada HTTP para o endpoint do Make.com
        return f"Informação encontrada para a localização '{location}': Procon Municipal - Endereço: Rua Principal, 123 - Telefone: (48) 3224-0000. Recomendo ligar antes de ir."
