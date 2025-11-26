"""
FarmTech Solutions - Fase 4: Pipeline de Machine Learning
Autor: Richard Schmitz - RM567951
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

class FarmTechMLPipeline:
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.metrics = {}
        
    def carregar_dados(self, arquivo_path="../data/dados_treinamento.csv"):
        """Carrega e prepara os dados para treinamento"""
        try:
            df = pd.read_csv(arquivo_path)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Criar features adicionais
            df['hora'] = df['timestamp'].dt.hour
            df['nutrientes_total'] = df['nitrogenio'] + df['fosforo'] + df['potassio']
            
            return df
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return None
    
    def preparar_features(self, df):
        """Prepara features para os modelos"""
        features = {
            'umidade': ['temperatura', 'chuva_mm', 'hora', 'nutrientes_total'],
            'ph': ['nitrogenio', 'fosforo', 'potassio', 'temperatura'],
            'irrigacao': ['umidade_solo', 'ph_solo', 'temperatura', 'chuva_mm', 'nutrientes_total']
        }
        return features
    
    def treinar_modelo_umidade(self, df):
        """Treina modelo para prever umidade do solo"""
        features = ['temperatura', 'chuva_mm', 'hora', 'nutrientes_total']
        X = df[features]
        y = df['umidade_solo']
        
        # Dividir dados
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Normalizar dados
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Treinar modelo
        model = LinearRegression()
        model.fit(X_train_scaled, y_train)
        
        # Fazer previsões
        y_pred = model.predict(X_test_scaled)
        
        # Calcular métricas
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred)
        }
        
        # Salvar modelo e scaler
        self.models['umidade'] = model
        self.scalers['umidade'] = scaler
        self.metrics['umidade'] = metrics
        
        return model, scaler, metrics
    
    def treinar_modelo_ph(self, df):
        """Treina modelo para prever pH do solo"""
        features = ['nitrogenio', 'fosforo', 'potassio', 'temperatura']
        X = df[features]
        y = df['ph_solo']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model = LinearRegression()
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred)
        }
        
        self.models['ph'] = model
        self.scalers['ph'] = scaler
        self.metrics['ph'] = metrics
        
        return model, scaler, metrics
    
    def treinar_modelo_irrigacao(self, df):
        """Treina modelo para prever necessidade de irrigação"""
        features = ['umidade_solo', 'ph_solo', 'temperatura', 'chuva_mm', 'nutrientes_total']
        X = df[features]
        y = df['irrigacao_ativa']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        y_pred = model.predict(X_test_scaled)
        
        metrics = {
            'mae': mean_absolute_error(y_test, y_pred),
            'mse': mean_squared_error(y_test, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2': r2_score(y_test, y_pred)
        }
        
        self.models['irrigacao'] = model
        self.scalers['irrigacao'] = scaler
        self.metrics['irrigacao'] = metrics
        
        return model, scaler, metrics
    
    def salvar_modelos(self, diretorio="../models/modelos_treinados"):
        """Salva todos os modelos treinados"""
        os.makedirs(diretorio, exist_ok=True)
        
        for nome, modelo in self.models.items():
            joblib.dump(modelo, f"{diretorio}/modelo_{nome}.pkl")
            joblib.dump(self.scalers[nome], f"{diretorio}/scaler_{nome}.pkl")
        
        # Salvar métricas
        import json
        with open(f"{diretorio}/metricas.json", 'w') as f:
            json.dump(self.metrics, f, indent=2)
    
    def carregar_modelos(self, diretorio="../models/modelos_treinados"):
        """Carrega modelos salvos"""
        try:
            for nome in ['umidade', 'ph', 'irrigacao']:
                self.models[nome] = joblib.load(f"{diretorio}/modelo_{nome}.pkl")
                self.scalers[nome] = joblib.load(f"{diretorio}/scaler_{nome}.pkl")
            
            import json
            with open(f"{diretorio}/metricas.json", 'r') as f:
                self.metrics = json.load(f)
            
            return True
        except Exception as e:
            print(f"Erro ao carregar modelos: {e}")
            return False
    
    def fazer_previsao(self, tipo, dados):
        """Faz previsão usando modelo específico"""
        if tipo not in self.models:
            return None
        
        dados_scaled = self.scalers[tipo].transform([dados])
        previsao = self.models[tipo].predict(dados_scaled)[0]
        
        return previsao
    
    def executar_pipeline_completo(self):
        """Executa pipeline completo de treinamento"""
        print("Iniciando pipeline de Machine Learning...")
        
        # Carregar dados
        df = self.carregar_dados()
        if df is None:
            return False
        
        print(f"Dados carregados: {len(df)} registros")
        
        # Treinar modelos
        print("Treinando modelo de umidade...")
        self.treinar_modelo_umidade(df)
        
        print("Treinando modelo de pH...")
        self.treinar_modelo_ph(df)
        
        print("Treinando modelo de irrigação...")
        self.treinar_modelo_irrigacao(df)
        
        # Salvar modelos
        print("Salvando modelos...")
        self.salvar_modelos()
        
        # Exibir métricas
        print("\nMétricas dos Modelos:")
        for modelo, metricas in self.metrics.items():
            print(f"\n{modelo.upper()}:")
            print(f"  MAE: {metricas['mae']:.4f}")
            print(f"  MSE: {metricas['mse']:.4f}")
            print(f"  RMSE: {metricas['rmse']:.4f}")
            print(f"  R²: {metricas['r2']:.4f}")
        
        print("\nPipeline concluído com sucesso!")
        return True

def main():
    pipeline = FarmTechMLPipeline()
    pipeline.executar_pipeline_completo()

if __name__ == "__main__":
    main()