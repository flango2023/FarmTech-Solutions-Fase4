# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# FarmTech Solutions - Fase 4: Assistente Agrícola Inteligente

## Descrição do Projeto

Nesta última fase do FarmTech Solutions, eu usei Sistema de Inteligência Artificial aplicado ao agronegócio que utiliza Machine Learning supervisionado para prever variáveis críticas do campo e sugerir ações automatizadas de irrigação e manejo agrícola.

## Cultura Escolhida: SOJA

### Parâmetros de Predição:
- **Umidade do solo**: Previsão baseada em histórico
- **pH do solo**: Estimativa de variação temporal
- **Rendimento esperado**: Cálculo baseado em condições ambientais
- **Volume de irrigação**: Recomendação automatizada

## Componentes do Sistema

### Machine Learning:
- **Scikit-Learn**: Modelos de regressão linear, múltipla e não-linear
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Operações matemáticas e estatísticas
- **Matplotlib/Plotly**: Visualizações e gráficos

### Dashboard Interativo:
- **Streamlit**: Interface web para gestores agrícolas
- **Métricas em tempo real**: MAE, MSE, RMSE, R²
- **Gráficos de correlação**: Análise visual de variáveis
- **Previsões interativas**: Entrada de parâmetros customizados

## Estrutura de Arquivos

```
FarmTech-Solutions-Fase4/
├── README.md
├── parte1/
│   ├── ml_pipeline.py
│   ├── dashboard_streamlit.py
│   └── requirements.txt
├── parte2/
│   ├── modelos_preditivos.py
│   ├── avaliacao_modelos.py
│   └── recomendacoes.py
├── data/
│   ├── dados_treinamento.csv
│   └── dados_teste.csv
├── models/
│   └── modelos_treinados/
├── docs/
│   └── relatorio_fase4.md
└── screenshots/
```

## Modelos Implementados

### 1. Regressão Linear Simples
- Previsão de umidade baseada em temperatura
- Estimativa de pH baseada em nutrientes

### 2. Regressão Múltipla
- Rendimento baseado em múltiplas variáveis
- Volume de irrigação considerando clima e solo

### 3. Regressão Não-Linear
- Modelos polinomiais para relações complexas
- Random Forest para previsões avançadas

## Métricas de Avaliação

- **MAE (Mean Absolute Error)**: Erro médio absoluto
- **MSE (Mean Squared Error)**: Erro quadrático médio
- **RMSE (Root Mean Squared Error)**: Raiz do erro quadrático médio
- **R² (Coefficient of Determination)**: Coeficiente de determinação

## Como Executar

### Parte 1: Pipeline Básico
```bash
cd parte1
pip install -r requirements.txt
python ml_pipeline.py
streamlit run dashboard_streamlit.py
```

### Parte 2: Sistema Completo (RECOMENDADO)
```bash
cd parte2
pip3 install scikit-learn pandas numpy matplotlib seaborn plotly streamlit joblib
python3 executar_parte2.py
streamlit run app_streamlit_completo.py
```

### Acessar Interface
- URL: http://localhost:8501
- Interface completa com todos os modelos de ML

## Funcionalidades do Dashboard

### Visualizações:
- Gráficos de correlação entre variáveis
- Tendências temporais de umidade e pH
- Distribuição de nutrientes NPK
- Histórico de irrigações

### Previsões Interativas:
- Entrada de parâmetros customizados
- Previsão de umidade futura
- Estimativa de rendimento
- Recomendações de irrigação

### Métricas de Performance:
- Acurácia dos modelos em tempo real
- Comparação entre diferentes algoritmos
- Análise de resíduos

## Integração com Fases Anteriores

- **Fase 2**: Utiliza dados coletados pelos sensores IoT
- **Fase 3**: Conecta com banco Oracle para dados históricos
- **Fase 4**: Aplica IA para previsões e recomendações

## Equipe

**FarmTech Solutions - Fase 4**
- Desenvolvimento: Richard Schmitz
- RM: 567951
- Curso: Inteligência Artificial - FIAP
- Data: 27.11.2025

# - Licença
Este projeto foi composto na maior parte com ajuda de IA ( Amazon Titan and GPT) 
