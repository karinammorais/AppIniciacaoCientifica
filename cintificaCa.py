import streamlit as st
import pandas as pd
from streamlit_lottie import st_lottie
import time

# Importar módulos personalizados
from utils import extrair_ano_do_arquivo, processar_dataframe
from metricas import (
    calcular_indicadores_incidencia,
    calcular_indicadores_mortalidade,
    calcular_tempos_medios,
    calcular_perfil_demografico
)
from styles import aplicar_estilos
from componentes import mostrar_sidebar, mostrar_header, mostrar_secao_upload
from tabs import (
    mostrar_tab_incidencia,
    mostrar_tab_mortalidade,
    mostrar_tab_tempos,
    mostrar_tab_perfil
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
    """Processa os arquivos carregados"""
    dados_por_ano = {}
    anos_disponiveis = []
    
    for file in uploaded_files:
        ano = extrair_ano_do_arquivo(file.name)
        if ano:
            try:
                df = pd.read_excel(file)
                df = processar_dataframe(df)
                dados_por_ano[ano] = df
                anos_disponiveis.append(ano)
            except Exception as e:
                st.error(f"Erro ao processar arquivo {file.name}: {e}")
                continue
    
    if not anos_disponiveis:
        st.warning("Não foi possível identificar o ano nos nomes dos arquivos.")
        return False
    
    anos_disponiveis.sort()
    st.session_state.dados_carregados = True
    st.session_state.dados_por_ano = dados_por_ano
    st.session_state.anos_disponiveis = anos_disponiveis
    
    return True

def main():
    """Função principal do dashboard"""
    mostrar_header()
    
    if not st.session_state.dados_carregados:
        dados_carregados = mostrar_secao_upload(processar_arquivos)
        # Logos institucionais
        col1, col2, col3 = st.columns([1,1,1])
        with col1:
            st.image("logo_sus.png", width=160)
        with col2:
            st.image("logo_inca.png", width=160)
        with col3:
            st.image("logo_uscs.png", width=160)
        # Rodapé sempre visível (agora abaixo dos logos)
        st.markdown("""
        <div style="text-align: center; opacity: 0.7; padding: 20px;">
            <p>Dashboard de Análise Epidemiológica - Versão 2.0</p>
            <p>© 2025 - Todos os direitos reservados</p>
        </div>
        """, unsafe_allow_html=True)
        if dados_carregados:
            st.rerun()
        return
    
    # Mostrar sidebar e obter seleção de ano e estado
    anos_selecionados, estados_selecionados = mostrar_sidebar(
        st.session_state.dados_por_ano,
        st.session_state.anos_disponiveis,
        estados_disponiveis=["SP", "RJ", "MG"]  # Exemplo de estados disponíveis
    )

    # Obter dados dos anos selecionados
    if anos_selecionados:
        dfs_selecionados = [st.session_state.dados_por_ano[ano] for ano in anos_selecionados]
        df = pd.concat(dfs_selecionados)
    else:
        st.warning("Nenhum ano foi selecionado. Por favor, selecione pelo menos um ano.")
        return
    
    # Calcular indicadores
    indicadores_incidencia = calcular_indicadores_incidencia(df, 211000000, estados_selecionados)  # valor padrão
    indicadores_mortalidade = calcular_indicadores_mortalidade(df, estados_selecionados)
    indicadores_tempos = calcular_tempos_medios(df)
    indicadores_perfil = calcular_perfil_demografico(df)
    
    # Criar abas na ordem correta
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Incidência",
        "Mortalidade",
        "Letalidade",
        "Perfil",
        "Tempo"
    ])
    # Conteúdo das abas
    with tab1:
        mostrar_tab_incidencia(indicadores_incidencia)
    with tab2:
        mostrar_tab_mortalidade(indicadores_mortalidade)
    with tab3:
        from tabs import mostrar_tab_letalidade
        mostrar_tab_letalidade(indicadores_mortalidade)
    with tab4:
        mostrar_tab_perfil(indicadores_perfil)
    with tab5:
        from tabs import mostrar_tab_tempos
        mostrar_tab_tempos(indicadores_tempos)
    # Rodapé sempre visível (apenas texto)
    st.markdown("""
    <div style="text-align: center; opacity: 0.7; padding: 20px;">
        <p>Dashboard de Análise Epidemiológica - Versão 2.0</p>
        <p>© 2025 - Todos os direitos reservados</p>
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
