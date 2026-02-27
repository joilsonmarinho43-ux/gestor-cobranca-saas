import streamlit as st
import os
from supabase import create_client, Client

# 1. Configuração da Página
st.set_page_config(page_title="Sol da Vida - Gestão", layout="wide", page_icon="☀️")

# 2. Ligação ao Supabase (usando os Secrets que salvou)
@st.cache_resource
def init_connection():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

try:
    supabase = init_connection()
except Exception as e:
    st.error(f"Erro na ligação ao banco de dados: {e}")
    supabase = None

# 3. Carregar CSS
if os.path.exists("assets/style.css"):
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 4. Importação dos módulos
from modules.clientes import gerenciar_clientes
from modules.financeiro import fluxo_caixa
from modules.whatsapp import mensagens
from modules.relatorios import dashboard_analitico

# 5. Menu Lateral
if os.path.exists("assets/logo.png"):
    st.sidebar.image("assets/logo.png", width=150)
else:
    st.sidebar.title("☀️ Sol da Vida")

menu = st.sidebar.radio(
    "Selecione o Módulo:",
    ["Dashboard", "Clientes", "Financeiro", "WhatsApp", "Relatórios"]
)

# 6. Navegação (Passando o 'supabase' para os módulos)
if menu == "Dashboard":
    st.title("🏠 Painel Principal")
    col1, col2, col3 = st.columns(3)
    # Aqui depois buscaremos os números reais do banco
    col1.metric("Clientes Ativos", "137")
    col2.metric("Vencidos", "65")
    st.line_chart({"Ativações": [10, 25, 40, 65, 90, 110, 137]})

elif menu == "Clientes":
    gerenciar_clientes.show(supabase)

elif menu == "Financeiro":
    fluxo_caixa.show()

elif menu == "WhatsApp":
    mensagens.show()

elif menu == "Relatórios":
    dashboard_analitico.show()
    
