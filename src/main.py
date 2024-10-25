import json
import sys

from calculations.clt_pj import calcular_equivalente
from validation import validar_json


def main():
    if len(sys.argv) != 3:
        print("Uso: python clt_pj.py <tipo_calculo> <arquivo_json>")
        sys.exit(1)

    tipo_calculo = sys.argv[1]
    arquivo_json = sys.argv[2]

    with open(arquivo_json, "r") as f:
        dados = json.load(f)

    try:
        validar_json(dados, tipo_calculo)
        if tipo_calculo == "equivalente":
            calcular_equivalente(dados)
        else:
            raise ValueError("Tipo de cálculo inválido.")
    except ValueError as e:
        print(f"Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
