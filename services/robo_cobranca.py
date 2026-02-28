from core.database import get_supabase

def executar_cobranca():
    print("Conectando ao Supabase...")

    supabase = get_supabase()

    print("Buscando clientes...")

    resposta = supabase.table("clientes").select("*").execute()

    total = len(resposta.data)

    print(f"Total de clientes encontrados: {total}")
