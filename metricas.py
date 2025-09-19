import pandas as pd
import numpy as np

def calcular_indicadores_incidencia(df, populacao_total, estados_selecionados):
    """Calcula indicadores de incidência considerando estados selecionados"""
    # Filtrar por estados selecionados
    if estados_selecionados:
        df = df[df['UF'].isin(estados_selecionados)]

    # Total de casos
    casos_totais = len(df)

    # Casos de câncer de pele (C43 + C44)
    df_pele = df[df["TOPOGRAF"].str.match("C4[34]", na=False)]
    casos_pele = len(df_pele)

    # Casos de C43 e C44 separados
    df_c43 = df[df["TOPOGRAF"].str.match("C43", na=False)]
    df_c44 = df[df["TOPOGRAF"].str.match("C44", na=False)]
    casos_c43 = len(df_c43)
    casos_c44 = len(df_c44)

    # Calcular taxas de incidência (em porcentagem)
    taxa_incidencia_geral = (casos_totais / populacao_total) * 100
    taxa_incidencia_pele = (casos_pele / populacao_total) * 100
    taxa_incidencia_c43 = (casos_c43 / populacao_total) * 100
    taxa_incidencia_c44 = (casos_c44 / populacao_total) * 100

    return {
        "taxa_incidencia_geral": taxa_incidencia_geral,
        "taxa_incidencia_pele": taxa_incidencia_pele,
        "taxa_incidencia_c43": taxa_incidencia_c43,
        "taxa_incidencia_c44": taxa_incidencia_c44,
        "casos_totais": casos_totais,
        "casos_pele": casos_pele,
        "casos_c43": casos_c43,
        "casos_c44": casos_c44
    }

