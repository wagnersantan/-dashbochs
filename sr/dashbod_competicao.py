import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Caminho do arquivo Excel
caminho_arquivo_excel = r"C:\Users\wagne\OneDrive\Desktop\evento.xlsx.xlsx"

# Lendo os dados do Excel
# Ajustar para ler apenas a coluna E (cidades) e a coluna F (quantidade de inscritos)
df = pd.read_excel(caminho_arquivo_excel, usecols="E,F", header=None)

# Corrigir possíveis espaços nos nomes das colunas
df.columns = ['Nome da Cidade', 'Inscritos']

# Limpar valores nulos e remover espaços extras nos nomes das cidades
df['Nome da Cidade'] = df['Nome da Cidade'].str.strip()  # Remove espaços extras
df = df.dropna(subset=['Nome da Cidade'])  # Remove registros com cidade nula

# Título
st.title("DADOS DA QUARTA EDIÇÃO: AEROSHAKE XADREZ")

# Verificando as colunas do DataFrame
st.write("Colunas do DataFrame:", df.columns)

# Exibindo um gráfico de barras interativo para as inscrições por cidade
st.write("### Inscrições por Cidade")

# Usando Plotly Express para criar o gráfico de barras interativo
fig_barras = px.bar(df, 
                    x='Nome da Cidade', 
                    y='Inscritos',
                    labels={'Nome da Cidade': 'Cidade', 'Inscritos': 'Número de Inscritos'},
                    title='Número de Inscritos por Cidade')
st.plotly_chart(fig_barras)

# Gráfico de proporção de inscritos por cidade
fig_pizza = px.pie(df, 
                   names='Nome da Cidade', 
                   values='Inscritos', 
                   title='Proporção de Inscritos por Cidade')
st.plotly_chart(fig_pizza)

# Conversão da data de nascimento
if 'Data de Nascimento' in df.columns:
    df['Data de Nascimento'] = pd.to_datetime(df['Data de Nascimento'], errors='coerce')
    df = df.dropna(subset=['Data de Nascimento'])

    # Calcular idade corretamente
    df['Idade'] = (pd.to_datetime('today') - df['Data de Nascimento']).dt.days // 365

    # Gráfico de distribuição de idades
    st.write('### Distribuição de Idades dos Inscritos')
    
    fig, ax = plt.subplots()
    ax.hist(df['Idade'], bins=10, edgecolor="black")
    st.pyplot(fig)

# Filtro de cidade
cidade_selecionada = st.selectbox("Escolha a Cidade", df['Nome da Cidade'].unique())
df_filtrado = df[df['Nome da Cidade'] == cidade_selecionada]

# Mostrar gráficos de inscritos da cidade selecionada
st.write(f"### Inscritos em {cidade_selecionada}")

# Mostrar o número total de inscritos da cidade selecionada
numero_de_inscritos = df_filtrado.shape[0]
st.write(f"Total de inscritos em {cidade_selecionada}: {numero_de_inscritos}")

# Gráfico de barras apenas com a cidade selecionada
st.write(f"### Inscritos em {cidade_selecionada}")
cidade_inscricoes = df_filtrado['Nome da Cidade'].value_counts()
fig_barras_selecionada = px.bar(cidade_inscricoes, 
                                x=cidade_inscricoes.index, 
                                y=cidade_inscricoes.values,
                                labels={'x': 'Cidade', 'y': 'Número de Inscritos'},
                                title=f'Inscrições na Cidade de {cidade_selecionada}')
st.plotly_chart(fig_barras_selecionada)





