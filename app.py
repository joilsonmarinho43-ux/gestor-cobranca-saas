import streamlit as st
import os

# Importação dos módulos que você criou nas pastas
try:
    from modules.clientes import gerenciar_clientes
    from modules.financeiro import fluxo_caixa
    from modules.whatsapp import mensagens
    from modules.relatorios import dashboard_analitico
except ImportError as e:
    st.error(f"Erro ao carregar módulos: {e}")

# 1. Configuração da Página
st.set_page_config(page_title="Sol da Vida - Gestão", layout="wide", page_icon="☀️")

# 2. Carregar CSS Personalizado de forma segura
if os.path.exists("assets/style.css"):
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 3. Sidebar - Menu Lateral
# Tenta carregar a logo, se não existir, exibe apenas o título
if os.path.exists("assets/logo.png"):
    st.sidebar.image("assets/logo.png", width=150)
else:
    st.sidebar.title("☀️ Sol da Vida")

st.sidebar.title("Menu Principal")

# Menu de navegação baseado no seu sistema original
menu = st.sidebar.radio(
    "Selecione o Módulo:",
    ["Dashboard", "Clientes", "Financeiro", "WhatsApp", "Relatórios"]
)

# 4. Lógica de Navegação
if menu == "Dashboard":
    st.title("🏠 Painel Principal")
    
    # Métricas principais extraídas dos seus prints
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes Ativos", "137")
    col2.metric("Clientes Vencidos", "65")
    col3.metric("Desativados", "0")
    
    st.subheader("Gráfico de Atividade")
    # Gráfico simulando as ativações mensais
    st.line_chart({"Ativações": [10, 25, 40, 65, 90, 110, 137]})

elif menu == "Clientes":
    gerenciar_clientes.show()

elif menu == "Financeiro":
    fluxo_caixa.show()

elif menu == "WhatsApp":
    mensagens.show()

elif menu == "Relatórios":
    dashboard_analitico.show()
    
