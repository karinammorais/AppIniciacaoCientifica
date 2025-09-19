import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from fpdf import FPDF
import base64
from io import BytesIO
import pandas as pd

# Paleta de cores moderna e vibrante
PALETA_CORES = [
    "#4361EE", "#3A0CA3", "#7209B7", "#F72585",
    "#4CC9F0", "#4895EF", "#560BAD", "#B5179E",
    "#3F37C9", "#4361EE", "#4895EF", "#4CC9F0"
]

PALETA_DIVERGENTE = [
    "#4CC9F0", "#4895EF", "#4361EE", "#3A0CA3", "#480CA8", 
    "#560BAD", "#7209B7", "#B5179E", "#F72585"
]

# Função para criar gráficos com estilo moderno
def aplicar_estilo_moderno(fig):
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_family="Arial, sans-serif",
        font_color="#FFFFFF",
        title_font_size=20,
        title_font_family="Arial, sans-serif",
        title_font_color="#FFFFFF",
        legend_title_font_color="#FFFFFF",
        legend_font_color="#FFFFFF",
        margin=dict(l=10, r=10, t=35, b=10),
    )
    
    # Atualizar eixos
    fig.update_xaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='rgba(255,255,255,0.1)',
        showline=True,
        linewidth=0.5,
        linecolor='rgba(255,255,255,0.5)'
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=0.5,
        gridcolor='rgba(255,255,255,0.1)',
        showline=True,
        linewidth=0.5,
        linecolor='rgba(255,255,255,0.5)'
    )
    
    return fig

def criar_grafico_pizza(dados, coluna, titulo, estados_selecionados=None):
    # Filtrar por estados selecionados, se aplicável
    if estados_selecionados:
        dados = dados[dados['UF'].isin(estados_selecionados)]

    # Se os dados vierem como Series, converter para DataFrame
    if isinstance(dados, pd.Series):
        df = dados.reset_index()
        if 'count' in df.columns:  # caso de value_counts()
            df.columns = [coluna, 'QUANTIDADE']
        else:
            df.columns = [coluna, 'QUANTIDADE']
    else:
        df = dados.copy()
        if 'count' in df.columns:
            df = df.rename(columns={'count': 'QUANTIDADE'})

    fig = px.pie(
        df, 
        names=coluna, 
        values='QUANTIDADE', 
        title=titulo,
        color_discrete_sequence=PALETA_CORES
    )

    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        marker=dict(line=dict(color='#1E1E1E', width=1))
    )

    fig = aplicar_estilo_moderno(fig)

    # Adicionar hoverlabels mais bonitos
    fig.update_traces(
        hoverinfo='label+percent+value',
        hovertemplate='<b>%{label}</b><br>Quantidade: %{value}<br>Percentual: %{percent}<extra></extra>'
    )

    return fig

def criar_grafico_barras(dados, x, y, titulo, estados_selecionados=None):
    # Filtrar por estados selecionados, se aplicável
    if estados_selecionados:
        dados = dados[dados['UF'].isin(estados_selecionados)]

    # Se os dados vierem como Series, converter para DataFrame
    if isinstance(dados, pd.Series):
        df = dados.reset_index()
        if 'count' in df.columns:  # caso de value_counts()
            df.columns = [x, 'QUANTIDADE']
            y = 'QUANTIDADE'
        elif y == 0:  # Caso especial quando y é o valor da contagem
            df.columns = [x, 'QUANTIDADE']
            y = 'QUANTIDADE'
    else:
        df = dados.copy()
        if 'count' in df.columns:
            df = df.rename(columns={'count': 'QUANTIDADE'})
            y = 'QUANTIDADE'

    fig = px.bar(
        df, 
        x=x, 
        y=y, 
        title=titulo,
        color_discrete_sequence=PALETA_CORES
    )

    fig = aplicar_estilo_moderno(fig)

    # Melhores hoverlabels
    fig.update_traces(
        hovertemplate='<b>%{x}</b><br>Quantidade: %{y}<extra></extra>',
        marker_line_width=0
    )

    return fig

