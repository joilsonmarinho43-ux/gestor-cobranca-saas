import streamlit as st
from auth import login_pagina  # Ajustado para o nome da função no seu auth.py

# 1. Configuração da Página
st.set_page_config(page_title="Gestor Pro - SaaS", layout="wide", page_icon="🚀")

# 2. Injeção de CSS para o Visual Premium
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; }
    .card-ativo { background-color: #28a745; padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; }
    .card-vencido { background-color: #dc3545; padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; }
    .card-desativado { background-color: #7030f0; padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. Gerenciamento de Estado de Login
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login_pagina()
else:
    # Menu Lateral
    # Exibe o nome da empresa vindo do banco de dados (armazenado no login)
    nome_empresa = st.session_state.usuario.get('nome_empresa', 'Empresa')
    st.sidebar.write(f"💼 Empresa: **{nome_empresa}**")
    
    menu = st.sidebar.selectbox("Navegação", ["Dashboard", "Clientes", "WhatsApp", "Financeiro"])
    
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    # --- TELA: DASHBOARD ---
    if menu == "Dashboard":
        st.title("📊 Painel de Controle")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('<div class="card-ativo">👥 Clientes Ativos<br><h2>137</h2></div>', unsafe_allow_html=True)
        with col2:
            st.markdown('<div class="card-vencido">⚠️ Clientes Vencidos<br><h2>65</h2></div>', unsafe_allow_html=True)
        with col3:
            st.markdown('<div class="card-desativado">🚫 Desativados<br><h2>0</h2></div>', unsafe_allow_html=True)

        st.divider()
        
        st.subheader("💰 Saldo Líquido do Mês")
        mostrar_saldo = st.checkbox("Mostrar Saldo")
        if mostrar_saldo:
            st.info("R$ 4.580,00")
        else:
            st.info("R$ ******")

    elif menu == "Clientes":
        st.title("👥 Gestão de Clientes")
        st.write("Em breve: Integração com a tabela de devedores do Supabase.")
        
