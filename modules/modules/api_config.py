import streamlit as st
import requests
import base64

def tela_conexao_whatsapp(supabase, user_id):
    st.subheader("🔗 Conexão com WhatsApp")
    
    # Tentando pegar dos Secrets, se não existir, usa o padrão
    # Isso evita o bloqueio de segurança do Deploy
    API_URL = st.secrets.get("API_URL", "http://161.97.181.130:8080")
    API_KEY = st.secrets.get("API_KEY", "123456")

    INSTANCE_NAME = f"funecob_{user_id[:8]}" 

    if 'whatsapp_conectado' not in st.session_state:
        st.session_state.whatsapp_conectado = False

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### Status da Instância")
            if st.session_state.whatsapp_conectado:
                st.success("✅ CONECTADO")
                if st.button("Desconectar WhatsApp", type="primary"):
                    st.session_state.whatsapp_conectado = False
                    st.rerun()
            else:
                st.warning("⚠️ DESCONECTADO")
                if st.button("Gerar QR Code Real"):
                    st.session_state.gerar_qr = True

    with col2:
        if 'gerar_qr' in st.session_state and st.session_state.gerar_qr:
            with st.container(border=True):
                st.markdown("### Escaneie o QR Code")
                try:
                    connect_url = f"{API_URL}/instance/connect/{INSTANCE_NAME}"
                    headers = {"apikey": API_KEY}
                    response = requests.get(connect_url, headers=headers, timeout=15)
                    
                    if response.status_code in [200, 201]:
                        qr_data = response.json().get('base64') or response.json().get('code')
                        if qr_data:
                            if "," in str(qr_data): qr_data = qr_data.split(",")[1]
                            st.image(base64.b64decode(qr_data), width=250)
                            st.caption("Aponte o WhatsApp para o código.")
                    else:
                        st.error("Erro ao gerar. Tente novamente.")
                except:
                    st.error("Erro de conexão com a VPS.")

    st.divider()
    with st.expander("🛠️ Detalhes"):
        st.write(f"Instância: {INSTANCE_NAME}")
