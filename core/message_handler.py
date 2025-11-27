"""
Contém a lógica de negócio principal para manipular e responder às mensagens dos usuários.
Agora utiliza o CrewAI para orquestrar a lógica dos agentes.
"""

from services.messaging_service import MessagingService
from services.audio_processing_service import AudioProcessingService
from core.clients import audio_api_client
from core.crew_manager import run_crew  # Importa a função de execução do CrewAI
from core.state_manager import conversation_history_manager
from core.logger import logger
from config import settings

# --- Instanciação dos Componentes Principais ---

audio_service = AudioProcessingService(audio_api_client)
messaging_service = MessagingService(settings.MESSAGING_API_TOKEN)

class MessageHandler:
    def __init__(self, payload: dict):
        self.payload = payload
        self.user_id = payload.get("user_id", "default_user")
        self.text_message = payload.get("message")
        self.audio_url = payload.get("audio_file_url")
        self.query_text = ""
        self.is_audio_response = False

    def _process_input(self):
        """Processa a entrada, seja texto ou áudio."""
        if self.audio_url:
            logger.info(f"Recebida mensagem de áudio do usuário {self.user_id}")
            self.is_audio_response = True
            # A conversão de áudio real seria implementada aqui
            audio_data_simulado = b""
            self.query_text = audio_service.convert_audio_to_text(audio_data_simulado)
        elif self.text_message:
            logger.info(f"Recebida mensagem de texto do usuário {self.user_id}: '{self.text_message}'")
            self.query_text = self.text_message

    def _get_final_response(self) -> str:
        """
        Executa a tripulação do CrewAI para obter a resposta final.
        """
        if not self.query_text:
            logger.warning(f"A consulta do usuário {self.user_id} está vazia.")
            return "Desculpe, não consegui entender sua mensagem."

        # A lógica complexa de planejamento e orquestração é substituída por uma única chamada
        logger.info(f"Iniciando CrewAI para a consulta: '{self.query_text}'")
        final_response = run_crew(self.query_text)
        logger.info(f"Resposta final do CrewAI gerada para o usuário {self.user_id}.")

        return final_response

    def _send_response(self, response_text: str):
        """Envia a resposta para o usuário (texto ou áudio simulado)."""
        if self.is_audio_response:
            # A conversão de texto para áudio real seria implementada aqui
            messaging_service.send_audio(self.user_id, b"audio_simulado")
        else:
            messaging_service.send_message(self.user_id, response_text)

    def handle(self):
        """
        Orquestra o pipeline de processamento da mensagem:
        1. Processa a entrada.
        2. Executa a lógica de IA com CrewAI.
        3. Envia a resposta.
        4. Atualiza o histórico.
        """
        try:
            logger.info(f"Iniciando processamento para o usuário {self.user_id}.")
            self._process_input()
            
            # O histórico não é mais passado diretamente, mas o gerenciador ainda é útil
            history = conversation_history_manager.get_history(self.user_id)
            logger.debug(f"Histórico para o usuário {self.user_id}: {history}")

            # Gera a resposta final usando o CrewAI
            final_response = self._get_final_response()
            
            # Envia a resposta
            self._send_response(final_response)
            
            # Atualiza o histórico com a pergunta e a resposta final
            conversation_history_manager.update_history(self.user_id, self.query_text, final_response)

            logger.info(f"Processamento para o usuário {self.user_id} concluído.")
        except Exception as e:
            logger.error(f"Ocorreu um erro inesperado ao processar a mensagem para o usuário {self.user_id}: {e}", exc_info=True)
            error_message = "Desculpe, ocorreu um erro ao processar sua solicitação."
            self._send_response(error_message)


# Função de conveniência para ser usada no endpoint da API
def process_incoming_message(payload: dict):
    """Ponto de entrada para processar uma nova mensagem."""
    handler = MessageHandler(payload)
    handler.handle()
