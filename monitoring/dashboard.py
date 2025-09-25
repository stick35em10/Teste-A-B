# monitoring/dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px

def create_dashboard():
    st.title("📊 Dashboard de Testes A/B - Tempo Real")
    
    # Métricas principais
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Experimentos Ativos", "15", "+2")
    
    with col2:
        st.metric("Taxa de Conversão Média", "12.5%", "+1.2%")
    
    with col3:
        st.metric("Usuários Participantes", "45.2K", "+3.1K")
    
    # Gráfico de resultados
    results_data = get_real_time_results()
    fig = px.bar(results_data, x='variant', y='conversion_rate', 
                 color='experiment', barmode='group')
    st.plotly_chart(fig)