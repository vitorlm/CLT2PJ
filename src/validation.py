def validar_json(dados, tipo):
    campos_obrigatorios = {
        "simples": [
            "ano_referencia",
            "salario_bruto_clt",
            "salario_bruto_pj",
            "vale_refeicao",
            "vale_transporte",
            "plano_saude",
            "outros_beneficios",
        ],
        "avancado": [
            "ano_referencia",
            "salario_bruto_clt",
            "salario_bruto_pj",
            "meses_trabalhado",
            "ppr_percentual",
            "dependentes",
            "vale_refeicao",
            "vale_transporte",
            "plano_saude",
            "outros_beneficios",
            "contabilidade",
            "impostos_pj",
        ],
        "equivalente": [
            "ano_referencia",
            "dependentes",
            "tipo_contrato",
            "salario_bruto",
            "regime_tributario",
        ],
    }
    for campo in campos_obrigatorios[tipo]:
        if campo not in dados:
            raise ValueError(f"Campo obrigatório ausente: {campo}")
