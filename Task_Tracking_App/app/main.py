import streamlit as st
from auth import login, check_auth, logout
from atividade_ui import display_activities, add_activity_ui, remove_activity_ui, calendar_view

st.title("Minhas Tarefas")

# 🔑 Login
login()
user_id = check_auth()

# 🔓 Se logado, mostrar funcionalidades
logout()
add_activity_ui(user_id)
display_activities(user_id)
remove_activity_ui(user_id)
calendar_view(user_id)  # 🔥 Agora o calendário interativo aparece!
