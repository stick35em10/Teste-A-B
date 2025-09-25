from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from scipy import stats
import math
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "teste-ab-api"})

@app.route('/api/analyze', methods=['POST'])
def analyze_ab_test():
    """
    API endpoint para análise de teste A/B
    """
    try:
        data = request.json
        
        # Parâmetros do teste
        n_control = data.get('n_control', 4720)
        n_treatment = data.get('n_treatment', 4720)
        conv_control = data.get('conv_control', 0.1155)
        conv_treatment = data.get('conv_treatment', 0.1290)
        alpha = data.get('alpha', 0.05)
        
        # Realizar análise
        resultado = realizar_analise_ab(n_control, n_treatment, conv_control, conv_treatment, alpha)
        
        return jsonify({
            "success": True,
            "result": resultado
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

def realizar_analise_ab(n_control, n_treatment, conv_control, conv_treatment, alpha=0.05):
    """
    Função principal de análise A/B
    """
    # Cálculo do teste Z
    conversoes_control = int(n_control * conv_control)
    conversoes_treatment = int(n_treatment * conv_treatment)
    
    p_pool = (conversoes_control + conversoes_treatment) / (n_control + n_treatment)
    se = math.sqrt(p_pool * (1 - p_pool) * (1/n_control + 1/n_treatment))
    diff = conv_treatment - conv_control
    z_stat = diff / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    # Intervalo de confiança
    z_value = stats.norm.ppf(1 - alpha/2)
    margem_erro = z_value * se
    ic_inferior = diff - margem_erro
    ic_superior = diff + margem_erro
    
    return {
        "z_statistic": round(z_stat, 4),
        "p_value": round(p_value, 6),
        "significant": p_value < alpha,
        "confidence_interval": [round(ic_inferior, 4), round(ic_superior, 4)],
        "conversion_improvement": round(((conv_treatment/conv_control)-1)*100, 2),
        "recommendation": "IMPLEMENTAR" if p_value < alpha else "NÃO IMPLEMENTAR"
    }

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)