import streamlit as st
import urllib.parse
from datetime import datetime

def gerar_link_whatsapp(telefone, nome_cliente, valor, data_vencimento):
    """
    Formata o número e cria o link com mensagem personalizada.
    """
    # Limpa o número (deixa apenas dígitos)
    telefone_limpo = "".join(filter(str.isdigit, str(telefone)))
    
    # Formata a mensagem
    mensagem = (
        f"Olá, *{nome_cliente}*! 👋\n\n"
        f"Passando para lembrar que sua fatura no valor de *R$ {valor:,.2f}* "
        f"vence no dia *{data_vencimento}*.\n\n"
        f"Se precisar de ajuda com o pagamento, estamos à disposição! 😊"
    )
    
    # Transforma o texto em formato de link (URL Encoding)
    mensagem_url = urllib.parse.quote(mensagem)
    
    return f"https://wa.me/{telefone_limpo}?text={mensagem_url}"

def listar_fila_cobranca(clientes):
    """
    Filtra quem está vencido e exibe os botões de envio.
    """
    hoje = datetime.now().date()
    
    # Filtra apenas os clientes cuja data de vencimento já passou
    vencidos = [
        c for c in clientes 
        if datetime.strptime(c['data_vencimento'], '%Y-%m-%d').date() < hoje
    ]

    if not vencidos:
        st.success("✅ Todos os clientes estão em dia!")
        return

    st.subheader(f"🚨 Fila de Cobrança ({len(vencidos)} pendentes)")
    
    for cli in vencidos:
        with st.container(border=True):
            col_info, col_btn = st.columns([3, 1])
            
            with col_info:
                st.write(f"👤 **{cli['nome']}**")
                st.caption(f"📅 Vencido em: {cli['data_vencimento']} | 💰 R$ {cli['valor_assinatura']:,.2f}")
            
            with col_btn:
                # Se não houver whatsapp cadastrado, avisa o usuário
                if cli.get('whatsapp'):
                    link = gerar_link_whatsapp(
                        cli['whatsapp'], 
                        cli['nome'], 
                        cli['valor_assinatura'], 
                        cli['data_vencimento']
                    )
                    st.link_button("Enviar Zap", link, type="primary", use_container_width=True)
                else:
                    st.error("Sem número")
  
