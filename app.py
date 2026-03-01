import streamlit as st
import os
from datetime import datetime

# Importações internas baseadas na estrutura de pastas da imagem
from core.database import Database
from services.cliente_service import ClienteService
from modules.dashboard import render_dashboard

def apply_enterprise_theme():
    """Configuração de página e tema visual."""
    st.set_page_config(
        page_title="Sol da Vida | Enterprise ERP",
        page_icon="☀️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS Profissional (Assets)
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
            html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
            .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #f0f2f6; }
            [data-testid="stSidebar"] { background-color: #f8f9fa; }
        </style>
    """, unsafe_allow_html=True)

def main():
    apply_enterprise_theme()
    
    # Inicialização do Serviço (Camada Services)
    service = ClienteService()

    # Sidebar
    with st.sidebar:
        # Verificação de logo na pasta assets
        logo_path = "assets/logo.png"
        if os.path.exists(logo_path):
            st.image(logo_path, width=160)
        else:
            st.title("☀️ Sol da Vida")
            
        st.markdown("---")
        
        # Menu de Navegação
        menu = st.radio(
            "Navegação Principal",
            ["📊 Dashboard", "👥 Clientes", "💰 Financeiro", "📈 Relatórios"],
            label_visibility="collapsed"
        )
        
        # Correção do Erro: Substituindo st.v_spacer por st.container ou markdown
        st.markdown("<br>" * 5, unsafe_allow_html=True) 
        
        st.divider()
        st.caption(f"v2.1.0-stable\n\n© {datetime.now().year} Enterprise Solutions")

    # Roteamento de Módulos (Camada Modules)
    if "Dashboard" in menu:
        render_dashboard(service)
        
    elif "Clientes" in menu:
        st.header("Gestão de Clientes")
        data = service.list_clients()
        if data.data:
            import pandas as pd
            df = pd.DataFrame(data.data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum cliente encontrado na base.")

    elif "Financeiro" in menu:
        st.header("Controle Financeiro")
        st.info("Módulo em integração com a pasta 'jobs'.")

if __name__ == "__main__":
    main()
    
