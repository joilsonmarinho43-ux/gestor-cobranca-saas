import streamlit as st
from core.database import get_connection

def autenticar_usuario(email, senha):
    supabase = get_connection()
    
    try:
        resposta = (
            supabase
            .table("empresas")
            .select("*")
            .eq("email", email)
            .eq("senha", senha)
            .execute()
        )

        if resposta.data:
            return resposta.data[0]
        return None

    except Exception:
        return None


def login_view():
    st.title("🔐 Login - Gestor de Cobrança")

    with st.form("login_form"):
        email_input = st.text_input("E-mail")
        senha_input = st.text_input("Senha", type="password")
        botao = st.form_submit_button("Entrar")

        if botao:
            usuario = autenticar_usuario(email_input, senha_input)

            if usuario:
                st.session_state["logado"] = True
                st.session_state["usuario"] = usuario
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("E-mail ou senha incorretos.")
