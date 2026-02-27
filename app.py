import streamlit as st
import os
import sys
import pandas as pd
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
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"Erro nas credenciais do Supabase: {e}")
        return None

supabase = init_connection()

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

# 6. Menu Lateral
with st.sidebar:
    try:
        if os.path.exists("assets/logo.png"):
            st.image("assets/logo.png", width=150)
        else:
            st.title("☀️ Sol da Vida")
    except Exception:
        st.title("☀️ Sol da Vida")
    
    st.markdown("---")
    menu = st.sidebar.radio(
        "Selecione o Módulo:",
        ["Dashboard", "Clientes", "Financeiro", "WhatsApp", "Relatórios"]
    )

# 7. Navegação e Lógica Dinâmica
if menu == "Dashboard":
    st.title("🏠 Painel Principal")
    
    if supabase:
        # Inicialização de variáveis para evitar erro de definição
        total_clientes = 0
        faturamento_previsto = 0.0
        total_pendente = 0.0

        # Busca de Clientes
        try:
            res_clie = supabase.table("clientes").select("id, valor_mensalidade").execute()
            if res_clie.data:
                total_clientes = len(res_clie.data)
                faturamento_previsto = sum([float(c.get('valor_mensalidade', 0) or 0) for c in res_clie.data])
        except Exception:
            st.warning("Tabela 'clientes' não encontrada ou vazia.")

        # Busca de Cobranças Pendentes
        try:
            res_cob = supabase.table("cobrancas").select("valor").eq("status", "Pendente").execute()
            if res_cob.data:
                total_pendente = sum([float(cob.get('valor', 0) or 0) for cob in res_cob.data])
        except Exception:
            # Silencia o erro caso a tabela cobrancas ainda não tenha sido criada no SQL Editor
            total_pendente = 0.0

        # Exibição das Métricas
        col1, col2, col3 = st.columns(3)
        col1.metric("Clientes Ativos", total_clientes)
        col2.metric("Faturamento Mensal (Previsto)", f"R$ {faturamento_previsto:,.2f}")
        col3.metric("Total a Receber (Pendentes)", f"R$ {total_pendente:,.2f}")
        
        st.divider()
        
        if total_clientes > 0:
            st.subheader("Evolução da Base")
            st.area_chart({"Clientes": [0, total_clientes]})
        else:
            st.info("💡 Dica: Cadastre clientes no módulo 'Clientes' para visualizar os dados aqui.")
    else:
        st.error("Conexão com o banco de dados não configurada.")

elif menu == "Clientes":
    if 'gerenciar_clientes' in globals():
        gerenciar_clientes.show(supabase)

elif menu == "Financeiro":
    if 'fluxo_caixa' in globals():
        fluxo_caixa.show(supabase)

elif menu == "WhatsApp":
    if 'mensagens' in globals():
        mensagens.show(supabase)

elif menu == "Relatórios":
    if 'dashboard_analitico' in globals():
        dashboard_analitico.show()
    
