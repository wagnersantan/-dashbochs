import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# --- Título do aplicativo ---
st.title("🏆 Torneio de Xadrez Ilhéus/Itabuna Online - 23/03/2025")
st.write("Bem-vindo ao painel de análise do torneio de xadrez!")

# --- Upload do arquivo pelo usuário ---
arquivo = st.file_uploader("Carregue o arquivo do torneio", type=['csv'])

# --- Carregar um arquivo CSV padrão se nenhum arquivo for enviado ---
if arquivo is None:
    # Exemplo de dados padrão (substitua este CSV com o seu arquivo padrão)
    csv_padrao = """Rank,Title,Nomes dos Enxadristas,Rating,Points,Tie Break,Performance
1,GM,Rogeriox,2500,4.5,0,2700
2,IM,Camila,2400,4.0,0,2600
3,FM,João,2300,3.5,0,2500
"""
    arquivo = io.StringIO(csv_padrao)

# --- Processamento dos dados ---
try:
    # Definir nomes das colunas
    colunas = ['Rank', 'Title', 'Nomes dos Enxadristas', 'Rating', 'Points', 'Tie Break', 'Performance']
    df = pd.read_csv(arquivo, encoding="utf-8", sep=",", header=0, names=colunas)

    # Converter a coluna 'Points' para numérico
    df['Points'] = pd.to_numeric(df['Points'], errors='coerce').fillna(0)

    # --- Exibição dos Dados ---
    st.write("### 📊 Dados Brutos do Torneio")
    st.dataframe(df)

    # --- Classificação Final ---
    st.write("### 🏅 Classificação Final")
    classificacao = df[['Nomes dos Enxadristas', 'Points']].sort_values(by='Points', ascending=False)
    st.dataframe(classificacao)

    # --- Jogadores com Mais Pontos ---
    st.write("### 🎖️ Jogadores com Mais Pontos")
    jogadores_top = classificacao.head(10)  # Exibir apenas os 10 primeiros
    st.dataframe(jogadores_top)

    # --- Filtragem de Jogadores ---
    jogador_selecionado = st.selectbox("🔍 Selecione um jogador para ver mais detalhes:", df['Nomes dos Enxadristas'].unique())
    if jogador_selecionado:
        st.write(df[df['Nomes dos Enxadristas'] == jogador_selecionado])

    # --- Criar Gráfico de Pontuação ---
    st.write("### 📈 Gráfico de Pontuação dos Jogadores")

    # Remover "Rogeriox" da classificação se necessário
    classificacao = classificacao[classificacao['Nomes dos Enxadristas'] != 'Rogeriox']

    # Ordenar os dados em ordem decrescente
    classificacao = classificacao.sort_values(by='Points', ascending=True)  # Invertido para gráfico de barras horizontais

    # Criar o gráfico de barras horizontal
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.barh(classificacao['Nomes dos Enxadristas'], classificacao['Points'], color='blue')

    # Melhorando a formatação do gráfico
    ax.set_xlabel("Pontos", fontsize=12)
    ax.set_ylabel("Jogador", fontsize=12)
    ax.set_title("Pontos por Jogador (Ordenado por Maior Pontuação)", fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Exibir gráfico no Streamlit
    st.pyplot(fig)

except Exception as e:
    st.error(f"❌ Erro ao carregar o arquivo: {e}")
