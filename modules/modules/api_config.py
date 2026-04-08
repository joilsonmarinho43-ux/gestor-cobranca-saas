import streamlit as st
import requests
import base64

def tela_conexao_whatsapp(supabase, user_id):
    st.subheader("🔗 Conexão com WhatsApp (Real)")
    
    # Configurações vindas da sua VPS Contabo
    API_URL = "http://api.funecob.com.br:8080"
    API_KEY = "123456"
    INSTANCE_NAME = f"funecob_{user_id[:5]}" # Cria uma instância única por usuário

    if 'whatsapp_conectado' not in st.session_state:
        st.session_state.whatsapp_conectado = False

    col1, col2 = st.columns(2)

    with col1:
        with st.container(border=True):
            st.markdown("### Status da Instância")
            if st.session_state.whatsapp_conectado:
                st.success("✅ CONECTADO")
                if st.button("Desconectar WhatsApp", type="primary"):
                    # Lógica para deletar instância se necessário
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
                
                # CHAMADA REAL PARA A EVOLUTION API
                try:
                    # 1. Criar a instância primeiro (ou verificar se existe)
                    check_url = f"{API_URL}/instance/fetchInstances"
                    headers = {"apikey": API_KEY}
                    
                    # 2. Buscar o QR Code
                    connect_url = f"{API_URL}/instance/connect/{INSTANCE_NAME}"
                    response = requests.get(connect_url, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()
                        # A Evolution retorna o base64 do QR Code
                        qr_base64 = data.get('base64') 
                        if qr_base64:
                            # Remove o cabeçalho do base64 se vier junto
                            if "," in qr_base64:
                                qr_base64 = qr_base64.split(",")[1]
                            
                            st.image(base64.b64decode(qr_base64), width=250)
                            st.caption("Aguardando leitura...")
                        else:
                            st.error("Instância já conectada ou aguardando.")
                    else:
                        st.error(f"Erro na API: {response.status_code}")
                        
                except Exception as e:
                    st.error(f"Não foi possível conectar à VPS: {e}")

                if st.button("Verificar Conexão"):
                    # Aqui você checa se o status mudou para 'open'
                    st.rerun()

    st.divider()
    with st.expander("🔑 Configurações Técnicas (Contabo)"):
        st.info(f"Conectado em: {API_URL}")
        st.text_input("Instância Atual", value=INSTANCE_NAME, disabled=True)
                            
