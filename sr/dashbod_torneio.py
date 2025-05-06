import streamlit as st
import pandas as pd
import plotly.express as px
import io
import os               
from PIL import Image   


st.set_page_config(
    page_title="Torneio de Xadrez Online",
    page_icon="♟️",
    layout="wide",
    initial_sidebar_state="expanded"
)


with st.sidebar:
    st.header("📌 Menu")
    # 🥈 Imagem do 2º Lugar - Ricardo Abdon
    st.subheader("🥈 2º Lugar - Ricardo Abdon")
    caminho_ricardo = os.path.join("sr", "Ricardo_Abdon.jpg")  
    imagem_ricardo = Image.open(caminho_ricardo)
    st.image(imagem_ricardo, caption="Ricardo Abdon", use_container_width=True)
    
    
    # 🥉 Imagem do 3º Lugar - Daniel Malta
   
    st.subheader("🥉 3º Lugar - Daniel Malta")
    caminho_imagem = os.path.join("sr", "daniel_malta.jpg")
    imagem = Image.open(caminho_imagem)
    st.image(imagem, caption="Daniel Malta", use_column_width=True)

    arquivos = st.file_uploader(
        "📂 Carregue os arquivos do torneio (CSV)", 
        type=['csv'], 
        accept_multiple_files=True
    )

if not arquivos:
    st.warning("Nenhum arquivo carregado. Faça o upload na barra lateral.")
else:
    st.success(f"{len(arquivos)} arquivo(s) carregado(s) com sucesso!")

# --- Título ---
st.title("🏆 Torneio de Xadrez Ilhéus/Itabuna Lichess 2025")
st.markdown("<h1 style='text-align: center; color: gold;'>🏆 Torneio de Xadrez</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>📊 Painel de Análise</h3>", unsafe_allow_html=True)
st.divider()

# --- Dados Padrão ---
if not arquivos:
    csv_padrao_1 = """Rank,Title,Nomes dos Enxadristas,Rating,Points,Tie Break,Performance,Torneio
1,,Alequis1991,2306,5.0,10.0,2480.2,Torneio 23/03/2025
2,,maalta7,2004,3.5,5.25,2240.6,Torneio 23/03/2025
3,,Capital78,2119,2.5,3.75,2017.6,Torneio 23/03/2025
4,,majCRVG,1800,2.0,2.5,1981.4,Torneio 23/03/2025
5,,ILUMINATE38,2289,2.0,2.0,1887.6,Torneio 23/03/2025"""

    csv_padrao_2 = """Rank,Title,Nomes dos Enxadristas,Rating,Points,Tie Break,Performance,Torneio
1,,ILUMINATE38,2280,4.0,8.0,2502.5,Torneio 30/03/2025
2,,maalta7,2021,3.0,4.0,2242.5,Torneio 30/03/2025
3,,HeronSilva10,2012,2.0,3.0,2094.6667,Torneio 30/03/2025
4,,Hunter04,1906,2.0,3.0,2040.75,Torneio 30/03/2025
5,,majCRVG,1791,2.0,2.0,1710.3334,Torneio 30/03/2025"""

    csv_padrao_3 = """Rank,Title,Nomes dos Enxadristas,Rating,Points,Tie Break,Performance,Torneio
1,,ILUMINATE38,2304,5.5,16.75,2387.0,Torneio 06/04/2025
2,,Capital78,2127,5.0,15.0,2288.8333,Torneio 06/04/2025
3,,maalta7,2004,3.0,8.0,1998.1666,Torneio 06/04/2025
4,,majCRVG,1812,3.0,7.0,1862.0,Torneio 06/04/2025
5,,Hunter04,1877,3.0,6.5,2053.8333,Torneio 06/04/2025
6,,Rogeriox,1830,3.0,6.5,1938.0,Torneio 06/04/2025
7,,sualks,1905,3.0,6.0,1859.8,Torneio 06/04/2025
8,,ramonnlucass,2040,2.0,4.5,1772.5,Torneio 06/04/2025
9,,wagsantana,1945,1.5,4.25,1545.8,Torneio 06/04/2025"""

    arquivos = [io.StringIO(csv_padrao_1), io.StringIO(csv_padrao_2), io.StringIO(csv_padrao_3)]

# --- Processamento dos Dados ---
df_list = []
colunas_esperadas = ["Rank", "Title", "Nomes dos Enxadristas", "Rating", "Points", "Tie Break", "Performance", "Torneio"]

for arquivo in arquivos:
    try:
        df = pd.read_csv(arquivo, encoding="utf-8")
        if not all(col in df.columns for col in colunas_esperadas):
            st.error("O arquivo carregado não possui todas as colunas necessárias!")
            continue
        df_list.append(df)
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")

if df_list:
    df_final = pd.concat(df_list, ignore_index=True).drop_duplicates()
    df_final['Points'] = pd.to_numeric(df_final['Points'], errors='coerce').fillna(0)

    # Filtro por Jogadores com mais pontos acumulados
    pontos_totais = df_final.groupby("Nomes dos Enxadristas")["Points"].sum().reset_index()
    pontos_totais = pontos_totais.sort_values(by="Points", ascending=False)
    
    top_jogadores = st.sidebar.multiselect(
        "🎯 Filtrar por Jogadores com Mais Pontos Acumulados",
        options=pontos_totais["Nomes dos Enxadristas"],
        default=pontos_totais.head(3)["Nomes dos Enxadristas"].tolist()
    )

    # Apresenta ranking geral de pontos
    with st.expander("📈 Ver Ranking Geral dos Jogadores"):
        st.dataframe(pontos_totais, use_container_width=True)

    torneios = df_final["Torneio"].unique()
    abas = st.tabs([f"{torneio}" for torneio in torneios])

    for i, torneio in enumerate(torneios):
        with abas[i]:
            st.markdown(f"## 🏆 {torneio}")
            df_torneio = df_final[df_final["Torneio"] == torneio]

            if top_jogadores:
                df_torneio = df_torneio[df_torneio["Nomes dos Enxadristas"].isin(top_jogadores)]

            col1, col2, col3, col4 = st.columns(4)
            col1.metric("👥 Total de Jogadores", df_torneio.shape[0])
            col2.metric("🔥 Maior Rating", df_torneio["Rating"].max())
            col3.metric("🏅 Pontuação Máxima", df_torneio["Points"].max())
            col4.metric("📊 Média de Rating", round(df_torneio["Rating"].mean(), 2))

            st.divider()

            st.markdown("### 🏅 Classificação Final")
            classificacao = df_torneio[['Nomes dos Enxadristas', 'Points']].sort_values(by='Points', ascending=False)

            st.markdown("### 🏆 Pódio dos Vencedores")
            top3 = classificacao.head(3)
            podium = {1: "🥇", 2: "🥈", 3: "🥉"}
            for i, row in enumerate(top3.itertuples(), start=1):
                st.markdown(f"**{podium[i]} {row[1]} - {row[2]} pontos**")

            num_jogadores = st.slider(f"👤 Jogadores no gráfico ({torneio})", 5, df_torneio.shape[0], 10)
            fig = px.bar(classificacao.head(num_jogadores),
                         x="Points",
                         y="Nomes dos Enxadristas",
                         text="Points",
                         orientation='h',
                         color="Points",
                         color_continuous_scale="blues",
                         title=f"Pontos por Jogador - {torneio}")
            fig.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

            csv_torneio = df_torneio.to_csv(index=False).encode('utf-8')
            st.download_button(f"📥 Baixar Dados de {torneio}", data=csv_torneio, file_name=f"{torneio}.csv", mime="text/csv")


