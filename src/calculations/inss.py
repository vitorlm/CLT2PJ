from utils import carregar_json


def carregar_tabela_inss(arquivo="src/calculations/tabela_inss.json"):
    """Carrega a tabela INSS de um arquivo JSON usando o utilitário."""
    return carregar_json(arquivo)


def calcular_inss(salario_bruto, ano):
    """
    Calcula o INSS com base na tabela para o ano informado, respeitando o teto de contribuição.

    Parâmetros:
    - salario_bruto (float|int): O salário bruto sobre o qual o INSS será calculado.
      Deve ser um valor numérico positivo.
    - ano (int): O ano para o qual a tabela do INSS deve ser aplicada.

    Retorna:
    - float: O valor do INSS calculado, arredondado para duas casas decimais.
    """

    # Validação dos parâmetros
    if not isinstance(salario_bruto, (int, float)) or salario_bruto < 0:
        raise ValueError("O salário bruto deve ser um valor numérico positivo.")
    if not isinstance(ano, int):
        raise ValueError("O ano deve ser um valor inteiro.")

    # Carregar a tabela INSS do arquivo JSON
    tabela_inss = carregar_tabela_inss()

    # Encontrar a tabela correspondente ao ano
    tabela_ano = next((t for t in tabela_inss["tabelas_inss"] if t["ano"] == ano), None)
    if not tabela_ano:
        raise ValueError(f"Tabela INSS para o ano {ano} não encontrada no arquivo.")

    faixas = tabela_ano["faixas"]
    teto = tabela_ano["teto"]

    # Cálculo progressivo do INSS
    inss = 0.0
    salario_restante = salario_bruto

    for faixa in faixas:
        limite = float("inf") if faixa["limite"] == "inf" else faixa["limite"]
        aliquota = faixa["aliquota"]

        if salario_restante <= 0:
            break

        valor_faixa = min(salario_restante, limite)
        inss += valor_faixa * aliquota
        salario_restante -= valor_faixa

    # Se o valor do INSS ultrapassar o teto, limitar ao valor do teto
    return round(min(inss, teto), 2)
