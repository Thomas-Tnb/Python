import streamlit as st
import pandas as pd
import datetime
from supabase import create_client, Client

# 🔗 Conectar ao Supabase
SUPABASE_URL = "https://oyxnleqakgfzsmnpwrnn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im95eG5sZXFha2dmenNtbnB3cm5uIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDA5MjA4NjYsImV4cCI6MjA1NjQ5Njg2Nn0.wSc9G3KKd75VlBdFjKgKdxeaLtnWs68YbH3LglAuLxE"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🎨 Definir cores para as prioridades
PRIORITY_COLORS = {
    "Alta": "#FF4B4B",
    "Média": "#FFA500",
    "Baixa": "#4CAF50"
}

# 🔒 Autenticação de Usuário
st.sidebar.header("🔑 Login")
email = st.sidebar.text_input("Email")
senha = st.sidebar.text_input("Senha", type="password")

if st.sidebar.button("Entrar"):
    # Buscar usuário no banco
    res = supabase.table("usuario").select("id, email").eq("email", email).execute()

    if res.data and len(res.data) > 0:
        user = res.data[0]
        st.session_state["user_id"] = user["id"]  # Armazena o ID do usuário logado
        st.sidebar.success("Login realizado!")
        st.rerun()
    else:
        st.sidebar.error("Usuário não encontrado ou senha incorreta.")

# 🚀 Verifica se o usuário está logado
if "user_id" not in st.session_state:
    st.warning("Por favor, faça login para acessar suas atividades.")
    st.stop()

user_id = st.session_state["user_id"]

# 🗃️ Carregar atividades do usuário logado
@st.cache_data
def load_activities(user_id):
    response = supabase.table("atividades").select("*").eq("usuario_id", user_id).execute()
    if response.data:
        df = pd.DataFrame(response.data)

        # ✅ Corrigir nomes das colunas para manter padrão no código
        df.rename(columns={
            "matéria": "Matéria",
            "atividade": "Atividade",
            "situação": "Situação",
            "prazo": "Prazo",
            "prioridade": "Prioridade"
        }, inplace=True)

        return df
    return pd.DataFrame(columns=["id", "Matéria", "Atividade", "Situação", "Prazo", "Prioridade"])  

df = load_activities(user_id)

st.title("📚 Gerenciador de Atividades - Faculdade")

# 📌 Sidebar - Adicionar Nova Atividade
st.sidebar.header("➕ Adicionar Atividade")
subject = st.sidebar.text_input("Matéria")
activity = st.sidebar.text_input("Atividade")
status = st.sidebar.text_input("Situação")
deadline = st.sidebar.date_input("Prazo", min_value=datetime.date.today())
priority = st.sidebar.selectbox("Prioridade", ["Alta", "Média", "Baixa"])

if st.sidebar.button("Adicionar"):
    new_data = {
        "usuario_id": user_id,  # Salvar o ID do usuário logado
        "matéria": subject,
        "atividade": activity,
        "situação": status,
        "prazo": str(deadline),
        "prioridade": priority
    }
    supabase.table("atividades").insert(new_data).execute()
    st.sidebar.success("Atividade adicionada!")
    st.rerun()

# 📋 Exibir Atividades
st.subheader("📌 Atividades Pendentes")
def apply_style(val):
    return f'background-color: {PRIORITY_COLORS.get(val, "white")}; color: white; font-weight: bold;'

if not df.empty:
    st.dataframe(df.style.applymap(apply_style, subset=["Prioridade"]))
else:
    st.info("Nenhuma atividade cadastrada.")

# ❌ Remover Atividade
st.sidebar.subheader("🗑️ Remover Atividade")
if not df.empty:
    remove_id = st.sidebar.selectbox("Selecione a atividade para remover", df["id"].tolist())
    if st.sidebar.button("Remover"):
        supabase.table("atividades").delete().eq("id", remove_id).execute()
        st.sidebar.success("Atividade removida!")
        st.rerun()

# 📅 Visualização no Calendário
st.subheader("📅 Visualização no Calendário")
if not df.empty:
    df_sorted = df.sort_values("Prazo")
    for _, row in df_sorted.iterrows():
        st.markdown(f"**{row['Prazo']}** - {row['Atividade']} ({row['Matéria']}) - *{row['Situação']}*")
else:
    st.info("Nenhuma atividade para mostrar no calendário.")
