from core.database import get_supabase


class ClientesService:

    def __init__(self):
        self.supabase = get_supabase()
        self.table = "clientes"

    def listar_por_empresa(self, empresa_id: str):
        response = (
            self.supabase
            .table(self.table)
            .select("*")
            .eq("empresa_id", empresa_id)
            .execute()
        )

        return response.data

    def buscar_por_id(self, cliente_id: str):
        response = (
            self.supabase
            .table(self.table)
            .select("*")
            .eq("id", cliente_id)
            .single()
            .execute()
        )

        return response.data

    def criar(self, empresa_id: str, nome: str):
        response = (
            self.supabase
            .table(self.table)
            .insert({
                "empresa_id": empresa_id,
                "nome": nome
            })
            .execute()
        )

        return response.data

    def atualizar(self, cliente_id: str, dados: dict):
        response = (
            self.supabase
            .table(self.table)
            .update(dados)
            .eq("id", cliente_id)
            .execute()
        )

        return response.data

    def deletar(self, cliente_id: str):
        response = (
            self.supabase
            .table(self.table)
            .delete()
            .eq("id", cliente_id)
            .execute()
        )

        return response.data
