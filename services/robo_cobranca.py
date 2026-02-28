from datetime import date
from core.database import get_supabase


def executar_cobranca():
    print("==========================================")
    print("CONECTANDO AO SUPABASE")
    print("==========================================")

    supabase = get_supabase()
    print("Conexão estabelecida.")

    hoje = date.today()

    print("Buscando clientes...")
    
    response = supabase.table("clientes").select("*").execute()
    clientes = response.data

    print(f"Total de clientes encontrados: {len(clientes)}")

    atualizados = 0

    for cliente in clientes:
        if cliente["status"] != "pago" and cliente["data_vencimento"]:
            
            data_vencimento = date.fromisoformat(cliente["data_vencimento"])

            if data_vencimento < hoje:
                
                supabase.table("clientes") \
                    .update({"status": "vencido"}) \
                    .eq("id", cliente["id"]) \
                    .execute()

                print(f"Cliente {cliente['nome']} atualizado para VENCIDO.")
                atualizados += 1

    print("==========================================")
    print(f"Total de clientes atualizados: {atualizados}")
    print("==========================================")
