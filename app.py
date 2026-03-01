import streamlit as st
import os
import sys
import pandas as pd
from PIL import Image

from core.database import get_supabase

# ================================
# CONFIGURAÇÃO DA PÁGINA
# ================================

st.set_page_config(
    page_title="Sol da Vida - Gestão",
    layout="wide",
    page_icon="☀️"
)

# ================================
# DIRETÓRIO BASE
# ================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================================
# AJUSTE DE PATH DOS MODULES
# ================================

modules_path = os.path.join(BASE_DIR, "modules")

if modules_path not in sys.path:
    sys.path.append(modules_path)

# ================================
# CONEXÃO SUPABASE
# ================================

@st.cache_resource
def init_connection():
    return get_supabase()

supabase = init_connection()

# ================================
# IMPORTAÇÃO DOS MÓDULOS
# ================================

try:
    import clientes.gerenciar_clientes as gerenciar_clientes
except:
    gerenciar_clientes = None

try:
    import financeiro.fluxo_caixa as fluxo_caixa
except:
    fluxo_caixa = None

try:
    import whatsapp.mensagens as mensagens
except:
    mensagens = None

try:
    import relatorios.dashboard_analitico as dashboard_analitico
except:
    dashboard_analitico = None

# ================================
# CSS
# ================================

style_path = os.path.join(BASE_DIR, "assets", "style.css")

if os.path.exists(style_path):
    with open(style_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ================================
# SIDEBAR
# ================================

with st.sidebar:

    assets_path = os.path.join(BASE_DIR, "assets")
    logo_encontrada = False

    if os.path.exists(assets_path):
        for arquivo in os.listdir(assets_path):
            if arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
                try:
                    img = Image.open(os.path.join(assets_path, arquivo))
                    st.image(img, width=150)
                    logo_encontrada = True
                    break
                except:
                    pass

    if not logo_encontrada:
        st.title("☀️ Sol da Vida")

    st.markdown("---")

    menu = st.radio(
        "Menu",
        [
            "Dashboard",
            "Clientes",
            "Financeiro",
            "WhatsApp",
            "Relatórios"
        ]
    )

# ================================
# DASHBOARD
# ================================

if menu == "Dashboard":

    st.title("🏠 Painel Principal")

    total_clientes = 0
    faturamento_previsto = 0
    total_pendente = 0

    try:
        clientes = supabase.table("clientes").select("*").execute()

        if clientes.data:
            total_clientes = len(clientes.data)

            faturamento_previsto = sum(
                float(c.get("valor_mensal", 0) or 0)
                for c in clientes.data
            )
    except:
        pass

    try:
        cobrancas = (
            supabase
            .table("parcelas")
            .select("valor")
            .eq("status", "pendente")
            .execute()
        )

        if cobrancas.data:
            total_pendente = sum(
                float(c.get("valor", 0) or 0)
                for c in cobrancas.data
            )
    except:
        pass

    col1, col2, col3 = st.columns(3)

    col1.metric("Clientes Ativos", total_clientes)
    col2.metric("Faturamento Previsto", f"R$ {faturamento_previsto:,.2f}")
    col3.metric("Total em Aberto", f"R$ {total_pendente:,.2f}")

    st.divider()

    if total_clientes > 0:
        st.subheader("Crescimento de Clientes")
        st.area_chart({"Clientes": [0, total_clientes]})

# ================================
# CLIENTES
# ================================

elif menu == "Clientes":

    if gerenciar_clientes:
        gerenciar_clientes.show(supabase)
    else:
        st.warning("Módulo de clientes não encontrado.")

# ================================
# FINANCEIRO
# ================================

elif menu == "Financeiro":

    if fluxo_caixa:
        fluxo_caixa.show(supabase)
    else:
        st.warning("Módulo financeiro não encontrado.")

# ================================
# WHATSAPP
# ================================

elif menu == "WhatsApp":

    if mensagens:
        mensagens.show(supabase)
    else:
        st.warning("Módulo WhatsApp não encontrado.")

# ================================
# RELATÓRIOS
# ================================

elif menu == "Relatórios":

    if dashboard_analitico:
        dashboard_analitico.show()
    else:
        st.warning("Módulo de relatórios não encontrado.")
