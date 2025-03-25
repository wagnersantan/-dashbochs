import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# Caminho correto do arquivo CSV
caminho_arquivo = r"C:\Users\wagne\OneDrive\Documentos\Meusprojetos\MeusProjetos\Torneio.csv.csv"  # Corrigido para o nome correto do arquivo

# Verificar se o arquivo existe antes de carregar
if os.path.exists(caminho_arquivo):
    try:
        # Carregar o arquivo CSV sem cabeçalhos e atribuindo as colunas manualmente
        colunas = ['Rank', 'Title', 'Nomes dos Enxadristas', 'Rating', 'Points', 'Tie Break', 'Performance']
        df = pd.read_csv(caminho_arquivo, encoding="utf-8", sep=",", header=None, names=colunas)  # Ajuste para o separador correto

        # Convertendo a coluna 'Points' para valores numéricos, substituindo NaN por 0
        df['Points'] = pd.to_numeric(df['Points'], errors='coerce').fillna(0)  # Substitui NaN por 0 para garantir que todas as barras sejam visíveis

        # Exibir título e dados brutos
        st.title("Torneio de Xadrez Ilhéus/Itabuna Online 23/03/2025")
        st.write("### Dados Brutos")
        st.dataframe(df)  # Mostrar os dados

        # **1. Exibir a Classificação Final**
        if 'Nomes dos Enxadristas' in df.columns and 'Points' in df.columns:
            st.write("### Classificação Final")
            # Classificar os jogadores pela pontuação (decrescente)
            classificacao = df[['Nomes dos Enxadristas', 'Points']].sort_values(by='Points', ascending=False)
            st.dataframe(classificacao)

        # **2. Exibir os Jogadores com Mais Pontos**
        st.write("### Jogadores com Mais Pontos")
        jogadores_top = df[['Nomes dos Enxadristas', 'Points']].sort_values(by='Points', ascending=False)
        st.dataframe(jogadores_top)

        # **3. Criar um Gráfico de Pontuação (Gráfico de Barras Horizontal)**
        if 'Nomes dos Enxadristas' in df.columns and 'Points' in df.columns:
            st.write("### Gráfico de Pontuação dos Jogadores")
            
            # Remover "Rogeriox" da classificação
            classificacao = classificacao[classificacao['Nomes dos Enxadristas'] != 'Rogeriox']

            # Ordenar os dados em ordem decrescente para o gráfico
            classificacao = classificacao.sort_values(by='Points', ascending=False)

            fig, ax = plt.subplots(figsize=(12, 8))  # Tamanho ajustado para o gráfico (aumentado para dar mais espaço)

            # Plotando as barras horizontais
            ax.barh(classificacao['Nomes dos Enxadristas'], classificacao['Points'], color='blue')

            # Ajustar as labels para evitar sobreposição
            plt.xticks(fontsize=10)
            plt.yticks(fontsize=10)  # Mostrar os nomes dos jogadores

            # Garantir que o eixo X comece do 0 para visualizar a barra com 0 pontos
            plt.xlim(left=0)  # Garante que o eixo X comece do 0

            # Ajustar o layout para evitar que as barras fiquem cortadas
            plt.tight_layout()

            # Ajustes para título e rótulos
            plt.xlabel("Pontos", fontsize=12)
            plt.ylabel("Jogador", fontsize=12)
            plt.title("Pontos por Jogador (Ordenado por Maior Pontuação)", fontsize=14)

            # Exibir gráfico
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
else:
    st.error(f"Arquivo não encontrado: {caminho_arquivo}")

