import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA (Sempre o primeiro comando)
st.set_page_config(page_title="Gestor Pro", layout="wide", page_icon="🚀")

# 2. TRATAMENTO DE CAMINHOS
current_dir = os.path.dirname(__file__)
modules_path = os.path.join(current_dir, 'modules')
if modules_path not in sys.path:
    sys.path.append(modules_path)

# 3. IMPORTAÇÕES COM SEGURANÇA (Evita o erro da imagem 1001723150.png)
try:
    from auth import login_pagina, get_supabase
    from database import buscar_dados_dashboard, cadastrar_cliente
    from whatsapp import listar_fila_cobranca
    # Tenta importar api_config, se falhar, define uma função vazia
    try:
        from api_config import tela_conexao_whatsapp
    except ImportError:
        def tela_conexao_whatsapp(*args, **kwargs):
            st.warning("Módulo de configuração de API não encontrado na pasta 'modules'.")
except ImportError as e:
    st.error(f"Erro crítico ao carregar módulos básicos: {e}")
    st.info("Verifique se os arquivos auth.py, database.py e whatsapp.py estão na pasta 'modules'.")
    st.stop()

# 4. CONTROLE DE ACESSO
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login_pagina()
else:
    supabase = get_supabase()
    user_id = st.session_state.usuario['id']
    
    # Busca dados (com garantia de não ser None)
    stats = buscar_dados_dashboard(supabase, user_id)
    if not stats:
        stats = {"lista_total": [], "ativos": 0, "vencidos": 0, "inativos": 0, "receita_total": 0, "valor_vencido": 0}

    total_clientes = len(stats.get("lista_total", []))

    # --- MENU LATERAL ---
    with st.sidebar:
        st.title("🚀 GESTOR PRO")
        st.write(f"💼 **{st.session_state.usuario.get('nome_empresa', 'Minha Empresa')}**")
        menu = st.radio("Navegação", ["Dashboard", "Clientes", "WhatsApp", "Configurações"])
        st.divider()
        if st.button("Sair"):
            st.session_state.logado = False
            st.rerun()

    # --- DASHBOARD ---
    if menu == "Dashboard":
        st.title("📊 Painel de Controle")
        c1, c2, c3 = st.columns(3)
        c1.metric("Clientes em Dia", stats.get("ativos", 0))
        c2.metric("Vencidos", stats.get("vencidos", 0))
        c3.metric("Total de Clientes", total_clientes)

    # --- CLIENTES ---
    elif menu == "Clientes":
        st.title("👥 Gestão de Clientes")
        aba1, aba2 = st.tabs(["Novo Cliente", "Lista"])
        with aba1:
            with st.form("add_cli"):
                nome = st.text_input("Nome")
                zap = st.text_input("WhatsApp")
                venc = st.date_input("Vencimento")
                valor = st.number_input("Valor", min_value=0.0)
                if st.form_submit_button("Salvar"):
                    # Lógica de cadastro aqui
                    st.success("Cliente pronto para salvar!")
        with aba2:
            if total_clientes > 0:
                st.dataframe(pd.DataFrame(stats["lista_total"]), use_container_width=True)

    # --- WHATSAPP ---
    elif menu == "WhatsApp":
        st.title("📲 WhatsApp")
        listar_fila_cobranca(stats["lista_total"])

    # --- CONFIGURAÇÕES ---
    elif menu == "Configurações":
        st.title("⚙️ Configurações")
        tela_conexao_whatsapp(supabase, user_id)
    
