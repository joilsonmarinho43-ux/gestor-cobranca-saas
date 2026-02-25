import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from auth import login_pagina

# --- CONFIGURAÇÃO INICIAL ---
st.set_page_config(page_title="Gestor Pro - SaaS", layout="wide", page_icon="🚀")

# CSS para melhorar o visual dos cards e da sidebar
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 24px; font-weight: bold; }
    .main-card { background-color: #f8f9fa; padding: 20px; border-radius: 15px; border: 1px solid #ddd; }
    section[data-testid="stSidebar"] { width: 320px !important; }
    </style>
""", unsafe_allow_html=True)

# --- CONTROLE DE ACESSO ---
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login_pagina()
else:
    # --- CABEÇALHO / TOP BAR ---
    col_logo, col_vazio, col_user = st.columns([2, 5, 2])
    with col_logo:
        st.subheader("🚀 GESTOR PRO")
    with col_user:
        with st.expander(f"👤 {st.session_state.usuario.get('nome_empresa', 'Minha Empresa')}"):
            if st.button("Sair"):
                st.session_state.logado = False
                st.rerun()

    st.divider()

    # --- MENU LATERAL (SIDEBAR) ---
    with st.sidebar:
        st.title("Navegação")
        menu = st.selectbox("Selecione o Módulo", [
            "Dashboard", "Clientes", "Servidores", "Planos", 
            "Financeiro", "Relatórios", "WhatsApp", "Configurações"
        ])
        
        st.info(f"Status: Conectado como Admin")

    # --- LÓGICA DAS PÁGINAS ---

    if menu == "Dashboard":
        st.title("📊 Painel de Controle")
        c1, c2, c3 = st.columns(3)
        c1.metric("Clientes Ativos", "137", "+5%")
        c2.metric("Clientes Vencidos", "65", "-2%", delta_color="inverse")
        c3.metric("Desativados", "0")

        st.divider()
        st.subheader("💰 Saldo Líquido")
        ver_valores = st.toggle("Exibir valores financeiros")
        f1, f2 = st.columns(2)
        f1.metric("Mês Atual", "R$ 4.580,00" if ver_valores else "R$ ****")
        f2.metric("Total Anual", "R$ 54.960,00" if ver_valores else "R$ ****")

        # Gráfico de exemplo
        df = pd.DataFrame(np.random.randn(20, 2), columns=['Ativos', 'Cancelados'])
        st.area_chart(df)

    elif menu == "Clientes":
        st.title("👥 Gestão de Clientes")
        acao = st.radio("Ação", ["Adicionar", "Gerenciar", "Aniversariantes"], horizontal=True)
        if acao == "Adicionar":
            with st.form("cad_cliente"):
                st.text_input("Nome do Cliente")
                st.text_input("WhatsApp (com DDD)")
                st.date_input("Vencimento")
                st.form_submit_button("Salvar Cliente")

    elif menu == "Financeiro":
        st.title("💰 Financeiro")
        tab1, tab2, tab3 = st.tabs(["Faturas", "Movimentações", "Bancos"])
        with tab3:
            st.metric("Saldo Nubank", "R$ 2.450,00")
            st.metric("Saldo Caixa", "R$ 1.130,00")

    elif menu == "WhatsApp":
        st.title("📲 WhatsApp")
        tab1, tab2 = st.tabs(["Parear Dispositivo", "Envios em Massa"])
        with tab1:
            st.warning("QR Code expirado. Gere um novo para conectar.")
            st.button("Gerar QR Code")

    elif menu == "Relatórios":
        st.title("📈 Relatórios Profissionais")
        st.selectbox("Tipo de Relatório", ["Inadimplência", "Receita por Plano", "Crescimento Mensal"])
        st.button("Exportar para Excel")

    elif menu == "Configurações":
        st.title("⚙️ Configurações do Gestor")
        with st.expander("Identidade Visual"):
            st.color_picker("Cor Principal do Painel", "#7030f0")
            st.file_uploader("Trocar Logotipo")
        with st.expander("WebHook & Integrações"):
            st.text_input("URL do WebHook")
        
