"""
FarmTech Solutions - Fase 4: Avaliação de Modelos
Autor: Richard Schmitz - RM567951
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import json
import joblib

class AvaliacaoModelos:
    def __init__(self):
        self.resultados = {}
        self.metricas_comparativas = {}
        
    def carregar_resultados(self, arquivo="../models/modelos_treinados/resultados_parte2.json"):
        """Carrega resultados dos modelos treinados"""
        try:
            with open(arquivo, 'r') as f:
                self.resultados = json.load(f)
            return True
        except Exception as e:
            print(f"Erro ao carregar resultados: {e}")
            return False
    
    def calcular_metricas_comparativas(self):
        """Calcula métricas comparativas entre modelos"""
        metricas = ['mae', 'rmse', 'r2']
        
        for metrica in metricas:
            self.metricas_comparativas[metrica] = {}
            for nome, resultado in self.resultados.items():
                self.metricas_comparativas[metrica][nome] = resultado[metrica]
        
        return self.metricas_comparativas
    
    def ranking_modelos(self):
        """Cria ranking dos modelos por performance"""
        # Ranking por R² (maior é melhor)
        ranking_r2 = sorted(self.metricas_comparativas['r2'].items(), 
                           key=lambda x: x[1], reverse=True)
        
        # Ranking por RMSE (menor é melhor)
        ranking_rmse = sorted(self.metricas_comparativas['rmse'].items(), 
                             key=lambda x: x[1])
        
        # Ranking por MAE (menor é melhor)
        ranking_mae = sorted(self.metricas_comparativas['mae'].items(), 
                            key=lambda x: x[1])
        
        return {
            'r2': ranking_r2,
            'rmse': ranking_rmse,
            'mae': ranking_mae
        }
    
    def analise_residuos(self, nome_modelo):
        """Análise de resíduos para um modelo específico"""
        if nome_modelo not in self.resultados:
            return None
        
        resultado = self.resultados[nome_modelo]
        y_test = np.array(resultado['y_test'])
        y_pred = np.array(resultado['y_pred'])
        
        residuos = y_test - y_pred
        
        analise = {
            'residuos': residuos,
            'residuos_padronizados': residuos / np.std(residuos),
            'media_residuos': np.mean(residuos),
            'std_residuos': np.std(residuos),
            'residuos_abs_medio': np.mean(np.abs(residuos)),
            'outliers': np.sum(np.abs(residuos) > 2 * np.std(residuos))
        }
        
        return analise
    
    def interpretacao_metricas(self, nome_modelo):
        """Interpreta as métricas de um modelo"""
        if nome_modelo not in self.resultados:
            return None
        
        resultado = self.resultados[nome_modelo]
        r2 = resultado['r2']
        mae = resultado['mae']
        rmse = resultado['rmse']
        
        interpretacao = {
            'qualidade_geral': '',
            'precisao': '',
            'aplicabilidade': '',
            'recomendacoes': []
        }
        
        # Interpretação do R²
        if r2 >= 0.9:
            interpretacao['qualidade_geral'] = 'Excelente'
        elif r2 >= 0.7:
            interpretacao['qualidade_geral'] = 'Boa'
        elif r2 >= 0.5:
            interpretacao['qualidade_geral'] = 'Moderada'
        else:
            interpretacao['qualidade_geral'] = 'Baixa'
        
        # Interpretação da precisão
        if mae < 2:
            interpretacao['precisao'] = 'Alta precisão'
        elif mae < 5:
            interpretacao['precisao'] = 'Precisão moderada'
        else:
            interpretacao['precisao'] = 'Baixa precisão'
        
        # Aplicabilidade
        if r2 >= 0.7 and mae < 3:
            interpretacao['aplicabilidade'] = 'Recomendado para produção'
        elif r2 >= 0.5:
            interpretacao['aplicabilidade'] = 'Adequado para análises exploratórias'
        else:
            interpretacao['aplicabilidade'] = 'Necessita melhorias'
        
        # Recomendações
        if r2 < 0.7:
            interpretacao['recomendacoes'].append('Coletar mais dados')
            interpretacao['recomendacoes'].append('Adicionar novas features')
        
        if mae > 3:
            interpretacao['recomendacoes'].append('Ajustar hiperparâmetros')
            interpretacao['recomendacoes'].append('Considerar ensemble de modelos')
        
        return interpretacao
    
    def comparacao_visual(self):
        """Cria visualizações comparativas dos modelos"""
        # Configurar estilo
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        
        # Gráfico 1: Comparação R²
        modelos = list(self.metricas_comparativas['r2'].keys())
        r2_values = list(self.metricas_comparativas['r2'].values())
        
        axes[0, 0].bar(modelos, r2_values, color='skyblue', alpha=0.7)
        axes[0, 0].set_title('Comparação R² por Modelo')
        axes[0, 0].set_ylabel('R²')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3)
        
        # Gráfico 2: Comparação RMSE
        rmse_values = list(self.metricas_comparativas['rmse'].values())
        
        axes[0, 1].bar(modelos, rmse_values, color='lightcoral', alpha=0.7)
        axes[0, 1].set_title('Comparação RMSE por Modelo')
        axes[0, 1].set_ylabel('RMSE')
        axes[0, 1].tick_params(axis='x', rotation=45)
        axes[0, 1].grid(True, alpha=0.3)
        
        # Gráfico 3: Scatter R² vs RMSE
        axes[1, 0].scatter(r2_values, rmse_values, s=100, alpha=0.7, color='green')
        for i, modelo in enumerate(modelos):
            axes[1, 0].annotate(modelo, (r2_values[i], rmse_values[i]), 
                               xytext=(5, 5), textcoords='offset points', fontsize=8)
        axes[1, 0].set_xlabel('R²')
        axes[1, 0].set_ylabel('RMSE')
        axes[1, 0].set_title('R² vs RMSE')
        axes[1, 0].grid(True, alpha=0.3)
        
        # Gráfico 4: Heatmap de métricas
        metricas_df = pd.DataFrame(self.metricas_comparativas).T
        sns.heatmap(metricas_df, annot=True, fmt='.3f', cmap='RdYlBu_r', 
                   ax=axes[1, 1], cbar_kws={'label': 'Valor da Métrica'})
        axes[1, 1].set_title('Heatmap de Métricas')
        
        plt.tight_layout()
        plt.savefig('../screenshots/comparacao_modelos.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return fig
    
    def relatorio_completo(self):
        """Gera relatório completo de avaliação"""
        print("="*80)
        print("RELATÓRIO DE AVALIAÇÃO DOS MODELOS - FARMTECH SOLUTIONS")
        print("="*80)
        
        # Métricas comparativas
        self.calcular_metricas_comparativas()
        
        # Rankings
        rankings = self.ranking_modelos()
        
        print(f"\n{'RANKING DOS MODELOS':<30}")
        print("-" * 50)
        
        print(f"\nPor R² (Coeficiente de Determinação):")
        for i, (modelo, valor) in enumerate(rankings['r2'], 1):
            print(f"  {i}. {modelo:<20} R² = {valor:.4f}")
        
        print(f"\nPor RMSE (Erro Quadrático Médio):")
        for i, (modelo, valor) in enumerate(rankings['rmse'], 1):
            print(f"  {i}. {modelo:<20} RMSE = {valor:.4f}")
        
        print(f"\nPor MAE (Erro Absoluto Médio):")
        for i, (modelo, valor) in enumerate(rankings['mae'], 1):
            print(f"  {i}. {modelo:<20} MAE = {valor:.4f}")
        
        # Análise detalhada por modelo
        print(f"\n{'ANÁLISE DETALHADA POR MODELO':<30}")
        print("-" * 50)
        
        for nome_modelo in self.resultados.keys():
            print(f"\n{nome_modelo.upper()}:")
            
            resultado = self.resultados[nome_modelo]
            print(f"  Target: {resultado['target']}")
            print(f"  Features: {len(resultado['features'])}")
            print(f"  MAE: {resultado['mae']:.4f}")
            print(f"  RMSE: {resultado['rmse']:.4f}")
            print(f"  R²: {resultado['r2']:.4f}")
            
            # Interpretação
            interpretacao = self.interpretacao_metricas(nome_modelo)
            if interpretacao:
                print(f"  Qualidade: {interpretacao['qualidade_geral']}")
                print(f"  Precisão: {interpretacao['precisao']}")
                print(f"  Aplicabilidade: {interpretacao['aplicabilidade']}")
                
                if interpretacao['recomendacoes']:
                    print(f"  Recomendações:")
                    for rec in interpretacao['recomendacoes']:
                        print(f"    - {rec}")
            
            # Análise de resíduos
            analise_res = self.analise_residuos(nome_modelo)
            if analise_res:
                print(f"  Média dos resíduos: {analise_res['media_residuos']:.4f}")
                print(f"  Desvio padrão dos resíduos: {analise_res['std_residuos']:.4f}")
                print(f"  Outliers detectados: {analise_res['outliers']}")
        
        # Recomendações gerais
        print(f"\n{'RECOMENDAÇÕES GERAIS':<30}")
        print("-" * 50)
        
        melhor_modelo = rankings['r2'][0]
        print(f"\nMelhor modelo geral: {melhor_modelo[0]} (R² = {melhor_modelo[1]:.4f})")
        
        if melhor_modelo[1] >= 0.8:
            print("✓ Modelo adequado para uso em produção")
        elif melhor_modelo[1] >= 0.6:
            print("⚠ Modelo adequado para análises, mas pode ser melhorado")
        else:
            print("✗ Modelo necessita melhorias significativas")
        
        print(f"\nPara melhorar a performance:")
        print("- Coletar mais dados históricos")
        print("- Adicionar features meteorológicas")
        print("- Implementar ensemble de modelos")
        print("- Ajustar hiperparâmetros via grid search")
        
        return rankings
    
    def salvar_relatorio(self, arquivo="../docs/relatorio_avaliacao.txt"):
        """Salva relatório em arquivo"""
        import sys
        from io import StringIO
        
        # Capturar output do relatório
        old_stdout = sys.stdout
        sys.stdout = buffer = StringIO()
        
        self.relatorio_completo()
        
        sys.stdout = old_stdout
        relatorio_texto = buffer.getvalue()
        
        # Salvar em arquivo
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(relatorio_texto)
        
        print(f"Relatório salvo em: {arquivo}")

def main():
    avaliacao = AvaliacaoModelos()
    
    if avaliacao.carregar_resultados():
        print("Resultados carregados com sucesso!")
        
        # Gerar relatório completo
        rankings = avaliacao.relatorio_completo()
        
        # Criar visualizações
        print("\nGerando visualizações...")
        avaliacao.comparacao_visual()
        
        # Salvar relatório
        avaliacao.salvar_relatorio()
        
        return avaliacao
    else:
        print("Erro: Execute primeiro os modelos preditivos (modelos_preditivos.py)")
        return None

if __name__ == "__main__":
    main()