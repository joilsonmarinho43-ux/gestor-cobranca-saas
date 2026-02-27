import streamlit as st
import pandas as pd

def show(supabase):
    st.header("💰 Fluxo de Caixa e Cobranças")
    
    if supabase is None:
        st.error("Erro na ligação ao banco.")
        return

    st.subheader("Gerar Cobranças do Mês")
    if st.button("🚀 Gerar Faturas para Todos os Clientes"):
        try:
            # Busca todos os clientes ativos com mensalidade
            clientes = supabase.table("clientes").select("id, valor_mensalidade").execute()
            
            if clientes.data:
                for clie in clientes.data:
                    nova_cobranca = {
                        "cliente_id": clie['id'],
                        "valor": float(clie['valor_mensalidade'] or 0),
                        "status": "Pendente",
                        "data_vencimento": "2026-02-27" # Data de exemplo
                    }
                    supabase.table("cobrancas").insert(nova_cobranca).execute()
                st.success("✅ Faturas geradas com sucesso!")
                st.rerun()
            else:
                st.warning("Nenhum cliente ativo encontrado.")
        except Exception as e:
            st.error(f"Erro ao gerar cobranças: {e}")

    st.divider()
    st.subheader("Cobranças Atuais")
    try:
        # Tenta listar cobranças unindo com o nome do cliente
        response = supabase.table("cobrancas").select("*, clientes(nome)").execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df['Cliente'] = df['clientes'].apply(lambda x: x['nome'] if x else "N/A")
            st.table(df[['Cliente', 'valor', 'status']])
        else:
            st.info("Nenhuma cobrança registada.")
    except Exception:
        st.warning("Tabela de cobranças ainda não configurada no banco.")
        
