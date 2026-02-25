import streamlit as st
from auth import autenticar

# 1. Configuração da Página (Título que aparece na aba do navegador)
st.set_page_config(page_title="Gestor Pro - SaaS", layout="wide", page_icon="🚀")

# 2. Injeção de CSS para o Visual Premium (Igual ao seu print)
st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; }
    .card-ativo { background-color: #28a745; padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; }
    .card-vencido { background-color: #dc3545; padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; }
    .card-desativado { background-color: #7030f0; padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. Verificação de Login
if autenticar():
    # Menu Lateral (Baseado nos seus prints)
    st.sidebar.write(f"💼 Empresa: **{st.session_state.empresa}**")
    menu = st.sidebar.selectbox("Navegação", ["Dashboard", "Clientes", "Planos", "WhatsApp", "Financeiro"])
    
    if st.sidebar.button("Sair"):
        st.session_state.logado = False
        st.rerun()

    # --- TELA: DASHBOARD ---
    if menu == "Dashboard":
        st.title("📊 Painel de Controle")
        
        # Grid de Cards (Igual ao seu sistema atual)
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="card-ativo">👥 Clientes Ativos<br><h2>137</h2></div>', unsafe_allow_html=True)
            
        with col2:
            st.markdown('<div class="card-vencido">⚠️ Clientes Vencidos<br><h2>65</h2></div>', unsafe_allow_html=True)
            
        with col3:
            st.markdown('<div class="card-desativado">🚫 Desativados<br><h2>0</h2></div>', unsafe_allow_html=True)

        st.divider()
        
        # Área do Financeiro com "Olhinho" para ocultar saldo
        st.subheader("💰 Saldo Líquido do Mês")
        mostrar_saldo = st.checkbox("Mostrar Saldo")
        if mostrar_saldo:
            st.info("R$ 4.580,00")
        else:
            st.info("R$ ******")

    # --- AS OUTRAS TELAS SERÃO CONSTRUÍDAS NOS PRÓXIMOS PASSOS ---
    elif menu == "Clientes":
        st.title("👥 Gestão de Clientes")
        st.write("Área para cadastro ilimitado em desenvolvimento...")

    elif menu == "WhatsApp":
        st.title("📲 Conexão WhatsApp")
        st.write("Área de pareamento de QR Code em desenvolvimento...")
  
