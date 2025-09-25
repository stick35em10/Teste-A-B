import numpy as np
import pandas as pd

# =====================
# 1. TESTE Z PARA PROPORÇÕES
# =====================

def realizar_teste_ab(n_control, n_treatment, conv_control, conv_treatment, alpha=0.05):
    """
    Realiza teste A/B para diferença de proporções
    """
    print("🎯 TESTE A/B - DIFERENÇA DE PROPORÇÕES")
    print("=" * 50)

    # Calcular número de conversões
    conversoes_control = int(n_control * conv_control)
    conversoes_treatment = int(n_treatment * conv_treatment)

    print(f"📊 Dados do Experimento:")
    print(f"   Grupo Controle: {conversoes_control}/{n_control} = {conv_control:.3%}")
    print(f"   Grupo Tratamento: {conversoes_treatment}/{n_treatment} = {conv_treatment:.3%}")
    print(f"   Diferença absoluta: {(conv_treatment - conv_control):.3%}")
    print(f"   Melhoria relativa: {((conv_treatment/conv_control)-1):.2%}")
    print()

    # Executar teste Z para duas proporções
    count = np.array([conversoes_control, conversoes_treatment])
    nobs = np.array([n_control, n_treatment])
    
    from statsmodels.stats.proportion import proportions_ztest
    # Teste bicaudal (alternative='two-sided')
    z_stat, p_value = proportions_ztest(count, nobs, alternative='two-sided')

    print("📈 RESULTADOS DO TESTE ESTATÍSTICO")
    print("=" * 50)
    print(f"   Estatística Z: {z_stat:.4f}")
    print(f"   Valor-p: {p_value:.6f}")
    print(f"   Nível de significância (α): {alpha}")
    print()

    # Interpretação do resultado
    if p_value < alpha:
        print("✅ RESULTADO: SIGNIFICATIVO")
        print("   Rejeitamos a hipótese nula (H₀)")
        print("   A diferença é estatisticamente significativa!")
    else:
        print("❌ RESULTADO: NÃO SIGNIFICATIVO")
        print("   Não rejeitamos a hipótese nula (H₀)")
        print("   A diferença pode ser devido ao acaso")

    return z_stat, p_value

# =====================
# 2. INTERVALO DE CONFIANÇA
# =====================
from scipy import stats
def calcular_intervalo_confianca(n_control, n_treatment, conv_control, conv_treatment, conf_level=0.95):
    """
    Calcula o intervalo de confiança para a diferença
    """
    print("\n🎯 INTERVALO DE CONFIANÇA")
    print("=" * 50)

    # Diferença observada
    diff = conv_treatment - conv_control

    # Erro padrão da diferença
    se_control = np.sqrt(conv_control * (1 - conv_control) / n_control)
    se_treatment = np.sqrt(conv_treatment * (1 - conv_treatment) / n_treatment)
    se_diff = np.sqrt(se_control**2 + se_treatment**2)

    # Valor Z para o nível de confiança
    z_value = stats.norm.ppf(1 - (1 - conf_level) / 2)

    # Intervalo de confiança
    margem_erro = z_value * se_diff
    ic_inferior = diff - margem_erro
    ic_superior = diff + margem_erro

    print(f"   Diferença observada: {diff:.4f} ({diff:.3%})")
    print(f"   Erro padrão: {se_diff:.6f}")
    print(f"   Intervalo de {conf_level:.0%} confiança:")
    print(f"   [{ic_inferior:.4f}, {ic_superior:.4f}]")
    print(f"   Ou: [{ic_inferior:.3%}, {ic_superior:.3%}]")

    return (ic_inferior, ic_superior)

# =====================
# 3. PODER ESTATÍSTICO
# =====================

