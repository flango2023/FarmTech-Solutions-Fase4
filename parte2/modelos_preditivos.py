"""
FarmTech Solutions - Fase 4: Modelos Preditivos Avançados
Autor: Richard Schmitz - RM567951
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

class ModelosPreditivosAvancados:
    def __init__(self):
        self.modelos = {}
        self.pipelines = {}
        self.resultados = {}
        self.dados = None
        
    def carregar_dados(self, arquivo_path="../data/dados_treinamento.csv"):
        """Carrega e prepara dados com features engenheiradas"""
        df = pd.read_csv(arquivo_path)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Feature engineering
        df['hora'] = df['timestamp'].dt.hour
        df['nutrientes_total'] = df['nitrogenio'] + df['fosforo'] + df['potassio']
        df['deficit_umidade'] = np.maximum(0, 60 - df['umidade_solo'])
        df['excesso_umidade'] = np.maximum(0, df['umidade_solo'] - 80)
        df['ph_ideal'] = ((df['ph_solo'] >= 6.0) & (df['ph_solo'] <= 6.8)).astype(int)
        df['temp_stress'] = (df['temperatura'] > 30).astype(int)
        df['chuva_categoria'] = pd.cut(df['chuva_mm'], bins=[-0.1, 0, 1, 5, 100], 
                                      labels=['sem_chuva', 'leve', 'moderada', 'forte'])
        
        self.dados = df
        return df
    
    def modelo_regressao_linear_simples(self):
        """Modelo de regressão linear simples para umidade"""
        df = self.dados
        
        # Umidade baseada em temperatura
        X = df[['temperatura']].values
        y = df['umidade_solo'].values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        modelo = LinearRegression()
        modelo.fit(X_train, y_train)
        
        y_pred = modelo.predict(X_test)
        
        resultados = {
            'modelo': 'Regressão Linear Simples',
            'target': 'umidade_solo',
            'features': ['temperatura'],
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        self.modelos['linear_simples'] = modelo
        self.resultados['linear_simples'] = resultados
        
        return modelo, resultados
    
    def modelo_regressao_multipla(self):
        """Modelo de regressão múltipla para rendimento estimado"""
        df = self.dados
        
        # Criar variável de rendimento estimado baseada nas condições
        df['rendimento_estimado'] = (
            (df['umidade_solo'] / 100) * 0.3 +
            (df['ph_ideal']) * 0.2 +
            (df['nutrientes_total'] / 3) * 0.3 +
            (1 - df['temp_stress']) * 0.2
        ) * 100  # Escala 0-100
        
        features = ['umidade_solo', 'ph_solo', 'temperatura', 'nutrientes_total', 'chuva_mm']
        X = df[features]
        y = df['rendimento_estimado']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Pipeline com normalização
        pipeline = Pipeline([
            ('scaler', StandardScaler()),
            ('regressor', LinearRegression())
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        resultados = {
            'modelo': 'Regressão Múltipla',
            'target': 'rendimento_estimado',
            'features': features,
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        self.pipelines['multipla'] = pipeline
        self.resultados['multipla'] = resultados
        
        return pipeline, resultados
    
    def modelo_regressao_polinomial(self):
        """Modelo de regressão polinomial para relações não-lineares"""
        df = self.dados
        
        # Volume de irrigação baseado em múltiplas variáveis
        df['volume_irrigacao'] = np.where(
            df['irrigacao_ativa'] == 1,
            np.maximum(0, (60 - df['umidade_solo']) * 2 + 
                      (df['temperatura'] - 20) * 0.5),
            0
        )
        
        features = ['umidade_solo', 'temperatura', 'deficit_umidade']
        X = df[features]
        y = df['volume_irrigacao']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Pipeline com features polinomiais
        pipeline = Pipeline([
            ('poly', PolynomialFeatures(degree=2, include_bias=False)),
            ('scaler', StandardScaler()),
            ('regressor', Ridge(alpha=1.0))
        ])
        
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        
        resultados = {
            'modelo': 'Regressão Polinomial',
            'target': 'volume_irrigacao',
            'features': features,
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        self.pipelines['polinomial'] = pipeline
        self.resultados['polinomial'] = resultados
        
        return pipeline, resultados
    
    def modelo_random_forest(self):
        """Modelo Random Forest para previsões complexas"""
        df = self.dados
        
        # Necessidade de fertilização baseada em nutrientes e condições
        df['necessidade_fertilizacao'] = (
            (3 - df['nutrientes_total']) * 0.4 +
            (1 - df['ph_ideal']) * 0.3 +
            (df['temp_stress']) * 0.3
        ) * 10  # Escala 0-30
        
        features = ['umidade_solo', 'ph_solo', 'temperatura', 'nitrogenio', 
                   'fosforo', 'potassio', 'chuva_mm', 'hora']
        X = df[features]
        y = df['necessidade_fertilizacao']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        modelo = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=2,
            random_state=42
        )
        
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        
        # Importância das features
        importancias = dict(zip(features, modelo.feature_importances_))
        
        resultados = {
            'modelo': 'Random Forest',
            'target': 'necessidade_fertilizacao',
            'features': features,
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred),
            'importancias': importancias,
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        self.modelos['random_forest'] = modelo
        self.resultados['random_forest'] = resultados
        
        return modelo, resultados
    
    def modelo_gradient_boosting(self):
        """Modelo Gradient Boosting para previsões avançadas"""
        df = self.dados
        
        # Índice de saúde da cultura
        df['indice_saude'] = (
            (df['ph_ideal'] * 25) +
            (np.clip((df['umidade_solo'] - 40) / 40, 0, 1) * 25) +
            ((df['nutrientes_total'] / 3) * 25) +
            ((1 - df['temp_stress']) * 25)
        )
        
        features = ['umidade_solo', 'ph_solo', 'temperatura', 'nutrientes_total', 
                   'chuva_mm', 'deficit_umidade', 'excesso_umidade']
        X = df[features]
        y = df['indice_saude']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        modelo = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            random_state=42
        )
        
        modelo.fit(X_train, y_train)
        y_pred = modelo.predict(X_test)
        
        resultados = {
            'modelo': 'Gradient Boosting',
            'target': 'indice_saude',
            'features': features,
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred),
            'y_test': y_test,
            'y_pred': y_pred
        }
        
        self.modelos['gradient_boosting'] = modelo
        self.resultados['gradient_boosting'] = resultados
        
        return modelo, resultados
    
    def validacao_cruzada(self):
        """Executa validação cruzada em todos os modelos"""
        df = self.dados
        
        # Preparar dados para validação cruzada
        modelos_cv = {
            'Linear': LinearRegression(),
            'Ridge': Ridge(),
            'Lasso': Lasso(),
            'Random Forest': RandomForestRegressor(n_estimators=50, random_state=42),
            'Gradient Boosting': GradientBoostingRegressor(n_estimators=50, random_state=42)
        }
        
        features = ['umidade_solo', 'ph_solo', 'temperatura', 'nutrientes_total', 'chuva_mm']
        X = df[features]
        y = df['irrigacao_ativa']
        
        resultados_cv = {}
        
        for nome, modelo in modelos_cv.items():
            scores = cross_val_score(modelo, X, y, cv=5, scoring='r2')
            resultados_cv[nome] = {
                'mean_r2': scores.mean(),
                'std_r2': scores.std(),
                'scores': scores
            }
        
        return resultados_cv
    
    def treinar_todos_modelos(self):
        """Treina todos os modelos e retorna comparação"""
        print("Carregando dados...")
        self.carregar_dados()
        
        print("Treinando Regressão Linear Simples...")
        self.modelo_regressao_linear_simples()
        
        print("Treinando Regressão Múltipla...")
        self.modelo_regressao_multipla()
        
        print("Treinando Regressão Polinomial...")
        self.modelo_regressao_polinomial()
        
        print("Treinando Random Forest...")
        self.modelo_random_forest()
        
        print("Treinando Gradient Boosting...")
        self.modelo_gradient_boosting()
        
        print("Executando Validação Cruzada...")
        cv_results = self.validacao_cruzada()
        
        return self.resultados, cv_results
    
    def salvar_modelos(self, diretorio="../models/modelos_treinados"):
        """Salva todos os modelos treinados"""
        import os
        os.makedirs(diretorio, exist_ok=True)
        
        # Salvar modelos individuais
        for nome, modelo in self.modelos.items():
            joblib.dump(modelo, f"{diretorio}/modelo_{nome}.pkl")
        
        # Salvar pipelines
        for nome, pipeline in self.pipelines.items():
            joblib.dump(pipeline, f"{diretorio}/pipeline_{nome}.pkl")
        
        # Salvar resultados
        import json
        with open(f"{diretorio}/resultados_parte2.json", 'w') as f:
            # Converter arrays numpy para listas para serialização JSON
            resultados_json = {}
            for nome, resultado in self.resultados.items():
                resultado_copy = resultado.copy()
                if 'y_test' in resultado_copy:
                    resultado_copy['y_test'] = resultado_copy['y_test'].tolist()
                if 'y_pred' in resultado_copy:
                    resultado_copy['y_pred'] = resultado_copy['y_pred'].tolist()
                resultados_json[nome] = resultado_copy
            
            json.dump(resultados_json, f, indent=2)
        
        print(f"Modelos salvos em: {diretorio}")

def main():
    modelos = ModelosPreditivosAvancados()
    resultados, cv_results = modelos.treinar_todos_modelos()
    
    print("\n" + "="*60)
    print("RESULTADOS DOS MODELOS PREDITIVOS")
    print("="*60)
    
    for nome, resultado in resultados.items():
        print(f"\n{resultado['modelo']}:")
        print(f"  Target: {resultado['target']}")
        print(f"  Features: {len(resultado['features'])}")
        print(f"  MAE: {resultado['mae']:.4f}")
        print(f"  RMSE: {resultado['rmse']:.4f}")
        print(f"  R²: {resultado['r2']:.4f}")
    
    print(f"\n{'='*60}")
    print("VALIDAÇÃO CRUZADA")
    print("="*60)
    
    for nome, resultado in cv_results.items():
        print(f"\n{nome}:")
        print(f"  R² médio: {resultado['mean_r2']:.4f} ± {resultado['std_r2']:.4f}")
    
    # Salvar modelos
    modelos.salvar_modelos()
    
    return modelos

if __name__ == "__main__":
    main()