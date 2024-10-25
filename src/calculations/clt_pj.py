from calculations.imposto_pj import (
    calcular_impostos_lucro_presumido,
    calcular_impostos_simples,
)
from calculations.inss import calcular_inss
from calculations.irpf import calcular_irrf


def calcular_equivalente(dados):
    """Calcula o salário equivalente no outro regime (CLT ↔ PJ)."""

    if dados["tipo_contrato"] == "clt":
        salario_pj = calcular_salario_pj_para_equivaler_clt(dados)
        print(
            f"Para equivaler ao contrato CLT, o salário PJ necessário é: R$ {salario_pj}"
        )
    elif dados["tipo_contrato"] == "pj":
        salario_clt = calcular_salario_clt_para_equivaler_pj(dados)
        print(
            f"Para equivaler ao contrato PJ, o salário CLT necessário é: R$ {salario_clt}"
        )
    else:
        raise ValueError("Tipo de contrato inválido. Use 'clt' ou 'pj'.")


def calcular_salario_pj_para_equivaler_clt(dados_clt):
    """Calcula o salário bruto PJ necessário para equivaler ao contrato CLT."""
    salario_bruto = dados_clt["salario_bruto"]
    inss = calcular_inss(salario_bruto, dados_clt["ano_referencia"])
    salario_bruto_menos_inss = salario_bruto - inss
    irpf = calcular_irrf(
        salario_bruto_menos_inss, dados_clt["ano_referencia"], dados_clt["dependentes"]
    )

    beneficios = sum(b["valor"] for b in dados_clt["beneficios"])
    descontos = sum(d["valor"] for d in dados_clt["descontos"])
    descontos_pj = sum(d["valor"] for d in dados_clt["descontos_pj"])

    fgts = salario_bruto * 0.08

    liquido_clt = salario_bruto_menos_inss + beneficios - descontos - irpf + fgts

    # Escolha do regime tributário (Simples Nacional ou Lucro Presumido)
    regime_tributario = dados_clt.get("regime_tributario", "simples")

    faturamento = liquido_clt
    impostos_pj = 0

    while True:
        if regime_tributario == "simples":
            impostos_pj = calcular_impostos_simples(faturamento)
        elif regime_tributario == "lucro_presumido":
            impostos_pj = calcular_impostos_lucro_presumido(faturamento)
        else:
            raise ValueError(
                "Regime tributário desconhecido: use 'simples' ou 'lucro_presumido'"
            )

        resultado = faturamento - impostos_pj - descontos_pj
        if resultado >= liquido_clt:
            break
        faturamento += 250

    return round(faturamento, 2)


def calcular_salario_clt_para_equivaler_pj(dados_pj):
    """Calcula o salário bruto CLT necessário para equivaler ao contrato PJ."""
    salario_bruto_pj = dados_pj["salario_bruto"]

    beneficios = sum(b["valor"] for b in dados_pj["beneficios"])
    descontos = sum(d["valor"] for d in dados_pj["descontos"])

    contabilidade = dados_pj["contabilidade"]
    liquido_pj = salario_bruto_pj + beneficios - descontos - contabilidade

    inss = calcular_inss(liquido_pj)
    irpf = calcular_irrf(liquido_pj)

    salario_clt = (liquido_pj + inss + irpf) / (1 - 0.27)

    return round(salario_clt, 2)
