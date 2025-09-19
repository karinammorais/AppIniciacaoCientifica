import streamlit as st
import plotly.express as px
from visualizations import criar_grafico_pizza, criar_grafico_barras, criar_card_estatistico

def mostrar_tab_letalidade(indicadores_mortalidade):
    """Aba Letalidade"""
    st.header("Letalidade")

    # Log temporário para validação dentro de um elemento expansível
    with st.expander("Valores calculados para validação"):
        st.write(indicadores_mortalidade)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Letalidade do câncer de pele (C43, em %)",
            f"{indicadores_mortalidade['letalidade_c43'] * 100:.2f}%"
        )

    with col2:
        st.metric(
            "Letalidade do câncer de pele (C44, em %)",
            f"{indicadores_mortalidade['letalidade_c44'] * 100:.2f}%"
        )

def mostrar_tab_incidencia(indicadores_incidencia):
    """Tab para indicadores de incidência"""
    st.header("Indicadores de Incidência")

    # Log temporário para validação dentro de um elemento expansível
    with st.expander("Valores calculados para validação"):
        st.write(indicadores_incidencia)

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Taxa de Incidência Geral (em %)",
            f"{indicadores_incidencia['taxa_incidencia_geral'] * 100:.2f}%"
        )

    with col2:
        st.metric(
            "Taxa de Incidência de Câncer de Pele (c43+c44, em %)",
            f"{indicadores_incidencia['taxa_incidencia_pele'] * 100:.2f}%"
        )

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Taxa de Incidência de Câncer de Pele (c43, em %)",
            f"{indicadores_incidencia['taxa_incidencia_c43'] * 100:.2f}%"
        )

    with col4:
        st.metric(
            "Taxa de Incidência de Câncer de Pele (c44, em %)",
            f"{indicadores_incidencia['taxa_incidencia_c44'] * 100:.2f}%"
        )

def mostrar_tab_mortalidade(indicadores_mortalidade):
    """Tab para indicadores de mortalidade"""
    st.header("Mortalidade")

    # Filtros
    idade = st.selectbox("Selecione a faixa etária", indicadores_mortalidade['faixas_etarias'])
    estado = st.selectbox("Selecione o estado", indicadores_mortalidade['estados'])
    tipo_cancer = st.selectbox("Selecione o tipo de câncer", ["C33", "C44", "Todos"])

    # Exibir métricas gerais
    st.metric("Mortalidade total por câncer", indicadores_mortalidade['obitos_total'])
    st.metric("Mortalidade por câncer de pele (C43 + C44)", indicadores_mortalidade['obitos_pele'])

    # Gráfico por sexo
    st.markdown("<h4 style='color:#fff;'>Por sexo</h4>", unsafe_allow_html=True)
    fig_sexo = criar_grafico_pizza(
        indicadores_mortalidade['mortalidade_sexo'],
        'SEXO',
        'Mortalidade por Sexo'
    )
    st.plotly_chart(fig_sexo)

    # Gráfico de coluna para C43 e C44
    st.markdown("<h4 style='color:#fff;'>Mortalidade por Câncer de Pele (C43 e C44)</h4>", unsafe_allow_html=True)
    fig_c43_c44 = criar_grafico_barras(
        indicadores_mortalidade['mortalidade_c43_c44'].reset_index(),
        'TOPOGRAF',
        0,
        'Mortalidade por Câncer de Pele (C43 e C44)'
    )
    st.plotly_chart(fig_c43_c44)

def mostrar_tab_tempos(indicadores_tempos):
    """Tab para tempos médios"""
    st.header("Tempo")

    # Adicionar logs para validação
    print("Log: Tempo médio até tratamento (dias):", indicadores_tempos['tempo_ate_tratamento'])
    print("Log: Tempo médio até óbito (dias):", indicadores_tempos['tempo_ate_obito'])

    # Converter tempos médios para dias e horas
    tempo_tratamento_dias = int(indicadores_tempos['tempo_ate_tratamento'])
    tempo_tratamento_horas = int((indicadores_tempos['tempo_ate_tratamento'] % 1) * 24)
    tempo_obito_dias = int(indicadores_tempos['tempo_ate_obito'])
    tempo_obito_horas = int((indicadores_tempos['tempo_ate_obito'] % 1) * 24)

    # Logs detalhados
    print(f"Tempo médio até tratamento: {tempo_tratamento_dias} dias e {tempo_tratamento_horas} horas")
    print(f"Tempo médio até óbito: {tempo_obito_dias} dias e {tempo_obito_horas} horas")

    # Exibir tempos médios em dias e horas
    st.metric(
        "Tempo médio do diagnóstico até o início do tratamento",
        f"{tempo_tratamento_dias} dias e {tempo_tratamento_horas} horas"
    )
    st.metric(
        "Tempo médio do diagnóstico até o óbito",
        f"{tempo_obito_dias} dias e {tempo_obito_horas} horas"
    )

def mostrar_tab_perfil(indicadores_perfil):
    """Tab para perfil demográfico"""
    st.header("Mapeamento de Perfil de Pacientes")
    st.subheader("Distribuição por raça/cor")
    fig_raca = criar_grafico_pizza(
        indicadores_perfil['raca'],
        'RACACOR',
        'Distribuição por Raça/Cor'
    )
    st.plotly_chart(fig_raca)
    st.subheader("Distribuição por idade")
    fig_idade = criar_grafico_barras(
        indicadores_perfil['idade'],
        'IDADE',
        0,
        'Distribuição por Idade'
    )
    st.plotly_chart(fig_idade)
    st.subheader("Distribuição por sexo")
    fig_sexo = criar_grafico_pizza(
        indicadores_perfil['sexo'],
        'SEXO',
        'Distribuição por Sexo'
    )
    st.plotly_chart(fig_sexo)
    st.subheader("Distribuição por estado")
    fig_estado = criar_grafico_barras(
        indicadores_perfil['estado'],
        'UF',
        0,
        'Distribuição por Estado'
    )
    st.plotly_chart(fig_estado)
    st.subheader("Distribuição por grau de instrução")
    fig_instrucao = criar_grafico_barras(
        indicadores_perfil['instrucao'],
        'INSTRUC',
        0,
        'Distribuição por Grau de Instrução'
    )
    st.plotly_chart(fig_instrucao)
    st.subheader("Localização do Tumor")
    fig_localizacao = criar_grafico_barras(
        indicadores_perfil['localizacao'],
        'LOUCTUPRI',
        0,
        'Localização do Tumor'
    )
    st.plotly_chart(fig_localizacao)
