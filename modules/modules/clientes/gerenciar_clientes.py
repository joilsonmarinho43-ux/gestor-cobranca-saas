import streamlit as st
import pandas as pd

def show(supabase):
    st.header("👥 Gerenciar Clientes")
    
    if supabase is None:
        st.error("Banco de dados não configurado.")
        return

    # Botão para adicionar novo (apenas visual por enquanto)
    if st.button("➕ Novo Cliente"):
        st.info("Funcionalidade de cadastro será implementada no próximo passo.")

    st.divider()

    # Procurar dados no Supabase
    try:
        # Tenta selecionar todos os dados da tabela 'clientes'
        response = supabase.table("clientes").select("*").execute()
        dados = response.data

        if dados:
            df = pd.DataFrame(dados)
            st.subheader("Lista de Clientes Cadastrados")
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Nenhum cliente encontrado na tabela 'clientes'.")
            
    except Exception as e:
        st.warning("Aviso: A tabela 'clientes' ainda não existe no seu Supabase ou está vazia.")
        st.code("Dica: Crie uma tabela chamada 'clientes' no painel do Supabase com as colunas: id, nome, status.")
        
