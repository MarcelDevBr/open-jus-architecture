"""
Gerencia o estado da conversa, como o histórico de mensagens.
"""
from collections import defaultdict, deque
from core.logger import logger

class ConversationHistoryManager:
    def __init__(self, max_history_length=10):
        """
        Inicializa o gerenciador de histórico.
        Usa um defaultdict com um deque de tamanho fixo para armazenar o histórico de cada usuário.
        """
        self.history = defaultdict(lambda: deque(maxlen=max_history_length))
        logger.info("ConversationHistoryManager inicializado.")

    def get_history(self, user_id: str) -> str:
        """
        Recupera o histórico de conversa formatado para um usuário.
        """
        user_history = self.history.get(user_id, deque())
        if not user_history:
            return "Nenhum histórico de conversa anterior."
        
        formatted_history = "\n".join(user_history)
        logger.info(f"Histórico recuperado para o usuário {user_id}.")
        return formatted_history

    def update_history(self, user_id: str, user_query: str, ai_response: str):
        """
        Atualiza o histórico de conversa de um usuário com a última interação.
        """
        self.history[user_id].append(f"Usuário: {user_query}")
        self.history[user_id].append(f"Assistente: {ai_response}")
        logger.info(f"Histórico atualizado para o usuário {user_id}.")

# Instância única para ser usada em toda a aplicação
conversation_history_manager = ConversationHistoryManager()
