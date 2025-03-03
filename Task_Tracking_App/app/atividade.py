import pandas as pd
from database import supabase

class Atividade:
    def __init__(self, usuario_id, materia, descricao, situacao, prazo, prioridade):
        self.usuario_id = usuario_id
        self.materia = materia
        self.descricao = descricao
        self.situacao = situacao
        self.prazo = prazo
        self.prioridade = prioridade

    def salvar(self):
        """Salva a atividade no banco de dados."""
        dados = {
            "usuario_id": self.usuario_id,
            "matéria": self.materia,
            "atividade": self.descricao,
            "situação": self.situacao,
            "prazo": str(self.prazo),
            "prioridade": self.prioridade
        }
        return supabase.table("atividades").insert(dados).execute()

    @staticmethod
    def carregar_por_usuario(user_id):
        """Carrega todas as atividades de um usuário e retorna um DataFrame."""
        response = supabase.table("atividades").select("matéria", "atividade", "situação", "prazo", "prioridade").eq("usuario_id", user_id).execute()
        if response.data:
            df = pd.DataFrame(response.data)
            df.rename(columns={
                "matéria": "Matéria",
                "atividade": "Atividade",
                "situação": "Situação",
                "prazo": "Prazo",
                "prioridade": "Prioridade"
            }, inplace=True)
            return df
        return pd.DataFrame(columns=["id", "Matéria", "Atividade", "Situação", "Prazo", "Prioridade"])

    @staticmethod
    def remover(atividade_id):
        """Remove uma atividade pelo ID."""
        return supabase.table("atividades").delete().eq("atividade", atividade_id).execute()
