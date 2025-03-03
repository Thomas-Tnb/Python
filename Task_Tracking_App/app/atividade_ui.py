import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import calendar
from atividade import Atividade
import datetime
from database import supabase

PRIORITY_COLORS = {"Alta": "#FF4B4B", "Média": "#FFA500", "Baixa": "#4CAF50"}

def apply_style(val):
    """Aplica cores à coluna de prioridade."""
    return f'background-color: {PRIORITY_COLORS.get(val, "white")}; color: white; font-weight: bold;'

def display_activities(user_id):
    """Exibe atividades na interface."""
    df = Atividade.carregar_por_usuario(user_id)

    st.subheader("📌 Atividades Pendentes")
    if not df.empty:
        st.dataframe(df.style.applymap(apply_style, subset=["Prioridade"]))
    else:
        st.info("Nenhuma atividade cadastrada.")

def add_activity_ui(user_id):
    """Interface para adicionar nova atividade."""
    st.sidebar.header("➕ Adicionar Atividade")
    subject = st.sidebar.text_input("Matéria")
    activity = st.sidebar.text_input("Atividade")
    status = st.sidebar.text_input("Situação")
    deadline = st.sidebar.date_input("Prazo", min_value=datetime.date.today())
    priority = st.sidebar.selectbox("Prioridade", ["Alta", "Média", "Baixa"])

    if st.sidebar.button("Adicionar"):
        nova_atividade = Atividade(user_id, subject, activity, status, deadline, priority)
        nova_atividade.salvar()
        st.sidebar.success("Atividade adicionada!")
        st.rerun()

def remove_activity_ui(user_id):
    """Interface para remover atividades."""
    df = Atividade.carregar_por_usuario(user_id)
    st.sidebar.subheader("🗑️ Remover Atividade")

    response = supabase.table("atividades").select("atividade").execute()
    atividades = [atividade['atividade'] for atividade in response.data]

    if not df.empty:
        remove_id = st.sidebar.selectbox("Selecione a atividade para remover", atividades)
        if st.sidebar.button("Remover"):
            Atividade.remover(remove_id)
            st.sidebar.success("Atividade removida!")
            st.rerun()

def calendar_view(user_id):
    """Exibe atividades em um calendário mensal."""
    st.subheader("📅 Calendário")

    df = Atividade.carregar_por_usuario(user_id)

    if df.empty:
        st.info("Nenhuma atividade cadastrada.")
        return

    df["Prazo"] = pd.to_datetime(df["Prazo"])  # Converte para data
    today = pd.Timestamp.today()
    
    # Seleção do mês
    st.sidebar.subheader("📆")
    selected_month = st.sidebar.selectbox("Escolha o mês", range(1, 13), index=today.month - 1)
    selected_year = st.sidebar.number_input("Ano", min_value=2000, max_value=2100, value=today.year)

    # Filtrar atividades para o mês selecionado
    df = df[(df["Prazo"].dt.month == selected_month) & (df["Prazo"].dt.year == selected_year)]

    # Criar estrutura do calendário
    cal = calendar.monthcalendar(selected_year, selected_month)
    days_labels = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]
    
    fig = go.Figure()

    for week_idx, week in enumerate(cal):
        for day_idx, day in enumerate(week):
            if day == 0:
                continue  # Dia vazio

            atividades_do_dia = df[df["Prazo"].dt.day == day]
            atividades_texto = "<br>".join(atividades_do_dia["Atividade"]) if not atividades_do_dia.empty else ""

            fig.add_trace(go.Scatter(
                x=[day_idx], y=[-week_idx], mode="text",
                text=f"<b>{day}</b><br>{atividades_texto}",
                showlegend=False,
                textposition="middle center",
                hoverinfo="text"
            ))

    fig.update_layout(
        title=f"📆 {calendar.month_name[selected_month]} {selected_year}",
        xaxis=dict(tickmode="array", tickvals=list(range(7)), ticktext=days_labels, showgrid=False),
        yaxis=dict(showgrid=False, showticklabels=False),
        plot_bgcolor="#0e1117",  # Cor de fundo do gráfico
        paper_bgcolor="#0e1117",  # Cor de fundo geral do gráfico
        margin=dict(l=20, r=20, t=50, b=20),
        height=400,
        font=dict(color="white")  # Cor da fonte em branco
    )

    st.plotly_chart(fig, use_container_width=True)
