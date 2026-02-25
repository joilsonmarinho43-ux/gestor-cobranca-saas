import streamlit as st
from supabase import create_client

# Inicializa a conexão com o Supabase
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

def login_pagina():
    st.title("🔐 Login - Gestor de Cobrança")
    
    with st.form("login_form"):
        email_input = st.text_input("E-mail")
        senha_input = st.text_input("Senha", type="password")
        botao = st.form_submit_button("Entrar")
        
        if botao:
            # Busca o usuário na tabela 'empresas' do seu Supabase
            try:
                resposta = supabase.table("empresas").select("*").eq("email", email_input).eq("senha", senha_input).execute()
                
                if len(resposta.data) > 0:
                    st.session_state.logado = True
                    st.session_state.usuario = resposta.data[0]
                    st.success("Login realizado com sucesso!")
                    st.rerun()
                else:
                    st.error("E-mail ou senha incorretos no banco de dados.")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
                
