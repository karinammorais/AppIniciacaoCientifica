# Manual para Continuação do Projeto com Nova Base de Dados

Este manual explica como adaptar este dashboard para análise de outros tipos de câncer ou bases de dados similares.

## 1. Requisitos da Base de Dados

### 1.1 Formato do Arquivo
- Formato: Excel (.xlsx)
- Nome do arquivo: Deve conter o ano dos dados (exemplo: `inCA_2021.xlsx`)

### 1.2 Campos Obrigatórios
A base de dados deve conter os seguintes campos (metadados):

| Campo | Descrição | Formato | Valores Possíveis |
|-------|-----------|---------|------------------|
| DTDIAGNO | Data do diagnóstico | Data (DD/MM/AAAA) | Data válida |
| TOPOGRAF | Código CID do câncer | Texto | C43 (Melanoma), C44 (Outros cânceres de pele) |
| SEXO | Sexo do paciente | Texto | M (Masculino), F (Feminino) |
| IDADE | Idade do paciente | Número inteiro | 0-120 |
| RACACOR | Raça/Cor do paciente | Texto | 1 (Branca), 2 (Preta), 3 (Parda), 4 (Amarela), 5 (Indígena) |
| UF | Estado de residência | Texto | Siglas dos estados brasileiros (SP, RJ, etc.) |
| INSTRUC | Nível de instrução | Texto | 1 (Nenhuma), 2 (Fundamental incompleto), 3 (Fundamental completo), 4 (Médio), 5 (Superior) |
| LOUCTUPRI | Localização do tumor primário | Texto | Códigos específicos de localização anatômica |
| DATAINITRT | Data de início do tratamento | Data (DD/MM/AAAA) | Data válida |
| DATAOBITO | Data do óbito (se aplicável) | Data (DD/MM/AAAA) | Data válida |
| DIAGNOST | Método diagnóstico | Texto | 0 (Sem confirmação), 1 (Histopatológico), 4 (Clínico), 5 (Imagem) |
| TPOTRTPRI | Tipo do primeiro tratamento | Texto | 00 (Sem tratamento), 01 (Cirurgia), 02 (Quimioterapia), 03 (Radioterapia) |
| ESTDTRAT | Estadiamento ao diagnóstico | Texto | 1 (I), 2 (II), 3 (III), 4 (IV) |
| METASTASE | Presença de metástase | Texto | 0 (Não), 1 (Sim) |
| RECIDIVA | Recidiva da doença | Texto | 0 (Não), 1 (Sim) |

### 1.3 Formatação dos Dados
- Certifique-se que as datas estejam em formato consistente
- Campos vazios devem ser preenchidos com NA ou deixados em branco
- Códigos CID devem seguir o padrão internacional
- Valores categóricos devem ser padronizados

### 1.4 Indicadores Calculados
O sistema calcula automaticamente os seguintes indicadores epidemiológicos:

#### 1.4.1 Indicadores de Incidência
- **Taxa de Incidência Bruta**: Número de casos novos/População total x 100.000
- **Taxa de Incidência Específica por Idade**: Casos em cada faixa etária/População da faixa x 100.000
- **Taxa de Incidência Específica por Sexo**: Casos por sexo/População por sexo x 100.000
- **Taxa de Incidência Padronizada**: Ajustada pela população padrão mundial

#### 1.4.2 Indicadores de Mortalidade
- **Taxa de Mortalidade**: Número de óbitos/População total x 100.000
- **Taxa de Letalidade**: Número de óbitos/Número de casos x 100
- **Sobrevida em 5 anos**: Percentual de pacientes vivos após 5 anos do diagnóstico
- **Mortalidade Proporcional**: Óbitos por câncer de pele/Total de óbitos x 100

#### 1.4.3 Indicadores de Qualidade da Atenção
- **Tempo até Primeiro Tratamento**: Média de dias entre diagnóstico e início do tratamento
- **Taxa de Diagnóstico Precoce**: Casos diagnosticados em estádios I e II/Total de casos
- **Taxa de Confirmação Histopatológica**: Casos com confirmação histopatológica/Total de casos
- **Taxa de Abandono**: Casos sem seguimento/Total de casos

#### 1.4.4 Indicadores Demográficos
- **Distribuição por Faixa Etária**: Percentual de casos por grupo etário
- **Distribuição por Sexo**: Razão entre casos masculinos e femininos
- **Distribuição por Raça/Cor**: Percentual de casos por categoria racial
- **Distribuição Geográfica**: Casos por UF e região

### 1.5 Visualizações Disponíveis
O sistema gera automaticamente as seguintes visualizações:

1. **Mapas Coropléticos**
   - Distribuição espacial dos casos
   - Taxas de incidência por estado
   - Taxas de mortalidade por região

2. **Gráficos Temporais**
   - Tendência de casos ao longo do tempo
   - Variação sazonal
   - Evolução das taxas de mortalidade

3. **Gráficos de Distribuição**
   - Pirâmide etária dos casos
   - Distribuição por sexo e raça
   - Boxplots de idade por tipo de câncer

4. **Indicadores de Qualidade**
   - Tempo até tratamento
   - Proporção de diagnóstico precoce
   - Taxa de confirmação diagnóstica

## 2. Adaptando o Código

### 2.1 Alterações em metricas.py
1. Atualize os filtros de TOPOGRAF para o novo tipo de câncer:
```python
# Exemplo para câncer de mama
df_cancer = df[df["TOPOGRAF"].str.match("C50", na=False)]
```

### 2.2 Atualização de Visualizações (visualizations.py)
1. Ajuste os títulos e legendas dos gráficos
2. Adapte as escalas de cores se necessário
3. Modifique os textos explicativos

### 2.3 Configuração da Interface (componentes.py)
1. Atualize os títulos da aplicação
2. Modifique os textos descritivos
3. Ajuste os filtros conforme necessidade

## 3. População de Referência

Para cálculos de taxas e indicadores, você precisará:
1. Dados populacionais do IBGE para o período
2. Distribuição populacional por faixa etária
3. Dados demográficos da região de interesse

## 4. Testes e Validação

1. Teste a importação dos dados
2. Verifique os cálculos de indicadores
3. Valide as visualizações
4. Compare com outras fontes oficiais

## 5. Documentação

1. Atualize o README.md com as especificações do novo tipo de câncer
2. Documente as alterações realizadas
3. Atualize os exemplos de visualizações
4. Registre as fontes dos dados

## 6. Possíveis Desafios

- Diferenças na codificação CID
- Variações nos padrões de registro
- Particularidades epidemiológicas do novo tipo de câncer
- Necessidade de novos indicadores específicos

## 7. Suporte e Recursos

- Consulte a documentação do INCA
- Verifique diretrizes epidemiológicas
- Utilize recursos do DataSUS
- Considere literatura científica específica
