import streamlit as st

def show():
    st.header("👥 Gerenciar Clientes")
    st.write("Aqui você poderá adicionar, editar e visualizar seus clientes.")
    
    # Métricas rápidas baseadas no sistema original
    col1, col2, col3 = st.columns(3)
    col1.metric("Ativos", "137")
    col2.metric("Vencidos", "65")
    col3.metric("Desativados", "0")
