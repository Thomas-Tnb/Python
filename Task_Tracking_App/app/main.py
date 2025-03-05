import streamlit as st
from auth import login, check_auth, logout
from atividade_ui import display_activities, add_activity_ui, remove_activity_ui, calendar_view

# st.title("Minhas Tarefas")

# Include Bootstrap for styling
st.markdown("""
<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
""", unsafe_allow_html=True)

# 🔑 Login
login()
user_id = check_auth()

# 🔓 Se logado, mostrar funcionalidades
logout()
add_activity_ui(user_id)

# Conteúdo
st.markdown("""
<div class="container mt-2 mb-5">
    <h1 class="text-center">Minhas Tarefas</h1>
    <p class="text-center">Você pode visualizá-las abaixo, caso haja alguma.</p>
</div>
""", unsafe_allow_html=True)

display_activities(user_id)
remove_activity_ui(user_id)
calendar_view(user_id)  # 🔥 Agora o calendário interativo aparece!
