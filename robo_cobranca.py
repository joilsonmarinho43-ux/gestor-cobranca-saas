import os

print("--- INICIANDO TESTE DE DIAGNÓSTICO ---")

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if not url or not key:
    print("ERRO: As chaves do Supabase não foram encontradas!")
else:
    print("Sucesso: As chaves foram carregadas corretamente.")
    print(f"Tentando conectar na URL: {url[:15]}...")

print("--- FIM DO TESTE ---")
