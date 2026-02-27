import streamlit as st
import os
from supabase import create_client, Client

# 1. Configuração de Conexão com Supabase (Secrets)
try:
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    supabase: Client = create_client(url, key)
except Exception as e:
    st.error("Erro ao carregar credenciais do Supabase. Verifique os Secrets.")

# 2. Importação dos módulos
try:
    from modules.clientes import gerenciar_clientes
    from modules.financeiro import fluxo_caixa
    from modules.whatsapp import mensagens
    from modules.relatorios import dashboard_analitico
except ImportError as e:
    st.error(f"Erro ao carregar módulos: {e}")

# ... (restante do código de navegação que já configuramos)
