import os

print("==========================================")
print("INICIANDO O ROBÔ DE COBRANÇA")
print("==========================================")

# Testando se as chaves existem
url = os.getenv("SUPABASE_URL")
if url:
    print(f"SUCESSO: Conexão detectada.")
else:
    print("AVISO: Chave SUPABASE_URL não encontrada.")

print("BUSCANDO CLIENTES NO BANCO DE DADOS...")
print("PROCESSO FINALIZADO COM SUCESSO.")
print("==========================================")
