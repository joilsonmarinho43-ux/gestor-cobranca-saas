from supabase import create_client, Client
import os
from functools import lru_cache


class SupabaseConfigError(Exception):
    pass


@lru_cache()
def get_supabase() -> Client:
    """
    Retorna uma instância única do cliente Supabase.
    Usa cache para evitar múltiplas conexões desnecessárias.
    """

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url:
        raise SupabaseConfigError("SUPABASE_URL não configurada nas variáveis de ambiente.")

    if not key:
        raise SupabaseConfigError("SUPABASE_KEY não configurada nas variáveis de ambiente.")

    try:
        client = create_client(url, key)
        return client
    except Exception as e:
        raise SupabaseConfigError(f"Erro ao conectar ao Supabase: {str(e)}")
