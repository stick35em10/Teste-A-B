from statsmodels.stats.power import TTestIndPower, NormalIndPower
from app.helper import * 
#Conferir_as_flags_3_2
import math

passo_1()


#passo_1_1()

# print("📥 Carregar dados /br ")
# print(df_raw.head())

print("Start 📊 # **2 Design de Experimentos** /br ")
### **2.2. Parâmetros do Experimento**
n_control, n_treatment, conv_control, conv_treatment, alpha, power = definir_parametros_experimento()
from statsmodels.stats.proportion import proportion_effectsize
effect_size = proportion_effectsize(p1, p2)
print(f"O tamanho do efeito é {effect_size}")

#from statsmodels.stats.power import TTestIndPower, NormalIndPower
#effect_size = (p2 - p1) / np.sqrt(p1 * (1 - p1)) # Calculate effect size manually

# Poder estatística
#power = 0.80 # erro de oportunidade

# sample size
#AttributeError: 'NormalIndPower' object has no attribute 'solver_power'
#sample_n = sms.NormalIndPower().solver_power(
sample_n = NormalIndPower().solve_power(
    effect_size=effect_size,
    power=power,
    alpha=significance_level
) #4720
#nobs1=None,
#ratio=1 # Assuming equal sample sizes for both groups

sample_n = math.ceil(sample_n)
#sample_n # amostras para cada um dos grupos
print(f' {sample_n} amostras para cada um dos grupos, de controle e de tratamento')

print("End 📊 # **2 Design de Experimentos** /br ")

print("Start 📊 # **## 3.1.Análise descritiva dos dados** /br ")
# 2.0 Análise descritiva dos dados
print(f' A base de dados apresenta {df_raw.shape[0]} rows and {df_raw.shape[1]} columns ')

print("End 📊 # **2 Design de Experimentos** /br ")

#Verificação_dos_dados_faltantes_check_NA_3_2_()
Conferir_as_flags_3_2()

amostragem_aleatoria_grupos_Controle_Tratamento_2_2()
# ## 3.2.Verificação dos dados faltantes, check NA
### 3.2.Conferir as "flags"
## 2.2.Amostragem aleatoria dos grupos Controle e Tratamento
## 2.3 Calculo da métrica de intersse entre os Grupos (conversão de cada página)¶
# 4 Testando as hipóteses
executar_analise_completa()