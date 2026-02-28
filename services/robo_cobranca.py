from datetime import date, timedelta
from core.database import get_supabase


def executar_cobranca():
    print("==========================================")
    print("INICIANDO ROBÔ DE COBRANÇA")
    print("==========================================")

    supabase = get_supabase()
    hoje = date.today()

    print("Buscando parcelas pendentes...")

    # 1️⃣ Atualizar parcelas vencidas
    response = (
        supabase
        .table("parcelas")
        .select("*")
        .eq("status", "pendente")
        .execute()
    )

    parcelas = response.data or []
    atualizadas = 0

    for parcela in parcelas:

        if parcela.get("data_vencimento"):

            vencimento = date.fromisoformat(parcela["data_vencimento"])

            if vencimento < hoje:

                supabase.table("parcelas") \
                    .update({"status": "vencido"}) \
                    .eq("id", parcela["id"]) \
                    .execute()

                print(f"Parcela {parcela['id']} marcada como VENCIDA.")
                atualizadas += 1

    print(f"Parcelas vencidas atualizadas: {atualizadas}")

    # 2️⃣ Gerar nova parcela mensal automaticamente
    print("Verificando geração automática de mensalidades...")

    clientes = supabase.table("clientes").select("*").execute().data or []
    geradas = 0

    for cliente in clientes:

        valor = cliente.get("valor_mensal")
        dia_vencimento = cliente.get("dia_vencimento")

        if not valor or not dia_vencimento:
            continue

        # Verifica se já existe parcela no mês atual
        mes_atual = hoje.month
        ano_atual = hoje.year

        existente = (
            supabase
            .table("parcelas")
            .select("id")
            .eq("cliente_id", cliente["id"])
            .gte("data_vencimento", f"{ano_atual}-{mes_atual:02d}-01")
            .lte("data_vencimento", f"{ano_atual}-{mes_atual:02d}-31")
            .execute()
        )

        if existente.data:
            continue

        nova_data = date(ano_atual, mes_atual, int(dia_vencimento))

        supabase.table("parcelas").insert({
            "cliente_id": cliente["id"],
            "valor": float(valor),
            "data_vencimento": nova_data.isoformat(),
            "status": "pendente"
        }).execute()

        print(f"Parcela gerada para {cliente['nome']}")
        geradas += 1

    print("==========================================")
    print(f"Parcelas vencidas atualizadas: {atualizadas}")
    print(f"Novas parcelas geradas: {geradas}")
    print("ROBÔ FINALIZADO")
    print("==========================================")
