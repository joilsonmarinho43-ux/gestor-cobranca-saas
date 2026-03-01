import streamlit as st
import pandas as pd

def render_dashboard(service, empresa_id):
    st.header("📊 Painel Estratégico")
    
    with st.spinner("Atualizando indicadores..."):
        clientes = service.listar_por_empresa(empresa_id)
        total_clientes = len(clientes)
        
    m1, m2, m3 = st.columns(3)
    m1.metric("Total de Clientes", total_clientes)
    m2.metric("Status do Sistema", "Online", delta="100%")
    m3.metric("Uptime", "99.9%")
    
    if clientes:
        st.subheader("Visualização Rápida")
        df = pd.DataFrame(clientes)
        st.dataframe(df[["nome", "created_at"]], use_container_width=True)
      
