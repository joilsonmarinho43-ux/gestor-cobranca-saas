import streamlit as st

def show():
    st.header("💰 Fluxo de Caixa")
    st.write("Controle de faturas, entradas e saídas financeiras.")
    
    tab1, tab2 = st.tabs(["Faturas em Aberto", "Faturas Pagas"])
    with tab1:
        st.info("Lista de cobranças pendentes.")
    with tab2:
        st.success("Histórico de recebimentos.")