def criar_grafico_linha(df, x, y, titulo):
    fig = px.line(
        df, 
        x=x, 
        y=y, 
        title=titulo, 
        markers=True,
        color_discrete_sequence=PALETA_CORES
    )
    
    fig = aplicar_estilo_moderno(fig)
    
    # Adicionar pontos para melhor visualização
    fig.update_traces(
        mode='lines+markers',
        marker=dict(size=8),
        line=dict(width=3),
        hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'
    )
    
    return fig

def criar_mapa_calor(df, titulo):
    # Criar mapa de calor por estado
    fig = px.choropleth(
        df,
        locations='ESTADO',
        locationmode='brazil states',
        color='QUANTIDADE',
        scope="south america",
        title=titulo,
        color_continuous_scale=PALETA_DIVERGENTE
    )
    
    fig = aplicar_estilo_moderno(fig)
    
    fig.update_geos(
        showcountries=True,
        showcoastlines=True,
        showland=True,
        fitbounds="locations",
        landcolor="rgba(60, 60, 60, 1)",
        countrycolor="rgba(255, 255, 255, 0.5)",
    )
    
    return fig

def criar_grafico_combinado_idade_sexo(df_idade, df_sexo, ano_selecionado):
    # Criar subplots: 1 row, 2 cols
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=(
            f"Distribuição por Idade ({ano_selecionado})", 
            f"Distribuição por Sexo ({ano_selecionado})"
        ),
        specs=[[{"type": "bar"}, {"type": "pie"}]]
    )

    # Adicionar gráfico de barras
    fig.add_trace(
        go.Bar(
            x=df_idade["IDADE"], 
            y=df_idade["QUANTIDADE"],
            marker_color=PALETA_CORES[0],
            name="Idade"
        ),
        row=1, col=1
    )

    # Adicionar gráfico de pizza
    fig.add_trace(
        go.Pie(
            labels=df_sexo["SEXO_NOME"], 
            values=df_sexo["QUANTIDADE"],
            marker=dict(colors=PALETA_CORES),
            name="Sexo",
            textinfo='percent+label'
        ),
        row=1, col=2
    )

    # Atualizar layout
    fig.update_layout(
        height=500,
        title_text=f"Análise Demográfica - {ano_selecionado}",
        showlegend=False
    )
    
    fig = aplicar_estilo_moderno(fig)
    
    return fig

def criar_card_estatistico(titulo, valor, subtexto="", delta=None, delta_color="normal"):
    """Cria um container estilizado como card para métricas estatísticas"""
    
    st.markdown(f"""
    <div style="
        background-color: rgba(49, 51, 63, 0.7);
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid {PALETA_CORES[0]};
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    ">
        <h5 style="margin: 0; color: #cccccc; font-size: 0.9rem;">{titulo}</h5>
        <h3 style="margin: 10px 0; font-size: 1.8rem; font-weight: bold;">{valor}</h3>
        <p style="margin: 0; font-size: 0.8rem; color: #aaaaaa;">{subtexto}</p>
    </div>
    """, unsafe_allow_html=True)

# Função para gerar PDF
def gerar_pdf(figs, titulos, metricas, ano_selecionado):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Relatório de Análise de Câncer de Pele - {ano_selecionado}", ln=True, align='C')
    
    # Adicionar métricas
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Métricas Principais:", ln=True)
    for chave, valor in metricas.items():
        pdf.cell(200, 10, txt=f"{chave}: {valor}", ln=True)
    
    # Adicionar gráficos
    for fig, titulo in zip(figs, titulos):
        img_bytes = fig.to_image(format="png")
        pdf.image(BytesIO(img_bytes), x=10, y=None, w=180)
        pdf.cell(200, 10, txt=titulo, ln=True, align='C')
    
    # Retornar PDF como base64
    pdf_output = BytesIO()
    pdf.output(pdf_output)
    pdf_data = base64.b64encode(pdf_output.getvalue()).decode('utf-8')
    return pdf_data