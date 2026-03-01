import streamlit as st
import os
import sys
import pandas as pd
import webbrowser

from core.database import get_supabase

# ================================
# CONFIGURAÇÃO DA PÁGINA
# ================================

st.set_page_config(
    page_title="Sol da Vida - Gestão",
    layout="wide",
    page_icon="☀️",
    initial_sidebar_state="expanded"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ================================
# SUPABASE
# ================================

@st.cache_resource
def init_connection():
    return get_supabase()

supabase = init_connection()

# ================================
# CSS CUSTOMIZADO
# ================================

style_path = os.path.join(BASE_DIR, "assets", "style.css")

if os.path.exists(style_path):
    with open(style_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ================================
# SIDEBAR
# ================================

with st.sidebar:

    logo_path = os.path.join(BASE_DIR, "assets", "logo.png")

    if os.path.exists(logo_path):
        st.image(logo_path, width=160)
    else:
        st.title("☀️ Sol da Vida")

    st.markdown("### Sistema de Gestão")

    menu = st.radio(
        "Navegação",
        [
            "Dashboard",
            "Clientes",
            "Financeiro",
            "Relatórios"
        ]
    )

# ================================
# DASHBOARD
# ================================

if menu == "Dashboard":

    st.title("📊 Painel Estratégico")

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
    except Exception as e:
        st.error("Erro ao buscar clientes")

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

# ================================
# CLIENTES
# ================================

elif menu == "Clientes":

    st.title("👥 Gestão de Clientes")

    try:
        response = supabase.table("clientes").select("*").execute()
        data = response.data

        if not data:
            st.warning("Nenhum cliente cadastrado.")
        else:
            df = pd.DataFrame(data)

            for index, row in df.iterrows():

                with st.container():

                    col1, col2, col3, col4 = st.columns([3, 2, 2, 1])

                    col1.write(f"**{row['nome']}**")
                    col2.write(f"Plano: R$ {row.get('valor_mensal', 0)}")
                    col3.write(f"Telefone: {row.get('telefone', '')}")

                    telefone = str(row.get("telefone", "")).replace(" ", "").replace("-", "")

                    if telefone:
                        whatsapp_url = f"https://wa.me/{telefone}"
                        col4.markdown(
                            f"""
                            <a href="{whatsapp_url}" target="_blank">
                                <button style="background-color:#25D366;color:white;border:none;padding:6px 12px;border-radius:6px;">
                                    WhatsApp
                                </button>
                            </a>
                            """,
                            unsafe_allow_html=True
                        )

                    st.divider()

    except Exception as e:
        st.error("Erro ao carregar clientes")

# ================================
# FINANCEIRO
# ================================

elif menu == "Financeiro":

    st.title("💰 Controle Financeiro")

    st.info("Módulo financeiro em desenvolvimento.")

# ================================
# RELATÓRIOS
# ================================

elif menu == "Relatórios":

    st.title("📈 Relatórios Analíticos")

    st.info("Relatórios avançados em breve.")
