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
        st.dataframe(df.style.applymap(apply_style, subset=["Prioridade"]), use_container_width=True)
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

    response = supabase.table("atividades").select("atividade").eq("usuario_id", user_id).execute()
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

    # Adicionar grade no calendário
    for week_idx, week in enumerate(cal):
        for day_idx, day in enumerate(week):
            if day == 0:
                continue  # Ignorar espaços vazios

            atividades_do_dia = df[df["Prazo"].dt.day == day]

            atividades_texto = ""
            for _, atividade in atividades_do_dia.iterrows():
                cor = PRIORITY_COLORS.get(atividade["Prioridade"], "white")
                atividades_texto += f'<span style="color:{cor};"><b>{atividade["Atividade"]}</b></span><br>'

            fig.add_trace(go.Scatter(
                x=[day_idx], y=[-(week_idx + 1)],
                mode="text",
                text=f"<b>{day}</b><br>{atividades_texto}",
                showlegend=False,
                textposition="middle center",
                hoverinfo="skip"
            ))

            # Criar a grade desenhando quadrados para os dias
            fig.add_shape(
                type="rect",
                x0=day_idx - 0.5, x1=day_idx + 0.5,
                y0=-(week_idx + 1) - 0.5, y1=-(week_idx + 1) + 0.5,
                line=dict(color="white", width=1)
            )

    # Adiciona os nomes dos dias da semana no topo
    for day_idx, day_label in enumerate(days_labels):
        fig.add_trace(go.Scatter(
            x=[day_idx], y=[0],
            mode="text",
            text=f"<b>{day_label}</b>",
            showlegend=False,
            textposition="middle center",
            hoverinfo="skip"
        ))

    fig.update_layout(
        title=f"📆 {calendar.month_name[selected_month]} {selected_year}",
        xaxis=dict(
            tickmode="array",
            tickvals=list(range(7)),
            ticktext=[],  # Remove os textos duplicados no eixo X
            showgrid=False,  # Remove as grades do fundo
            zeroline=False
        ),
        yaxis=dict(
            showgrid=False,  # Remove as grades no eixo Y
            showticklabels=False,
            zeroline=False
        ),
        plot_bgcolor="#0e1117",  # Fundo do calendário
        paper_bgcolor="#0e1117",  # Fundo geral do gráfico
        margin=dict(l=20, r=20, t=50, b=20),
        height=400,
        font=dict(color="white")  # Texto em branco para melhor contraste
    )

    st.plotly_chart(fig, use_container_width=True)
