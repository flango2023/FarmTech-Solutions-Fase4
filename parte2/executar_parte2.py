"""
FarmTech Solutions - Fase 4: Script de Execução da Parte 2
Autor: Richard Schmitz - RM567951
"""

import sys
import os
sys.path.append('../parte1')

from modelos_preditivos import ModelosPreditivosAvancados
from avaliacao_modelos import AvaliacaoModelos
from recomendacoes import SistemaRecomendacoes
from ml_pipeline import FarmTechMLPipeline

def executar_parte2_completa():
    """Executa todo o pipeline da Parte 2"""
    
    print("="*80)
    print("FARMTECH SOLUTIONS - FASE 4: EXECUÇÃO COMPLETA DA PARTE 2")
    print("="*80)
    print("Autor: Richard Schmitz - RM567951")
    print("Sistema de IA para Otimização do Cultivo de Soja")
    print("="*80)
    
    # 1. Pipeline básico
    print("\n🚀 ETAPA 1: Pipeline de Machine Learning Básico")
    print("-" * 50)
    
    pipeline_basico = FarmTechMLPipeline()
    sucesso_basico = pipeline_basico.executar_pipeline_completo()
    
    if sucesso_basico:
        print("✅ Pipeline básico executado com sucesso!")
    else:
        print("❌ Erro no pipeline básico")
        return False
    
    # 2. Modelos preditivos avançados
    print("\n🤖 ETAPA 2: Modelos Preditivos Avançados")
    print("-" * 50)
    
    modelos_avancados = ModelosPreditivosAvancados()
    resultados, cv_results = modelos_avancados.treinar_todos_modelos()
    
    print("\n📊 Resultados dos Modelos:")
    for nome, resultado in resultados.items():
        print(f"  {resultado['modelo']}: R² = {resultado['r2']:.4f}")
    
    # 3. Avaliação de modelos
    print("\n📈 ETAPA 3: Avaliação de Performance")
    print("-" * 50)
    
    avaliacao = AvaliacaoModelos()
    if avaliacao.carregar_resultados():
        rankings = avaliacao.relatorio_completo()
        print("✅ Avaliação concluída!")
    else:
        print("⚠️ Avaliação não pôde ser executada")
    
    # 4. Sistema de recomendações
    print("\n💡 ETAPA 4: Sistema de Recomendações")
    print("-" * 50)
    
    # Dados de exemplo
    dados_exemplo = {
        'umidade_solo': 45.2,
        'ph_solo': 6.3,
        'nitrogenio': 1,
        'fosforo': 0,
        'potassio': 1,
        'temperatura': 32.5,
        'chuva_mm': 0.0
    }
    
    previsao_exemplo = {
        'chuva_mm': 0.5,
        'temperatura': 30.0
    }
    
    sistema_rec = SistemaRecomendacoes()
    recomendacoes = sistema_rec.gerar_relatorio_recomendacoes(dados_exemplo, previsao_exemplo)
    
    # 5. Resumo final
    print("\n🎯 RESUMO FINAL")
    print("=" * 50)
    
    print("✅ Pipeline de ML: Concluído")
    print("✅ Modelos Avançados: 5 modelos treinados")
    print("✅ Avaliação: Métricas calculadas")
    print("✅ Recomendações: Sistema ativo")
    print("✅ Interface: Streamlit disponível")
    
    print(f"\n📋 COMO EXECUTAR A INTERFACE:")
    print("1. cd parte2")
    print("2. streamlit run app_streamlit_completo.py")
    print("3. Acesse: http://localhost:8501")
    
    print(f"\n🎥 DEMONSTRAÇÃO PARA VÍDEO:")
    print("- Dashboard principal com métricas")
    print("- Pipeline ML completo")
    print("- Modelos preditivos avançados")
    print("- Avaliação de performance")
    print("- Recomendações inteligentes")
    print("- Previsões interativas")
    
    return True

def main():
    sucesso = executar_parte2_completa()
    
    if sucesso:
        print("\n🎉 PARTE 2 EXECUTADA COM SUCESSO!")
        print("Sistema pronto para demonstração em vídeo.")
    else:
        print("\n❌ Erro na execução da Parte 2")

if __name__ == "__main__":
    main()