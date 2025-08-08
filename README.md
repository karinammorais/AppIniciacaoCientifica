# Dashboard de Análise Epidemiológica - Câncer de Pele
## 📊 Estrutura do Projeto

```
AppIniciacaoCientifica/
├── cintificaCa.py          # Aplicação principal Streamlit
├── componentes.py          # Componentes da interface
├── metricas.py            # Cálculos de indicadores epidemiológicos
├── tabs.py                # Configuração das abas da interface
├── utils.py               # Funções utilitárias
├── visualizations.py      # Funções de visualização de dados
├── styles.py              # Estilos CSS personalizados
├── requirements.txt       # Dependências do projeto
├── README.md              # Documentação principal
├── manual_usuario.md      # Manual detalhado para usuários
├── manual_continuacao.md  # Guia para extensão do projeto
└── manual_criacao_zero.md # Tutorial para criar projeto similar
```o Projeto](https://img.shields.io/badge/Status-Em%20Desenvolvimento-brightgreen)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red)

## 📌 Visão Geral

Dashboard interativo para análise epidemiológica de casos de câncer de pele no Brasil, utilizando dados do Ministério da Saúde. Esta aplicação permite visualizar e analisar dados sobre incidência, mortalidade, distribuição demográfica e outras métricas relevantes para pesquisadores e profissionais de saúde.

## ✨ Funcionalidades

- **Indicadores Epidemiológicos**: Taxas de incidência, prevalência e letalidade
- **Análise Demográfica**: Distribuição por idade, sexo, raça/cor
- **Análise de Mortalidade**: Por estado, sexo, raça/cor e idade
- **Relatórios**: Geração de PDF com análises completas
- **Visualizações Interativas**: Gráficos e dashboards responsivos
- **Interface Moderna**: Design intuitivo e visual agradável

## 💻 Tecnologias Utilizadas

- **Python**: Linguagem base
- **Streamlit**: Framework para criação de aplicativos web
- **Pandas/NumPy**: Manipulação e análise de dados
- **Plotly**: Visualizações interativas
- **Streamlit-Lottie**: Animações modernas
- **Streamlit-Extras**: Componentes adicionais para melhor UX
- **FPDF**: Geração de relatórios em PDF

## 🚀 Como Executar

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/karinammorais/AppIniciacaoCientifica.git
   cd AppIniciacaoCientifica
   ```

2. **Crie um ambiente virtual**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação**:
   ```bash
   streamlit run app.py
   ```

5. **Acesse no navegador**:
   A aplicação estará disponível em `http://localhost:8501`

## 📁 Formato dos Dados

O sistema espera arquivos Excel (.xlsx) com os seguintes requisitos:
- O nome do arquivo deve conter o ano dos dados (ex: inCA_2021.xlsx)
- O arquivo deve conter colunas específicas (DTDIAGNO, LOCTUPRI, SEXO, etc.)

## 📊 Exemplos de Visualizações

- Distribuição de casos por estado (mapas de calor)
- Gráficos de pizza para distribuição por sexo e raça/cor
- Gráficos de barras para análise por idade
- Cards com métricas principais
- Relatórios em PDF para exportação

## 🔄 Atualizações Futuras

- [ ] Implementação de Machine Learning para previsões
- [ ] Adição de novas fontes de dados
- [ ] Comparações entre anos diferentes
- [ ] Visualizações geoespaciais avançadas
- [ ] Exportação de dados em outros formatos

## � Documentação Adicional

Para facilitar o uso e desenvolvimento do projeto, foram criados três manuais detalhados:

1. **[Manual do Usuário](manual_usuario.md)**: Guia completo sobre como utilizar todas as funcionalidades do dashboard, incluindo dicas de navegação, uso de filtros e geração de relatórios.

2. **[Manual de Continuação](manual_continuacao.md)**: Instruções detalhadas para adaptar este projeto para outros tipos de câncer ou bases de dados similares, incluindo requisitos de dados e passos para adaptação.

3. **[Manual de Criação do Zero](manual_criacao_zero.md)**: Tutorial passo a passo para criar um projeto similar desde o início, incluindo configuração do ambiente, estrutura do projeto e boas práticas.

## �📣 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias e correções. Consulte os manuais para entender melhor a estrutura do projeto.

## 📜 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.

---

Desenvolvido com ❤️ para análise de dados epidemiológicos 
