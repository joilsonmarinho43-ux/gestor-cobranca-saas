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
    st.title("Menu Principal")

menu = st.sidebar.radio(
    "Selecione o Módulo:",
    ["Dashboard", "Clientes", "Financeiro", "WhatsApp", "Relatórios"]
)

# 7. Navegação e Lógica de Negócio
if menu == "Dashboard":
    st.title("🏠 Painel Principal")
    
    if supabase:
        try:
            # Busca total de clientes
            res_clientes = supabase.table("clientes").select("id", count="exact").execute()
            total_clientes = res_clientes.count if res_clientes.count else 0
            
            # Busca faturamento previsto (soma de mensalidades dos clientes)
            res_mensalidades = supabase.table("clientes").select("valor_mensalidade").execute()
            faturamento_previsto = sum([c['valor_mensalidade'] for c in res_mensalidades.data if c['valor_mensalidade']])
            
            # Busca cobranças pendentes
            res_pendente = supabase.table("cobrancas").select("valor").eq("status", "Pendente").execute()
            total_pendente = sum([cob['valor'] for cob in res_pendente.data])

            # Exibição das Métricas Reais
            col1, col2, col3 = st.columns(3)
            col1.metric("Clientes Ativos", total_clientes)
            col2.metric("Faturamento Mensal (Previsto)", f"R$ {faturamento_previsto:,.2f}")
            col3.metric("Total a Receber (Pendentes)", f"R$ {total_pendente:,.2f}")
            
            st.divider()
            st.subheader("Evolução da Carteira")
            # Exemplo de gráfico baseado no número real de clientes
            st.area_chart({"Clientes": [0, total_clientes]})
            
        except Exception as e:
            st.warning(f"Algumas métricas ainda não podem ser calculadas: {e}")
    else:
        st.error("Banco de dados offline.")

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
    
