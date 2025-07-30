def mostrar_tab_letalidade(indicadores_mortalidade):
    """Aba Letalidade"""
    st.header("Letalidade")
    st.metric("Letalidade do câncer de pele (%)", f"{indicadores_mortalidade['letalidade']:.2f}")
import streamlit as st
import plotly.express as px
from visualizations import criar_grafico_pizza, criar_grafico_barras, criar_card_estatistico

def mostrar_tab_incidencia(indicadores_incidencia):
    """Tab para indicadores de incidência"""
    st.header("Indicadores de Incidência")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Taxa de Incidência Geral (por 100.000 habitantes)",
            f"{indicadores_incidencia['taxa_incidencia_geral']:.2f}"
        )
    
    with col2:
        st.metric(
            "Taxa de Incidência de Câncer de Pele (por 100.000 habitantes)",
            f"{indicadores_incidencia['taxa_incidencia_pele']:.2f}"
        )

def mostrar_tab_mortalidade(indicadores_mortalidade):
    """Tab para indicadores de mortalidade"""
    st.header("Mortalidade")
    st.metric("Mortalidade total por câncer", indicadores_mortalidade['obitos_total'])
    st.metric("Mortalidade por câncer de pele (C43 + C44)", indicadores_mortalidade['obitos_pele'])
    st.markdown("<h4 style='color:#fff;'>Por sexo</h4>", unsafe_allow_html=True)
    fig_sexo = criar_grafico_pizza(
        indicadores_mortalidade['mortalidade_sexo'],
        'SEXO',
        'Mortalidade por Sexo'
    )
    st.plotly_chart(fig_sexo)

def mostrar_tab_tempos(indicadores_tempos):
    """Tab para tempos médios"""
    st.header("Tempo")
    st.metric(
        "Tempo médio do diagnóstico até o início do tratamento (dias)",
        f"{indicadores_tempos['tempo_ate_tratamento']:.1f}"
    )
    st.metric(
        "Tempo médio do diagnóstico até o óbito (dias)",
        f"{indicadores_tempos['tempo_ate_obito']:.1f}"
    )

def mostrar_tab_perfil(indicadores_perfil):
    """Tab para perfil demográfico"""
    st.header("Perfil")
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
    st.subheader("Parte do corpo mais afetada")
    fig_localizacao = criar_grafico_barras(
        indicadores_perfil['localizacao'],
        'LOUCTUPRI',
        0,
        'Parte do Corpo Mais Afetada'
    )
    st.plotly_chart(fig_localizacao)
    
    # Parte do corpo mais afetada
    st.subheader("Localização do Tumor")
    fig_local = criar_grafico_barras(
        indicadores_perfil['localizacao'],
        'LOUCTUPRI',
        0,
        'Localização do Tumor'
    )
    st.plotly_chart(fig_local)
