import streamlit as st
import pandas as pd
from auth import login_pagina, get_supabase

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestor Pro - SaaS", layout="wide", page_icon="🚀")

# 2. CONTROLE DE ACESSO
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login_pagina()
else:
    supabase = get_supabase()
    user_id = st.session_state.usuario['id']

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🚀 Gestor Pro")
        st.write(f"💼 **{st.session_state.usuario['nome_empresa']}**")
        menu = st.selectbox("Navegação", ["Dashboard", "Clientes", "WhatsApp", "Configurações"])
        if st.button("Sair"):
            st.session_state.logado = False
            st.rerun()

    # --- DASHBOARD REAL ---
    if menu == "Dashboard":
        st.title("📊 Painel de Controle")
        
        # Busca dados reais do Supabase
        res = supabase.table("clientes").select("*").eq("empresa_id", user_id).execute()
        clientes = res.data
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Clientes Ativos", len([c for c in clientes if c['status'] == 'Ativo']))
        col2.metric("Clientes Vencidos", "0") # Lógica de data em breve
        col3.metric("Desativados", len([c for c in clientes if c['status'] == 'Inativo']))

        st.divider()
        st.subheader("💰 Saldo Líquido")
        ver = st.toggle("Exibir valores")
        st.info(f"R$ 0,00" if ver else "R$ ****")

    # --- CADASTRO DE CLIENTES REAL ---
    elif menu == "Clientes":
        st.title("👥 Gestão de Clientes")
        
        with st.form("novo_cliente", clear_on_submit=True):
            st.subheader("Cadastrar Novo Devedor")
            nome = st.text_input("Nome Completo")
            zap = st.text_input("WhatsApp (Ex: 5511999999999)")
            vencimento = st.date_input("Data de Vencimento")
            valor = st.number_input("Valor da Fatura", min_value=0.0)
            
            if st.form_submit_button("Salvar Cliente"):
                novo_cli = {
                    "empresa_id": user_id,
                    "nome": nome,
                    "whatsapp": zap,
                    "data_vencimento": str(vencimento),
                    "valor_assinatura": valor
                }
                supabase.table("clientes").insert(novo_cli).execute()
                st.success("Cliente cadastrado com sucesso!")
                st.balloons()

    # --- CONFIGURAÇÕES REAIS ---
    elif menu == "Configurações":
        st.title("⚙️ Configurações")
        # Busca configurações ou cria se não existir
        conf_res = supabase.table("configuracoes").select("*").eq("empresa_id", user_id).execute()
        
        if not conf_res.data:
            supabase.table("configuracoes").insert({"empresa_id": user_id}).execute()
            st.rerun()
            
        config = conf_res.data[0]
        cor = st.color_picker("Cor do Painel", config['cor_principal'])
        if st.button("Salvar Preferências"):
            supabase.table("configuracoes").update({"cor_principal": cor}).eq("empresa_id", user_id).execute()
            st.success("Configurações atualizadas!")
        
