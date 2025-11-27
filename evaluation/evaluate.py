import json
import requests
import os

# --- Configurações ---
GOLDEN_DATASET_PATH = os.path.join(os.path.dirname(__file__), 'golden_dataset.json')
API_URL = "http://127.0.0.1:8000/query" # URL da sua API FastAPI local

def load_golden_dataset():
    """Carrega o dataset de avaliação a partir do arquivo JSON."""
    try:
        with open(GOLDEN_DATASET_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo golden_dataset.json não encontrado em {GOLDEN_DATASET_PATH}")
        return []
    except json.JSONDecodeError:
        print(f"Erro: Falha ao decodificar o JSON em {GOLDEN_DATASET_PATH}")
        return []

def run_evaluation():
    """
    Executa a avaliação, comparando as respostas do sistema com o golden dataset.
    """
    dataset = load_golden_dataset()
    if not dataset:
        return

    print("--- Iniciando Avaliação do Sistema ---")
    print(f"Dataset: {GOLDEN_DATASET_PATH}")
    print(f"API Alvo: {API_URL}\n")

    for i, item in enumerate(dataset):
        question = item.get("question")
        ideal_answer = item.get("ideal_answer")

        if not question or not ideal_answer:
            print(f"Item {i+1} do dataset está mal formatado. Pulando.")
            continue

        print(f"--- Teste {i+1}/{len(dataset)} ---")
        print(f"Pergunta: {question}")

        try:
            # Chama a API com a pergunta
            response = requests.post(API_URL, json={"query": question})
            response.raise_for_status()  # Lança um erro para status HTTP 4xx/5xx

            generated_answer = response.json().get("response", "N/A")

            print("\n[RESPOSTA GERADA PELO SISTEMA]")
            print(f"{generated_answer}\n")

            print("[RESPOSTA IDEAL (Gabarito)]")
            print(f"{ideal_answer}\n")

            print("-" * 25)

        except requests.exceptions.RequestException as e:
            print(f"\n[ERRO] Não foi possível conectar à API em {API_URL}.")
            print(f"Detalhes: {e}")
            print("Por favor, certifique-se de que o servidor FastAPI (main.py) está em execução.")
            break # Interrompe a avaliação se a API não estiver acessível

if __name__ == "__main__":
    run_evaluation()
