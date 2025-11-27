"""
Define a ferramenta para realizar buscas na base de conhecimento vetorial (RAG).
"""

import os
from crewai_tools import tool
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from core.logger import logger

# --- Constantes ---
FAISS_INDEX_PATH = "storage/faiss_index"

# --- Carregamento do Índice ---
# O índice é carregado uma vez quando o módulo é importado para eficiência.
vector_store = None
if os.path.exists(FAISS_INDEX_PATH):
    try:
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
        logger.info(f"Índice FAISS carregado com sucesso de '{FAISS_INDEX_PATH}'.")
    except Exception as e:
        logger.error(f"Falha ao carregar o índice FAISS: {e}. A ferramenta de busca não funcionará.", exc_info=True)
else:
    logger.warning(f"O índice FAISS não foi encontrado em '{FAISS_INDEX_PATH}'. Execute 'build_knowledge_base.py' para criá-lo.")

# --- Definição da Ferramenta ---

@tool("knowledge_base_retriever")
def knowledge_base_retriever(query: str) -> str:
    """Busca na base de conhecimento jurídica (leis, CDC, etc.) por informações relevantes a uma consulta. Use esta ferramenta sempre que precisar de embasamento legal ou informações específicas sobre leis de consumo para responder a uma pergunta."""
    if not vector_store:
        return "Erro: A base de conhecimento não está disponível ou não foi carregada. Avise ao usuário para contatar o suporte."

    logger.info(f"Executando busca na base de conhecimento com a query: '{query}'")
    try:
        # Realiza a busca por similaridade
        results = vector_store.similarity_search(query, k=3)  # Retorna os 3 chunks mais relevantes
        
        if not results:
            return "Nenhuma informação relevante encontrada na base de conhecimento para esta consulta."

        # Formata os resultados para serem retornados ao agente
        context = "\n\n---\n\n".join([doc.page_content for doc in results])
        logger.info(f"Resultados da busca encontrados. Retornando contexto para o agente.")
        return f"Aqui estão os trechos da base de conhecimento mais relevantes para sua consulta:\n\n{context}"
    except Exception as e:
        logger.error(f"Erro durante a busca na base de conhecimento: {e}", exc_info=True)
        return "Erro ao realizar a busca na base de conhecimento."
