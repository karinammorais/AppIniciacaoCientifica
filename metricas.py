import pandas as pd
import numpy as np

def calcular_indicadores_incidencia(df, populacao_total):
    """Calcula indicadores de incidência"""
    # Total de casos
    casos_totais = len(df)
    
    # Casos de câncer de pele (C43 + C44)
    df_pele = df[df["TOPOGRAF"].str.match("C4[34]", na=False)]
    casos_pele = len(df_pele)
    
    # Calcular taxas de incidência (por 100.000 habitantes)
    taxa_incidencia_geral = (casos_totais / populacao_total) * 100000
    taxa_incidencia_pele = (casos_pele / populacao_total) * 100000
    
    return {
        "taxa_incidencia_geral": taxa_incidencia_geral,
        "taxa_incidencia_pele": taxa_incidencia_pele,
        "casos_totais": casos_totais,
        "casos_pele": casos_pele
    }

def calcular_indicadores_mortalidade(df):
    """Calcula indicadores de mortalidade"""
    # Filtrar óbitos
    df_obitos = df[pd.notna(df["DATAOBITO"])]
    
    # Total de óbitos
    obitos_total = len(df_obitos)
    
    # Óbitos por câncer de pele
    df_obitos_pele = df_obitos[df_obitos["TOPOGRAF"].str.match("C4[34]", na=False)]
    obitos_pele = len(df_obitos_pele)
    
    # Mortalidade por sexo
    mortalidade_sexo = df_obitos_pele.groupby("SEXO").size()
    
    # Mortalidade por idade
    mortalidade_idade = df_obitos_pele.groupby("IDADE").size()
    
    # Mortalidade por raça/cor
    mortalidade_raca = df_obitos_pele.groupby("RACACOR").size()
    
    # Mortalidade por estado (usando ESTADRES)
    mortalidade_estado = df_obitos_pele.groupby("UF").size()
    
    # Letalidade (óbitos/casos totais)
    df_pele = df[df["TOPOGRAF"].str.match("C4[34]", na=False)]
    letalidade = (obitos_pele / len(df_pele)) * 100 if len(df_pele) > 0 else 0
    
    return {
        "obitos_total": obitos_total,
        "obitos_pele": obitos_pele,
        "mortalidade_sexo": mortalidade_sexo,
        "mortalidade_idade": mortalidade_idade,
        "mortalidade_raca": mortalidade_raca,
        "mortalidade_estado": mortalidade_estado,
        "letalidade": letalidade
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
