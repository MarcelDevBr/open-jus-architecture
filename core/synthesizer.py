"""
Contém a lógica para sintetizar as respostas de múltiplos especialistas em uma única saída.
"""

class Synthesizer:
    def __init__(self, generative_ai_client):
        self.generative_ai_client = generative_ai_client

    def synthesize(self, user_query: str, expert_responses: list[dict]) -> str:
        """
        Combina as respostas de múltiplos especialistas em uma única resposta final.
        """
        if not expert_responses:
            return "Desculpe, não foi possível obter uma resposta dos especialistas."
        
        if len(expert_responses) == 1:
            # Se houver apenas um especialista, retorna sua resposta diretamente.
            return expert_responses[0]["response"]

        formatted_responses = "\n\n".join(
            [f"**Análise do Especialista em {resp['agent_name']}:**\n{resp['response']}" for resp in expert_responses]
        )

        # Este prompt poderia ser externalizado para um arquivo YAML também, seguindo o mesmo padrão.
        prompt = f"""Você é um assistente de IA sênior. Sua tarefa é sintetizar as análises de vários especialistas em uma única resposta coesa e fácil de entender para o usuário final. 
        Não se apresente, apenas forneça a resposta combinada.

        A pergunta original do usuário foi: "{user_query}"

        Abaixo estão as análises dos especialistas consultados:
        ---
        {formatted_responses}
        ---

        Com base nessas análises, formule uma resposta unificada e completa para o usuário.
        """

        return self.generative_ai_client.generate(prompt)
