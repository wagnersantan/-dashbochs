# IMPORTS ====================================================
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from io import BytesIO

# LAYOUT LATERAL ==============================================
st.set_page_config(layout="wide", page_title="Painel AEROSHAKE XADREZ")
#st.sidebar.image("logo.png", use_column_width=True)  # <-- MODIFICAÇÃO: logo na lateral

# CARREGAMENTO DE DADOS =======================================
caminho_arquivo_excel = '/home/wagne/desenvolvimento/dashbochs/sr/evento.xlsx'
df = pd.read_excel(caminho_arquivo_excel, usecols="E,F", header=None)
df.columns = ['Nome da Cidade', 'Inscritos']

df['Inscritos'] = pd.to_numeric(df['Inscritos'], errors='coerce')  # ✅ CORREÇÃO AQUI

df['Nome da Cidade'] = df['Nome da Cidade'].str.strip()
df = df.dropna(subset=['Nome da Cidade'])

# TÍTULO E MÉTRICAS =============================================
st.title("DADOS DA QUARTA EDIÇÃO: AEROSHAKE XADREZ")

col1, col2 = st.columns(2)  # <-- MODIFICAÇÃO: Métricas em colunas
col1.metric("Total de Inscritos", int(df['Inscritos'].sum()))
col2.metric("Total de Cidades", df['Nome da Cidade'].nunique())

# GRÁFICOS GERAIS ==============================================
st.markdown("### Distribuição Geral")
g1, g2 = st.columns(2)  # <-- MODIFICAÇÃO: Gráficos lado a lado

fig_barras = px.bar(df,
                    x='Nome da Cidade',
                    y='Inscritos',
                    labels={'Nome da Cidade': 'Cidade', 'Inscritos': 'Número de Inscritos'},
                    title='Número de Inscritos por Cidade')
g1.plotly_chart(fig_barras, use_container_width=True)

fig_pizza = px.pie(df,
                   names='Nome da Cidade',
                   values='Inscritos',
                   title='Proporção de Inscritos por Cidade')
g2.plotly_chart(fig_pizza, use_container_width=True)

# RANKING DAS CIDADES COM MAIS INSCRITOS =======================
st.markdown("### Top 10 Cidades com Mais Inscritos")  # <-- MODIFICAÇÃO
ranking = df.groupby("Nome da Cidade")["Inscritos"].sum().sort_values(ascending=False).head(10)
st.dataframe(ranking.reset_index(), use_container_width=True)

# FILTRO DE CIDADE ============================================
st.markdown("### Análise por Cidade")
cidade_selecionada = st.selectbox("Escolha a Cidade", df['Nome da Cidade'].unique())
df_filtrado = df[df['Nome da Cidade'] == cidade_selecionada]

st.write(f"Total de inscritos em {cidade_selecionada}: {df_filtrado['Inscritos'].sum()}")

fig_cidade = px.bar(df_filtrado,
                    x='Nome da Cidade',
                    y='Inscritos',
                    labels={'Nome da Cidade': 'Cidade', 'Inscritos': 'Número de Inscritos'},
                    title=f'Inscrições em {cidade_selecionada}')
st.plotly_chart(fig_cidade, use_container_width=True)

# DOWNLOAD DOS DADOS ==========================================
st.markdown("### Download dos Dados Filtrados")  # <-- MODIFICAÇÃO
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📂 Baixar CSV",
    data=csv,
    file_name=f"inscritos_{cidade_selecionada}.csv",
    mime='text/csv'
)

# FIM DO CÓDIGO ================================================
