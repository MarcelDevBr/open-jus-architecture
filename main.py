"""
Arquivo principal da aplicação FastAPI.

Define os endpoints da API e delega a lógica de negócio para os módulos do core.
"""

from fastapi import FastAPI, Request, Response, BackgroundTasks
import uvicorn

from core.message_handler import process_incoming_message
from core.logger import logger

# --- Inicialização da Aplicação ---
app = FastAPI(
    title="Sistema Multiagente de Apoio Jurídico",
    description="Uma API para um assistente jurídico baseado em IA, capaz de rotear consultas para agentes especialistas.",
    version="1.0.0"
)

# --- Endpoints da API ---

@app.get("/")
async def root():
    """ Endpoint de health-check para verificar se a API está no ar. """
    return {"status": "ok", "message": "Sistema Multiagente de Apoio Jurídico no ar!"}


@app.post("/webhook")
async def handle_message_webhook(request: Request, background_tasks: BackgroundTasks):
    """
    Endpoint principal que recebe as mensagens dos usuários (via texto ou áudio).
    
    Responde imediatamente e adiciona o processamento da mensagem como uma tarefa em segundo plano.
    """
    payload = await request.json()
    logger.info(f"Webhook recebido. Adicionando tarefa em segundo plano.")
    
    # Adiciona o trabalho pesado a uma fila de tarefas em segundo plano
    background_tasks.add_task(process_incoming_message, payload)
    
    # Responde imediatamente com 200 OK.
    return Response(status_code=200, content="Mensagem recebida para processamento.")


# --- Execução da Aplicação ---

if __name__ == "__main__":
    # Para executar: uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
