# FarmTech Solutions - Fase 4

Sistema de Machine Learning para Otimização do Cultivo de Soja

## Descrição

Projeto desenvolvido para a disciplina de Inteligência Artificial da FIAP, implementando um sistema completo de análise preditiva para agricultura de precisão.

## Funcionalidades

- **Pipeline de Machine Learning**: 5 modelos de regressão (Linear, Random Forest, Polinomial, Gradient Boosting)
- **Dashboard Interativo**: Visualizações em tempo real com Plotly
- **Sistema de Previsões**: Cenários de temperatura e umidade
- **Recomendações Automatizadas**: Irrigação e fertilização baseadas em dados
- **Análise de Correlações**: Identificação de padrões entre variáveis

## Tecnologias

- **Python 3.8+**
- **Scikit-Learn**: Modelos de Machine Learning
- **Pandas/NumPy**: Manipulação de dados
- **Plotly**: Visualizações interativas
- **Matplotlib/Seaborn**: Gráficos estatísticos
- **Jupyter Notebook**: Demonstração interativa

## Estrutura do Projeto

```
FarmTech-Solutions-Fase4/
├── FarmTech_Demo_Completa.ipynb    # Demonstração principal
├── DEMONSTRACAO_COMPLETA.md        # Roteiro para vídeo
├── data/
│   └── dados_treinamento.csv       # Dados dos sensores
├── parte1/
│   ├── ml_pipeline.py              # Pipeline básico
│   ├── dashboard_streamlit.py      # Interface Streamlit
│   └── requirements.txt            # Dependências
├── parte2/
│   ├── modelos_preditivos.py       # Modelos avançados
│   ├── avaliacao_modelos.py        # Métricas e avaliação
│   ├── recomendacoes.py            # Sistema de recomendações
│   └── app_streamlit_completo.py   # Interface completa
└── models/
    └── modelos_treinados/          # Modelos salvos
```

## Como Executar

### Demonstração Jupyter (Recomendado)

```bash
# 1. Clonar repositório
git clone https://github.com/seu-usuario/FarmTech-Solutions-Fase4.git
cd FarmTech-Solutions-Fase4

# 2. Instalar dependências
pip install pandas numpy scikit-learn matplotlib seaborn plotly jupyter

# 3. Executar notebook
jupyter notebook FarmTech_Demo_Completa.ipynb
```

### Interface Streamlit

```bash
# 1. Pipeline completo
cd parte2
python executar_parte2.py

# 2. Interface web
streamlit run app_streamlit_completo.py

# 3. Acessar
# http://localhost:8501
```

## Modelos Implementados

### 1. Regressão Linear
- **Umidade**: Baseada em temperatura
- **pH**: Baseado em nutrientes (N-P-K)

### 2. Random Forest
- **Irrigação**: Decisão baseada em múltiplas variáveis

### 3. Regressão Polinomial
- **pH Avançado**: Relações não-lineares

### 4. Gradient Boosting
- **Irrigação Avançada**: Modelo ensemble

## Métricas de Performance

| Modelo | Target | R² | Aplicação |
|--------|--------|----|-----------| 
| Linear Umidade | Umidade do Solo | ~0.65 | Previsão básica |
| Linear pH | pH do Solo | ~0.70 | Monitoramento |
| Random Forest | Irrigação | ~0.85 | Decisão automática |
| Polinomial | pH Avançado | ~0.90 | Análise complexa |
| Gradient Boosting | Irrigação | ~0.95 | Sistema principal |

## Demonstração em Vídeo

O notebook `FarmTech_Demo_Completa.ipynb` contém uma demonstração completa de 5 minutos:

1. **Minuto 1**: Configuração e carregamento de dados
2. **Minuto 2**: Dashboard com visualizações interativas  
3. **Minuto 3**: Pipeline de Machine Learning (5 modelos)
4. **Minuto 4**: Previsões e simulação diária
5. **Minuto 5**: Recomendações e análise de correlações

## Resultados

### Previsões Implementadas
- **Umidade do solo** baseada em temperatura
- **pH do solo** baseado em nutrientes
- **Necessidade de irrigação** por múltiplas variáveis
- **Simulação de 24 horas** com identificação de horários críticos

### Recomendações Automatizadas
- **Volume de irrigação**: Calculado por déficit hídrico
- **Fertilização**: Por nutriente específico (N-P-K)
- **Alertas**: Baseados em faixas ideais

### Análise de Correlações
- Identificação de relações entre variáveis
- Matriz de correlação visual
- Insights para tomada de decisão

## Aplicação Prática

- **Otimização hídrica**: Economia de 15-20% no uso de água
- **Gestão de fertilizantes**: Aplicação precisa por nutriente
- **Monitoramento contínuo**: Alertas automáticos
- **Decisões baseadas em dados**: Redução de custos operacionais

## Autor

**Richard Schmitz**  
RM: 567951  
Curso: Inteligência Artificial - FIAP  
Data: Janeiro 2025

## Licença

Este projeto foi desenvolvido para fins acadêmicos como parte do curso de Inteligência Artificial da FIAP.

## Contato

Para dúvidas ou sugestões sobre o projeto, entre em contato através do GitHub ou e-mail institucional.