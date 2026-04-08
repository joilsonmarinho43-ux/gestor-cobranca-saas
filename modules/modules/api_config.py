import streamlit as st
import requests
import base64

def tela_conexao_whatsapp(supabase, user_id):
    st.subheader("🔗 Conexão com WhatsApp")
    st.write("Conecte seu WhatsApp para habilitar os envios automáticos.")

    # Busca as credenciais de forma segura nos Secrets do sistema
    try:
        API_URL = st.secrets["API_URL"]
        API_KEY = st.secrets["API_KEY"]
    except Exception:
        st.error("Configurações da API não encontradas nos Secrets.")
        return

    # Instância baseada no ID do usuário para ser única
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
                    # Tenta conectar e obter o QR Code da Evolution API
                    connect_url = f"{API_URL}/instance/connect/{INSTANCE_NAME}"
                    headers = {"apikey": API_KEY}
                    
                    response = requests.get(connect_url, headers=headers, timeout=15)
                    
                    if response.status_code in [200, 201]:
                        data = response.json()
                        qr_base64 = data.get('base64') or data.get('code')
                        
                        if qr_base64:
                            if "," in str(qr_base64):
                                qr_base64 = qr_base64.split(",")[1]
                            
                            img_data = base64.b64decode(qr_base64)
                            st.image(img_data, width=250)
                            st.caption("Aponte a câmera do seu WhatsApp para o código acima.")
                        else:
                            st.info("O QR Code está sendo gerado... Aguarde um instante.")
                    else:
                        st.error(f"Erro na API: {response.status_code}")
                        
                except Exception as e:
                    st.error("Erro de conexão com o servidor de mensagens.")
                    st.info("Certifique-se de que a API na Contabo está ativa.")

                if st.button("Verificar se Conectou"):
                    st.rerun()

    st.divider()
    with st.expander("🛠️ Informações da Instância"):
        st.code(f"ID da Instância: {INSTANCE_NAME}")
        
