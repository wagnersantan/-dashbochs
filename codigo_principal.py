import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# --- Título do aplicativo ---
st.title("🏆 Torneio de Xadrez Ilhéus/Itabuna Online - 23/03/2025")
st.write("Bem-vindo ao painel de análise do torneio de xadrez!")

# --- Upload do arquivo pelo usuário ---
arquivo = st.file_uploader("📂 Carregue o arquivo do torneio (CSV)", type=['csv'])

# --- Dados padrão caso nenhum arquivo seja enviado ---
if arquivo is None:
    st.warning("Nenhum arquivo carregado. Usando dados de exemplo!")
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
    # Carregar os dados
    df = pd.read_csv(arquivo, encoding="utf-8")

    # Garantir que as colunas esperadas estão presentes
    colunas_esperadas = {'Rank', 'Title', 'Nomes dos Enxadristas', 'Rating', 'Points', 'Tie Break', 'Performance'}
    if not colunas_esperadas.issubset(df.columns):
        st.error("❌ O arquivo CSV não contém as colunas esperadas! Verifique o formato.")
        st.stop()

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
    st.write("### 🎖️ Top 10 Jogadores")
    jogadores_top = classificacao.head(10)
    st.dataframe(jogadores_top)

    # --- Filtragem de Jogadores ---
    jogador_selecionado = st.selectbox("🔍 Selecione um jogador para ver mais detalhes:", df['Nomes dos Enxadristas'].unique())
    if jogador_selecionado:
        st.write(df[df['Nomes dos Enxadristas'] == jogador_selecionado])

    # --- Criar Gráfico de Pontuação ---
    st.write("### 📈 Gráfico de Pontuação dos Jogadores")

    # Remover jogadores sem pontuação (opcional)
    classificacao = classificacao[classificacao['Points'] > 0]

    # Ordenar os dados para o gráfico
    classificacao = classificacao.sort_values(by='Points', ascending=True)

    # Criar gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    cores = ['gold' if i == classificacao.index[-1] else 
             'silver' if i == classificacao.index[-2] else 
             'brown' if i == classificacao.index[-3] else 'blue' 
             for i in classificacao.index]

    ax.barh(classificacao['Nomes dos Enxadristas'], classificacao['Points'], color=cores)

    # Melhorando a formatação do gráfico
    ax.set_xlabel("Pontos", fontsize=12)
    ax.set_ylabel("Jogador", fontsize=12)
    ax.set_title("Pontos por Jogador (Ordenado por Maior Pontuação)", fontsize=14)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)

    # Exibir gráfico no Streamlit
    st.pyplot(fig)

    # --- Opção para baixar os dados processados ---
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Dados do Torneio", data=csv, file_name="torneio_xadrez.csv", mime="text/csv")

except Exception as e:
    st.error(f"❌ Erro ao carregar o arquivo: {e}")
