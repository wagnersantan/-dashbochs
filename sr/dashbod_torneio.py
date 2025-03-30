import streamlit as st
import pandas as pd
import plotly.express as px
import io

# --- Configuração de Estilo ---
st.set_page_config(page_title="Torneio de Xadrez", page_icon="♟️", layout="wide")

# --- Título do aplicativo ---
st.title("🏆 Torneio de Xadrez Ilhéus/Itabuna Online - 30/03/2025")
st.write("Bem-vindo ao painel de análise do torneio de xadrez!")

# --- Título do Aplicativo ---
st.markdown(
     "<h1 style='text-align: center; color: gold;'>🏆 Torneio de Xadrez Ilhéus/Itabuna - 30/03/2025</h1>",
    unsafe_allow_html=True
)
st.markdown("<h3 style='text-align: center;'>📊 Painel de Análise do Torneio</h3>", unsafe_allow_html=True)
st.divider()

# --- Upload do Arquivo ---
arquivo = st.file_uploader("📂 Carregue o arquivo do torneio (CSV)", type=['csv'])

# --- Dados Padrão Caso Nenhum Arquivo Seja Enviado ---
if arquivo is None:
    st.warning("Nenhum arquivo carregado. Usando dados de exemplo!")
    csv_padrao = """Rank,Title,Nomes dos Enxadristas,Rating,Points,Tie Break,Performance
1,,ILUMINATE38,2280,4.0,8.0,2502.5
2,,maalta7,2021,3.0,4.0,2242.5
3,,HeronSilva10,2012,2.0,3.0,2094.6667
4,,Hunter04,1906,2.0,3.0,2040.75
5,,majCRVG,1791,2.0,2.0,1710.3334
6,,Rogeriox,1713,1.0,1.5,1441.3334
7,,Capital78,2071,1.0,0.5,1569.0
"""
    arquivo = io.StringIO(csv_padrao)

# --- Processamento dos Dados ---
try:
    df = pd.read_csv(arquivo, encoding="utf-8")
    df['Points'] = pd.to_numeric(df['Points'], errors='coerce').fillna(0)

    # --- Estatísticas Gerais ---
    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Total de Jogadores", df.shape[0])
    col2.metric("🔥 Maior Rating", df["Rating"].max())
    col3.metric("🏅 Pontuação Máxima", df["Points"].max())

    st.divider()

    # --- Classificação Final ---
    st.markdown("### 🏅 Classificação Final")
    classificacao = df[['Nomes dos Enxadristas', 'Points']].sort_values(by='Points', ascending=False)

    # --- Destaque para os 3 Primeiros ---
    st.markdown("### 🏆 Pódio dos Vencedores")
    top3 = classificacao.head(3)
    podium = {
        1: "🥇",
        2: "🥈",
        3: "🥉"
    }
    for i, row in enumerate(top3.itertuples(), start=1):
        st.markdown(f"**{podium[i]} {row[1]} - {row[2]} pontos**")

    # --- Seleção de Jogador ---
    jogador_selecionado = st.selectbox("🔍 Selecione um jogador para ver mais detalhes:", df['Nomes dos Enxadristas'].unique())
    if jogador_selecionado:
        st.write(df[df['Nomes dos Enxadristas'] == jogador_selecionado])

    st.divider()

    # --- Criar Gráfico de Pontuação (Interativo) ---
    st.markdown("### 📈 Gráfico de Pontuação dos Jogadores")
    fig = px.bar(classificacao, 
                 x="Points", 
                 y="Nomes dos Enxadristas", 
                 text="Points",
                 orientation='h', 
                 color="Points", 
                 color_continuous_scale="blues",
                 title="Pontos por Jogador")

    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

    # --- Opção para Baixar os Dados ---
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Baixar Dados do Torneio", data=csv, file_name="torneio_xadrez.csv", mime="text/csv")

except Exception as e:
    st.error(f"❌ Erro ao carregar o arquivo: {e}")
