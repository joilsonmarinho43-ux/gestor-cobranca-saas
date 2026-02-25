import streamlit as st
import pandas as pd
from auth import login_pagina, get_supabase

# 1. CONFIGURAÇÃO DA PÁGINA
st.set_page_config(page_title="Gestor Pro - SaaS", layout="wide", page_icon="🚀")

# 2. CONTROLE DE ACESSO
if 'logado' not in st.session_state:
    st.session_state.logado = False

if not st.session_state.logado:
    login_pagina()
else:
    supabase = get_supabase()
    user_id = st.session_state.usuario['id']

    # --- SIDEBAR ---
    with st.sidebar:
        st.title("🚀 Gestor Pro")
        st.write(f"💼 **{st.session_state.usuario['nome_empresa']}**")
        menu = st.selectbox("Navegação", ["Dashboard", "Clientes", "WhatsApp", "Configurações"])
        if st.button("Sair"):
            st.session_state.logado = False
            st.rerun()

    # --- DASHBOARD REAL ---
    if menu == "Dashboard":
        st.title("📊 Painel de Controle")
        
        try:
            # Busca dados reais filtrando pelo ID da empresa logada
            res = supabase.table("clientes").select("*").eq("empresa_id", user_id).execute()
            clientes = res.data if res.data else []
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Clientes Ativos", len([c for c in clientes if c.get('status') == 'Ativo']))
            col2.metric("Clientes Vencidos", "0") # Lógica de data em desenvolvimento
            col3.metric("Desativados", len([c for c in clientes if c.get('status') == 'Inativo']))

            st.divider()
            st.subheader("💰 Resumo Financeiro")
            ver = st.toggle("Exibir valores")
            
            # Cálculo de saldo real baseado nos clientes cadastrados
            total_receita = sum([float(c['valor_assinatura']) for c in clientes if c.get('valor_assinatura')])
            
            if ver:
                st.info(f"Receita Prevista Total: R$ {total_receita:,.2f}")
            else:
                st.info("R$ ****")
        
        except Exception as e:
            st.error(f"Erro ao carregar Dashboard: {e}")

    # --- CADASTRO DE CLIENTES REAL ---
    elif menu == "Clientes":
        st.title("👥 Gestão de Clientes")
        
        tab_cad, tab_lista = st.tabs(["Cadastrar Novo", "Lista de Clientes"])
        
        with tab_cad:
            with st.form("novo_cliente", clear_on_submit=True):
                st.subheader("Dados do Devedor")
                nome = st.text_input("Nome Completo")
                zap = st.text_input("WhatsApp (Ex: 5511999999999)")
                vencimento = st.date_input("Data de Vencimento")
                valor = st.number_input("Valor da Fatura", min_value=0.0, step=0.01)
                
                if st.form_submit_button("Salvar Cliente"):
                    try:
                        novo_cli = {
                            "empresa_id": user_id,
                            "nome": nome,
                            "whatsapp": zap,
                            "data_vencimento": str(vencimento),
                            "valor_assinatura": float(valor),
                            "status": "Ativo"
                        }
                        # Inserção no banco
                        supabase.table("clientes").insert(novo_cli).execute()
                        st.success(f"✅ Cliente {nome} cadastrado com sucesso!")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Erro técnico ao salvar: {e}")
        
        with tab_lista:
            try:
                res = supabase.table("clientes").select("*").eq("empresa_id", user_id).execute()
                if res.data:
                    df = pd.DataFrame(res.data)
                    st.dataframe(df[['nome', 'whatsapp', 'valor_assinatura', 'data_vencimento', 'status']], use_container_width=True)
                else:
                    st.write("Nenhum cliente cadastrado ainda.")
            except:
                st.error("Não foi possível carregar a lista.")

    # --- CONFIGURAÇÕES REAIS ---
    elif menu == "Configurações":
        st.title("⚙️ Configurações")
        try:
            conf_res = supabase.table("configuracoes").select("*").eq("empresa_id", user_id).execute()
            
            if not conf_res.data:
                supabase.table("configuracoes").insert({"empresa_id": user_id}).execute()
                st.rerun()
                
            config = conf_res.data[0]
            cor = st.color_picker("Cor do Painel", config.get('cor_principal', '#7030f0'))
            
            if st.button("Salvar Preferências"):
                supabase.table("configuracoes").update({"cor_principal": cor}).eq("empresa_id", user_id).execute()
                st.success("Configurações atualizadas!")
        except Exception as e:
            st.error(f"Erro ao carregar configurações: {e}")
            
