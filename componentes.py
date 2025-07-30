import streamlit as st
import pandas as pd
import numpy as np
from utils import get_sexo_map, get_raca_map, calcular_metricas_basicas, calcular_tempos_medios, calcular_diferenca
from visualizations import (
    criar_grafico_pizza, criar_grafico_barras, criar_grafico_linha, criar_mapa_calor,
    criar_grafico_combinado_idade_sexo, criar_card_estatistico
)
import plotly.express as px
import requests
from streamlit_lottie import st_lottie
import time
import json

# Função para carregar animações Lottie
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception as e:
        st.error(f"Erro ao carregar animação: {e}")
        return None

# Animações Lottie para cada seção
ANIMATIONS = {
    "cancer": "https://lottie.host/6ac29ae5-48c3-480e-99a8-8dac0ed2df6a/wR4LjnEKkm.json",
    "upload": "https://lottie.host/62a50f8e-621a-477d-9637-8513f7ee2c03/gWFbpuF62k.json",
    "analytics": "https://lottie.host/85de38cd-bc89-45ec-8b0d-b4af44eb240d/2KDgxT5s5k.json"
}

def mostrar_sidebar(dados_por_ano, anos_disponiveis):
    """Mostra a barra lateral com opções de filtro"""
    with st.sidebar:
        st.markdown("""
        <style>
            .css-1cpxqw2 {
                background-color: #000000;
                border: 2px solid #7D3C98;
                border-radius: 12px;
                padding: 10px;
                color: white;
                font-weight: bold;
            }
        </style>
        """, unsafe_allow_html=True)
        ano_selecionado = st.selectbox(
            "Filtre o ano",
            options=anos_disponiveis,
            index=len(anos_disponiveis)-1 if anos_disponiveis else 0
        )
    return ano_selecionado

