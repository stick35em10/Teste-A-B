# core/statistical_engine.py
import numpy as np
from scipy import stats
from statsmodels.stats.proportion import proportions_ztest
from datetime import datetime, timedelta

class RealTimeStatisticalEngine:
    def __init__(self):
        self.confidence_level = 0.95
    
    def calculate_conversion_rate(self, conversions: int, visitors: int) -> float:
        """Calcula taxa de conversão com correção de Laplace"""
        if visitors == 0:
            return 0.0
        return (conversions + 1) / (visitors + 2)
    
    def bayesian_analysis(self, variant_a, variant_b):
        """Análise Bayesiana para resultados mais robustos"""
        # Implementar análise Bayesiana
        pass
    
    def check_peeking(self, data, alpha=0.05):
        """Verifica se há problema de 'peeking' nos dados"""
        # Implementar correção para múltiplas comparações
        pass