import sys
import os
from datetime import datetime


# ================================
# GARANTE PATH DO PROJETO
# ================================

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)


# ================================
# VALIDA VARIÁVEIS DE AMBIENTE
# ================================

def validar_ambiente():
    if not os.getenv("SUPABASE_URL"):
        raise Exception("SUPABASE_URL não configurada.")

    if not os.getenv("SUPABASE_KEY"):
        raise Exception("SUPABASE_KEY não configurada.")


# ================================
# EXECUÇÃO
# ================================

if __name__ == "__main__":

    try:

        print("==========================================")
        print("ROBÔ DE COBRANÇA - INÍCIO")
        print(f"Data/Hora: {datetime.now()}")
        print("==========================================")

        validar_ambiente()

        from services.robo_cobranca import executar_cobranca

        executar_cobranca()

        print("==========================================")
        print("ROBÔ FINALIZADO COM SUCESSO")
        print("==========================================")

    except Exception as e:

        print("==========================================")
        print("ERRO NA EXECUÇÃO DO ROBÔ")
        print(str(e))
        print("==========================================")

        raise e
