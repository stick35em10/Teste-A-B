README - Teste A/B

📌 Visão Geral

Este repositório contém a implementação de um teste A/B completo, desde a coleta de dados até a análise estatística. O objetivo é comparar duas versões (A e B) de um produto, página web ou feature para determinar qual performa melhor de acordo com métricas pré-definidas.

🎯 Objetivos

Comparar a eficácia de duas variantes (A e B)

Determinar estatisticamente qual versão performa melhor

Tomar decisões baseadas em dados para implementação

📋 Estrutura do Repositório
```
/teste_ab/
│
|
├── /data/                    # Dados brutos e processados
│   ├── raw/                  # Dados originais
│   └── processed/            # Dados tratados
│
├── /notebooks/               # Jupyter notebooks de análise
│   ├── 01_data_cleaning.ipynb
│   └── 02_ab_test_analysis.ipynb
│
├── /src/                     # Código fonte
│   ├── data_processing.py    # Scripts de limpeza
│   └── ab_test.py            # Análise estatística
│
├── results/                  # Resultados e visualizações
│   ├── plots/                # Gráficos
│   └── ab_test_report.pdf    # Relatório final
│
├── requirements.txt          # Dependências do projeto
└── README.md                 # Este arquivo
```

🔧 Pré-requisitos
```
Python 3.8+
```
Bibliotecas listadas em requirements.txt

bash
Copy
pip install -r requirements.txt
🚀 Como Executar
1. Preparação dos Dados
bash
Copy
python src/data_processing.py --input data/raw/ --output data/processed/
2. Executar Análise do Teste A/B
bash
Copy
python src/ab_test.py --data data/processed/ab_test_data.csv --metric conversion_rate
3. Opções de Parâmetros
Parâmetro	Descrição	Padrão
--data	Caminho para os dados	data/processed/
--metric	Métrica a ser analisada	conversion_rate
--confidence	Nível de confiança estatística	0.95
📊 Métricas Analisadas
Taxa de conversão

Tempo na página

CTR (Click-Through Rate)

Receita por usuário

Taxa de rejeição

📈 Métodos Estatísticos
Teste de hipóteses (bicaudal)

Cálculo do valor-p

Intervalos de confiança

Tamanho do efeito (Cohen's d)

Análise de poder estatístico

📝 Exemplo de Uso
python
Copy
from src.ab_test import ABTestAnalyzer

# Carregar dados
analyzer = ABTestAnalyzer('data/processed/ab_test_results.csv')

# Rodar análise
results = analyzer.run_analysis(metric='conversion_rate')

# Visualizar resultados
analyzer.plot_results(save_path='results/plots/conversion_rate.png')
📌 Resultados Esperados
Relatório estatístico completo

Visualizações comparando os grupos

Recomendação sobre qual versão implementar

Análise de significância prática e estatística

📅 Cronograma
Fase de Preparação: 1 semana

Coleta de Dados: 2-4 semanas

Análise: 1 semana

Relatório: 3 dias

🤝 Contribuição
Faça um fork do projeto

Crie sua branch (git checkout -b feature/nova-analise)

Commit suas mudanças (git commit -m 'Adiciona nova métrica')

Push para a branch (git push origin feature/nova-analise)

Abra um Pull Request

📚 Recursos Adicionais
Guia Completo de Testes A/B

Calculadora de Tamanho de Amostra

Artigos sobre Estatística para Testes A/B

📧 Contato
Para dúvidas ou sugestões, entre em contato com:
[Seu Nome] - [seu.email@example.com] - [@seuusuario]
