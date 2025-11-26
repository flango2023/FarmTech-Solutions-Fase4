"""
FarmTech Solutions - Fase 4: Sistema de Recomendações Agrícolas
Autor: Richard Schmitz - RM567951
"""

import pandas as pd
import numpy as np
import joblib
from datetime import datetime, timedelta

class SistemaRecomendacoes:
    def __init__(self):
        self.modelos = {}
        self.thresholds = {
            'umidade_min': 60,
            'umidade_max': 80,
            'ph_min': 6.0,
            'ph_max': 6.8,
            'temp_max': 30,
            'nutrientes_min': 2
        }
        
    def carregar_modelos(self, diretorio="../models/modelos_treinados"):
        """Carrega modelos treinados"""
        try:
            # Carregar modelos da Parte 1
            self.modelos['umidade'] = joblib.load(f"{diretorio}/modelo_umidade.pkl")
            self.modelos['ph'] = joblib.load(f"{diretorio}/modelo_ph.pkl")
            self.modelos['irrigacao'] = joblib.load(f"{diretorio}/modelo_irrigacao.pkl")
            
            # Carregar scalers
            self.scalers = {}
            self.scalers['umidade'] = joblib.load(f"{diretorio}/scaler_umidade.pkl")
            self.scalers['ph'] = joblib.load(f"{diretorio}/scaler_ph.pkl")
            self.scalers['irrigacao'] = joblib.load(f"{diretorio}/scaler_irrigacao.pkl")
            
            return True
        except Exception as e:
            print(f"Erro ao carregar modelos: {e}")
            return False
    
    def analisar_condicoes_atuais(self, dados_sensores):
        """Analisa condições atuais dos sensores"""
        analise = {
            'timestamp': datetime.now(),
            'condicoes': {},
            'alertas': [],
            'status_geral': 'normal'
        }
        
        # Análise da umidade
        umidade = dados_sensores.get('umidade_solo', 0)
        if umidade < self.thresholds['umidade_min']:
            analise['condicoes']['umidade'] = 'baixa'
            analise['alertas'].append(f"Umidade baixa ({umidade}%) - Irrigação necessária")
            analise['status_geral'] = 'atencao'
        elif umidade > self.thresholds['umidade_max']:
            analise['condicoes']['umidade'] = 'alta'
            analise['alertas'].append(f"Umidade alta ({umidade}%) - Risco de encharcamento")
            analise['status_geral'] = 'atencao'
        else:
            analise['condicoes']['umidade'] = 'ideal'
        
        # Análise do pH
        ph = dados_sensores.get('ph_solo', 7.0)
        if ph < self.thresholds['ph_min'] or ph > self.thresholds['ph_max']:
            analise['condicoes']['ph'] = 'inadequado'
            analise['alertas'].append(f"pH inadequado ({ph}) - Faixa ideal: 6.0-6.8")
            analise['status_geral'] = 'atencao'
        else:
            analise['condicoes']['ph'] = 'ideal'
        
        # Análise dos nutrientes
        nutrientes = (dados_sensores.get('nitrogenio', 0) + 
                     dados_sensores.get('fosforo', 0) + 
                     dados_sensores.get('potassio', 0))
        
        if nutrientes < self.thresholds['nutrientes_min']:
            analise['condicoes']['nutrientes'] = 'insuficientes'
            analise['alertas'].append(f"Nutrientes insuficientes ({nutrientes}/3)")
            analise['status_geral'] = 'atencao'
        else:
            analise['condicoes']['nutrientes'] = 'adequados'
        
        # Análise da temperatura
        temperatura = dados_sensores.get('temperatura', 25)
        if temperatura > self.thresholds['temp_max']:
            analise['condicoes']['temperatura'] = 'alta'
            analise['alertas'].append(f"Temperatura alta ({temperatura}°C) - Stress térmico")
            if analise['status_geral'] == 'normal':
                analise['status_geral'] = 'atencao'
        else:
            analise['condicoes']['temperatura'] = 'normal'
        
        return analise
    
    def recomendar_irrigacao(self, dados_sensores, previsao_clima=None):
        """Recomenda ações de irrigação"""
        recomendacao = {
            'acao': 'manter',
            'volume_litros': 0,
            'duracao_minutos': 0,
            'prioridade': 'baixa',
            'justificativa': [],
            'proxima_verificacao': datetime.now() + timedelta(hours=2)
        }
        
        umidade = dados_sensores.get('umidade_solo', 70)
        temperatura = dados_sensores.get('temperatura', 25)
        chuva_prevista = previsao_clima.get('chuva_mm', 0) if previsao_clima else 0
        
        # Calcular necessidade de irrigação
        deficit_umidade = max(0, self.thresholds['umidade_min'] - umidade)
        
        if deficit_umidade > 0 and chuva_prevista < 2:
            recomendacao['acao'] = 'irrigar'
            
            # Calcular volume baseado no déficit
            area_m2 = 1000  # Área padrão em m²
            volume_base = deficit_umidade * area_m2 * 0.01  # Litros
            
            # Ajustar por temperatura
            fator_temperatura = 1 + max(0, (temperatura - 25) * 0.02)
            volume_final = volume_base * fator_temperatura
            
            recomendacao['volume_litros'] = round(volume_final)
            recomendacao['duracao_minutos'] = round(volume_final / 10)  # 10L/min
            
            # Definir prioridade
            if deficit_umidade > 15:
                recomendacao['prioridade'] = 'alta'
                recomendacao['proxima_verificacao'] = datetime.now() + timedelta(hours=1)
            elif deficit_umidade > 5:
                recomendacao['prioridade'] = 'media'
            
            recomendacao['justificativa'].append(f"Déficit de umidade: {deficit_umidade}%")
            
            if temperatura > 28:
                recomendacao['justificativa'].append(f"Temperatura elevada: {temperatura}°C")
        
        elif chuva_prevista >= 2:
            recomendacao['acao'] = 'suspender'
            recomendacao['justificativa'].append(f"Chuva prevista: {chuva_prevista}mm")
        
        elif umidade > self.thresholds['umidade_max']:
            recomendacao['acao'] = 'suspender'
            recomendacao['justificativa'].append(f"Umidade alta: {umidade}%")
        
        return recomendacao
    
    def recomendar_fertilizacao(self, dados_sensores, historico_aplicacao=None):
        """Recomenda fertilização baseada em nutrientes e condições"""
        recomendacao = {
            'necessaria': False,
            'nutrientes': [],
            'quantidade_kg_ha': {},
            'tipo_aplicacao': 'foliar',
            'melhor_horario': '06:00-08:00',
            'justificativa': []
        }
        
        # Verificar nutrientes disponíveis
        nitrogenio = dados_sensores.get('nitrogenio', 1)
        fosforo = dados_sensores.get('fosforo', 1)
        potassio = dados_sensores.get('potassio', 1)
        ph = dados_sensores.get('ph_solo', 6.5)
        
        # Análise de necessidade por nutriente
        if not nitrogenio:
            recomendacao['necessaria'] = True
            recomendacao['nutrientes'].append('nitrogenio')
            recomendacao['quantidade_kg_ha']['nitrogenio'] = 30
            recomendacao['justificativa'].append("Deficiência de nitrogênio detectada")
        
        if not fosforo:
            recomendacao['necessaria'] = True
            recomendacao['nutrientes'].append('fosforo')
            recomendacao['quantidade_kg_ha']['fosforo'] = 20
            recomendacao['justificativa'].append("Deficiência de fósforo detectada")
        
        if not potassio:
            recomendacao['necessaria'] = True
            recomendacao['nutrientes'].append('potassio')
            recomendacao['quantidade_kg_ha']['potassio'] = 25
            recomendacao['justificativa'].append("Deficiência de potássio detectada")
        
        # Ajustar por pH
        if ph < 6.0:
            recomendacao['justificativa'].append(f"pH baixo ({ph}) - Aplicar calcário")
            recomendacao['quantidade_kg_ha']['calcario'] = 500
        elif ph > 7.0:
            recomendacao['justificativa'].append(f"pH alto ({ph}) - Reduzir aplicação")
            # Reduzir quantidades em 20%
            for nutriente in recomendacao['quantidade_kg_ha']:
                if nutriente != 'calcario':
                    recomendacao['quantidade_kg_ha'][nutriente] *= 0.8
        
        # Definir tipo de aplicação
        if len(recomendacao['nutrientes']) >= 2:
            recomendacao['tipo_aplicacao'] = 'solo'
            recomendacao['melhor_horario'] = '16:00-18:00'
        
        return recomendacao
    
    def recomendar_manejo_geral(self, dados_sensores, previsao_clima=None):
        """Recomendações gerais de manejo da cultura"""
        recomendacoes = {
            'irrigacao': self.recomendar_irrigacao(dados_sensores, previsao_clima),
            'fertilizacao': self.recomendar_fertilizacao(dados_sensores),
            'monitoramento': [],
            'acoes_preventivas': [],
            'cronograma_semanal': {}
        }
        
        # Análise das condições
        analise = self.analisar_condicoes_atuais(dados_sensores)
        
        # Recomendações de monitoramento
        if analise['status_geral'] == 'atencao':
            recomendacoes['monitoramento'].append("Aumentar frequência de monitoramento para 2x/dia")
        
        temperatura = dados_sensores.get('temperatura', 25)
        if temperatura > 32:
            recomendacoes['monitoramento'].append("Monitorar stress hídrico das plantas")
            recomendacoes['acoes_preventivas'].append("Considerar sombreamento temporário")
        
        # Ações preventivas
        umidade = dados_sensores.get('umidade_solo', 70)
        if umidade > 85:
            recomendacoes['acoes_preventivas'].append("Melhorar drenagem do solo")
            recomendacoes['acoes_preventivas'].append("Monitorar doenças fúngicas")
        
        # Cronograma semanal
        hoje = datetime.now()
        for i in range(7):
            data = hoje + timedelta(days=i)
            dia_semana = data.strftime('%A')
            
            if i == 0:  # Hoje
                recomendacoes['cronograma_semanal'][dia_semana] = "Aplicar recomendações atuais"
            elif i == 2:  # Daqui a 2 dias
                recomendacoes['cronograma_semanal'][dia_semana] = "Verificar desenvolvimento das plantas"
            elif i == 4:  # Daqui a 4 dias
                recomendacoes['cronograma_semanal'][dia_semana] = "Análise completa do solo"
            elif i == 6:  # Daqui a 6 dias
                recomendacoes['cronograma_semanal'][dia_semana] = "Planejamento da próxima semana"
        
        return recomendacoes
    
    def gerar_relatorio_recomendacoes(self, dados_sensores, previsao_clima=None):
        """Gera relatório completo de recomendações"""
        print("="*80)
        print("RELATÓRIO DE RECOMENDAÇÕES AGRÍCOLAS - FARMTECH SOLUTIONS")
        print("="*80)
        print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Cultura: Soja")
        
        # Análise das condições atuais
        analise = self.analisar_condicoes_atuais(dados_sensores)
        
        print(f"\nSTATUS GERAL: {analise['status_geral'].upper()}")
        print("-" * 40)
        
        print(f"\nCONDIÇÕES ATUAIS:")
        for parametro, status in analise['condicoes'].items():
            print(f"  {parametro.title()}: {status}")
        
        if analise['alertas']:
            print(f"\nALERTAS:")
            for alerta in analise['alertas']:
                print(f"  ⚠ {alerta}")
        
        # Recomendações detalhadas
        recomendacoes = self.recomendar_manejo_geral(dados_sensores, previsao_clima)
        
        print(f"\nRECOMENDAÇÕES DE IRRIGAÇÃO:")
        print("-" * 40)
        irrig = recomendacoes['irrigacao']
        print(f"  Ação: {irrig['acao'].upper()}")
        print(f"  Prioridade: {irrig['prioridade']}")
        
        if irrig['acao'] == 'irrigar':
            print(f"  Volume: {irrig['volume_litros']} litros")
            print(f"  Duração: {irrig['duracao_minutos']} minutos")
        
        print(f"  Próxima verificação: {irrig['proxima_verificacao'].strftime('%H:%M')}")
        
        if irrig['justificativa']:
            print(f"  Justificativa:")
            for just in irrig['justificativa']:
                print(f"    - {just}")
        
        print(f"\nRECOMENDAÇÕES DE FERTILIZAÇÃO:")
        print("-" * 40)
        fert = recomendacoes['fertilizacao']
        
        if fert['necessaria']:
            print(f"  Fertilização: NECESSÁRIA")
            print(f"  Nutrientes: {', '.join(fert['nutrientes'])}")
            print(f"  Tipo de aplicação: {fert['tipo_aplicacao']}")
            print(f"  Melhor horário: {fert['melhor_horario']}")
            
            if fert['quantidade_kg_ha']:
                print(f"  Quantidades (kg/ha):")
                for nutriente, quantidade in fert['quantidade_kg_ha'].items():
                    print(f"    {nutriente.title()}: {quantidade}")
        else:
            print(f"  Fertilização: NÃO NECESSÁRIA no momento")
        
        # Monitoramento e ações preventivas
        if recomendacoes['monitoramento']:
            print(f"\nMONITORAMENTO:")
            print("-" * 40)
            for item in recomendacoes['monitoramento']:
                print(f"  • {item}")
        
        if recomendacoes['acoes_preventivas']:
            print(f"\nAÇÕES PREVENTIVAS:")
            print("-" * 40)
            for acao in recomendacoes['acoes_preventivas']:
                print(f"  • {acao}")
        
        print(f"\nCRONOGRAMA SEMANAL:")
        print("-" * 40)
        for dia, atividade in recomendacoes['cronograma_semanal'].items():
            print(f"  {dia}: {atividade}")
        
        print("\n" + "="*80)
        
        return recomendacoes

def main():
    # Dados de exemplo dos sensores
    dados_exemplo = {
        'umidade_solo': 45.2,
        'ph_solo': 6.3,
        'nitrogenio': 1,
        'fosforo': 0,
        'potassio': 1,
        'temperatura': 32.5,
        'chuva_mm': 0.0
    }
    
    # Previsão de exemplo
    previsao_exemplo = {
        'chuva_mm': 0.5,
        'temperatura': 30.0
    }
    
    # Criar sistema de recomendações
    sistema = SistemaRecomendacoes()
    
    # Gerar relatório
    print("Gerando relatório de recomendações...")
    recomendacoes = sistema.gerar_relatorio_recomendacoes(dados_exemplo, previsao_exemplo)
    
    return sistema, recomendacoes

if __name__ == "__main__":
    main()