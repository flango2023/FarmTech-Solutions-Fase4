"""
FarmTech Solutions - Fase 4: Dashboard Streamlit
Autor: Richard Schmitz - RM567951
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
from ml_pipeline import FarmTechMLPipeline

# Configuração da página
st.set_page_config(
    page_title="FarmTech Solutions - Assistente Agrícola IA",
    page_icon="🌱",
    layout="wide"
)

# Inicializar pipeline ML
@st.cache_resource
def carregar_pipeline():
    pipeline = FarmTechMLPipeline()
    if not pipeline.carregar_modelos():
        # Se não conseguir carregar, treinar novos modelos
        pipeline.executar_pipeline_completo()
    return pipeline

def main():
    st.title("FarmTech Solutions - Assistente Agrícola Inteligente")
    st.markdown("**Sistema de IA para Otimização do Cultivo de Soja**")
    
    # Carregar pipeline
    pipeline = carregar_pipeline()
    
    # Sidebar para navegação
    st.sidebar.title("Navegação")
    opcao = st.sidebar.selectbox(
        "Selecione uma opção:",
        ["Dashboard Principal", "Previsões Interativas", "Métricas dos Modelos", "Análise de Dados"]
    )
    
    if opcao == "Dashboard Principal":
        dashboard_principal(pipeline)
    elif opcao == "Previsões Interativas":
        previsoes_interativas(pipeline)
    elif opcao == "Métricas dos Modelos":
        metricas_modelos(pipeline)
    elif opcao == "Análise de Dados":
        analise_dados()

def dashboard_principal(pipeline):
    st.header("Dashboard Principal")
    
    # Carregar dados
    df = pd.read_csv("../data/dados_treinamento.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['nutrientes_total'] = df['nitrogenio'] + df['fosforo'] + df['potassio']
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Umidade Média", f"{df['umidade_solo'].mean():.1f}%")
    
    with col2:
        st.metric("pH Médio", f"{df['ph_solo'].mean():.1f}")
    
    with col3:
        st.metric("Irrigações Realizadas", f"{df['irrigacao_ativa'].sum()}")
    
    with col4:
        st.metric("Temperatura Média", f"{df['temperatura'].mean():.1f}°C")
    
    # Gráficos principais
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Umidade do Solo ao Longo do Tempo")
        fig_umidade = px.line(df, x='timestamp', y='umidade_solo', 
                             title="Variação da Umidade")
        fig_umidade.add_hline(y=60, line_dash="dash", line_color="red", 
                             annotation_text="Limite Mínimo (60%)")
        fig_umidade.add_hline(y=80, line_dash="dash", line_color="red", 
                             annotation_text="Limite Máximo (80%)")
        st.plotly_chart(fig_umidade, use_container_width=True)
    
    with col2:
        st.subheader("pH do Solo")
        fig_ph = px.scatter(df, x='timestamp', y='ph_solo', 
                           color='irrigacao_ativa',
                           title="Variação do pH")
        fig_ph.add_hline(y=6.0, line_dash="dash", line_color="green")
        fig_ph.add_hline(y=6.8, line_dash="dash", line_color="green")
        st.plotly_chart(fig_ph, use_container_width=True)
    
    # Correlações
    st.subheader("Matriz de Correlação")
    corr_data = df[['umidade_solo', 'ph_solo', 'temperatura', 'chuva_mm', 'nutrientes_total']].corr()
    fig_corr = px.imshow(corr_data, text_auto=True, aspect="auto",
                        title="Correlação entre Variáveis")
    st.plotly_chart(fig_corr, use_container_width=True)

def previsoes_interativas(pipeline):
    st.header("Previsões Interativas")
    
    st.markdown("Insira os parâmetros para obter previsões:")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Parâmetros de Entrada")
        temperatura = st.slider("Temperatura (°C)", 15.0, 40.0, 25.0)
        chuva = st.slider("Chuva (mm)", 0.0, 10.0, 0.0)
        hora = st.slider("Hora do Dia", 0, 23, 12)
        
        nitrogenio = st.checkbox("Nitrogênio Disponível", value=True)
        fosforo = st.checkbox("Fósforo Disponível", value=True)
        potassio = st.checkbox("Potássio Disponível", value=True)
        
        nutrientes_total = int(nitrogenio) + int(fosforo) + int(potassio)
    
    with col2:
        st.subheader("Previsões")
        
        if st.button("Calcular Previsões"):
            # Previsão de umidade
            dados_umidade = [temperatura, chuva, hora, nutrientes_total]
            umidade_pred = pipeline.fazer_previsao('umidade', dados_umidade)
            
            # Previsão de pH
            dados_ph = [int(nitrogenio), int(fosforo), int(potassio), temperatura]
            ph_pred = pipeline.fazer_previsao('ph', dados_ph)
            
            # Previsão de irrigação
            dados_irrigacao = [umidade_pred, ph_pred, temperatura, chuva, nutrientes_total]
            irrigacao_pred = pipeline.fazer_previsao('irrigacao', dados_irrigacao)
            
            # Exibir resultados
            st.success(f"Umidade Prevista: {umidade_pred:.1f}%")
            st.success(f"pH Previsto: {ph_pred:.1f}")
            
            if irrigacao_pred > 0.5:
                st.warning("Recomendação: IRRIGAR")
            else:
                st.info("Recomendação: NÃO IRRIGAR")
            
            # Análise das condições
            st.subheader("Análise das Condições")
            
            if 60 <= umidade_pred <= 80:
                st.success("Umidade: IDEAL para soja")
            elif umidade_pred < 60:
                st.warning("Umidade: BAIXA - Irrigação necessária")
            else:
                st.error("Umidade: ALTA - Risco de encharcamento")
            
            if 6.0 <= ph_pred <= 6.8:
                st.success("pH: IDEAL para soja")
            else:
                st.warning("pH: Fora da faixa ideal (6.0-6.8)")

def metricas_modelos(pipeline):
    st.header("Métricas dos Modelos de Machine Learning")
    
    if not pipeline.metrics:
        st.error("Métricas não disponíveis. Execute o pipeline primeiro.")
        return
    
    # Exibir métricas em colunas
    col1, col2, col3 = st.columns(3)
    
    modelos = ['umidade', 'ph', 'irrigacao']
    colunas = [col1, col2, col3]
    
    for i, modelo in enumerate(modelos):
        with colunas[i]:
            st.subheader(f"Modelo: {modelo.title()}")
            metricas = pipeline.metrics[modelo]
            
            st.metric("MAE", f"{metricas['mae']:.4f}")
            st.metric("MSE", f"{metricas['mse']:.4f}")
            st.metric("RMSE", f"{metricas['rmse']:.4f}")
            st.metric("R²", f"{metricas['r2']:.4f}")
            
            # Interpretação do R²
            r2 = metricas['r2']
            if r2 > 0.8:
                st.success("Excelente ajuste")
            elif r2 > 0.6:
                st.info("Bom ajuste")
            else:
                st.warning("Ajuste moderado")
    
    # Gráfico comparativo
    st.subheader("Comparação de Performance (R²)")
    
    r2_values = [pipeline.metrics[m]['r2'] for m in modelos]
    fig_r2 = px.bar(x=modelos, y=r2_values, 
                    title="Coeficiente de Determinação (R²) por Modelo")
    fig_r2.update_layout(yaxis_title="R²", xaxis_title="Modelo")
    st.plotly_chart(fig_r2, use_container_width=True)

def analise_dados():
    st.header("Análise Exploratória dos Dados")
    
    # Carregar dados
    df = pd.read_csv("../data/dados_treinamento.csv")
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['hora'] = df['timestamp'].dt.hour
    df['nutrientes_total'] = df['nitrogenio'] + df['fosforo'] + df['potassio']
    
    # Estatísticas descritivas
    st.subheader("Estatísticas Descritivas")
    st.dataframe(df.describe())
    
    # Distribuições
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição da Umidade")
        fig_hist_umidade = px.histogram(df, x='umidade_solo', nbins=10,
                                       title="Distribuição da Umidade do Solo")
        st.plotly_chart(fig_hist_umidade, use_container_width=True)
    
    with col2:
        st.subheader("Distribuição do pH")
        fig_hist_ph = px.histogram(df, x='ph_solo', nbins=10,
                                  title="Distribuição do pH do Solo")
        st.plotly_chart(fig_hist_ph, use_container_width=True)
    
    # Análise temporal
    st.subheader("Padrões Temporais")
    
    # Agrupamento por hora
    df_hora = df.groupby('hora').agg({
        'umidade_solo': 'mean',
        'temperatura': 'mean',
        'irrigacao_ativa': 'sum'
    }).reset_index()
    
    fig_temporal = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Umidade por Hora', 'Temperatura por Hora', 
                       'Irrigações por Hora', 'Nutrientes Disponíveis'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}],
               [{"secondary_y": False}, {"secondary_y": False}]]
    )
    
    # Umidade por hora
    fig_temporal.add_trace(
        go.Scatter(x=df_hora['hora'], y=df_hora['umidade_solo'], 
                  name='Umidade', line=dict(color='blue')),
        row=1, col=1
    )
    
    # Temperatura por hora
    fig_temporal.add_trace(
        go.Scatter(x=df_hora['hora'], y=df_hora['temperatura'], 
                  name='Temperatura', line=dict(color='red')),
        row=1, col=2
    )
    
    # Irrigações por hora
    fig_temporal.add_trace(
        go.Bar(x=df_hora['hora'], y=df_hora['irrigacao_ativa'], 
               name='Irrigações', marker_color='green'),
        row=2, col=1
    )
    
    # Nutrientes disponíveis
    nutrientes_dist = df['nutrientes_total'].value_counts().sort_index()
    fig_temporal.add_trace(
        go.Bar(x=nutrientes_dist.index, y=nutrientes_dist.values, 
               name='Nutrientes', marker_color='orange'),
        row=2, col=2
    )
    
    fig_temporal.update_layout(height=600, showlegend=False)
    st.plotly_chart(fig_temporal, use_container_width=True)

if __name__ == "__main__":
    main()