import os
import streamlit as st
from supabase import create_client, Client
from functools import lru_cache

class SupabaseConfigError(Exception):
    pass

@lru_cache()
def get_supabase() -> Client:
    """
    Retorna uma instância única do cliente Supabase.
    Prioriza st.secrets (Streamlit Cloud) e fallback para os.getenv (Local).
    """
    # Tenta obter do st.secrets, se falhar, busca no ambiente
    url = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY")

    if not url or not key:
        raise SupabaseConfigError("Credenciais SUPABASE_URL ou SUPABASE_KEY não encontradas.")

    try:
        return create_client(url, key)
    except Exception as e:
        raise SupabaseConfigError(f"Falha na conexão com Supabase: {str(e)}")
        
