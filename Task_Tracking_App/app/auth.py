import streamlit as st
from database import supabase

def login():
    """Interface de Login"""
    if "user_id" not in st.session_state:
        st.sidebar.header("🔑 Login")
        email = st.sidebar.text_input("Email")
        senha = st.sidebar.text_input("Senha", type="password")

        if st.sidebar.button("Entrar"):
            res = supabase.table("usuario").select("id, email").match({"email" : email, "senha" :senha}).execute()
            if res.data and len(res.data) > 0:
                user = res.data[0]
                st.session_state["user_id"] = user["id"]  # Guarda o ID do usuário logado
                st.sidebar.success("Login realizado!")
                st.rerun()
            else:
                st.sidebar.error("Usuário não encontrado ou senha incorreta.")

def check_auth():
    """Verifica se o usuário está logado"""
    if "user_id" not in st.session_state:
        st.warning("Por favor, faça login para acessar suas atividades.")
        st.stop()
    return st.session_state["user_id"]

def logout():
    """Botão para sair"""
    if st.sidebar.button("Sair"):
        del st.session_state["user_id"]
        st.rerun()
