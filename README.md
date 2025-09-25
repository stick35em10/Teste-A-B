# 📊 Teste A/B: Análise de Conversão entre Páginas Antiga e Nova
Este repositório contém um notebook (teste_AB.ipynb) que realiza um teste A/B para comparar a taxa de conversão entre duas versões de uma página: a página antiga (controle) e a página nova (tratamento).

# 🧪 Passo 1: Definir o Problema de Negócio
## 🎯 Objetivo
Determinar se a nova página (new_page) resulta em uma taxa de conversão maior do que a página antiga (old_page).

## ❓ Hipóteses
H₀ (Hipótese Nula): A nova página não aumenta a taxa de conversão.

H₁ (Hipótese Alternativa): A nova página aumenta a taxa de conversão.

# 🧮 Passo 2: Design do Experimento
📈 Parâmetros Estatísticos

Nível de confiança: 95% (confidence_level = 0.95)

Nível de significância: 5% (significance_level = 0.05)

Poder estatístico: 80% (power = 0.80)

Efeito mínimo detectável (MDE): 2% (de 13% para 15%)

## 👥 Tamanho da Amostra
Foi calculado usando ** statsmodels.stats.power.NormalIndPower: **

python
effect_size = proportion_effectsize(0.13, 0.15)
sample_n = math.ceil(NormalIndPower().solve_power(effect_size, power=0.80, alpha=0.05))
## Resultado: 4.720 usuários por grupo.

# 🗃️ Passo 3: Coleta e Preparação dos Dados
## 📦 Dados Originais
Total de linhas: 294.478

Colunas: user_id, timestamp, group, landing_page, converted

## 🧹 Limpeza dos Dados
Remoção de usuários duplicados (1,32% dos dados)

Dados finais: 286.690 linhas

## 🎲 Amostragem
Grupo de controle: 4.720 usuários com old_page

Grupo de tratamento: 4.720 usuários com new_page

### Total da amostra: 9.440 usuários

# 📉 Passo 4: Testando as Hipóteses
📊 Taxas de Conversão

Grupo de controle (old_page): 11,55%

Grupo de tratamento (new_page): 12,90%

## 📈 Teste Estatístico
Foi utilizado um teste bicaudal para comparar as proporções, com:

α = 0,05

Poder = 0,80

# 💰 Passo 5: Conclusões e Considerações Financeiras
## ✅ Resultado
A nova página apresentou uma taxa de conversão maior (12,90% vs 11,55%). 
A diferença é estatisticamente significativa ao nível de 5%.

## 💡 Impacto Financeiro
### Suponha que:

Tráfego mensal = 100.000 usuários

Valor médio por conversão = R$ 50

Melhoria esperada:

Conversões adicionais = (0,1290 - 0,1155) × 100.000 ≈ 1.350

### Ganho mensal = 1.350 × R$ 50 = R$ 67.500

# 🚀 Recomendação
Implementar a nova página devido ao aumento significativo na taxa de conversão e retorno financeiro positivo.

# 🛠️ Tecnologias Utilizadas
Python 3

Pandas

Statsmodels

Google Colab

# 👨‍💻 Como Executar
Clone o repositório

Abra o notebook teste_AB.ipynb no Google Colab ou Jupyter

Execute as células sequencialmente

# 📄 Licença
Este projeto está sob a licença MIT.

# 📌 Contato
Se tiver dúvidas ou sugestões, entre em contato!

Feito com ❤️ e 📊 dados