def analisar_poder_estatistico(n_control, n_treatment, conv_control, conv_treatment, alpha=0.05):
    """
    Analisa o poder estatístico do teste
    """
    print("\n🎯 ANÁLISE DO PODER ESTATÍSTICO")
    print("=" * 50)

    # Tamanho do efeito
    effect_size = proportion_effectsize(conv_control, conv_treatment)

    # Calcular poder estatístico
    power_analysis = NormalIndPower()
    poder_calculado = power_analysis.solve_power(
        effect_size=effect_size,
        nobs1=n_control,
        alpha=alpha,
        power=None
    )

    print(f"   Tamanho do efeito: {effect_size:.4f}")
    print(f"   Poder estatístico calculado: {poder_calculado:.3f}")

    # Verificar se o poder é adequado
    if poder_calculado >= 0.8:
        print("   ✅ Poder estatístico adequado (≥ 0.8)")
    else:
        print("   ⚠️  Poder estatístico insuficiente (< 0.8)")

    return poder_calculado

# =====================
# 4. TAMANHO MÍNIMO DETECTÁVEL (MDE)
# =====================

# nivel de confianca
confidence_level    = 0.95
# nivel de significancia
significance_level  = 0.05

# conversao da pagina actual e da nova pagina
p1 = 0.13 # medido
p2 = 0.15 # esperado pelo time de negocio
#n_control, n_treatment, conv_control, conv_treatment, alpha, power = definir_parametros_experimento()

def definir_parametros_experimento(confidence_level = confidence_level, significance_level = significance_level, n_control    = 100, n_treatment = 100, conv_control = p1, conv_treatment = p2, alpha=0.05, power=0.80):
    #confidence_level = 0.95, significance_level = 0.05, n_control    = 100, n_treatment = 100, conv_control = p1, conv_treatment = p2, alpha=0.05, power=0.80)
    return n_control, n_treatment, conv_control, conv_treatment, alpha, power


n_control, n_treatment, conv_control, conv_treatment, alpha, power = definir_parametros_experimento()
conversion_control, conversion_treatment = conv_control, conv_treatment

def calcular_mde(n_control, n_treatment, conv_control, alpha=0.05, power=0.80):
    """
    Calcula o efeito mínimo detectável (MDE)
    """
    print("\n🎯 EFEITO MÍNIMO DETECTÁVEL (MDE)")
    print("=" * 50)

    power_analysis = NormalIndPower()

    # Calcular MDE para o poder desejado
    effect_size_required = power_analysis.solve_power(
        nobs1=n_control,
        alpha=alpha,
        power=power,
        effect_size=None
    )

    # Converter effect size de volta para diferença de proporções
    # Para proporções: effect_size = 2 * arcsin(sqrt(p1)) - 2 * arcsin(sqrt(p2))
    # Podemos aproximar invertendo a fórmula
    from math import sin, asin, sqrt

    # Aproximação do MDE
    arcsin_p1 = 2 * asin(sqrt(conv_control))
    arcsin_p2_required = arcsin_p1 + effect_size_required
    p2_required = (sin(arcsin_p2_required / 2)) ** 2
    mde_absoluto = p2_required - conv_control

    print(f"   Conversão base (controle): {conv_control:.3%}")
    print(f"   MDE absoluto: {mde_absoluto:.4f} ({mde_absoluto:.3%})")
    print(f"   Efeito observado: {conversion_treatment - conversion_control:.4f} ({(conversion_treatment - conversion_control):.3%})")

    # Comparar com efeito observado
    efeito_observado = conversion_treatment - conversion_control
    if efeito_observado >= mde_absoluto:
        print("   ✅ Efeito observado maior que MDE")
    else:
        print("   ⚠️  Efeito observado menor que MDE")

    return mde_absoluto

# =====================
# 5. EXECUÇÃO COMPLETA
# =====================

