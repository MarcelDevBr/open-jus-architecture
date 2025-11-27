from ..base_agent import BaseAgent

class AdvogadoAgent(BaseAgent):
    def __init__(self):
        super().__init__()
        self.speciality = "Direito do Consumidor"
        self.prompt_name = "advogado_prompt"

    def get_speciality(self):
        return self.speciality
