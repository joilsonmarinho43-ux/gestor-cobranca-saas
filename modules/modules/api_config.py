import streamlit as st
import requests
import base64
import time

def tela_conexao_whatsapp(supabase, user_id):
    st.subheader("🔗 Conexão com WhatsApp")
    st.write("Conecte seu WhatsApp para habilitar os envios automáticos do Funecob.")

    # Configurações Reais da sua VPS Contabo
    API_URL = "http://161.97.181.130:8080"
    API_KEY = "123456"
    # Criando um nome de instância único baseado no seu ID de usuário
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
                st.info("Clique no botão abaixo para gerar o código de conexão.")
                
                if st.button("Gerar QR Code Real"):
                    st.session_state.gerar_qr = True

    with col2:
        if 'gerar_qr' in st.session_state and st.session_state.gerar_qr:
            with st.container(border=True):
                st.markdown("### Escaneie o QR Code")
                
                try:
                    # Endpoint da Evolution API para conectar instância
                    connect_url = f"{API_URL}/instance/connect/{INSTANCE_NAME}"
                    headers = {"apikey": API_KEY}
                    
                    response = requests.get(connect_url, headers=headers, timeout=10)
                    
                    if response.status_code == 200 or response.status_code == 201:
                        data = response.json()
                        # Pega o base64 (imagem) retornado pela API
                        qr_base64 = data.get('base64') or data.get('code')
                        
                        if qr_base64:
                            # Limpeza de cabeçalho base64 se existir
                            if "," in str(qr_base64):
                                qr_base64 = qr_base64.split(",")[1]
                            
                            img_data = base64.b64decode(qr_base64)
                            st.image(img_data, width=250)
                            st.caption("Abra o WhatsApp > Aparelhos conectados > Conectar um aparelho")
                        else:
                            st.info("Aguardando o servidor gerar a imagem... Tente novamente.")
                    else:
                        st.error(f"Erro {response.status_code}: Verifique se a instância '{INSTANCE_NAME}' já existe.")
                        
                except Exception as e:
                    st.error(f"Erro de conexão: Não foi possível alcançar a VPS no IP 161.97.181.130")
                    st.info("Dica: Verifique se a porta 8080 está aberta no firewall da Contabo.")

                if st.button("Atualizar Status"):
                    st.rerun()

    st.divider()
    with st.expander("🛠️ Dados de Conexão Técnica"):
        st.code(f"Host: {API_URL}\nInstância: {INSTANCE_NAME}")
                    
