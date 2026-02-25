import streamlit as st

def tela_conexao_whatsapp(supabase, user_id):
    st.subheader("🔗 Conexão com WhatsApp")
    st.write("Conecte seu WhatsApp para habilitar os envios automáticos.")

    # Simulação de status de conexão
    if 'whatsapp_conectado' not in st.session_state:
        st.session_state.whatsapp_conectado = False

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### Status da Instância")
            if st.session_state.whatsapp_conectado:
                st.success("✅ CONECTADO")
                st.button("Desconectar WhatsApp", type="primary")
            else:
                st.warning("⚠️ DESCONECTADO")
                st.info("Para vender este serviço, você integrará aqui o QR Code da API (Evolution ou Z-API).")
                
                if st.button("Gerar QR Code"):
                    st.session_state.gerar_qr = True

    with col2:
        if 'gerar_qr' in st.session_state and st.session_state.gerar_qr:
            with st.container(border=True):
                st.markdown("### Escaneie o QR Code")
                # Placeholder para o QR Code real da API
                st.image("https://upload.wikimedia.org/wikipedia/commons/d/d0/QR_code_for_mobile_English_Wikipedia.svg", width=200)
                st.caption("Abra o WhatsApp > Aparelhos conectados > Conectar um aparelho")
                if st.button("Já escaneei"):
                    st.session_state.whatsapp_conectado = True
                    st.rerun()

    st.divider()
    st.subheader("🔑 Credenciais da API")
    st.text_input("URL da API (Gateway)", placeholder="https://sua-api.com")
    st.text_input("Token de Segurança", type="password")
  