def mostrar_header():
    """Exibe o cabeçalho da aplicação"""
    col1, col2 = st.columns([1, 8])
    with col1:
        st.image("logo.png", width=110)
    with col2:
        st.markdown("""
        <div style='display:flex; align-items:center;'>
            <span class='painel-title'>PAINEL SKIN </span>
            <span class='painel-title-roxo'>MELANOMA BRASIL</span>
        </div>
        <div style='margin-top:0.5rem; font-size:1.1rem; color:#ccc;'>
            Nosso sistema gera automaticamente relatórios epidemiológicos históricos sobre o câncer de pele tipo melanoma, com base em dados abertos de fontes oficiais nacionais e internacionais. A plataforma integra essas informações de forma inteligente, permitindo análises rápidas, confiáveis e atualizadas sobre a evolução do melanoma no Brasil e no mundo.
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='display:flex; justify-content:center; margin-top:1.5rem;'>", unsafe_allow_html=True)
        st.button("Visualizar relatório epidemiológico")
        st.markdown("</div>", unsafe_allow_html=True)

def mostrar_secao_upload(callback_processamento=None):
    """Exibe a seção de upload de arquivos"""    
    st.markdown("""
        <div style='display:flex; justify-content:center; margin-top:2rem;'>
            <div style='width: 100%; max-width: 500px;'>
                <div style='border: 2px dashed #7D3C98; border-radius: 10px; padding: 30px; background: #181818;'>
                    <h4 style='text-align:center; color:#fff; margin-bottom:1.5rem;'>Arraste e solte os arquivos aqui</h4>
                    <div style='display:flex; justify-content:center;'>
                        <span style='color:#aaa; font-size:0.95rem;'>Formatos aceitos: .xlsx</span>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    uploaded_files = st.file_uploader(
        "",
        type=["xlsx"],
        accept_multiple_files=True,
        key="file_uploader"
    )
    st.markdown("<div style='display:flex; justify-content:center; margin-top:1.5rem;'>", unsafe_allow_html=True)
    if st.button("Processar", key="enviar-arquivos", use_container_width=False):
        if uploaded_files:
            if callback_processamento:
                with st.spinner("Processando os dados..."):
                    progresso = st.progress(0)
                    for i in range(101):
                        time.sleep(0.01)
                        progresso.progress(i)
                    resultado = callback_processamento(uploaded_files)
                    progresso.empty()
                    if resultado:
                        st.success("✅ Dados carregados com sucesso!")
        else:
            st.warning("Por favor, selecione pelo menos um arquivo.")
    st.markdown("</div>", unsafe_allow_html=True)
    return False

def mostrar_indicadores_gerais(dados, ano_selecionado, populacao_brasil):
    """Exibe a seção de indicadores gerais"""
    st.markdown("## 📊 Indicadores Epidemiológicos Gerais")
    
    data_pele = dados.get('data_pele', pd.DataFrame())
    data_melanoma = dados.get('data_melanoma', pd.DataFrame())
    
    # Calcular métricas básicas
    metricas = calcular_metricas_basicas(
        data_pele, 
        data_melanoma, 
        ano_selecionado, 
        populacao_brasil
    )
    
    # Exibir cards com as métricas principais
    col1, col2, col3 = st.columns(3)
    with col1:
        criar_card_estatistico(
            "Total de Casos de Câncer", 
            f"{metricas['total_cancer']:,}",
            f"Taxa de Incidência: {metricas['taxa_incidencia_cancer']:.4f}%"
        )
    
    with col2:
        criar_card_estatistico(
            "Casos de Câncer de Pele", 
            f"{metricas['total_cancer_pele']:,}", 
            f"Taxa de Incidência: {metricas['taxa_incidencia_pele']:.4f}%"
        )
    
    with col3:
        criar_card_estatistico(
            "Casos de Melanoma", 
            f"{metricas['total_melanoma']:,}",
            f"Taxa: {metricas['taxa_incidencia_melanoma']:.2f} por 100.000"
        )
    
    # Segunda linha de cards
    col1, col2, col3 = st.columns(3)
    with col1:
        criar_card_estatistico(
            "Total de Óbitos", 
            f"{metricas['total_obitos']:,}", 
            f"Letalidade: {metricas['letalidade']:.2f}%"
        )
    
    with col2:
        # Calcular tempos médios
        media_tempo_initr, media_tempo_obito = calcular_tempos_medios(data_pele)
        criar_card_estatistico(
            "Tempo até Tratamento", 
            f"{media_tempo_initr:.1f} dias", 
            "Média entre diagnóstico e início do tratamento"
        )
    
    with col3:
        criar_card_estatistico(
            "Sobrevida Média", 
            f"{media_tempo_obito:.1f} dias", 
            "Média entre diagnóstico e óbito"
        )
    
    return metricas

def mostrar_analise_demografica(dados, ano_selecionado, mostrar_tabelas=False):
    """Exibe a seção de análise demográfica"""
    st.markdown("## 👥 Análise Demográfica")
    
    data_pele = dados.get('data_pele', pd.DataFrame())
    
    # Distribuição por raça/cor
    raca_map = get_raca_map()
    dist_raca = data_pele.groupby("RACACOR").size().reset_index(name="QUANTIDADE")
    dist_raca["RACA_NOME"] = dist_raca["RACACOR"].map(raca_map)
    
    # Distribuição por idade
    dist_idade = data_pele.groupby("IDADE").size().reset_index(name="QUANTIDADE")
    
    # Distribuição por sexo
    sexo_map = get_sexo_map()
    dist_sexo = data_pele.groupby("SEXO").size().reset_index(name="QUANTIDADE")
    dist_sexo["SEXO_NOME"] = dist_sexo["SEXO"].map(sexo_map)
    
    # Gráfico de distribuição por raça/cor
    st.plotly_chart(
        criar_grafico_pizza(
            dist_raca, 
            "RACA_NOME", 
            f"Distribuição por Raça/Cor ({ano_selecionado})"
        ),
        use_container_width=True
    )
    
    # Gráfico combinado de idade e sexo
    st.plotly_chart(
        criar_grafico_combinado_idade_sexo(
            dist_idade, 
            dist_sexo, 
            ano_selecionado
        ),
        use_container_width=True
    )
    
    # Mostrar tabelas se a opção estiver habilitada
    if mostrar_tabelas:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Tabela de Raça/Cor")
            st.dataframe(dist_raca[["RACA_NOME", "QUANTIDADE"]])
        
        with col2:
            st.markdown("### Tabela de Sexo")
            st.dataframe(dist_sexo[["SEXO_NOME", "QUANTIDADE"]])
        
        st.markdown("### Tabela de Idade")
        st.dataframe(dist_idade)

def mostrar_analise_mortalidade(dados, ano_selecionado, mostrar_tabelas=False):
    """Exibe a seção de análise de mortalidade"""
    st.markdown("## ⚠️ Análise de Mortalidade")
    
    # Obter dados
    data_pele = dados.get('data_pele', pd.DataFrame())
    metricas = dados.get('metricas', {})
    obitos_pele = metricas.get('obitos_pele', pd.DataFrame())
    
    # Mapas para conversão
    sexo_map = get_sexo_map()
    raca_map = get_raca_map()
    
    # Calcular mortalidade por sexo
    obitos_por_sexo = obitos_pele.groupby("SEXO").size().reset_index(name="QUANTIDADE")
    obitos_por_sexo["SEXO_NOME"] = obitos_por_sexo["SEXO"].map(sexo_map)
    
    # Calcular mortalidade por raça/cor
    obitos_por_raca = obitos_pele.groupby("RACACOR").size().reset_index(name="QUANTIDADE")
    obitos_por_raca["RACA_NOME"] = obitos_por_raca["RACACOR"].map(raca_map)
    
    # Calcular mortalidade por estado
    obitos_por_estado = obitos_pele.groupby("ESTADRES").size().reset_index(name="QUANTIDADE")
    obitos_por_estado = obitos_por_estado.rename(columns={"ESTADRES": "ESTADO"})
    
    # Layout com duas colunas
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de mortalidade por sexo
        st.plotly_chart(
            criar_grafico_pizza(
                obitos_por_sexo, 
                "SEXO_NOME", 
                f"Mortalidade por Sexo ({ano_selecionado})"
            ),
            use_container_width=True
        )
    
    with col2:
        # Gráfico de mortalidade por raça/cor
        st.plotly_chart(
            criar_grafico_pizza(
                obitos_por_raca, 
                "RACA_NOME", 
                f"Mortalidade por Raça/Cor ({ano_selecionado})"
            ),
            use_container_width=True
        )
    
    # Gráfico de mortalidade por estado em uma linha separada
    st.plotly_chart(
        criar_grafico_barras(
            obitos_por_estado, 
            "ESTADO", 
            "QUANTIDADE", 
            f"Mortalidade por Estado ({ano_selecionado})"
        ),
        use_container_width=True
    )
    
    # Mostrar tabelas se a opção estiver habilitada
    if mostrar_tabelas:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### Tabela por Sexo")
            st.dataframe(obitos_por_sexo[["SEXO_NOME", "QUANTIDADE"]])
        
        with col2:
            st.markdown("### Tabela por Raça/Cor")
            st.dataframe(obitos_por_raca[["RACA_NOME", "QUANTIDADE"]])
        
        st.markdown("### Tabela por Estado")
        st.dataframe(obitos_por_estado)

def mostrar_tempos_medios(dados, ano_selecionado, mostrar_tabelas=False):
    """Exibe a seção de análise de tempos médios entre diagnóstico, tratamento e óbito"""
    st.markdown("## ⏱️ Análise de Tempos Médios")
    
    # Obter dados do câncer de pele
    data_pele = dados.get('data_pele', pd.DataFrame())
    
    # Título da seção
    st.subheader(f"Tempos Médios - {ano_selecionado}")
    
    # Criar colunas para organizar os cards de métricas
    col1, col2 = st.columns(2)
    
    with col1:
        # 1. Médias de Tempo do primeiro diagnóstico até início tratamento
        st.markdown("### Tempo até início do tratamento")
        
        # Calculando as diferenças de datas entre DTDIAGNO e DATAINITRT
        data_pele["DIFF_DTDIAGNO_DATAINITRT"] = data_pele.apply(
            lambda row: calcular_diferenca(
                row["DTDIAGNO"].strftime('%d/%m/%Y') if pd.notna(row["DTDIAGNO"]) else None, 
                row["DATAINITRT"].strftime('%d/%m/%Y') if pd.notna(row["DATAINITRT"]) else None
            ), 
            axis=1
        )
        
        # Filtrar valores válidos para calcular as médias (remover NaN)
        tempos_tratamento = data_pele["DIFF_DTDIAGNO_DATAINITRT"].dropna()
        media_tempo_initr = tempos_tratamento.mean()
        
        # Métricas
        st.metric(
            "Média de tempo entre diagnóstico e início do tratamento", 
            f"{media_tempo_initr:.2f} dias"
        )
        
        # Estatísticas adicionais se houver dados
        if len(tempos_tratamento) > 0:
            st.markdown(f"""
            - **Mediana**: {tempos_tratamento.median():.1f} dias
            - **Mínimo**: {tempos_tratamento.min():.1f} dias 
            - **Máximo**: {tempos_tratamento.max():.1f} dias
            - **Número de casos**: {len(tempos_tratamento)} pacientes
            """)
    
    with col2:
        # 2. Médias de Tempo do primeiro diagnóstico até óbito
        st.markdown("### Tempo até óbito")
        
        # Calculando as diferenças de datas entre DTDIAGNO e DATAOBITO
        data_pele["DIFF_DTDIAGNO_DATAOBITO"] = data_pele.apply(
            lambda row: calcular_diferenca(
                row["DTDIAGNO"].strftime('%d/%m/%Y') if pd.notna(row["DTDIAGNO"]) else None, 
                row["DATAOBITO"].strftime('%d/%m/%Y') if pd.notna(row["DATAOBITO"]) else None
            ), 
            axis=1
        )
        
        # Filtrar valores válidos para calcular as médias (remover NaN)
        tempos_obito = data_pele["DIFF_DTDIAGNO_DATAOBITO"].dropna()
        media_tempo_obito = tempos_obito.mean()
        
        # Métricas
        st.metric(
            "Média de tempo entre diagnóstico e óbito", 
            f"{media_tempo_obito:.2f} dias"
        )
        
        # Estatísticas adicionais se houver dados
        if len(tempos_obito) > 0:
            st.markdown(f"""
            - **Mediana**: {tempos_obito.median():.1f} dias
            - **Mínimo**: {tempos_obito.min():.1f} dias 
            - **Máximo**: {tempos_obito.max():.1f} dias
            - **Número de óbitos**: {len(tempos_obito)} pacientes
            """)
    
    # Histograma de distribuição dos tempos (se houver dados suficientes)
    if len(tempos_tratamento) > 10 or len(tempos_obito) > 10:
        st.subheader("Distribuição dos Tempos")
        
        col1, col2 = st.columns(2)
        
        # Histograma para tempo até tratamento
        if len(tempos_tratamento) > 10:
            with col1:
                fig_tempo_tratamento = px.histogram(
                    data_pele.dropna(subset=["DIFF_DTDIAGNO_DATAINITRT"]), 
                    x="DIFF_DTDIAGNO_DATAINITRT",
                    nbins=20,
                    title=f"Distribuição do Tempo até Início do Tratamento ({ano_selecionado})"
                )
                fig_tempo_tratamento.update_layout(
                    xaxis_title="Dias entre diagnóstico e início do tratamento",
                    yaxis_title="Número de pacientes"
                )
                st.plotly_chart(fig_tempo_tratamento, use_container_width=True)
        
        # Histograma para tempo até óbito
        if len(tempos_obito) > 10:
            with col2:
                fig_tempo_obito = px.histogram(
                    data_pele.dropna(subset=["DIFF_DTDIAGNO_DATAOBITO"]), 
                    x="DIFF_DTDIAGNO_DATAOBITO",
                    nbins=20,
                    title=f"Distribuição do Tempo até Óbito ({ano_selecionado})"
                )
                fig_tempo_obito.update_layout(
                    xaxis_title="Dias entre diagnóstico e óbito",
                    yaxis_title="Número de pacientes"
                )
                st.plotly_chart(fig_tempo_obito, use_container_width=True)
    
    # Mostrar tabelas detalhadas se a opção estiver habilitada
    if mostrar_tabelas:
        st.subheader("Dados Detalhados")
        
        # Criar dataframe com informações relevantes
        colunas_relevantes = ["NUMDOC", "DTDIAGNO", "DATAINITRT", "DATAOBITO", 
                             "DIFF_DTDIAGNO_DATAINITRT", "DIFF_DTDIAGNO_DATAOBITO"]
        
        dados_tempos = data_pele[colunas_relevantes].copy()
        
        # Formatar as datas para exibição
        for col in ["DTDIAGNO", "DATAINITRT", "DATAOBITO"]:
            dados_tempos[col] = dados_tempos[col].dt.strftime('%d/%m/%Y')
        
        # Exibir tabela
        st.dataframe(dados_tempos) 