def executar_analise_completa():
    """
    Executa toda a análise estatística do teste A/B
    """
    
    print("🧪 ANÁLISE ESTATÍSTICA COMPLETA DO TESTE A/B")
    print("=" * 60)
    
    # 1. Teste de hipóteses
    z_stat, p_value = realizar_teste_ab(
        n_control, n_treatment,
        conversion_control, conversion_treatment,
        alpha
    )

    # 2. Intervalo de confiança
    ic = calcular_intervalo_confianca(
        n_control, n_treatment,
        conversion_control, conversion_treatment
    )

    # 3. Poder estatístico
    poder = analisar_poder_estatistico(
        n_control, n_treatment,
        conversion_control, conversion_treatment,
        alpha
    )

    # 4. MDE
    mde = calcular_mde(n_control, n_treatment, conversion_control, alpha, power)

    # 5. Resumo executivo
    print("\n" + "🎯 RESUMO EXECUTIVO" + "=" * 50)

    efeito_observado = conversion_treatment - conversion_control
    significativo = p_value < alpha
    poder_adequado = poder >= 0.8

    print(f"📊 Resultado Principal:")
    print(f"   • Diferença: {efeito_observado:.3%} ({conversion_treatment/conversion_control-1:+.1%})")
    print(f"   • Significativo: {'✅ SIM' if significativo else '❌ NÃO'}")
    print(f"   • Poder adequado: {'✅ SIM' if poder_adequado else '❌ NÃO'}")
    print(f"   • Valor-p: {p_value:.6f}")

    print(f"\n💡 Recomendação:")
    if significativo and poder_adequado:
        print("   ✅ IMPLEMENTAR - Resultado confiável e significativo")
    elif significativo and not poder_adequado:
        print("   ⚠️  CAUTELA - Significativo mas poder insuficiente")
    elif not significativo and poder_adequado:
        print("   ❌ NÃO IMPLEMENTAR - Diferença não significativa")
    else:
        print("   🔄 MAIS DADOS - Poder insuficiente para conclusão")

    return {
        'z_statistic': z_stat,
        'p_value': p_value,
        'confidence_interval': ic,
        'power': poder,
        'mde': mde,
        'significant': significativo,
        'adequate_power': poder_adequado
    }

##📥 Carregar dados  **1.0. Load data**
path_ab_data ='data/raw/ab_data_.csv' #data/raw/ab_data_.csv'
df_raw=pd.read_csv(path_ab_data)

def passo_1():
    print("# 🧪 Passo 1: Definir o Problema de Negócio ")
    print("## 🎯 Objetivo ")
    print("Determinar se a nova página (new_page) resulta em uma taxa de conversão maior do que a página antiga (old_page).")
    print("## 📊 H₀ (Hipótese Nula): A nova página não aumenta a taxa de conversão. ")
    print("## 📊 H₁ (Hipótese Alternativa): A nova página aumenta a taxa de conversão.")
    print("")
    
from statsmodels.stats.proportion import proportion_effectsize

effect_size = proportion_effectsize(p1, p2)
# effect_size = sms.proportion_effectsize(p1, p2) #This function might be deprecated
# Instead, try using the following:
from statsmodels.stats.power import TTestIndPower, NormalIndPower

def passo_1_1():
    sample_n = NormalIndPower().solve_power(
        effect_size=effect_size,
        power = power, #definir_parametros_experimento() #power,
        #_ ,_ ,_ ,_ ,_ , power = definir_parametros_experimento() #power,
        alpha=significance_level
    ) #4720
    #nobs1=None,
    #ratio=1 # Assuming equal sample sizes for both groups

    sample_n = math.ceil(sample_n)
    #sample_n # amostras para cada um dos grupos
    print(f' {sample_n} amostras para cada um dos grupos, de controle e de tratamento')
    print("")
    return sample_n
