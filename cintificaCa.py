import streamlit as st
import pandas as pd
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

# Leitura dos arquivos
st.title("Análise de Casos de Câncer de Pele")
uploaded_files = st.file_uploader("Faça upload dos arquivos .xlsx", accept_multiple_files=True, type="xlsx")

if uploaded_files:
    df_list = []
    for file in uploaded_files:
        df = pd.read_excel(file)
        df_list.append(df)

    # Concatenar todos os dataframes
    data = pd.concat(df_list)

    # Filtrar cânceres de pele
    data = data[data["LOCTUPRI"].str.startswith("C44", na=False)]

    # Métricas
    st.subheader("Quantidade de casos")

    # Exibindo contagem por Estado
    st.write("Por Estado:")
    df_estados = data["ESTADRES"].value_counts().rename_axis("ESTADOS").reset_index(name="QUANTIDADE")
    st.dataframe(df_estados)

    # Exibindo contagem por Idade
    st.write("Por Idade:")
    df_idade = data["IDADE"].value_counts().rename_axis("IDADE").reset_index(name="QUANTIDADE")
    st.dataframe(df_idade)

    # Exibindo contagem por Raça/Cor
    st.write("Por Raça/Cor:")
    df_racacor = data["RACACOR"].value_counts().rename_axis("RAÇA/COR").reset_index(name="QUANTIDADE")
    st.dataframe(df_racacor)

    # Ajuste para calcular corretamente a quantidade de óbitos por ano
    st.write("Por Ano de Óbito:")

    # Garantir que a conversão para datetime seja feita corretamente
    data["DATAOBITO"] = pd.to_datetime(data["DATAOBITO"], errors="coerce", format="%d/%m/%Y")

    # Filtrar apenas as linhas com uma data válida (não NaT)
    data_validos = data[data["DATAOBITO"].notna()].copy()

    # Extraindo o ano do óbito
    data_validos["ANO_OBITO"] = data_validos["DATAOBITO"].dt.year

    # Contar a quantidade de óbitos por ano
    anos_obito_counts = (
        data_validos["ANO_OBITO"]
        .value_counts()
        .sort_index()
        .rename_axis("ANO_OBITO")
        .reset_index(name="QUANTIDADE")
    )
    st.dataframe(anos_obito_counts.style.format({"ANO_OBITO": "{:.0f}", "QUANTIDADE": "{:.0f}"}))

    # Calculando as diferenças de datas entre DTDIAGNO e DATAINITRT, e DTDIAGNO e DATAOBITO
    data["DIFF_DTDIAGNO_DATAINITRT"] = data.apply(lambda row: calcular_diferenca(row["DTDIAGNO"], row["DATAINITRT"]), axis=1)
    data["DIFF_DTDIAGNO_DATAOBITO"] = data.apply(lambda row: calcular_diferenca(row["DTDIAGNO"], row["DATAOBITO"]), axis=1)

    # Filtrar valores válidos para calcular as médias (remover NaN)
    media_tempo_initr = data["DIFF_DTDIAGNO_DATAINITRT"].dropna().mean()  # Média para a diferença entre DTDIAGNO e DATAINITRT
    media_tempo_obito = data["DIFF_DTDIAGNO_DATAOBITO"].dropna().mean()  # Média para a diferença entre DTDIAGNO e DATAOBITO

    # Exibir médias de tempo
    st.subheader("Médias de Tempo")
    
    # Validar se a média foi calculada corretamente
    if not pd.isna(media_tempo_initr) and media_tempo_initr > 0:
        st.write(f"Média de tempo entre DTDIAGNO e DATAINITRT: **{media_tempo_initr:.2f} dias**")
    else:
        st.write("Média de tempo entre DTDIAGNO e DATAINITRT: **Dados insuficientes ou inválidos para cálculo**")

    if not pd.isna(media_tempo_obito) and media_tempo_obito > 0:
        st.write(f"Média de tempo entre DTDIAGNO e DATAOBITO: **{media_tempo_obito:.2f} dias**")
    else:
        st.write("Média de tempo entre DTDIAGNO e DATAOBITO: **Dados insuficientes ou inválidos para cálculo**")

    # Exibindo casos por hospital (CNES)
    st.write("Casos por Hospital (CNES):")
    df_cnes = (
        data["CNES"]
        .value_counts()
        .rename_axis("HOSPITAL (CNES)")
        .reset_index(name="QUANTIDADE")
    )
    df_cnes["HOSPITAL (CNES)"] = df_cnes["HOSPITAL (CNES)"].astype(int)
    st.dataframe(df_cnes.style.format({"HOSPITAL (CNES)": "{:.0f}", "QUANTIDADE": "{:.0f}"}))
