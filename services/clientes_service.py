import streamlit as st
import os
from supabase import create_client, Client
from functools import lru_cache

class SupabaseConfigError(Exception):
    pass

@lru_cache()
def get_supabase() -> Client:
    """Retorna instância única do cliente Supabase."""
    # Prioriza Streamlit Secrets para Cloud e os.getenv para Local
    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise SupabaseConfigError("Credenciais de banco de dados não encontradas.")

    try:
        return create_client(url, key)
    except Exception as e:
        raise SupabaseConfigError(f"Erro na conexão Supabase: {str(e)}")
        
