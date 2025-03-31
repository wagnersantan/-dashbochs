import streamlit as st
import pandas as pd
import plotly.express as px
import io

# --- Configuração de Estilo ---

st.set_page_config(page_title="Torneio de Xadrez", page_icon="♟️", layout="wide", initial_sidebar_state="expanded")

# --- Título do aplicativo ---
st.title("🏆 Torneio de Xadrez Ilhéuse/Itabuna Lichess ")
st.write("Bem-vindo ao painel de análise do torneio de xadrez!")

# --- Título do Aplicativo ---
st.markdown(
    "<h1 style='text-align: center; color: gold;'>🏆 Torneio de Xadrez</h1>",
    unsafe_allow_html=True
)
st.markdown("<h3 style='text-align: center;'>📊 Painel de Análise</h3>", unsafe_allow_html=True)
st.divider()

# --- Upload do Arquivo ---
arquivos = st.file_uploader("📂 Carregue os arquivos do torneio (CSV)", type=['csv'], accept_multiple_files=True)

# --- Dados Padrão Caso Nenhum Arquivo Seja Enviado ---
if not arquivos:
    st.warning("Nenhum arquivo carregado. Usando dados de exemplo!")
    csv_padrao_1 = """Rank,Title,Nomes dos Enxadristas,Rating,Points,Tie Break,Performance,Torneio
1,,Alequis1991,2306,5.0,10.0,2480.2,Torneio 23/03/2025
2,,maalta7,2004,3.5,5.25,2240.6,Torneio 23/03/2025
3,,Capital78,2119,2.5,3.75,2017.6,Torneio 23/03/2025
4,,majCRVG,1800,2.0,2.5,1981.4,Torneio 23/03/2025
5,,ILUMINATE38,2289,2.0,2.0,1887.6,Torneio 23/03/2025
"""
    csv_padrao_2 = """Rank,Title,Nomes dos Enxadristas,Rating,Points,Tie Break,Performance,Torneio
1,,ILUMINATE38,2280,4.0,8.0,2502.5,Torneio 30/03/2025
2,,maalta7,2021,3.0,4.0,2242.5,Torneio 30/03/2025
3,,HeronSilva10,2012,2.0,3.0,2094.6667,Torneio 30/03/2025
4,,Hunter04,1906,2.0,3.0,2040.75,Torneio 30/03/2025
5,,majCRVG,1791,2.0,2.0,1710.3334,Torneio 30/03/2025
"""
    arquivos = [io.StringIO(csv_padrao_1), io.StringIO(csv_padrao_2)]

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
    # Concatena os DataFrames e remove duplicatas
    df_final = pd.concat(df_list, ignore_index=True).drop_duplicates()
    
    # Certifique-se de que a coluna 'Points' seja numérica
    df_final['Points'] = pd.to_numeric(df_final['Points'], errors='coerce').fillna(0)

    # --- Estatísticas por Torneio ---
    torneios = df_final["Torneio"].unique()
    if len(torneios) == 0:
        st.warning("Nenhum torneio encontrado.")
    else:
        for torneio in torneios:
            st.markdown(f"## 🏆 {torneio}")
            df_torneio = df_final[df_final["Torneio"] == torneio]
            
            if df_torneio.empty:
                st.warning(f"Nenhum dado encontrado para o torneio {torneio}.")
                continue
            
            # --- Estatísticas Gerais ---
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("👥 Total de Jogadores", df_torneio.shape[0])
            col2.metric("🔥 Maior Rating", df_torneio["Rating"].max())
            col3.metric("🏅 Pontuação Máxima", df_torneio["Points"].max())
            col4.metric("📊 Média de Rating", round(df_torneio["Rating"].mean(), 2))
            
            st.divider()
            
            # --- Classificação Final ---
            st.markdown("### 🏅 Classificação Final")
            classificacao = df_torneio[['Nomes dos Enxadristas', 'Points']].sort_values(by='Points', ascending=False)
            
            # --- Pódio dos 3 Primeiros ---
            st.markdown("### 🏆 Pódio dos Vencedores")
            top3 = classificacao.head(3)
            podium = {1: "🥇", 2: "🥈", 3: "🥉"}
            for i, row in enumerate(top3.itertuples(), start=1):
                st.markdown(f"**{podium[i]} {row[1]} - {row[2]} pontos**")
            
            # --- Criar Gráfico de Pontuação ---
            num_jogadores = st.slider(f"👤 Quantos jogadores exibir no gráfico ({torneio})?", 5, df_torneio.shape[0], 10)
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
            
            # --- Download dos Dados ---
            csv_torneio = df_torneio.to_csv(index=False).encode('utf-8')
            st.download_button(f"📥 Baixar Dados de {torneio}", data=csv_torneio, file_name=f"{torneio}.csv", mime="text/csv")
