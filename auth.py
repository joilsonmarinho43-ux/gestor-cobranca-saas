import streamlit as st

def autenticar():
    if 'logado' not in st.session_state:
        st.session_state.logado = False

    if not st.session_state.logado:
        st.sidebar.title("🔐 Acesso ao Sistema")
        opcao = st.sidebar.radio("Escolha uma opção", ["Login", "Cadastrar Empresa"])

        if opcao == "Login":
            st.title("Bem-vindo ao seu Gestor")
            usuario = st.text_input("E-mail da Empresa")
            senha = st.text_input("Senha", type="password")
            
            if st.button("Entrar no Painel"):
                # No próximo passo conectaremos isso ao banco de dados
                if usuario and senha:
                    st.session_state.logado = True
                    st.session_state.empresa = usuario
                    st.success("Login realizado!")
                    st.rerun()
                else:
                    st.error("Preencha todos os campos.")

        else:
            st.title("Crie sua Conta Ilimitada")
            nome = st.text_input("Nome da Empresa")
            novo_email = st.text_input("E-mail de Acesso")
            nova_senha = st.text_input("Defina uma Senha", type="password")
            
            if st.button("Finalizar Cadastro"):
                st.balloons()
                st.success("Empresa cadastrada com sucesso! Agora faça o login.")
        
        return False
    return True
