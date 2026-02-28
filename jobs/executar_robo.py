import sys
import os

# Garante que o diretório raiz do projeto seja reconhecido
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    print("==========================================")
    print("INICIANDO EXECUÇÃO DO ROBÔ DE COBRANÇA")
    print("==========================================")

    from services.robo_cobranca import executar_cobranca

    print("Importação realizada com sucesso.")
    print("Executando robô...")

    executar_cobranca()

    print("==========================================")
    print("ROBÔ EXECUTADO COM SUCESSO")
    print("==========================================")

except Exception as e:
    print("==========================================")
    print("ERRO DURANTE EXECUÇÃO:")
    print(str(e))
    print("==========================================")
    raise e
