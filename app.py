import streamlit as st
from modules.clientes import gerenciar_clientes
from modules.financeiro import fluxo_caixa
from modules.whatsapp import mensagens
from modules.relatorios import dashboard_analitico

# Configuração da Página
st.set_page_config(page_title="Sol da Vida - Gestão", layout="wide")

# Carregar CSS Personalizado (Opcional, se criou o style.css)
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar - Menu Lateral
st.sidebar.image("assets/logo.png", width=150) # Certifique-se que o nome da logo está correto
st.sidebar.title("Menu Principal")

menu = st.sidebar.radio(
    "Selecione o Módulo:",
    ["Dashboard", "Clientes", "Financeiro", "WhatsApp", "Relatórios"]
)

# Lógica de Navegação
if menu == "Dashboard":
    st.title("🏠 Painel Principal")
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes Ativos", "137")
    col2.metric("Clientes Vencidos", "65")
    col3.metric("Desativados", "0")
    st.subheader("Gráfico de Atividade")
    st.line_chart({"Ativações": [10, 20, 15, 25, 30, 22, 137]})

elif menu == "Clientes":
    gerenciar_clientes.show()

elif menu == "Financeiro":
    fluxo_caixa.show()

elif menu == "WhatsApp":
    mensagens.show()

elif menu == "Relatórios":
    dashboard_analitico.show()
    
