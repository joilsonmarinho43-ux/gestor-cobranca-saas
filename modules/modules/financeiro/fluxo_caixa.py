import streamlit as st

def show():
    st.header("💰 Fluxo de Caixa")
    st.write("Controle de faturas e recebimentos.")
    
    tab1, tab2 = st.tabs(["Faturas Pendentes", "Histórico"])
    with tab1:
        st.warning("Você tem 65 faturas vencidas.")
      
