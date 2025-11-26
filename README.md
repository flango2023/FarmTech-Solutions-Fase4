# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# FarmTech Solutions - Fase 4: Assistente Agrícola Inteligente

## Grupo FarmTech Solutions

## 👨🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/richard-schmitz/">Richard Schmitz - RM567951</a>

## 👩🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/company/fiap/">Professor FIAP</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/company/fiap/">Coordenador FIAP</a>

## 📜 Descrição

O projeto FarmTech Solutions - Fase 4 representa a evolução do sistema de irrigação inteligente para um Assistente Agrícola completo baseado em Inteligência Artificial. Esta fase implementa Machine Learning supervisionado utilizando Scikit-Learn para prever variáveis críticas do campo e sugerir ações automatizadas de irrigação e manejo agrícola.

O sistema integra modelos de regressão (linear, múltipla e não-linear) com um dashboard interativo desenvolvido em Streamlit, permitindo que gestores agrícolas visualizem métricas de desempenho, gráficos de correlação e previsões geradas em tempo real. A solução foca na cultura da soja, utilizando dados históricos das fases anteriores para treinar modelos que preveem umidade do solo, pH, necessidade de irrigação, volume de água necessário, necessidade de fertilização e estimativa de rendimento.

A implementação inclui cinco modelos diferentes: Regressão Linear Simples, Regressão Múltipla, Regressão Polinomial, Random Forest e Gradient Boosting, todos avaliados com métricas MAE, MSE, RMSE e R². O sistema de recomendações automatizado analisa condições atuais e gera sugestões inteligentes para otimização da produção, representando um marco na aplicação de IA ao agronegócio brasileiro.

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

- <b>assets</b>: Arquivos relacionados a elementos não-estruturados deste repositório, como imagens e logos.

- <b>data</b>: Datasets utilizados para treinamento e teste dos modelos de Machine Learning.

- <b>docs</b>: Documentação técnica completa do projeto, incluindo relatórios e análises.

- <b>models</b>: Modelos treinados salvos em formato pickle para reutilização e deploy.

- <b>parte1</b>: Implementação do pipeline de Machine Learning e dashboard Streamlit básico.

- <b>parte2</b>: Modelos preditivos avançados, sistema de avaliação e recomendações agrícolas.

- <b>screenshots</b>: Capturas de tela das funcionalidades e resultados do sistema.

- <b>README.md</b>: Arquivo que serve como guia e explicação geral sobre o projeto.

- <b>INSTRUCOES_EXECUCAO.md</b>: Guia detalhado para execução e demonstração do projeto.

## 🔧 Como executar o código

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (para clonagem do repositório)

### Instalação e Execução

#### 1. Clonar o repositório
```bash
git clone https://github.com/flango2023/FarmTech-Solutions-Fase4.git
cd FarmTech-Solutions-Fase4
```

#### 2. Instalar dependências
```bash
cd parte1
pip install -r requirements.txt
```

#### 3. Executar PARTE 1 - Pipeline ML + Dashboard
```bash
# Treinar modelos básicos
python ml_pipeline.py

# Iniciar dashboard Streamlit
streamlit run dashboard_streamlit.py
```

#### 4. Executar PARTE 2 - Modelos Avançados
```bash
cd ../parte2

# Treinar modelos preditivos avançados
python modelos_preditivos.py

# Avaliar performance dos modelos
python avaliacao_modelos.py

# Gerar recomendações agrícolas
python recomendacoes.py
```

#### 5. Acessar o Dashboard
- URL: http://localhost:8501
- Interface otimizada para gestores agrícolas
- Navegação por abas: Dashboard Principal, Previsões Interativas, Métricas dos Modelos, Análise de Dados

### Funcionalidades Principais
- **Pipeline ML**: 3 modelos básicos (umidade, pH, irrigação)
- **Dashboard Interativo**: Visualizações em tempo real com Streamlit
- **Modelos Avançados**: 5 algoritmos diferentes com avaliação comparativa
- **Sistema de Recomendações**: Sugestões automatizadas para irrigação e fertilização
- **Métricas de Performance**: MAE, MSE, RMSE, R² para todos os modelos

## 🗃 Histórico de lançamentos

* 1.0.0 - 15/01/2025
    * Implementação completa da Fase 4
    * Pipeline de Machine Learning com Scikit-Learn
    * Dashboard Streamlit interativo
    * 5 modelos preditivos avançados
    * Sistema de recomendações agrícolas
    * Documentação técnica completa

* 0.3.0 - 09/11/2024
    * Fase 3: Implementação do banco de dados Oracle
    * Consultas SQL analíticas
    * Integração com dados IoT da Fase 2

* 0.2.0 - 01/10/2024
    * Fase 2: Sistema de irrigação inteligente
    * Hardware ESP32 + sensores IoT
    * Software Python + análise estatística R
    * Integração com API meteorológica

* 0.1.0 - 15/09/2024
    * Concepção inicial do projeto FarmTech Solutions
    * Definição da cultura da soja como foco
    * Estabelecimento dos parâmetros ideais de cultivo

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/flango2023/FarmTech-Solutions-Fase4">FarmTech Solutions - Fase 4</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">FIAP</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>