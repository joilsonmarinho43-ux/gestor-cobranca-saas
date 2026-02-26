import os
import sys

# Força a exibição imediata de mensagens
def imprimir(msg):
    print(msg)
    sys.stdout.flush()

imprimir("=== INICIANDO TESTE FORÇADO ===")

try:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    imprimir(f"Verificando chaves: {'OK' if url and key else 'FALTANDO'}")
    
    if url:
        imprimir(f"URL detectada (início): {url[:10]}...")
    
    imprimir("Tentando processar lógica...")
    # Se houver qualquer erro aqui, o 'except' abaixo vai capturar
    imprimir("PROCESSO CONCLUÍDO COM SUCESSO.")

except Exception as e:
    imprimir(f"ERRO ENCONTRADO: {str(e)}")

imprimir("=== FIM DO TESTE ===")
