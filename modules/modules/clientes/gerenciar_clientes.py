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
            
            col3, col4 = col1, col2 = st.columns(2)
            # number_input garante que o valor seja numérico para o cálculo no dashboard
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
                        st.error(f"Erro ao salvar no banco: {e}")
                else:
                    st.warning("Por favor, preencha o Nome e o WhatsApp.")

    st.divider()

    # --- LISTAGEM DE CLIENTES ---
    st.subheader("Lista de Clientes")
    try:
        # Busca os dados ordenados por nome
        response = supabase.table("clientes").select("*").order("nome").execute()
        dados = response.data

        if dados:
            df = pd.DataFrame(dados)
            
            # Define as colunas que devem aparecer na tabela
            colunas_exibicao = ["nome", "whatsapp", "valor_mensalidade", "vencimento", "status"]
            # Filtra apenas as colunas que realmente existem no banco para evitar erro de index
            colunas_disponiveis = [c for c in colunas_exibicao if c in df.columns]
            
            if colunas_disponiveis:
                st.dataframe(
                    df[colunas_disponiveis],
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.error("As colunas esperadas não foram encontradas no banco de dados.")
        else:
            st.info("Nenhum cliente cadastrado ainda.")
            
    except Exception as e:
        # Resolve o erro de "not in index" verificando a existência das colunas
        st.error(f"Erro ao carregar lista: {e}")
