import streamlit as st

def aplicar_estilos():
    """Aplica estilos CSS personalizados para melhorar a interface do usuário"""
    
    # CSS personalizado para melhorar a aparência da aplicação
    st.markdown("""
    <style>
    /* Estilo geral */
    [data-testid="stAppViewContainer"] {
        background-color: #1E1E1E;
        color: #FFFFFF;
    }
    
    /* Cabeçalhos */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Arial', sans-serif;
        font-weight: 600;
        color: #FFFFFF;
    }
    
    h1 {
        margin-bottom: 2rem;
        font-size: 2.5rem;
        background: linear-gradient(90deg, #4361EE, #4CC9F0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }
    
    h2 {
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.8rem;
        color: #4CC9F0;
    }
    
    h3 {
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
        font-size: 1.4rem;
        color: #4895EF;
    }
    
    /* Containers */
    [data-testid="stVerticalBlock"] {
        padding: 0.5rem;
    }
    
    /* Cards e blocos de conteúdo */
    .card {
        padding: 1.5rem;
        border-radius: 10px;
        background-color: rgba(49, 51, 63, 0.7);
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 7px 10px rgba(0, 0, 0, 0.2);
    }
    
    /* Tabs estilizadas */
    .stTabs [data-baseweb="tab"] {
        font-size: 16px;
        padding: 10px 20px;
        background-color: rgba(67, 97, 238, 0.1);
        border-radius: 5px 5px 0 0;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(67, 97, 238, 0.2);
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(67, 97, 238, 0.3) !important;
        border-bottom: 2px solid #4361EE !important;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 5px;
    }
    
    .stTabs [data-baseweb="tab-panel"] {
        padding: 15px 10px;
        background-color: rgba(49, 51, 63, 0.4);
        border-radius: 0 5px 5px 5px;
    }
    
    /* Barra lateral */
    [data-testid="stSidebar"] {
        background-color: rgba(30, 30, 30, 0.9);
        box-shadow: 2px 0 5px rgba(0, 0, 0, 0.2);
        padding-top: 2rem;
    }
    
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3 {
        padding-left: 1rem;
        margin-bottom: 1.5rem;
    }
    
    /* Botões */
    .stButton>button {
        background-color: #4361EE;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #3A0CA3;
        box-shadow: 0 4px 10px rgba(58, 12, 163, 0.5);
        transform: translateY(-2px);
    }
    
    /* DataFrames/Tabelas */
    [data-testid="stTable"] {
        width: 100%;
        margin-bottom: 1.5rem;
    }
    
    [data-testid="stDataFrame"] {
        background-color: rgba(67, 97, 238, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    /* Métricas mais elegantes */
    [data-testid="stMetric"] {
        background-color: rgba(49, 51, 63, 0.7);
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
    }
    
    /* Animações sutis para carregamento */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fadeIn {
        animation: fadeIn 0.5s ease-out forwards;
    }
    
    /* Melhoria de layout para elementos responsivos */
    @media (max-width: 768px) {
        .responsive-columns > div {
            width: 100% !important;
            margin-bottom: 1rem;
        }
        
        h1 {
            font-size: 2rem;
        }
        
        h2 {
            font-size: 1.5rem;
        }
        
        h3 {
            font-size: 1.2rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

def card_container():
    """Retorna o HTML para encapsular elementos em um card estilizado"""
    return """
    <div class="card">
        {content}
    </div>
    """

def cria_animacao_entrada():
    """Aplica animação de entrada a componentes da página"""
    st.markdown("""
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const elements = document.querySelectorAll('[data-testid="stVerticalBlock"] > div');
            elements.forEach((el, index) => {
                el.classList.add('fadeIn');
                el.style.animationDelay = `${index * 0.1}s`;
            });
        });
    </script>
    """, unsafe_allow_html=True)

def exibir_loader():
    """Exibe um loader animado"""
    loader_html = """
    <div style="display: flex; justify-content: center; margin: 2rem 0;">
        <div style="
            width: 50px;
            height: 50px;
            border: 5px solid rgba(76, 201, 240, 0.3);
            border-radius: 50%;
            border-top-color: #4CC9F0;
            animation: spin 1s ease-in-out infinite;
        "></div>
    </div>
    <style>
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
    </style>
    """
    return loader_html 