from utils import carregar_json


def carregar_tabela_irpf(arquivo="src/calculations/tabela_irpf.json"):
    """Carrega a tabela IRPF de um arquivo JSON usando o utilitário."""
    return carregar_json(arquivo)


def calcular_irrf(salario_bruto, ano, dependentes=0, pensao_alimenticia=0.0):
    """
    Calcula o IRRF (Imposto de Renda Retido na Fonte) com base no salário bruto,
    subtraindo deduções por dependentes e pensão alimentícia.

    Parâmetros:
    - salario_bruto (float|int): O salário bruto sobre o qual o IRRF será calculado.
    - ano (int): O ano para o qual a tabela do IRPF deve ser aplicada.
    - dependentes (int): O número de dependentes, para calcular a dedução.
    - pensao_alimenticia (float): O valor pago em pensão alimentícia.

    Retorna:
    - float: O valor do IRRF calculado, arredondado para duas casas decimais.
    """

    # Validação dos parâmetros
    if not isinstance(salario_bruto, (int, float)) or salario_bruto < 0:
        raise ValueError("O salário bruto deve ser um valor numérico positivo.")
    if not isinstance(ano, int):
        raise ValueError("O ano deve ser um valor inteiro.")
    if not isinstance(dependentes, int) or dependentes < 0:
        raise ValueError(
            "O número de dependentes deve ser um valor inteiro não negativo."
        )
    if not isinstance(pensao_alimenticia, (int, float)) or pensao_alimenticia < 0:
        raise ValueError(
            "O valor da pensão alimentícia deve ser um valor numérico não negativo."
        )

    # Carregar a tabela de IRPF do arquivo JSON
    tabela_irpf = carregar_tabela_irpf()

    # Encontrar a tabela correspondente ao ano
    tabela_ano = next((t for t in tabela_irpf["tabelas_irpf"] if t["ano"] == ano), None)
    if not tabela_ano:
        raise ValueError(f"Tabela IRPF para o ano {ano} não encontrada no arquivo.")

    # Aplicar deduções
    deducao_dependente = tabela_ano["deducao_dependente"] * dependentes
    salario_base = salario_bruto - deducao_dependente - pensao_alimenticia

    if salario_base <= 0:
        return 0.0

    faixas = tabela_ano["faixas"]
    irrf = 0.0

    # Cálculo progressivo do IRRF
    salario_restante = salario_base
    for faixa in faixas:
        limite = float("inf") if faixa["limite"] == "inf" else faixa["limite"]
        aliquota = faixa["aliquota"]
        deducao = faixa["deducao"]

        if salario_restante <= 0:
            break

        valor_faixa = min(salario_restante, limite)
        irrf += valor_faixa * aliquota - deducao
        salario_restante -= valor_faixa

    return round(irrf, 2)
