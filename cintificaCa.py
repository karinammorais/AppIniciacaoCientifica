import streamlit as st
import pandas as pd
import numpy as np
from streamlit_lottie import st_lottie
from streamlit_extras.add_vertical_space import add_vertical_space
import time
import os
import re

# Importar módulos personalizados
from utils import extrair_ano_do_arquivo, processar_dataframe, filtrar_dados, calcular_metricas_basicas
from visualizations import criar_grafico_pizza, criar_grafico_barras, aplicar_estilo_moderno
from styles import aplicar_estilos, exibir_loader
from componentes import (
    mostrar_sidebar, mostrar_header, mostrar_secao_upload,
    mostrar_indicadores_gerais, mostrar_analise_demografica,
    mostrar_analise_mortalidade, mostrar_tempos_medios, load_lottieurl
)

# Configuração da página
st.set_page_config(
    page_title="Dashboard de Análise Epidemiológica",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.streamlit.io',
        'Report a bug': "https://www.streamlit.io/feedback",
        'About': "# Dashboard de Análise Epidemiológica - Câncer de Pele"
    }
)

# Aplicar estilos personalizados
aplicar_estilos()

# Inicializar estado da sessão se necessário
if 'dados_carregados' not in st.session_state:
    st.session_state.dados_carregados = False
    st.session_state.dados_por_ano = {}
    st.session_state.anos_disponiveis = []
    st.session_state.dados_atuais = {}

# Função para processar os arquivos enviados
def processar_arquivos(uploaded_files):
    dados_por_ano = {}
    anos_disponiveis = []
    
    # Processar cada arquivo
    for file in uploaded_files:
        # Extrair o ano do nome do arquivo
        ano = extrair_ano_do_arquivo(file.name)
        if ano:
            # Ler o arquivo Excel
            try:
                df = pd.read_excel(file)
                # Processar o dataframe (converter datas, etc.)
                df = processar_dataframe(df)
                
                # Armazenar dataframe no dicionário
                dados_por_ano[ano] = df
                anos_disponiveis.append(ano)
            except Exception as e:
                st.error(f"Erro ao processar arquivo {file.name}: {e}")
                continue
    
    # Verificar se foram encontrados anos válidos
    if not anos_disponiveis:
        st.warning("Não foi possível identificar o ano nos nomes dos arquivos. Os nomes devem conter o ano (ex: inCA_2021.xlsx)")
        return False
    
    # Ordenar os anos disponíveis
    anos_disponiveis.sort()
    
    # Armazenar os dados na sessão
    st.session_state.dados_carregados = True
    st.session_state.dados_por_ano = dados_por_ano
    st.session_state.anos_disponiveis = anos_disponiveis
    
    return True

# Interface principal da aplicação
def main():
    # Exibir cabeçalho
    mostrar_header()
    
    # Se os dados ainda não foram carregados, mostrar a interface de upload
    if not st.session_state.dados_carregados:
        dados_carregados = mostrar_secao_upload(processar_arquivos)
        
        # Se os dados foram carregados com sucesso, continuar
        if dados_carregados:
            st.rerun()
        return
    
    # Mostrar a barra lateral com filtros e obter valores selecionados
    ano_selecionado, populacao_brasil, mostrar_tabelas = mostrar_sidebar(
        st.session_state.dados_por_ano,
        st.session_state.anos_disponiveis
    )
    
    # Recuperar os dados do ano selecionado
    data = st.session_state.dados_por_ano.get(ano_selecionado, pd.DataFrame())
    
    # Se temos dados para o ano selecionado
    if not data.empty:
        # Filtrar dados para câncer de pele e melanoma
        data_pele, data_melanoma = filtrar_dados(data)
        
        # Calcular métricas básicas
        metricas = calcular_metricas_basicas(
            data_pele, data_melanoma, ano_selecionado, populacao_brasil
        )
        
        # Armazenar dados processados para uso em outras seções
        dados_atuais = {
            'data_pele': data_pele,
            'data_melanoma': data_melanoma,
            'metricas': metricas
        }
        st.session_state.dados_atuais = dados_atuais
        
        # Criar tabs para organizar o conteúdo
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Indicadores Gerais", 
            "👥 Análise Demográfica", 
            "⚠️ Mortalidade",
            "⏱️ Tempos Médios"
        ])
        
        with tab1:
            metricas = mostrar_indicadores_gerais(
                dados_atuais, 
                ano_selecionado, 
                populacao_brasil
            )
        
        with tab2:
            mostrar_analise_demografica(
                dados_atuais, 
                ano_selecionado, 
                mostrar_tabelas
            )
        
        with tab3:
            mostrar_analise_mortalidade(
                dados_atuais, 
                ano_selecionado, 
                mostrar_tabelas
            )
            
        with tab4:
            mostrar_tempos_medios(
                dados_atuais,
                ano_selecionado,
                mostrar_tabelas
            )
    
    else:
        st.warning(f"Não há dados disponíveis para o ano {ano_selecionado}.")
    
    # Adicionar rodapé
    add_vertical_space(2)
    st.markdown("""
    <div style="text-align: center; opacity: 0.7; padding: 20px;">
        <p>Dashboard de Análise Epidemiológica - Versão 2.0</p>
        <p>© 2023 - Todos os direitos reservados</p>
    </div>
    """, unsafe_allow_html=True)

# Função para redefinir os dados (resetar a aplicação)
def resetar_aplicacao():
    for key in ['dados_carregados', 'dados_por_ano', 'anos_disponiveis', 'dados_atuais']:
        if key in st.session_state:
            del st.session_state[key]

# Executar a aplicação
if __name__ == "__main__":
    main() 