# from main import df_raw
def Verificação_dos_dados_faltantes_check_NA_3_2_():
    print("## Start 3.2.Verificação dos dados faltantes, check NA")
    # Interpretação do resultado
    
    
    if df_raw.isna().sum().sum()==0:
        print("✅ Os dados não apresentam dados faltantes")
        print(" Podemos proseguir")
        print("")
        #print("   A diferença é estatisticamente significativa!")
        #elif : 
    else:
        print(f'❌ Os dados tem dados faltantes, um total de {df_raw.isna().sum().sum()}')
        print(" Devemos analisar antes de prosseguir")
        print({df_raw.isna().sum()})
        print("")
    #print("   A diferença pode ser devido ao acaso")
    print("## End 3.2.Verificação dos dados faltantes, check NA")
    print("")
    
def Conferir_as_flags_3_2():
    print("  ## 3.2.Conferir_as_flags_3.2.")
    #df_raw[['user_id','group','landing_page']].groupby(['user_id']).count().reset_index().query("group == 'control' and (landing_page == 'new_page' or landing_page == 'old_page')")
    linhas_com_duplicação=len(df_raw[['user_id','group','landing_page']].groupby(['user_id']).count().reset_index().query('landing_page >1'))
    percentagem_duplicado=linhas_com_duplicação/df_raw.shape[0]

    # Interpretação do resultado
    # df1 =
    if percentagem_duplicado < 0.05:
        print(f'Dados iniciais {df_raw.shape}')
        print()
        print(f'✅ A percentagem dos dados duplicados são inferiores que 5%, isto é com {round(percentagem_duplicado*100,2)} % de linhas duplicadas')
        print('portando são considerados poucos dados duplicados e podemos deletar os dados duplicados ')
        df_user_delete = df_raw[['user_id','group','landing_page']].groupby(['user_id']).count().reset_index().query('landing_page >1')['user_id']
        #data without duplicated
        #print("data without duplicated")
        print()
        df1 = df_raw[~df_raw['user_id'].isin(df_user_delete)] # .groupby(['user_id']).count().reset_index().query('landing_page >1')
        # Gravar em CSV
        df1.to_csv('data/processed/df1.csv', index=False)
        #df1.head()
        # todo: faser uma função para verificar se existe dados duplicados, para usarmos e voltar a chamar para confirmar se ficou algum dado duplicado
        print(f'Total de dados apagagos {df_raw.shape[0]-df1.shape[0]}')
        print()
        print(df1.head())
        print()
        #print(df1.shape)
        print(f'Dados finais {df1.shape}')
        #print(" Podemos proseguir")
        #print("   A diferença é estatisticamente significativa!")
        #elif : 
        #return df1
    else:
        print(f'❌ A percentagem dos dados duplicados é superior que 5%, com {round(percentagem_duplicado*100,2)} % de linhas duplicadas')
        print('portando são considerados muitos dados duplicados e devemos tratar os dados duplicados ')

def amostragem_aleatoria_grupos_Controle_Tratamento_2_2():
    print("")
    print("2.2.Amostragem aleatoria dos grupos Controle e Tratamento")
    ### 2.2.Amostragem aleatoria dos grupos Controle e Tratamento
    # Control Group
    
    path_ab_data ='data/processed/df1.csv' #data/raw/ab_data_.csv'
    df1=pd.read_csv(path_ab_data) #'/content/drive/MyDrive/Colab Notebooks/Teste AB/dataset/ab_data.crdownload')
    
    #df1=.to_csv(
    #sample_n=passo_1_1()
    from main import sample_n
    df_control_sample = df1[df1['group'] == 'control'].sample(n=sample_n, random_state=42)
    print('Size of Control or old_page Group: {}'.format(df_control_sample.shape[0]))

    # Treatment Group
    df_treatment_sample = df1[df1['group'] == 'treatment'].sample(n=sample_n, random_state=42)
    print('Size of Treatment or new_page Group: {}'.format(df_treatment_sample.shape[0]))

    # Total sample Size
    df_ad = pd.concat([df_control_sample, df_treatment_sample], axis=0)
    print("Total sample Size",df_ad.shape[0])