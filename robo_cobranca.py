import sys
import os

# Força a saída de texto imediata
def falar(texto):
    print(texto)
    sys.stdout.flush()

falar("==========================================")
falar("INICIANDO DIAGNÓSTICO DO ROBÔ")
falar("==========================================")

try:
    falar("Testando acesso às variáveis...")
    url = os.getenv("SUPABASE_URL")
    if url:
        falar(f"Variável SUPABASE_URL encontrada.")
    else:
        falar("AVISO: SUPABASE_URL está vazia.")

    falar("Tentando importar bibliotecas...")
    import supabase
    import requests
    falar("Sucesso: Bibliotecas importadas corretamente.")

except Exception as e:
    falar(f"ERRO IDENTIFICADO: {str(e)}")

falar("==========================================")
falar("FIM DO DIAGNÓSTICO")
falar("==========================================")
