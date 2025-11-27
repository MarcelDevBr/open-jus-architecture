"""
Script para construir a base de conhecimento vetorial (FAISS) a partir de documentos.

Este script deve ser executado sempre que os documentos na pasta `knowledge_base`
forem atualizados.

Uso:
1. Adicione seus arquivos de texto (.txt, .pdf, .md) na pasta `knowledge_base`.
2. Execute este script no seu terminal: `python build_knowledge_base.py`
3. O índice FAISS será criado e salvo na pasta `storage/faiss_index`.
"""

import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
from core.logger import logger

# Carrega as variáveis de ambiente (necessário para a OPENAI_API_KEY)
load_dotenv()

# --- Constantes ---
KNOWLEDGE_BASE_DIR = "knowledge_base"
FAISS_INDEX_PATH = "storage/faiss_index"

# Mapeia extensões de arquivo para as classes de loader correspondentes
LOADER_MAPPING = {
    ".pdf": PyPDFLoader,
    ".txt": TextLoader,
    ".md": TextLoader,
}

def build_knowledge_base():
    """Lê os documentos, cria os embeddings e salva o índice FAISS."""
    logger.info(f"Iniciando a construção da base de conhecimento a partir de '{KNOWLEDGE_BASE_DIR}'...")

    # Usa DirectoryLoader com um glob para carregar todos os arquivos suportados
    loader = DirectoryLoader(
        KNOWLEDGE_BASE_DIR,
        glob="**/*[!.gitkeep]",  # Ignora o arquivo .gitkeep
        loader_cls=TextLoader, # Loader padrão
        use_multithreading=True
    )

    try:
        documents = loader.load()
        if not documents:
            logger.warning(f"Nenhum documento encontrado em '{KNOWLEDGE_BASE_DIR}'. O índice não será criado.")
            return
    except Exception as e:
        logger.error(f"Erro ao carregar documentos: {e}", exc_info=True)
        return

    # 2. Dividir os documentos em pedaços (chunks)
    logger.info(f"{len(documents)} documentos carregados. Dividindo em chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    logger.info(f"{len(chunks)} chunks criados.")

    # 3. Gerar os embeddings e criar o Vector Store (FAISS)
    logger.info("Gerando embeddings com a OpenAI e criando o índice FAISS...")
    try:
        embeddings = OpenAIEmbeddings()
        vector_store = FAISS.from_documents(chunks, embeddings)
    except Exception as e:
        logger.error(f"Erro ao gerar embeddings ou criar o índice FAISS: {e}", exc_info=True)
        return

    # 4. Salvar o índice FAISS localmente
    logger.info(f"Salvando o índice FAISS em '{FAISS_INDEX_PATH}'...")
    vector_store.save_local(FAISS_INDEX_PATH)

    logger.info("Base de conhecimento construída e salva com sucesso!")

if __name__ == "__main__":
    # Garante que o diretório de armazenamento exista
    if not os.path.exists("storage"):
        os.makedirs("storage")
    
    build_knowledge_base()
