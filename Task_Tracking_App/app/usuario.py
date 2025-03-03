from database import supabase

class Usuario:
    def __init__(self, email: str, senha: str = None):
        self.email = email
        self.senha = senha
        self.id = None

    def autenticar(self):
        """Autentica o usuário e define seu ID na sessão."""
        res = supabase.table("usuario").select("id, email").eq("email", self.email).execute()
        if res.data and len(res.data) > 0:
            self.id = res.data[0]["id"]
            return True
        return False

    @staticmethod
    def obter_por_id(user_id):
        """Obtém um usuário pelo ID."""
        res = supabase.table("usuario").select("id, email").eq("id", user_id).execute()
        if res.data and len(res.data) > 0:
            user = res.data[0]
            return Usuario(user["email"])

        return None
