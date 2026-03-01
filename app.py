import streamlit as st
import os
from services.clientes_service import ClientesService
from modules.modules.dashboard import render_dashboard

# Configuração de Página Nível SaaS
st.set_page_config(
    page_title="Sol da Vida | Enterprise ERP",
    page_icon="☀️",
    layout="wide"
)

# Carregamento de CSS Profissional (Pasta Assets)
def load_styles():
    css_path = "assets/style.css"
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def main():
    load_styles()
    
    # Contexto do Usuário (ID da Empresa)
    # Em produção, este valor viria do auth.py
    EMPRESA_ID = "001" 
    
    try:
        service = ClientesService()
    except Exception as e:
        st.error(f"Erro ao inicializar serviços: {e}")
        return

    # Sidebar Profissional
    with st.sidebar:
        logo = "assets/logo.png"
        if os.path.exists(logo):
            st.image(logo, width=150)
        else:
            st.title("☀️ Sol da Vida")
            
        st.divider()
        menu = st.radio("Navegação", ["Dashboard", "Clientes", "Financeiro"])
        
        # Espaçamento para o rodapé
        st.markdown("<br>" * 10, unsafe_allow_html=True)
        st.caption("v2.1.0-stable | Licença Enterprise")

    # Navegação por Módulos
    if menu == "Dashboard":
        render_dashboard(service, EMPRESA_ID)
        
    elif menu == "Clientes":
        st.header("👥 Gestão de Clientes")
        
        with st.expander("➕ Cadastrar Novo Cliente"):
            nome = st.text_input("Nome Completo")
            if st.button("Salvar Registro", type="primary"):
                if nome:
                    service.criar_cliente(EMPRESA_ID, nome)
                    st.success("Cliente cadastrado com sucesso!")
                    st.rerun()

        st.divider()
        clientes = service.listar_por_empresa(EMPRESA_ID)
        if clientes:
            st.dataframe(clientes, use_container_width=True)
        else:
            st.info("Nenhum cliente encontrado na base.")

    elif menu == "Financeiro":
        st.header("💰 Controle Financeiro")
        st.info("Módulo em integração com a camada de serviços.")

if __name__ == "__main__":
    main()
        
