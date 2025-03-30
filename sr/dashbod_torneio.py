import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# --- Título do aplicativo ---
st.title("🏆 Torneio de Xadrez Ilhéus/Itabuna Online - 30/03/2025")
st.write("Bem-vindo ao painel de análise do torneio de xadrez!")

# --- Upload do arquivo pelo usuário ---
arquivo = st.file_uploader("Carregue o arquivo do torneio", type=['csv'])

# --- Carregar um arquivo CSV padrão se nenhum arquivo for enviado ---
if arquivo is None:
    # Exemplo de dados padrão (substitua este CSV com o seu arquivo padrão)
    csv_padrao = """Rank,Title,Nomes dos Enxadristas,Rating,Points,Tie Break,Performance
1,,Alequis1991,2306,5.0,10.0,2480.2
2,,maalta7,2004,3.5,5.25,2240.6
3,,Capital78,2119,2.5,3.75,2017.6
4,,majCRVG,1800,2.0,2.5,1981.4
5,,ILUMINATE38,2289,2.0,2.0,1887.6
6,,Rogeriox,1709,0.0,0.0,1599.6
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
