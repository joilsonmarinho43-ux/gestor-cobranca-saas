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
            whatsapp = col2.text_input("WhatsApp (Ex: 5511999998888)")
            
            col3, col4 = st.columns(2)
            # Garantindo que o valor seja um número decimal (float)
            valor = col3.number_input("Valor da Mensalidade (R$)", min_value=0.0, step=1.0, format="%.2f")
            vencimento = col4.date_input("Data de Vencimento")
            
            submit = st.form_submit_button("Salvar Cliente")
            
            if submit:
                if nome and whatsapp:
                    # Preparando os dados com conversão explícita
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
        # Busca todos os dados da tabela
        response = supabase.table("clientes").select("*").order("nome").execute()
        dados = response.data

        if dados:
            df = pd.DataFrame(dados)
            
            # Seleção de colunas existentes para exibição limpa
            cols_exibicao = ['nome', 'whatsapp', 'valor_mensalidade', 'vencimento', 'status']
            cols_presentes = [c for c in cols_exibicao if c in df.columns]
            
            # Formatação visual da tabela
            st.dataframe(
                df[cols_presentes].style.format({"valor_mensalidade": "R$ {:.2f}"}),
                use_container_width=True
            )
        else:
            st.info("Ainda não há clientes cadastrados no banco.")
            
    except Exception as e:
        st.error(f"Erro ao carregar lista de clientes: {e}")
