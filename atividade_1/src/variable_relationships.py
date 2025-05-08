import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import seaborn as sns

from frequency_tables import sturges_rule

# Carregar o dataset
data = pd.read_csv('assets/rym_clean1.csv')

def group_and_average(data, column, values_column, nbins):
    """
    Agrupa os valores em intervalos e calcula a média para cada intervalo.
    """
    is_datetime = np.issubdtype(data[column].dtype, np.datetime64)

    # Se for datetime, criar uma cópia numérica para binning
    col_for_binning = data[column].astype('int64') if is_datetime else data[column]

    min_val, max_val = col_for_binning.min(), col_for_binning.max()
    bin_edges = np.linspace(min_val, max_val, nbins + 1)
    data['Intervalo'] = pd.cut(col_for_binning, bins=bin_edges, include_lowest=True)
    grouped = data.groupby('Intervalo')[values_column].mean().reset_index()
    grouped.rename(columns={values_column: 'Média'}, inplace=True)

    # Reverter intervalos para datas legíveis, se necessário
    if is_datetime:
        grouped['Intervalo'] = grouped['Intervalo'].apply(
            lambda x: f"{pd.to_datetime(x.left).date()} - {pd.to_datetime(x.right).date()}"
        )

    return grouped


def plot_variable_relationships():
    """
    Gera gráficos de relação entre variáveis.
    """
    # Configuração geral
    plt.style.use('ggplot')

    # Gráfico 1: Média das avaliações vs. Número de resenhas
    plt.figure(figsize=(8, 6))
    plt.scatter(data['review_count'], data['avg_rating'], alpha=0.7)
    plt.xlabel('Número de Resenhas')
    plt.ylabel('Média das Avaliações')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('outputs/Media_vs_Resenhas.png')

    # Gráfico 2: Data de lançamento vs. Média das avaliações
    data['release_date'] = pd.to_datetime(data['release_date'])
    nbins = sturges_rule(len(data))
    grouped_data = group_and_average(data, 'release_date', 'avg_rating', nbins)
    grouped_data.plot(kind='line', x='Intervalo', y='Média', figsize=(10, 6), marker='o')
    plt.xlabel('Intervalos de Data de Lançamento')
    plt.ylabel('Média das Avaliações')
    plt.xticks(rotation=45, ha='right')  # Rotacionar os rótulos do eixo X
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('outputs/Media_vs_Data.png')

    # Gráfico 3: Gêneros primários vs. Média das avaliações
    genre_data = data[['primary_genres', 'avg_rating']].dropna()

    # Separar múltiplos gêneros
    genre_data['primary_genres'] = genre_data['primary_genres'].str.split(',')

    # Remover espaços extras e explodir
    genre_data = genre_data.explode('primary_genres')
    genre_data['primary_genres'] = genre_data['primary_genres'].str.strip()

    # Contar aparições de cada gênero
    genre_counts = genre_data['primary_genres'].value_counts()

    # Definir mínimo de ocorrências (ex: pelo menos 20)
    min_count = 100
    valid_genres = genre_counts[genre_counts >= min_count].index

    # Filtrar gêneros válidos
    filtered_genre_data = genre_data[genre_data['primary_genres'].isin(valid_genres)]

    # Calcular média apenas dos válidos
    genre_avg = filtered_genre_data.groupby('primary_genres')['avg_rating'].mean().reset_index()
    genre_avg = genre_avg.sort_values(by='avg_rating', ascending=False).head(10)

    # Plotar
    plt.figure(figsize=(10, 6))
    bars = plt.bar(genre_avg['primary_genres'], genre_avg['avg_rating'], color='skyblue')
    plt.xlabel('Gêneros Primários')
    plt.ylabel('Média das Avaliações')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Adicionar valores acima das barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

    plt.savefig('outputs/Media_por_Genero.png')

    # Gráfico 4: Descritores vs. Média das avaliações
    descriptor_data = data[['descriptors', 'avg_rating']].dropna()

    # Separar múltiplos descritores em listas
    descriptor_data['descriptors'] = descriptor_data['descriptors'].str.split(',')

    # Remover espaços e explodir
    descriptor_data = descriptor_data.explode('descriptors')
    descriptor_data['descriptors'] = descriptor_data['descriptors'].str.strip()

    # Contar aparições de cada descritor
    descriptor_counts = descriptor_data['descriptors'].value_counts()

    # Definir mínimo de ocorrências (ex: pelo menos 20)
    min_count = 100
    valid_descriptors = descriptor_counts[descriptor_counts >= min_count].index

    # Filtrar descritores válidos
    filtered_descriptor_data = descriptor_data[descriptor_data['descriptors'].isin(valid_descriptors)]

    # Calcular média apenas dos válidos
    descriptor_avg = filtered_descriptor_data.groupby('descriptors')['avg_rating'].mean().reset_index()
    descriptor_avg = descriptor_avg.sort_values(by='avg_rating', ascending=False).head(10)

    # Plotar
    plt.figure(figsize=(10, 6))
    bars = plt.bar(descriptor_avg['descriptors'], descriptor_avg['avg_rating'], color='lightgreen')
    plt.xlabel('Descritores')
    plt.ylabel('Média das Avaliações')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Adicionar valores acima das barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}', ha='center', va='bottom')

    plt.savefig('outputs/Media_por_Descritor.png')

    # Descritor por data
    descriptor_time_data = data[['release_date', 'descriptors']].dropna()
    descriptor_time_data['release_date'] = pd.to_datetime(descriptor_time_data['release_date'])
    descriptor_time_data['year'] = descriptor_time_data['release_date'].dt.year

    # Criar colunas de década
    descriptor_time_data['decade'] = (descriptor_time_data['year'] // 10) * 10
    descriptor_time_data['decade'] = descriptor_time_data['decade'].astype(int).astype(str) + 's'

    # Explodir os descritores
    descriptor_time_data['descriptors'] = descriptor_time_data['descriptors'].str.split(',')
    descriptor_time_data = descriptor_time_data.explode('descriptors')
    descriptor_time_data['descriptors'] = descriptor_time_data['descriptors'].str.strip()

    # Filtrar descritores frequentes
    descriptor_counts = descriptor_time_data['descriptors'].value_counts()
    min_count = 100
    top_descriptors = descriptor_counts[descriptor_counts >= min_count].index
    descriptor_time_data = descriptor_time_data[descriptor_time_data['descriptors'].isin(top_descriptors)]

    # Tabela de frequência: descritor vs. década
    freq_table = pd.crosstab(descriptor_time_data['decade'], descriptor_time_data['descriptors'])

    # Manter apenas os N descritores mais frequentes
    top_N = 10
    top_columns = freq_table.sum().sort_values(ascending=False).head(top_N).index
    freq_table = freq_table[top_columns]

    # Plotar heatmap
    plt.figure(figsize=(12, 6))
    sns.heatmap(freq_table.T, cmap='YlGnBu', annot=True, fmt='d')
    plt.xlabel('Década')
    plt.ylabel('Descritor')
    plt.tight_layout()
    plt.savefig('outputs/Descritores_por_Tempo.png')


if __name__ == "__main__":
    plot_variable_relationships()