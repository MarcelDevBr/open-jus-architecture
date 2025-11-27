"""
Define a interface base para todas as ferramentas que os agentes podem usar.
"""
from abc import ABC, abstractmethod

class BaseTool(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        """Nome da ferramenta."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Descrição do que a ferramenta faz, para que a IA saiba quando usá-la."""
        pass

    @abstractmethod
    def execute(self, params: dict) -> str:
        """Executa a ferramenta com os parâmetros fornecidos."""
        pass
