import streamlit as st
import pandas as pd
import urllib.parse

def show(supabase):
    st.title("📱 Notificações via WhatsApp")
    
    if supabase is None:
        st.error("Conexão com o banco não disponível.")
        return

    st.subheader("Enviar Cobranças Pendentes")
    
    try:
        # Busca cobranças pendentes e dados dos clientes
        response = supabase.table("cobrancas").select("*, clientes(nome, whatsapp)").eq("status", "Pendente").execute()
        
        if response.data:
            df = pd.DataFrame(response.data)
            # Organiza os dados para o envio
            df['Cliente'] = df['clientes'].apply(lambda x: x['nome'] if x else "N/A")
            df['Telefone'] = df['clientes'].apply(lambda x: x['whatsapp'] if x else "")
            
            for index, row in df.iterrows():
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    
                    # Mensagem personalizada
                    msg = f"Olá {row['Cliente']}, sua fatura no valor de R$ {row['valor']} vence em {row['data_vencimento']}. Solicitamos a gentileza do pagamento."
                    msg_encoded = urllib.parse.quote(msg)
                    link_zap = f"https://wa.me/{row['Telefone']}?text={msg_encoded}"
                    
                    col1.write(f"**{row['Cliente']}** ({row['Telefone']}) - Vence: {row['data_vencimento']}")
                    col2.markdown(f"[Enviar Zap 🚀]({link_zap})")
                    st.divider()
        else:
            st.info("Nenhuma cobrança pendente para enviar hoje.")
            
    except Exception as e:
        st.error(f"Erro ao carregar mensagens: {e}")
                    
