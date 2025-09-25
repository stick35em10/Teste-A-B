from flask import Flask, render_template, request, jsonify
from datetime import datetime
import numpy as np
from scipy import stats
import math
import json

import io
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Para evitar problemas em produção
import seaborn as sns

app = Flask(__name__)

# Configuração do estilo dos gráficos
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

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

def create_conversion_comparison_chart(conv_control, conv_treatment, monthly_traffic):
    """Cria gráfico de comparação de conversões"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Gráfico 1: Taxas de conversão
    labels = ['Controle', 'Tratamento']
    conversion_rates = [conv_control * 100, conv_treatment * 100]
    colors = ['#ff6b6b', '#51cf66']
    
    bars = ax1.bar(labels, conversion_rates, color=colors, alpha=0.8)
    ax1.set_ylabel('Taxa de Conversão (%)')
    ax1.set_title('Comparação de Taxas de Conversão')
    ax1.grid(True, alpha=0.3)
    
    # Adicionar valores nas barras
    for bar, rate in zip(bars, conversion_rates):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{rate:.2f}%', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico 2: Conversões mensais
    conversions_control = monthly_traffic * conv_control
    conversions_treatment = monthly_traffic * conv_treatment
    additional_conversions = conversions_treatment - conversions_control
    
    conversions_data = [conversions_control, conversions_treatment, additional_conversions]
    conversion_labels = ['Conversões\nAtuais', 'Conversões\nEsperadas', 'Conversões\nAdicionais']
    conversion_colors = ['#ff6b6b', '#51cf66', '#339af0']
    
    bars2 = ax2.bar(conversion_labels, conversions_data, color=conversion_colors, alpha=0.8)
    ax2.set_ylabel('Número de Conversões')
    ax2.set_title('Impacto nas Conversões Mensais')
    ax2.grid(True, alpha=0.3)
    
    # Formatar eixos Y para milhares
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1000:.0f}K'))
    
    for bar, value in zip(bars2, conversions_data):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 100,
                f'{value:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    
    # Converter para base64
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
    img.seek(0)
    plt.close()
    
    return base64.b64encode(img.getvalue()).decode()

def create_revenue_chart(monthly_revenue_gain, annual_revenue_gain):
    """Cria gráfico de impacto na receita"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Gráfico 1: Receita mensal
    months = ['Mensal', 'Anual']
    revenue = [monthly_revenue_gain, annual_revenue_gain]
    colors = ['#74c0fc', '#339af0']
    
    bars = ax1.bar(months, revenue, color=colors, alpha=0.8)
    ax1.set_ylabel('Receita Adicional (R$)')
    ax1.set_title('Impacto na Receita')
    ax1.grid(True, alpha=0.3)
    
    # Formatar eixos Y para milhares
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K'))
    
    for bar, value in zip(bars, revenue):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 1000,
                f'R$ {value:,.0f}', ha='center', va='bottom', fontweight='bold')
    
    # Gráfico 2: Projeção anual
    months_projection = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 
                        'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    cumulative_revenue = [monthly_revenue_gain * (i+1) for i in range(12)]
    
    ax2.plot(months_projection, cumulative_revenue, marker='o', linewidth=2, 
             color='#ff922b', markersize=6)
    ax2.fill_between(months_projection, cumulative_revenue, alpha=0.3, color='#ffd8a8')
    ax2.set_ylabel('Receita Acumulada (R$)')
    ax2.set_title('Projeção de Receita Anual')
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K'))
    
    # Adicionar valor no último ponto
    ax2.annotate(f'R$ {cumulative_revenue[-1]:,.0f}', 
                xy=(11, cumulative_revenue[-1]), 
                xytext=(8, cumulative_revenue[-1] * 0.8),
                arrowprops=dict(arrowstyle='->', color='#ff922b'),
                fontweight='bold')
    
    plt.tight_layout()
    
    # Converter para base64
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
    img.seek(0)
    plt.close()
    
    return base64.b64encode(img.getvalue()).decode()

