from core.database import get_supabase

def executar_cobranca():
    print("==========================================")
    print("CONECTANDO AO SUPABASE")
    print("==========================================")

    supabase = get_supabase()

    print("Conexão estabelecida.")
    print("Buscando clientes na tabela 'clientes'...")

    resposta = supabase.table("clientes").select("*").execute()

    total = len(resposta.data)

    print(f"Total de clientes encontrados: {total}")
    print("==========================================")
    print("TESTE FINALIZADO COM SUCESSO")
    print("==========================================")
