from utils import carregar_json


def calcular_impostos_simples(faturamento):
    """Calcula o imposto do Simples Nacional de acordo com a faixa de faturamento."""
    tabela_simples = carregar_json("tabelas_impostos.json")["tabelas_simples"][0][
        "faixas"
    ]
    for faixa in tabela_simples:
        if faturamento <= faixa["limite"]:
            aliquota = faixa["aliquota"]
            return faturamento * aliquota
    return faturamento * tabela_simples[-1]["aliquota"]


def calcular_impostos_lucro_presumido(faturamento):
    """Calcula o imposto do regime de Lucro Presumido considerando IRPJ, CSLL, PIS, COFINS e ISS."""
    tabela_lucro_presumido = carregar_json("tabelas_impostos.json")[
        "tabelas_lucro_presumido"
    ][0]
    base_lucro_presumido = faturamento * tabela_lucro_presumido["base_lucro_presumido"]

    irpj = base_lucro_presumido * tabela_lucro_presumido["aliquotas"][0]["aliquota"]
    csll = base_lucro_presumido * tabela_lucro_presumido["aliquotas"][1]["aliquota"]
    pis_cofins = faturamento * tabela_lucro_presumido["aliquotas"][2]["aliquota"]
    iss = faturamento * tabela_lucro_presumido["aliquotas"][3]["aliquota"]

    return irpj + csll + pis_cofins + iss