def create_roi_chart(monthly_revenue_gain, monthly_traffic, conversion_value):
    """Cria gráfico de ROI e sensibilidade"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Gráfico 1: ROI por valor de conversão
    conversion_values = np.linspace(conversion_value * 0.5, conversion_value * 1.5, 10)
    roi_values = [(monthly_revenue_gain / (monthly_traffic * 0.01)) * 100 for _ in conversion_values]
    
    ax1.plot(conversion_values, roi_values, marker='o', linewidth=2, color='#cc5de8')
    ax1.set_xlabel('Valor por Conversão (R$)')
    ax1.set_ylabel('ROI Estimado (%)')
    ax1.set_title('Sensibilidade do ROI')
    ax1.grid(True, alpha=0.3)
    
    # Destacar ponto atual
    current_roi = (monthly_revenue_gain / (monthly_traffic * 0.01)) * 100
    ax1.axvline(x=conversion_value, color='red', linestyle='--', alpha=0.7)
    ax1.annotate(f'ROI Atual: {current_roi:.1f}%', 
                xy=(conversion_value, current_roi),
                xytext=(conversion_value * 1.1, current_roi * 1.1),
                arrowprops=dict(arrowstyle='->', color='red'))
    
    # Gráfico 2: Impacto no tráfego
    traffic_scenarios = [monthly_traffic * 0.5, monthly_traffic, monthly_traffic * 1.5, monthly_traffic * 2]
    revenue_scenarios = [monthly_revenue_gain * factor for factor in [0.5, 1, 1.5, 2]]
    
    bars = ax2.bar([f'{t/1000:.0f}K' for t in traffic_scenarios], revenue_scenarios, 
                   color=['#ffa8a8', '#ff6b6b', '#fa5252', '#e03131'], alpha=0.8)
    ax2.set_xlabel('Tráfego Mensal')
    ax2.set_ylabel('Receita Adicional (R$)')
    ax2.set_title('Impacto do Volume de Tráfego')
    ax2.grid(True, alpha=0.3)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'R$ {x/1000:.0f}K'))
    
    for bar, value in zip(bars, revenue_scenarios):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1000,
                f'R$ {value:,.0f}', ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    
    # Converter para base64
    img = io.BytesIO()
    plt.savefig(img, format='png', dpi=100, bbox_inches='tight')
    img.seek(0)
    plt.close()
    
    return base64.b64encode(img.getvalue()).decode()

@app.route('/api/generate-charts', methods=['POST'])
def generate_charts():
    """Endpoint para gerar todos os gráficos"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
        
        conv_control = float(data.get('conv_control', 0.1155))
        conv_treatment = float(data.get('conv_treatment', 0.1290))
        monthly_traffic = int(data.get('monthly_traffic', 100000))
        conversion_value = float(data.get('conversion_value', 50.0))
        
        # Calcular métricas para os gráficos
        monthly_revenue_gain = monthly_traffic * (conv_treatment - conv_control) * conversion_value
        annual_revenue_gain = monthly_revenue_gain * 12
        
        # Gerar gráficos
        conversion_chart = create_conversion_comparison_chart(conv_control, conv_treatment, monthly_traffic)
        revenue_chart = create_revenue_chart(monthly_revenue_gain, annual_revenue_gain)
        roi_chart = create_roi_chart(monthly_revenue_gain, monthly_traffic, conversion_value)
        
        return jsonify({
            "success": True,
            "charts": {
                "conversion_comparison": conversion_chart,
                "revenue_impact": revenue_chart,
                "roi_analysis": roi_chart
            }
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro na geração de gráficos: {str(e)}"
        }), 500


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
        
        # Novos parâmetros de impacto financeiro
        monthly_traffic = int(data.get('monthly_traffic', 100000))
        conversion_value = float(data.get('conversion_value', 50.0))
        
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
        
        if monthly_traffic <= 0:
            return jsonify({
                "success": False,
                "error": "Tráfego mensal deve ser maior que 0"
            }), 400
        
        if conversion_value <= 0:
            return jsonify({
                "success": False,
                "error": "Valor por conversão deve ser maior que 0"
            }), 400
        
        # Realizar análise
        resultado = realizar_analise_ab(n_control, n_treatment, conv_control, conv_treatment, alpha)
        
        # Calcular impacto financeiro
        impacto_financeiro = calcular_impacto_financeiro(
            conv_control, 
            conv_treatment, 
            monthly_traffic, 
            conversion_value
        )
        
        return jsonify({
            "success": True,
            "result": resultado,
            "financial_impact": impacto_financeiro
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

def calcular_impacto_financeiro(conv_control, conv_treatment, monthly_traffic, conversion_value):
    """
    Calcula o impacto financeiro da implementação
    """
    try:
        # Cálculo das conversões
        conversoes_control_mensal = monthly_traffic * conv_control
        conversoes_treatment_mensal = monthly_traffic * conv_treatment
        
        # Diferença esperada
        conversoes_adicionais = conversoes_treatment_mensal - conversoes_control_mensal
        
        # Impacto financeiro
        ganho_mensal = conversoes_adicionais * conversion_value
        ganho_anual = ganho_mensal * 12
        
        # ROI aproximado (considerando custo zero para simplificar)
        roi_mensal = (ganho_mensal / (monthly_traffic * 0.01)) * 100 if monthly_traffic > 0 else 0  # ROI simplificado
        
        return {
            "monthly_traffic": monthly_traffic,
            "conversion_value": conversion_value,
            "current_monthly_conversions": round(conversoes_control_mensal),
            "expected_monthly_conversions": round(conversoes_treatment_mensal),
            "additional_conversions": round(conversoes_adicionais),
            "monthly_revenue_gain": round(ganho_mensal, 2),
            "annual_revenue_gain": round(ganho_anual, 2),
            "improvement_percentage": round(((conv_treatment/conv_control)-1)*100, 2) if conv_control > 0 else 0,
            "roi_estimate": round(roi_mensal, 2)
        }
    
    except Exception as e:
        raise ValueError(f"Erro no cálculo financeiro: {str(e)}")

@app.route('/api/financial-impact', methods=['POST'])
def financial_impact_only():
    """
    Endpoint específico para cálculo de impacto financeiro
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No JSON data provided"}), 400
        
        conv_control = float(data.get('conv_control', 0.1155))
        conv_treatment = float(data.get('conv_treatment', 0.1290))
        monthly_traffic = int(data.get('monthly_traffic', 100000))
        conversion_value = float(data.get('conversion_value', 50.0))
        
        impacto = calcular_impacto_financeiro(conv_control, conv_treatment, monthly_traffic, conversion_value)
        
        return jsonify({
            "success": True,
            "financial_impact": impacto
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Erro no cálculo financeiro: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)