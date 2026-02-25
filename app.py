import streamlit as st
import pandas as pd
from auth import login_pagina, get_supabase
from datetime import datetime
# IMPORTANTE: Importamos as funções que você acabou de criar na pasta modules
from modules.database import buscar_dados_dashboard, cadastrar_cliente

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestor Pro", layout="wide", page_icon="🚀", initial_sidebar_state="expanded")

# 2. CONTROLE DE ACESSO
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login_pagina()
else:
    supabase = get_supabase()
    user_id = st.session_state.usuario['id']
    
    # Buscamos os dados usando a função da pasta modules
    stats = buscar_dados_dashboard(supabase, user_id)
    total_clientes = len(stats["lista_total"]) if stats else 0

    # --- CABEÇALHO (TOP BAR) ---
    col_logo, col_nav, col_status, col_user = st.columns([2, 1, 2, 2])
    with col_logo: st.markdown("### 🚀 LOGOTIPO")
    with col_nav:
        if st.button("🏠 Home"): st.rerun()
    with col_status: st.info(f"👥 Status: {total_clientes} Clientes")
    with col_user:
        with st.popover(f"👤 {st.session_state.usuario['nome_empresa']}"):
            if st.button("Sair"):
                st.session_state.logado = False
                st.rerun()

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("Menu")
        menu = st.radio("Navegação", ["Dashboard", "Clientes", "Financeiro", "WhatsApp", "Configurações"])

    # --- DASHBOARD ---
    if menu == "Dashboard" and stats:
        st.title("📊 Dashboard")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Clientes em Dia", stats["ativos"])
        with c2:
            st.markdown(f"""<div style="background-color: #ff4b4b; padding: 15px; border-radius: 10px; color: white; text-align: center;">
                <span style="font-size: 16px; font-weight: bold;">🚨 Clientes Vencidos</span><br>
                <span style="font-size: 32px; font-weight: bold;">{stats['vencidos']}</span>
                </div>""", unsafe_allow_html=True)
        c3.metric("Clientes Desativados", stats["inativos"])

        st.divider()
        st.subheader("💰 Resumo Financeiro")
        mostrar = st.toggle("👁️ Exibir Saldos")
        f1, f2 = st.columns(2)
        f1.metric("Saldo Líquido", f"R$ {stats['receita_total']:,.2f}" if mostrar else "R$ ****")
        f2.metric("Total em Atraso", f"R$ {stats['valor_vencido']:,.2f}" if mostrar else "R$ ****")

    # --- CLIENTES ---
    elif menu == "Clientes":
        st.title("👥 Gestão de Clientes")
        nome = st.text_input("Nome do Cliente")
        venc = st.date_input("Vencimento")
        valor = st.number_input("Valor", min_value=0.0)
        
        if st.button("Salvar"):
            novo_cli = {
                "empresa_id": user_id,
                "nome": nome,
                "data_vencimento": str(venc),
                "valor_assinatura": valor,
                "status": "Ativo"
            }
            cadastrar_cliente(supabase, novo_cli)
            st.success("Cliente salvo via Módulo Database!")
            st.balloons()
    
