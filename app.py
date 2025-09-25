from flask import Flask, render_template, request, jsonify
from datetime import datetime
import numpy as np
from scipy import stats
import math
import json
import requests
import time
from threading import Thread

app = Flask(__name__)

# Custom JSON encoder para lidar com tipos NumPy
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.integer, np.int64, np.int32)):
            return int(obj)
        elif isinstance(obj, (np.floating, np.float64, np.float32)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)

app.json_encoder = NumpyEncoder

@app.route('/ping')
def ping():
    return jsonify({"status": "pong", "message": "Service is alive"})

@app.route('/keep-alive')
def keep_alive():
    return jsonify({"status": "active", "timestamp": datetime.now().isoformat()})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({
        "status": "healthy", 
        "service": "teste-ab-api",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

def keep_alive_thread():
    """Thread para manter o serviço ativo"""
    while True:
        try:
            # Faz uma requisição para si mesmo a cada 10 minutos
            requests.get('https://teste-ab-dashboard.onrender.com/health', timeout=10)
            time.sleep(600)  # 10 minutos
        except:
            time.sleep(60)

# Nova forma de inicializar threads no Flask 2.3+
@app.before_request
def before_first_request():
    if not hasattr(app, 'keep_alive_started'):
        app.keep_alive_started = True
        if not app.debug:  # Só em produção
            thread = Thread(target=keep_alive_thread)
            thread.daemon = True
            thread.start()
        
@app.route('/api/analyze', methods=['POST'])
def analyze_ab_test():
    """
    API endpoint para análise de teste A/B
    """
    try:
        # Verifica se os dados são JSON
        if not request.is_json:
            return jsonify({
                "success": False,
                "error": "Content-Type must be application/json"
            }), 400
        
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        # Validação dos parâmetros (convertendo para tipos Python nativos)
        n_control = int(data.get('n_control', 4720))
        n_treatment = int(data.get('n_treatment', 4720))
        conv_control = float(data.get('conv_control', 0.1155))
        conv_treatment = float(data.get('conv_treatment', 0.1290))
        alpha = float(data.get('alpha', 0.05))
        
        # Validações básicas
        if n_control <= 0 or n_treatment <= 0:
            return jsonify({
                "success": False,
                "error": "Tamanho da amostra deve ser maior que 0"
            }), 400
        
        if not (0 <= conv_control <= 1) or not (0 <= conv_treatment <= 1):
            return jsonify({
                "success": False,
                "error": "Taxas de conversão devem estar entre 0 e 1"
            }), 400
        
        if not (0 < alpha < 1):
            return jsonify({
                "success": False,
                "error": "Alpha deve estar entre 0 e 1"
            }), 400
        
        # Realizar análise
        resultado = realizar_analise_ab(n_control, n_treatment, conv_control, conv_treatment, alpha)
        
        return jsonify({
            "success": True,
            "result": resultado
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro interno: {str(e)}"
        }), 500

def realizar_analise_ab(n_control, n_treatment, conv_control, conv_treatment, alpha=0.05):
    """
    Função principal de análise A/B
    """
    try:
        # Cálculo do teste Z - usando math em vez de numpy quando possível
        conversoes_control = int(n_control * conv_control)
        conversoes_treatment = int(n_treatment * conv_treatment)
        
        # Evitar divisão por zero
        if n_control == 0 or n_treatment == 0:
            raise ValueError("Tamanho da amostra não pode ser zero")
        
        p_pool = (conversoes_control + conversoes_treatment) / (n_control + n_treatment)
        se = math.sqrt(p_pool * (1 - p_pool) * (1/n_control + 1/n_treatment))
        diff = conv_treatment - conv_control
        z_stat = diff / se if se != 0 else 0
        
        # Converter resultado do scipy para tipo Python nativo
        p_value = float(2 * (1 - stats.norm.cdf(abs(z_stat)))) if se != 0 else 1.0
        
        # Intervalo de confiança
        z_value = float(stats.norm.ppf(1 - alpha/2))
        margem_erro = z_value * se
        ic_inferior = float(diff - margem_erro)
        ic_superior = float(diff + margem_erro)
        
        # Cálculo da melhoria (evitar divisão por zero)
        improvement = float(((conv_treatment/conv_control)-1)*100) if conv_control != 0 else 0.0
        
        # Garantir que todos os valores são tipos Python nativos
        significant = bool(p_value < alpha)
        
        return {
            "z_statistic": float(round(z_stat, 4)),
            "p_value": float(round(p_value, 6)),
            "significant": significant,
            "confidence_interval": [float(round(ic_inferior, 6)), float(round(ic_superior, 6))],
            "conversion_improvement": float(round(improvement, 2)),
            "recommendation": "IMPLEMENTAR" if p_value < alpha and improvement > 0 else "NÃO IMPLEMENTAR",
            "effect_size": float(round(diff, 6))
        }
    
    except Exception as e:
        raise ValueError(f"Erro no cálculo estatístico: {str(e)}")

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)