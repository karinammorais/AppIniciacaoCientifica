import pandas as pd
import re
from datetime import datetime

# Função para calcular a diferença entre datas
def calcular_diferenca(data1, data2):
    # Verificar se alguma das datas é '99/99/9999'
    if data1 == '99/99/9999' or data2 == '99/99/9999':
        return None  # Ignorar o cálculo se encontrar '99/99/9999'
    
    # Tentar converter as datas para o formato datetime e ignorar erros
    try:
        d1 = pd.to_datetime(data1, errors='coerce', format='%d/%m/%Y')
        d2 = pd.to_datetime(data2, errors='coerce', format='%d/%m/%Y')
        # Verificar se ambas as datas são válidas antes de calcular a diferença
        if pd.notna(d1) and pd.notna(d2):
            return (d2 - d1).days
        else:
            return None  # Retornar None se qualquer data não for válida
    except Exception as e:
        return None  # Retornar None se ocorrer qualquer erro

# Função para extrair o ano do nome do arquivo
def extrair_ano_do_arquivo(nome_arquivo):
    # Procurar por padrão como inCA_2021.xlsx ou qualquer número de 4 dígitos no nome do arquivo
    match = re.search(r'(\d{4})', nome_arquivo)
    if match:
        return int(match.group(1))
    return None

# Mapeamentos para códigos
def get_sexo_map():
    return {1: "Masculino", 2: "Feminino", 3: "Não Informado"}

def get_raca_map():
    return {1: "Branca", 2: "Preta", 3: "Parda", 4: "Amarela", 5: "Indígena", 9: "Sem informação"}

# Função para processar os dados carregados
def processar_dataframe(df):
    # Converter datas importantes
    df["DTDIAGNO"] = pd.to_datetime(df["DTDIAGNO"], errors="coerce", format="%d/%m/%Y")
    df["DATAINITRT"] = pd.to_datetime(df["DATAINITRT"], errors="coerce", format="%d/%m/%Y")
    df["DATAOBITO"] = pd.to_datetime(df["DATAOBITO"], errors="coerce", format="%d/%m/%Y")
    
    # Extrair o ano de diagnóstico e óbito
    df["ANO_DIAGNO"] = df["DTDIAGNO"].dt.year
    df["ANO_OBITO"] = df["DATAOBITO"].dt.year
    
    return df

# Obter dados filtrados por tipo de câncer
def filtrar_dados(data):
    # Filtrar cânceres de pele (todos os C44)
    data_pele = data[data["LOCTUPRI"].str.startswith("C44", na=False)].copy()
    
    # Filtrar melanoma (um subconjunto específico)
    data_melanoma = data[data["LOCTUPRI"].str.contains("C43", na=False)].copy()
    
    # Garantir que as colunas de ano sejam adicionadas aos dataframes filtrados
    for df in [data_pele, data_melanoma]:
        df["ANO_DIAGNO"] = df["DTDIAGNO"].dt.year
        df["ANO_OBITO"] = df["DATAOBITO"].dt.year
    
    return data_pele, data_melanoma

# Calcular métricas básicas
def calcular_metricas_basicas(data_pele, data_melanoma, ano_selecionado, populacao_brasil=211000000):
    # Filtrar óbitos de câncer de pele no ano selecionado
    obitos_pele = data_pele[
        (data_pele["ANO_OBITO"] == ano_selecionado) & 
        (data_pele["DATAOBITO"].notna())
    ]
    
    # Calcular totais
    total_cancer = len(data_pele) + len(data_melanoma)
    total_cancer_pele = len(data_pele)
    total_melanoma = len(data_melanoma)
    total_obitos = len(obitos_pele)
    
    # Calcular taxas
    taxa_incidencia_melanoma = (total_melanoma / populacao_brasil) * 100000
    taxa_incidencia_cancer = (total_cancer / populacao_brasil) * 100
    taxa_incidencia_pele = (total_cancer_pele / populacao_brasil) * 100
    prevalencia_pele = (total_cancer_pele / populacao_brasil) * 100
    letalidade = (total_obitos / total_cancer_pele) * 100 if total_cancer_pele > 0 else 0
    
    return {
        "total_cancer": total_cancer,
        "total_cancer_pele": total_cancer_pele,
        "total_melanoma": total_melanoma,
        "total_obitos": total_obitos,
        "taxa_incidencia_melanoma": taxa_incidencia_melanoma,
        "taxa_incidencia_cancer": taxa_incidencia_cancer,
        "taxa_incidencia_pele": taxa_incidencia_pele,
        "prevalencia_pele": prevalencia_pele,
        "letalidade": letalidade,
        "obitos_pele": obitos_pele
    }

# Calcular tempos médios
def calcular_tempos_medios(data):
    # Calculando as diferenças de datas entre DTDIAGNO e DATAINITRT
    data["DIFF_DTDIAGNO_DATAINITRT"] = data.apply(
        lambda row: calcular_diferenca(
            row["DTDIAGNO"].strftime('%d/%m/%Y') if pd.notna(row["DTDIAGNO"]) else None, 
            row["DATAINITRT"].strftime('%d/%m/%Y') if pd.notna(row["DATAINITRT"]) else None
        ), 
        axis=1
    )
    
    # Calculando as diferenças de datas entre DTDIAGNO e DATAOBITO
    data["DIFF_DTDIAGNO_DATAOBITO"] = data.apply(
        lambda row: calcular_diferenca(
            row["DTDIAGNO"].strftime('%d/%m/%Y') if pd.notna(row["DTDIAGNO"]) else None, 
            row["DATAOBITO"].strftime('%d/%m/%Y') if pd.notna(row["DATAOBITO"]) else None
        ), 
        axis=1
    )
    
    # Filtrar valores válidos para calcular as médias (remover NaN)
    media_tempo_initr = data["DIFF_DTDIAGNO_DATAINITRT"].dropna().mean()
    media_tempo_obito = data["DIFF_DTDIAGNO_DATAOBITO"].dropna().mean()
    
    return media_tempo_initr, media_tempo_obito 