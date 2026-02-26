import streamlit as st
import pandas as pd
import sys
import os
from datetime import datetime

# Garante que o Python encontre a pasta 'modules'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'modules')))

# Importações após o ajuste do path
from auth import login_pagina, get_supabase
try:
    from modules.database import buscar_dados_dashboard, cadastrar_cliente
    from modules.whatsapp import listar_fila_cobranca
    # Importação do novo módulo de Configuração de API
    from modules.api_config import tela_conexao_whatsapp
except ImportError:
    # Fallback caso o Streamlit Cloud demore a reconhecer a pasta
    st.error("Erro ao carregar módulos. Verifique se a pasta 'modules' existe no GitHub.")
    st.stop()

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestor Pro", layout="wide", page_icon="🚀", initial_sidebar_state="expanded")

# 2. CONTROLE DE ACESSO
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login_pagina()
else:
    supabase = get_supabase()
    user_id = st.session_state.usuario['id']
    
    # Busca dados globais
    stats = buscar_dados_dashboard(supabase, user_id)
    total_clientes = len(stats["lista_total"]) if stats and "lista_total" in stats else 0

    # --- CABEÇALHO (TOP BAR) ---
    col_logo, col_nav, col_status, col_user = st.columns([2, 1, 2, 2])
    
    with col_logo: 
        st.markdown("### 🚀 GESTOR PRO")
    
    with col_nav:
        if st.button("🏠 Home"): 
            st.rerun()
    
    with col_status: 
        st.info(f"👥 {total_clientes} Clientes")
    
    with col_user:
        st.write(f"💼 **{st.session_state.usuario.get('nome_empresa', 'Empresa')}**")
        if st.button("Sair", key="logout_top"):
            st.session_state.logado = False
            st.rerun()

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("Menu Lateral")
        menu = st.radio("Navegação Principal", 
                        ["Dashboard", "Clientes", "Financeiro", "WhatsApp", "Configurações"])
        st.divider()
        st.caption("SaaS v1.0")

    # --- PAINEL: DASHBOARD ---
    if menu == "Dashboard":
        st.title("📊 Painel de Controle")
        if stats:
            c1, c2, c3 = st.columns(3)
            c1.metric("Clientes em Dia", stats.get("ativos", 0))
            with c2:
                st.markdown(f"""
                    <div style="background-color: #ff4b4b; padding: 15px; border-radius: 10px; color: white; text-align: center;">
                        <span style="font-size: 14px; font-weight: bold;">🚨 CLIENTES VENCIDOS</span><br>
                        <span style="font-size: 28px; font-weight: bold;">{stats.get('vencidos', 0)}</span>
                    </div>
                    """, unsafe_allow_html=True)
            c3.metric("Clientes Desativados", stats.get("inativos", 0))

            st.divider()
            st.subheader("💰 Resumo Financeiro")
            mostrar_valores = st.toggle("👁️ Exibir Saldos", value=False)
            f1, f2 = st.columns(2)
            f1.metric("Saldo Líquido (Mês)", f"R$ {stats.get('receita_total', 0):,.2f}" if mostrar_valores else "R$ ****")
            f2.metric("Total em Atraso", f"R$ {stats.get('valor_vencido', 0):,.2f}" if mostrar_valores else "R$ ****")

            st.divider()
            st.subheader("📈 Crescimento de Base")
            if total_clientes > 0:
                df_grafico = pd.DataFrame(stats["lista_total"])
                df_grafico['created_at'] = pd.to_datetime(df_grafico['created_at']).dt.date
                contagem = df_grafico.groupby('created_at').size()
                st.line_chart(contagem)
        else:
            st.error("Não foi possível carregar as métricas.")

    # --- PAINEL: CLIENTES ---
    elif menu == "Clientes":
        st.title("👥 Gestão de Clientes")
        aba1, aba2 = st.tabs(["Adicionar", "Gerenciar"])
        
        with aba1:
            with st.form("form_novo_cli", clear_on_submit=True):
                nome = st.text_input("Nome Completo")
                zap = st.text_input("WhatsApp (DDD + Número)")
                venc = st.date_input("Vencimento", value=datetime.now())
                valor = st.number_input("Valor", min_value=0.0, step=0.1)
                if st.form_submit_button("Salvar Cliente"):
                    try:
                        novo = {"empresa_id": user_id, "nome": nome, "whatsapp": zap, 
                                "data_vencimento": str(venc), "valor_assinatura": float(valor), "status": "Ativo"}
                        cadastrar_cliente(supabase, novo)
                        st.success("✅ Cadastrado!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro: {e}")
        with aba2:
            if total_clientes > 0:
                df = pd.DataFrame(stats["lista_total"])
                st.dataframe(df[['nome', 'whatsapp', 'data_vencimento', 'valor_assinatura', 'status']], use_container_width=True)

    # --- PAINEL: WHATSAPP ---
    elif menu == "WhatsApp":
        st.title("📲 Central de Mensagens")
        if total_clientes > 0:
            tab1, tab2 = st.tabs(["Fila de Cobrança", "Configurar API"])
            with tab1:
                listar_fila_cobranca(stats["lista_total"])
            with tab2:
                # Reutilizando a lógica de conexão também aqui se desejar
                tela_conexao_whatsapp(supabase, user_id)
        else:
            st.info("Nenhum cliente para cobrar.")

    # --- PAINEL: CONFIGURAÇÕES ---
    elif menu == "Configurações":
        st.title("⚙️ Configurações do Sistema")
        
        tab_perfil, tab_api, tab_pagamento = st.tabs(["Meu Perfil", "Conexão WhatsApp", "Pagamentos/Pix"])
        
        with tab_perfil:
            st.subheader("Dados da Empresa")
            st.write(f"**Empresa:** {st.session_state.usuario.get('nome_empresa')}")
            st.write(f"**ID de Usuário:** `{user_id}`")
            st.button("Alterar Senha")
            
        with tab_api:
            # Chamada do módulo de API
            tela_conexao_whatsapp(supabase, user_id)
            
        with tab_pagamento:
            st.subheader("Configuração de Recebimento")
            st.info("Aqui seu cliente configurará o Token do Mercado Pago ou Asaas.")
            st.text_input("Chave API (Produção)")
            st.text_input("Chave Pix")
            st.button("Salvar Configurações Financeiras")
