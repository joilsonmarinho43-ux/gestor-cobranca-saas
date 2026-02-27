import streamlit as st
import pandas as pd

def show(supabase):
    st.header("👥 Gerenciar Clientes")
    
    if supabase is None:
        st.error("Erro: Conexão com o banco de dados não estabelecida.")
        return

    # --- FORMULÁRIO DE CADASTRO ---
    with st.expander("➕ Cadastrar Novo Cliente", expanded=False):
        with st.form("form_cadastro"):
            col1, col2 = st.columns(2)
            nome = col1.text_input("Nome Completo")
            whatsapp = col2.text_input("WhatsApp (com DDD)")
            
            col3, col4 = st.columns(2)
            valor = col3.number_input("Valor da Mensalidade", min_value=0.0, step=10.0, format="%.2f")
            vencimento = col4.date_input("Data de Vencimento")
            
            submit = st.form_submit_button("Salvar Cliente")
            
            if submit:
                if nome and whatsapp:
                    novo_cliente = {
                        "nome": nome,
                        "whatsapp": whatsapp,
                        "valor_mensalidade": float(valor),
                        "vencimento": str(vencimento),
                        "status": "Ativo"
                    }
                    try:
                        supabase.table("clientes").insert(novo_cliente).execute()
                        st.success(f"✅ {nome} cadastrado com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar: {e}")
                else:
                    st.warning("Preencha Nome e WhatsApp.")

    st.divider()

    # --- LISTAGEM DE CLIENTES ---
    st.subheader("Lista de Clientes")
    try:
        response = supabase.table("clientes").select("*").order("nome").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            
            # Colunas que queremos exibir (se existirem)
            colunas_alvo = ["nome", "whatsapp", "valor_mensalidade", "vencimento"]
            colunas_existentes = [c for c in colunas_alvo if c in df.columns]
            
            st.dataframe(df[colunas_existentes], use_container_width=True, hide_index=True)
        else:
            st.info("Nenhum cliente cadastrado.")
    except Exception as e:
        st.error(f"Erro ao carregar lista: {e}")
