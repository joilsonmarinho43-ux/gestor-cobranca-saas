import streamlit as st
import pandas as pd
from datetime import datetime

def show(supabase):
    st.title("💰 Fluxo de Caixa")
    
    if supabase is None:
        st.error("Erro na conexão com o banco.")
        return

    tabs = st.tabs(["Faturas Pendentes", "Gerar Cobranças", "Histórico"])

    # ABA 1: LISTAGEM
    with tabs[0]:
        try:
            response = supabase.table("cobrancas").select("*, clientes(nome)").eq("status", "Pendente").execute()
            if response.data:
                df = pd.DataFrame(response.data)
                df['Cliente'] = df['clientes'].apply(lambda x: x['nome'] if x else "N/A")
                st.dataframe(df[['Cliente', 'valor', 'data_vencimento']], use_container_width=True)
            else:
                st.info("Nenhuma fatura pendente encontrada.")
        except Exception as e:
            st.error(f"Erro ao carregar faturas: {e}")

    # ABA 2: GERADOR AUTOMÁTICO
    with tabs[1]:
        st.subheader("Gerar Mensalidades do Mês")
        st.write("Este botão criará uma fatura para TODOS os clientes cadastrados.")
        
        col1, col2 = st.columns(2)
        valor_padrao = col1.number_input("Valor Padrão (R$)", min_value=0.0, value=150.0)
        data_venc = col2.date_input("Vencimento das Faturas")

        if st.button("Gerar Faturas para Todos 🚀"):
            try:
                # Busca todos os clientes (como Elieusa e Joelison)
                clientes = supabase.table("clientes").select("id, nome").execute()
                
                for c in clientes.data:
                    data_insert = {
                        "cliente_id": c['id'],
                        "valor": valor_padrao,
                        "data_vencimento": str(data_venc),
                        "status": "Pendente"
                    }
                    supabase.table("cobrancas").insert(data_insert).execute()
                
                st.success(f"✅ Faturas geradas para {len(clientes.data)} clientes!")
                st.rerun()
            except Exception as e:
                st.error(f"Erro ao gerar: {e}")
        
