import streamlit as st
import pandas as pd
from auth import login_pagina, get_supabase
from datetime import datetime
# Importamos as funções dos seus novos módulos
from modules.database import buscar_dados_dashboard, cadastrar_cliente

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
    
    # Buscamos os dados usando o módulo que você criou
    stats = buscar_dados_dashboard(supabase, user_id)
    total_clientes = len(stats["lista_total"]) if stats else 0

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
        st.write(f"💼 **{st.session_state.usuario['nome_empresa']}**")
        if st.button("Sair", key="logout_top"):
            st.session_state.logado = False
            st.rerun()

    # --- SIDEBAR (ARQUITETURA DO MENU) ---
    with st.sidebar:
        st.title("Menu Lateral")
        menu = st.radio("Navegação Principal", 
                        ["Dashboard", "Clientes", "Financeiro", "WhatsApp", "Configurações"])
        
        st.divider()
        st.caption("Sistema de Gestão SaaS v1.0")

    # --- PAINEL PRINCIPAL: DASHBOARD ---
    if menu == "Dashboard":
        st.title("📊 Painel de Controle")
        
        if stats:
            # Cards de Status
            c1, c2, c3 = st.columns(3)
            c1.metric("Clientes em Dia", stats["ativos"])
            with c2:
                st.markdown(f"""
                    <div style="background-color: #ff4b4b; padding: 15px; border-radius: 10px; color: white; text-align: center;">
                        <span style="font-size: 14px; font-weight: bold;">🚨 CLIENTES VENCIDOS</span><br>
                        <span style="font-size: 28px; font-weight: bold;">{stats['vencidos']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            c3.metric("Clientes Desativados", stats["inativos"])

            st.divider()
            
            # Cards Financeiros
            st.subheader("💰 Resumo Financeiro")
            mostrar_valores = st.toggle("👁️ Exibir Saldos", value=False)
            
            f1, f2 = st.columns(2)
            f1.metric("Saldo Líquido (Mês)", f"R$ {stats['receita_total']:,.2f}" if mostrar_valores else "R$ ****")
            f2.metric("Total em Atraso", f"R$ {stats['valor_vencido']:,.2f}" if mostrar_valores else "R$ ****")

            # Área de Gráfico
            st.divider()
            st.subheader("📈 Gráfico de Clientes Ativados")
            df_grafico = pd.DataFrame(stats["lista_total"])
            if not df_grafico.empty:
                df_grafico['created_at'] = pd.to_datetime(df_grafico['created_at']).dt.date
                contagem = df_grafico.groupby('created_at').size()
                st.line_chart(contagem)
        else:
            st.error("Erro ao carregar dados do dashboard.")

    # --- PAINEL: CLIENTES ---
    elif menu == "Clientes":
        st.title("👥 Gestão de Clientes")
        aba1, aba2 = st.tabs(["Adicionar", "Gerenciar"])
        
        with aba1:
            with st.form("form_novo_cli", clear_on_submit=True):
                nome = st.text_input("Nome Completo")
                zap = st.text_input("WhatsApp (com DDD)")
                venc = st.date_input("Data de Vencimento")
                valor = st.number_input("Valor da Assinatura", min_value=0.0, step=0.01)
                
                if st.form_submit_button("Salvar Cliente"):
                    try:
                        novo_cli = {
                            "empresa_id": user_id,
                            "nome": nome,
                            "whatsapp": zap,
                            "data_vencimento": str(venc),
                            "valor_assinatura": float(valor),
                            "status": "Ativo"
                        }
                        cadastrar_cliente(supabase, novo_cli)
                        st.success("✅ Cliente cadastrado com sucesso!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Erro ao salvar: {e}")
        
        with aba2:
            if stats and stats["lista_total"]:
                df = pd.DataFrame(stats["lista_total"])
                st.dataframe(df[['nome', 'whatsapp', 'data_vencimento', 'valor_assinatura', 'status']], use_container_width=True)
            else:
                st.info("Nenhum cliente encontrado.")

    # --- PAINEL: WHATSAPP (AQUI ENTRARÁ O PRÓXIMO MÓDULO) ---
    elif menu == "WhatsApp":
        st.title("📲 Central de Mensagens")
        st.warning("Pronto para configurar o módulo de WhatsApp. Verifique se o arquivo modules/whatsapp.py já foi criado.")

    # --- PAINEL: CONFIGURAÇÕES ---
    elif menu == "Configurações":
        st.title("⚙️ Configurações do Sistema")
        st.write("Módulos de Identidade, Social e Temas em desenvolvimento.")
    
