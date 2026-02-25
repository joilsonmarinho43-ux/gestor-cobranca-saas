import streamlit as st
from supabase import create_client

# Inicializa a conexão com o Supabase usando as Secrets do Streamlit
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

def login_pagina():
    st.title("🔐 Login - Gestor de Cobrança")
    
    with st.form("login_form"):
        email = st.text_input("E-mail")
        senha = st.text_input("Senha", type="password")
        botao = st.form_submit_button("Entrar")
        
        if botao:
            # Aqui simulamos o login. Em breve conectaremos com a tabela de usuários.
            if email == "admin" and senha == "admin":
                st.session_state.logado = True
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos.")

def cadastro_pagina():
    st.title("📝 Criar Conta")
    # Lógica de cadastro será implementada no próximo passo
    if st.button("Voltar para o Login"):
        st.session_state.pagina = 'login'
        st.rerun()
        
