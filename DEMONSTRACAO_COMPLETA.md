# FarmTech Solutions - Demonstração Completa

## Execução para Vídeo (5 minutos)

### Opção 1: Jupyter Notebook (RECOMENDADO)
```bash
cd FarmTech-Solutions-Fase4/parte2
jupyter notebook FarmTech_Demo_Completa.ipynb
```

### Opção 2: Streamlit
```bash
cd FarmTech-Solutions-Fase4/parte2
python3 executar_parte2.py
streamlit run app_streamlit_completo.py
```

---

## Roteiro Jupyter Notebook

### Minuto 1: Configuração e Dados (Células 1-2)
- **Executar:** Importações e carregamento de dados
- **Mostrar:** 15 registros de sensores agrícolas
- **Destacar:** Dados sintéticos para demonstração

### Minuto 2: Dashboard e Visualizações (Célula 3)
- **Executar:** Dashboard com 4 gráficos interativos
- **Destacar:** Faixas ideais (Umidade 60-80%, pH 6.0-6.8)
- **Mostrar:** Tendências temporais dos sensores

### Minuto 3: Pipeline Machine Learning (Células 4-5)
- **Executar:** 3 modelos básicos + 2 avançados
- **Mostrar:** Gráfico de performance (R²)
- **Destacar:** Melhor modelo e métricas

### Minuto 4: Previsões Inteligentes (Células 6-7)
- **Executar:** 3 cenários de temperatura
- **Mostrar:** Simulação de 24 horas
- **Destacar:** Horários críticos identificados

### Minuto 5: Recomendações e Conclusão (Células 8-10)
- **Executar:** Sistema de recomendações
- **Mostrar:** Correlações entre variáveis
- **Concluir:** Resumo executivo e impacto

---

## Script de Narração Atualizado

> "O FarmTech Solutions é um sistema de Machine Learning para otimização do cultivo de soja.
> 
> Iniciamos carregando dados de sensores agrícolas com 15 registros incluindo umidade, pH, temperatura e nutrientes.
> 
> O dashboard apresenta visualizações interativas com faixas ideais destacadas: umidade entre 60-80% e pH entre 6.0-6.8.
> 
> Nosso pipeline treina 5 modelos: Linear para umidade e pH, Random Forest para irrigação, Polinomial e Gradient Boosting.
> 
> O gráfico de performance mostra as métricas R² de cada modelo, identificando os mais eficazes.
> 
> O sistema gera previsões para três cenários: temperatura normal, stress térmico e condições baixas.
> 
> A simulação diária identifica horários críticos baseados no ciclo de temperatura.
> 
> As recomendações incluem volume de irrigação calculado e fertilização por nutriente.
> 
> A matriz de correlação revela relações importantes entre as variáveis agrícolas.
> 
> Resultado: sistema funcional para agricultura baseada em dados e decisões automatizadas."

---

## Métricas Demonstradas

### Modelos ML:
- **Regressão Polinomial:** R² = 0.9955
- **Gradient Boosting:** R² = 0.9700
- **Regressão Linear:** R² = 0.0145
- **Random Forest:** R² = -1.1149
- **Regressão Múltipla:** R² = -0.2952

### Previsões:
- **Cenário Normal:** 25°C - Umidade ideal
- **Stress Térmico:** 35°C - Irrigação urgente
- **Após Chuva:** 22°C + 5mm - Suspender irrigação

### Recomendações:
- **Volume:** 170 litros
- **Duração:** 17 minutos
- **Fertilização:** Fósforo necessário (20 kg/ha)

---

## Pontos de Destaque

### Técnicos:
- **5 algoritmos** de Machine Learning
- **Métricas robustas** (MAE, MSE, RMSE, R²)
- **Validação cruzada** implementada
- **Pipeline automatizado** completo

### Práticos:
- **Previsões em tempo real** para soja
- **Recomendações automáticas** de manejo
- **Sistema de alertas** inteligente
- **Otimização de recursos** hídricos

### Diferenciais:
- **Sistema end-to-end** funcional
- **Interface profissional** para produção
- **Machine Learning aplicado** ao agronegócio
- **Resultados interpretáveis** e acionáveis

---

## Checklist de Execução

### Antes de Gravar:
- [ ] Jupyter instalado (`pip3 install jupyter`)
- [ ] Dependências instaladas
- [ ] Notebook testado célula por célula
- [ ] Dados carregando corretamente

### Durante a Gravação:
- [ ] Executar células sequencialmente
- [ ] Destacar métricas principais
- [ ] Explicar aplicação prática
- [ ] Mostrar visualizações

### Resultado Final:
- [ ] Demonstração completa em 5 minutos
- [ ] Todos os componentes funcionando
- [ ] Sistema pronto para produção
- [ ] Impacto prático demonstrado

**Sistema FarmTech Solutions: Machine Learning aplicado à agricultura com resultados mensuráveis**