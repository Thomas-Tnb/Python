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
    res = supabase.auth.sign_in_with_password({"email": email, "password": senha})
    if res.get("error"):
        st.sidebar.error("Credenciais inválidas")
    else:
        st.session_state["user"] = res.user.id  # Agora salvamos o ID do usuário
        st.sidebar.success("Login realizado!")
        st.experimental_rerun()

# 🚀 Verifica se o usuário está logado
if "user" not in st.session_state:
    st.warning("Por favor, faça login para acessar suas atividades.")
    st.stop()

user_email = st.session_state["user"]

# 🗃️ Carregar atividades do banco
@st.cache_data
def load_activities():
    response = supabase.table("atividades").select("*").execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame(columns=["id", "Matéria", "Atividade", "Situação", "Prazo", "Prioridade"])

df = load_activities()

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
        "usuario_id": st.session_state["user"],  # Salvar o ID do usuário
        "Matéria": subject,
        "Atividade": activity,
        "Situação": status,
        "Prazo": str(deadline),
        "Prioridade": priority
    }
    supabase.table("atividades").insert(new_data).execute()
    st.sidebar.success("Atividade adicionada!")
    st.experimental_rerun()

# 📋 Exibir Atividades
st.subheader("📌 Atividades Pendentes")
def apply_style(val):
    return f'background-color: {PRIORITY_COLORS.get(val, "white")}; color: white; font-weight: bold;'

if not df.empty:
    st.dataframe(df.style.applymap(apply_style, subset=['Prioridade']))
else:
    st.info("Nenhuma atividade cadastrada.")

# ❌ Remover Atividade
st.sidebar.subheader("🗑️ Remover Atividade")
if not df.empty:
    remove_id = st.sidebar.selectbox("Selecione a atividade para remover", df["id"].tolist())
    if st.sidebar.button("Remover"):
        supabase.table("atividades").delete().eq("id", remove_id).execute()
        st.sidebar.success("Atividade removida!")
        st.experimental_rerun()

# 📅 Visualização no Calendário
st.subheader("📅 Visualização no Calendário")
if not df.empty:
    df_sorted = df.sort_values("Prazo")
    for _, row in df_sorted.iterrows():
        st.markdown(f"**{row['Prazo']}** - {row['Atividade']} ({row['Matéria']}) - *{row['Situação']}*")
else:
    st.info("Nenhuma atividade para mostrar no calendário.")