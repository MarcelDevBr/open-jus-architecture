"""
Configura o logger para a aplicação.
"""
import logging
import sys

# Configura o formato do log
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

# Cria um logger
logger = logging.getLogger("TCC_Multiagente")
logger.setLevel(logging.INFO)

# Cria um handler para enviar os logs para a saída padrão (console)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Adiciona o handler ao logger
logger.addHandler(handler)
