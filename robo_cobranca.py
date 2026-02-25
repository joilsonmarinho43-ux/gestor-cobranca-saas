import os
import requests
from supabase import create_client
from datetime import datetime

# O robô pega essas informações das configurações de segurança do GitHub
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
# Essas serão as chaves da sua API de WhatsApp que vamos configurar depois
API_URL = os.environ.get("API_WHATSAPP_URL") 
API_KEY = os.environ.get("API_WHATSAPP_KEY")

def enviar_msg(telefone, mensagem):
    """Essa função envia o comando para a API de WhatsApp"""
    if not API_URL:
        print(f"Simulando envio para {telefone}: {mensagem}")
        return True
    
    url = f"{API_URL}/message/sendText"
    payload = {"number": telefone, "text": mensagem}
    headers = {"Content-Type": "application/json", "apikey": API_KEY}
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.status_code == 201
    except:
        return False

def executar_robot():
    # Conecta ao seu banco de dados
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    hoje = datetime.now().date().isoformat()
    
    # 1. Busca quem vence HOJE para mandar o lembrete com o PIX
    vencem_hoje = supabase.table("clientes").select("*").eq("data_vencimento", hoje).execute()
    
    for cli in vencem_hoje.data:
        pix = cli.get('chave_pix_manual', 'Solicite ao suporte')
        msg = f"Olá {cli['nome']}! 🚀\n\nLembramos que sua fatura de R$ {cli['valor_assinatura']} vence hoje.\n\nPagamento via PIX:\n`{pix}`"
        enviar_msg(cli['whatsapp'], msg)
        print(f"Lembrete enviado para {cli['nome']}")

if __name__ == "__main__":
    executar_robot()
  
