import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
    plt.title('Média das Avaliações vs. Número de Resenhas')
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
    plt.title('Média das Avaliações vs. Data de Lançamento')
    plt.xlabel('Intervalos de Data de Lançamento')
    plt.ylabel('Média das Avaliações')
    plt.xticks(rotation=45, ha='right')  # Rotacionar os rótulos do eixo X
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('outputs/Media_vs_Data.png')

    # Gráfico 3: Gêneros primários vs. Média das avaliações (corrigido)
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
    plt.bar(genre_avg['primary_genres'], genre_avg['avg_rating'], color='skyblue')
    plt.title('Média das Avaliações por Gênero Primário')
    plt.xlabel('Gêneros Primários')
    plt.ylabel('Média das Avaliações')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('outputs/Media_por_Genero.png')


    # Gráfico 4: Descritores vs. Média das avaliações (corrigido)
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
    plt.bar(descriptor_avg['descriptors'], descriptor_avg['avg_rating'], color='lightgreen')
    plt.title('Média das Avaliações por Descritor')
    plt.xlabel('Descritores')
    plt.ylabel('Média das Avaliações')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('outputs/Media_por_Descritor.png')

    # Gráfico 5: Evolução temporal da média por gênero
    genre_time_data = data[['release_date', 'primary_genres', 'avg_rating']].dropna()
    genre_time_data['release_date'] = pd.to_datetime(genre_time_data['release_date'])
    genre_time_data['primary_genres'] = genre_time_data['primary_genres'].str.split(',')
    genre_time_data = genre_time_data.explode('primary_genres')
    genre_time_data['primary_genres'] = genre_time_data['primary_genres'].str.strip()

    # Filtrar gêneros com pelo menos 100 ocorrências
    genre_counts = genre_time_data['primary_genres'].value_counts()
    valid_genres = genre_counts[genre_counts >= 100].index
    genre_time_data = genre_time_data[genre_time_data['primary_genres'].isin(valid_genres)]

    # Agrupar por intervalo de anos e gênero
    genre_time_data['year'] = genre_time_data['release_date'].dt.year
    bins = pd.interval_range(start=1950, end=2025, freq=10, closed='left')
    genre_time_data['decade'] = pd.cut(genre_time_data['year'], bins=bins)

    grouped = genre_time_data.groupby(['decade', 'primary_genres'])['avg_rating'].mean().reset_index()

    # Pivotar para ter décadas como eixo x e gêneros como colunas
    pivoted = grouped.pivot(index='decade', columns='primary_genres', values='avg_rating')

    # Selecionar os gêneros com mais dados (top 5 com menos valores nulos)
    top_genres = pivoted.count().sort_values(ascending=False).head(5).index
    pivoted = pivoted[top_genres]

    # Plotar gráfico
    plt.figure(figsize=(12, 6))
    pivoted.plot(marker='o')
    plt.title('Evolução da Média das Avaliações por Gênero ao Longo das Décadas')
    plt.xlabel('Década')
    plt.ylabel('Média das Avaliações')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.legend(title='Gênero')
    plt.savefig('outputs/Media_por_Genero_Tempo.png')

if __name__ == "__main__":
    plot_variable_relationships()