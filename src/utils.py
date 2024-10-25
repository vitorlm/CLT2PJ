import json


def carregar_json(arquivo):
    """Carrega e retorna os dados de um arquivo JSON."""
    try:
        with open(arquivo, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        raise Exception(f"Arquivo {arquivo} não encontrado.")
    except json.JSONDecodeError:
        raise Exception(
            f"Erro ao decodificar o arquivo JSON {arquivo}. Verifique a sintaxe."
        )


def salvar_json(arquivo, dados):
    """Salva dados em um arquivo JSON."""
    try:
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
    except Exception as e:
        raise Exception(f"Erro ao salvar dados no arquivo {arquivo}: {e}")