def calcular_indicadores_mortalidade(df, estados_selecionados):
    """Calcula indicadores de mortalidade considerando estados selecionados"""
    # Filtrar por estados selecionados
    if estados_selecionados:
        df = df[df['UF'].isin(estados_selecionados)]

    # Garantir que as colunas esperadas existam no DataFrame
    colunas_esperadas = ["DATAOBITO", "TOPOGRAF", "SEXO", "IDADE", "RACACOR", "UF"]
    for coluna in colunas_esperadas:
        if coluna not in df.columns:
            df[coluna] = None

    # Filtrar óbitos
    df_obitos = df[pd.notna(df["DATAOBITO"])]

    # Total de óbitos
    obitos_total = len(df_obitos)

    # Óbitos por câncer de pele
    df_obitos_pele = df_obitos[df_obitos["TOPOGRAF"].str.match("C4[34]", na=False)]
    obitos_pele = len(df_obitos_pele)

    # Mortalidade por sexo
    mortalidade_sexo = df_obitos_pele.groupby("SEXO").size() if not df_obitos_pele.empty else {}

    # Mortalidade por idade
    mortalidade_idade = df_obitos_pele.groupby("IDADE").size() if not df_obitos_pele.empty else {}

    # Criar faixas etárias
    bins = [0, 18, 35, 50, 65, 80, 100]
    labels = ["0-17", "18-34", "35-49", "50-64", "65-79", "80+"]

    if not df_obitos_pele.empty:
        # Corrigir SettingWithCopyWarning
        df_obitos_pele.loc[:, 'FAIXA_ETARIA'] = pd.cut(df_obitos_pele['IDADE'], bins=bins, labels=labels, right=False)

        # Corrigir FutureWarning sobre observed
        mortalidade_faixas_etarias = df_obitos_pele.groupby('FAIXA_ETARIA', observed=False).size()
    else:
        mortalidade_faixas_etarias = {}

    # Mortalidade por raça/cor
    mortalidade_raca = df_obitos_pele.groupby("RACACOR").size() if not df_obitos_pele.empty else {}

    # Mortalidade por estado (usando ESTADRES)
    mortalidade_estado = df_obitos_pele.groupby("UF").size() if not df_obitos_pele.empty else {}

    # Lista de estados únicos
    estados = df_obitos_pele['UF'].unique().tolist() if not df_obitos_pele.empty else []

    # Mortalidade por tipo de câncer (C43 e C44)
    mortalidade_c43_c44 = df_obitos_pele.groupby(["TOPOGRAF", "LOCTUDET", "LOCTUPRI"]).size() if not df_obitos_pele.empty else {}
    print("Log: Agrupamento de mortalidade por TOPOGRAF, LOCTUDET e LOCTUPRI:")
    print(mortalidade_c43_c44)

    # Letalidade (óbitos/casos totais)
    df_pele = df[df["TOPOGRAF"].str.match("C4[34]", na=False)]
    if df_pele.empty:
        print("Aviso: Nenhum caso encontrado para C43 ou C44.")
    else:
        # Filtrar óbitos
        df_obitos_pele = df_pele[df_pele["DATAOBITO"].notna()]

        # Filtrar casos por tipo de câncer
        df_c43 = df_pele[df_pele["TOPOGRAF"].str.contains("C43", na=False)]
        df_c44 = df_pele[df_pele["TOPOGRAF"].str.contains("C44", na=False)]

        # Validar DataFrames
        if df_c43.empty:
            print("Aviso: Nenhum caso encontrado para C43. Verifique os dados de entrada ou os filtros aplicados.")
        if df_c44.empty:
            print("Aviso: Nenhum caso encontrado para C44. Verifique os dados de entrada ou os filtros aplicados.")

        # Logs detalhados para validação
        print("Casos totais de C43:", len(df_c43))
        print("Óbitos por C43:", len(df_obitos_pele[df_obitos_pele["TOPOGRAF"].str.contains("C43", na=False)]))
        print("Casos totais de C44:", len(df_c44))
        print("Óbitos por C44:", len(df_obitos_pele[df_obitos_pele["TOPOGRAF"].str.contains("C44", na=False)]))

        # Calcular letalidade
        letalidade_c43 = (len(df_obitos_pele[df_obitos_pele["TOPOGRAF"].str.contains("C43", na=False)]) / len(df_c43)) * 100 if len(df_c43) > 0 else 0
        letalidade_c44 = (len(df_obitos_pele[df_obitos_pele["TOPOGRAF"].str.contains("C44", na=False)]) / len(df_c44)) * 100 if len(df_c44) > 0 else 0

        # Calcular letalidade geral
        letalidade = (len(df_obitos_pele) / len(df_pele)) * 100 if len(df_pele) > 0 else 0

        # Validar intervalos de letalidade
        if letalidade_c43 < 0 or letalidade_c43 > 100:
            print("Erro: Letalidade de C43 fora do intervalo válido (0% a 100%).")
        if letalidade_c44 < 0 or letalidade_c44 > 100:
            print("Erro: Letalidade de C44 fora do intervalo válido (0% a 100%).")
        if letalidade < 0 or letalidade > 100:
            print("Erro: Letalidade geral fora do intervalo válido (0% a 100%).")

    # Retornar resultados
    return {
        "obitos_total": obitos_total,
        "obitos_pele": obitos_pele,
        "mortalidade_sexo": mortalidade_sexo,
        "mortalidade_idade": mortalidade_idade,
        "faixas_etarias": mortalidade_faixas_etarias,
        "mortalidade_raca": mortalidade_raca,
        "mortalidade_estado": mortalidade_estado,
        "estados": estados,
        "mortalidade_c43_c44": mortalidade_c43_c44,
        "letalidade": letalidade,
        "letalidade_c43": letalidade_c43,
        "letalidade_c44": letalidade_c44
    }

def calcular_tempos_medios(df):
    """Calcula tempos médios entre eventos"""
    df_pele = df[df["TOPOGRAF"].str.match("C4[34]", na=False)]
    
    # Tempo até início do tratamento
    tempo_ate_tratamento = (df_pele["DATAINITRT"] - df_pele["DTDIAGNO"]).dt.days.mean()
    
    # Tempo até óbito
    tempo_ate_obito = (df_pele["DATAOBITO"] - df_pele["DTDIAGNO"]).dt.days.mean()
    
    return {
        "tempo_ate_tratamento": tempo_ate_tratamento if not pd.isna(tempo_ate_tratamento) else 0,
        "tempo_ate_obito": tempo_ate_obito if not pd.isna(tempo_ate_obito) else 0
    }

def calcular_perfil_demografico(df):
    """Calcula distribuições demográficas"""
    df_pele = df[df["TOPOGRAF"].str.match("C4[34]", na=False)]
    
    distribuicoes = {
        "raca": df_pele["RACACOR"].value_counts(),
        "idade": df_pele["IDADE"].value_counts(),
        "sexo": df_pele["SEXO"].value_counts(),
        "estado": df_pele["UF"].value_counts(),
        "instrucao": df_pele["INSTRUC"].value_counts(),
        "localizacao": df_pele["LOUCTUPRI"].value_counts()
    }
    
    return distribuicoes
