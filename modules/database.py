import streamlit as st
from datetime import datetime

def buscar_dados_dashboard(supabase, user_id):
    """Busca e processa todos os indicadores do Dashboard"""
    try:
        res = supabase.table("clientes").select("*").eq("empresa_id", user_id).execute()
        clientes = res.data if res.data else []
        
        hoje = datetime.now().date()
        stats = {
            "ativos": 0,
            "vencidos": 0,
            "inativos": 0,
            "receita_total": 0.0,
            "valor_vencido": 0.0,
            "lista_total": clientes
        }

        for c in clientes:
            data_venc = datetime.strptime(c['data_vencimento'], '%Y-%m-%d').date()
            status = c.get('status', 'Ativo')
            valor = float(c.get('valor_assinatura', 0))

            if status == 'Inativo':
                stats["inativos"] += 1
            elif data_venc < hoje:
                stats["vencidos"] += 1
                stats["valor_vencido"] += valor
            else:
                stats["ativos"] += 1
                stats["receita_total"] += valor
        
        return stats
    except Exception as e:
        st.error(f"Erro ao buscar dados: {e}")
        return None

def cadastrar_cliente(supabase, dados):
    """Função centralizada para inserir novos clientes"""
    return supabase.table("clientes").insert(dados).execute()
