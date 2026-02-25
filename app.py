import streamlit as st
import pandas as pd
from auth import login_pagina, get_supabase
from datetime import datetime

# 1. CONFIGURAÇÃO DA PÁGINA (Design Moderno e Responsivo)
st.set_page_config(page_title="Gestor Pro", layout="wide", page_icon="🚀", initial_sidebar_state="expanded")

# 2. CONTROLE DE ACESSO
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login_pagina()
else:
    supabase = get_supabase()
    user_id = st.session_state.usuario['id']
    
    # Busca dados globais para os Badges
    res_cli = supabase.table("clientes").select("id", count="exact").eq("empresa_id", user_id).execute()
    total_clientes = res_cli.count if res_cli.count else 0

    # --- 2. CABEÇALHO E PERFIL (TOP BAR) ---
    col_logo, col_nav, col_status, col_user = st.columns([2, 1, 2, 2])
    
    with col_logo:
        st.markdown("### 🚀 LOGOTIPO") # Aqui entrará a logo das configurações
    
    with col_nav:
        if st.button("🏠 Home"):
            st.session_state.menu_choice = "Dashboard"
    
    with col_status:
        st.info(f"👥 Status: {total_clientes} Clientes")
        
    with col_user:
        with st.popover(f"👤 {st.session_state.usuario['nome_empresa']}"):
            st.button("Meus Dados")
            if st.button("Sair"):
                st.session_state.logado = False
                st.rerun()

    # --- 1. ARQUITETURA DO MENU LATERAL (SIDEBAR) ---
    with st.sidebar:
        st.title("Menu de Navegação")
        
        menu = st.radio("Navegação Principal", ["Dashboard", "Clientes", "Servidores", "Planos", "Financeiro", "Integrações", "WhatsApp", "Configurações"])
        
        st.divider()
        if menu == "Clientes":
            sub_cliente = st.selectbox("Ações de Clientes", ["Gerenciar", "Adicionar", "Aniversariantes"])
        
        elif menu == "Financeiro":
            sub_fin = st.selectbox("Módulos", ["Faturas em Aberto", "Faturas Pagas", "Gerenciar Vendas", "Entradas e Saídas", "Relatórios"])
            if sub_fin == "Relatórios":
                st.write("---")
                st.caption("Sub-menu Relatórios")
                st.button("Gráfico Detalhado")
                st.button("Exportar Relatórios")
        
        elif menu == "WhatsApp":
            sub_zap = st.selectbox("Mensageria", ["Gerenciar Mensagens", "Fila de Envios", "Envios em Massa", "Parear WhatsApp"])

    # --- 3. LAYOUT DO PAINEL PRINCIPAL (DASHBOARD) ---
    if menu == "Dashboard":
        st.title("📊 Dashboard")
        
        # Cards de Status
        c1, c2, c3 = st.columns(3)
        c1.metric("Clientes Ativos", total_clientes)
        c2.markdown(f"<div style='background-color: #ff4b4b; padding: 20px; border-radius: 10px; color: white;'><strong>Clientes Vencidos</strong><br><h2>0</h2></div>", unsafe_allow_html=True)
        c3.metric("Clientes Desativados", "0")

        st.divider()
        
        # Cards Financeiros com Ocultar Valor
        st.subheader("💰 Resumo Financeiro")
        mostrar_valores = st.toggle("Exibir Saldos (Botão de Olho)", value=False)
        
        f1, f2 = st.columns(2)
        saldo_mes = "R$ 1.250,00" if mostrar_valores else "R$ ****"
        saldo_ano = "R$ 15.000,00" if mostrar_valores else "R$ ****"
        
        f1.metric("Saldo Líquido (Mês)", saldo_mes)
        f2.metric("Saldo Líquido (Ano)", saldo_ano)

        # Área de Gráfico
        st.divider()
        st.subheader("📈 Gráfico de Clientes Ativados")
        # Placeholder para o gráfico real futuramente
        st.caption(f"Período: 01/01/2026 a {datetime.now().strftime('%d/%m/%Y')}")
        st.line_chart(pd.DataFrame([1, 5, 3, 10, 7], columns=['Clientes']))

    # --- 4. CENTRAL DE CONFIGURAÇÕES ---
    elif menu == "Configurações":
        st.title("⚙️ Central do Gestor")
        
        tab_id, tab_social, tab_com, tab_regras, tab_tema = st.tabs([
            "Identidade", "Social", "Comunicação", "Regras de Negócio", "Personalização"
        ])
        
        with tab_id:
            st.text_input("Título do Sistema", value="Gestor Pro")
            st.file_uploader("Upload do Logotipo")
            st.button("Salvar Identidade")
            
        with tab_com:
            st.subheader("API WhatsApp")
            st.text_input("Token da API")
            st.text_input("Instância")
            
        with tab_tema:
            st.subheader("Cores do Painel (Admin)")
            st.color_picker("Cor Primária", "#7030f0")
            st.color_picker("Cor de Fundo", "#ffffff")
            st.subheader("Área do Cliente")
            st.color_picker("Cor Botões Cliente", "#00ff00")

    # --- ÁREA DE CLIENTES (ADICIONAR/GERENCIAR) ---
    elif menu == "Clientes":
        if sub_cliente == "Adicionar":
            st.subheader("🆕 Adicionar Novo Cliente")
            # (Aqui entra o formulário que já testamos e funcionou)
            with st.form("cad_novo"):
                nome = st.text_input("Nome")
                if st.form_submit_button("Cadastrar"):
                    st.success("Pronto para gravar no banco!")

    else:
        st.warning(f"A área {menu} está em desenvolvimento.")
    
