import streamlit as st
from auth import login_pagina, cadastro_pagina

# Configuração inicial da página
st.set_page_config(page_title="Gestor de Cobrança", layout="centered")

# Gerenciamento de estado de login
if 'logado' not in st.session_state:
    st.session_state.logado = False
if 'pagina' not in st.session_state:
    st.session_state.pagina = 'login'

# Navegação simples
if not st.session_state.logado:
    if st.session_state.pagina == 'login':
        login_pagina()
    elif st.session_state.pagina == 'cadastro':
        cadastro_pagina()
else:
    st.sidebar.title(f"Bem-vindo!")
    st.write("### Painel de Gestão de Clientes")
    st.info("Conexão com banco de dados ativa. Em breve listaremos seus clientes aqui.")
    
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()
      
