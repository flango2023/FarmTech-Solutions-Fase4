# Instruções de Execução - FarmTech Solutions Fase 4

## Pré-requisitos

### 1. Python 3.8 ou superior
```bash
python --version
```

### 2. Instalar dependências
```bash
cd /Users/richardschmitz/FIAP/FarmTech-Solutions-Fase4/parte1
pip install -r requirements.txt
```

## Execução da PARTE 1

### 1. Treinar Modelos de Machine Learning
```bash
cd parte1
python ml_pipeline.py
```

**Saída esperada:**
- Modelos treinados e salvos em `models/modelos_treinados/`
- Métricas exibidas no terminal
- Arquivos `.pkl` gerados para cada modelo

### 2. Executar Dashboard Streamlit
```bash
streamlit run dashboard_streamlit.py
```

**Acesso:**
- URL: http://localhost:8501
- Interface web interativa
- Navegação por abas: Dashboard, Previsões, Métricas, Análise

### Funcionalidades do Dashboard:
- **Dashboard Principal**: Métricas e gráficos em tempo real
- **Previsões Interativas**: Entrada de parâmetros customizados
- **Métricas dos Modelos**: Comparação de performance
- **Análise de Dados**: Exploração estatística

## Execução da PARTE 2

### 1. Treinar Modelos Preditivos Avançados
```bash
cd parte2
python modelos_preditivos.py
```

**Saída esperada:**
- 5 modelos diferentes treinados
- Métricas comparativas exibidas
- Modelos salvos em `models/modelos_treinados/`

### 2. Avaliar Performance dos Modelos
```bash
python avaliacao_modelos.py
```

**Saída esperada:**
- Relatório completo de avaliação
- Gráficos comparativos salvos em `screenshots/`
- Ranking dos modelos por performance

### 3. Gerar Recomendações Agrícolas
```bash
python recomendacoes.py
```

**Saída esperada:**
- Relatório de recomendações detalhado
- Análise de condições atuais
- Sugestões de irrigação e fertilização

## Estrutura de Arquivos Gerados

```
FarmTech-Solutions-Fase4/
├── models/modelos_treinados/
│   ├── modelo_umidade.pkl
│   ├── modelo_ph.pkl
│   ├── modelo_irrigacao.pkl
│   ├── scaler_*.pkl
│   ├── metricas.json
│   └── resultados_parte2.json
├── screenshots/
│   └── comparacao_modelos.png
└── docs/
    ├── relatorio_fase4.md
    └── relatorio_avaliacao.txt
```

## Solução de Problemas

### Erro: Módulo não encontrado
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Erro: Dados não encontrados
- Verificar se `data/dados_treinamento.csv` existe
- Executar primeiro `ml_pipeline.py` para gerar dados

### Erro: Streamlit não inicia
```bash
streamlit --version
streamlit run dashboard_streamlit.py --server.port 8502
```

### Erro: Modelos não carregados
- Executar primeiro `ml_pipeline.py`
- Verificar permissões da pasta `models/`

## Demonstração Completa

### Sequência Recomendada:
1. **Treinar modelos básicos** (`parte1/ml_pipeline.py`)
2. **Iniciar dashboard** (`streamlit run dashboard_streamlit.py`)
3. **Treinar modelos avançados** (`parte2/modelos_preditivos.py`)
4. **Avaliar performance** (`parte2/avaliacao_modelos.py`)
5. **Gerar recomendações** (`parte2/recomendacoes.py`)

### Para Vídeo de Demonstração:
1. Mostrar execução do pipeline ML
2. Navegar pelo dashboard Streamlit
3. Demonstrar previsões interativas
4. Exibir métricas e comparações
5. Apresentar sistema de recomendações

## Dados de Teste

### Exemplo de entrada para previsões:
```python
dados_teste = {
    'temperatura': 28.5,
    'chuva_mm': 0.0,
    'hora': 14,
    'nitrogenio': 1,
    'fosforo': 0,
    'potassio': 1,
    'umidade_solo': 45.0,
    'ph_solo': 6.2
}
```

### Resultados esperados:
- Umidade prevista: ~52%
- pH previsto: ~6.4
- Recomendação: IRRIGAR
- Volume: ~150 litros
- Prioridade: MÉDIA

## Métricas de Sucesso

### PARTE 1:
- ✅ Pipeline ML executado sem erros
- ✅ Dashboard acessível em localhost:8501
- ✅ Previsões interativas funcionando
- ✅ Métricas R² > 0.6 para todos os modelos

### PARTE 2:
- ✅ 5 modelos treinados com sucesso
- ✅ Melhor modelo com R² > 0.8
- ✅ Relatório de avaliação gerado
- ✅ Sistema de recomendações operacional

## Contato

**Desenvolvedor**: Richard Schmitz  
**RM**: 567951  
**Curso**: Inteligência Artificial - FIAP