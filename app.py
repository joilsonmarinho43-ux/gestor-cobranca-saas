import streamlit as st
import os
import sys
from supabase import create_client, Client

# 1. Configuração da Página
st.set_page_config(page_title="Sol da Vida - Gestão", layout="wide", page_icon="☀️")

# 2. Ajuste de Caminho para Pastas Duplicadas
current_dir = os.path.dirname(os.path.abspath(__file__))
nested_modules_path = os.path.join(current_dir, "modules", "modules")
if nested_modules_path not in sys.path:
    sys.path.append(nested_modules_path)

# 3. Conexão ao Supabase
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

# 4. Importação dos Módulos
try:
    import clientes.gerenciar_clientes as gerenciar_clientes
    import financeiro.fluxo_caixa as fluxo_caixa
    import whatsapp.mensagens as mensagens
    import relatorios.dashboard_analitico as dashboard_analitico
except Exception as e:
    st.error(f"Erro ao carregar arquivos de módulos: {e}")

# 5. Estilização (CSS)
if os.path.exists("assets/style.css"):
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 6. Menu Lateral (CORRIGIDO PARA EVITAR ERRO DE IMAGEM)
with st.sidebar:
    try:
        # Tenta carregar a imagem. Se falhar por ser um arquivo inválido, cai no except
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=150)
        else:
            st.title("☀️ Sol da Vida")
    except Exception:
        # Caso o arquivo logo.png não seja uma imagem real, exibe apenas o texto
        st.title("☀️ Sol da Vida")
    
    st.markdown("---")
    st.title("Menu Principal")

menu = st.sidebar.radio(
    "Selecione o Módulo:",
    ["Dashboard", "Clientes", "Financeiro", "WhatsApp", "Relatórios"]
)

# 7. Navegação
if menu == "Dashboard":
    st.title("🏠 Painel Principal")
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes Ativos", "137")
    col2.metric("Vencidos", "65")
    st.line_chart({"Ativações": [10, 25, 40, 65, 90, 110, 137]})

elif menu == "Clientes":
    if 'gerenciar_clientes' in globals():
        gerenciar_clientes.show(supabase)
    else:
        st.error("Módulo de Clientes não carregado.")

elif menu == "Financeiro":
    if 'fluxo_caixa' in globals():
        fluxo_caixa.show()

elif menu == "WhatsApp":
    if 'mensagens' in globals():
        mensagens.show()

elif menu == "Relatórios":
    if 'dashboard_analitico' in globals():
        dashboard_analitico.show()
        
