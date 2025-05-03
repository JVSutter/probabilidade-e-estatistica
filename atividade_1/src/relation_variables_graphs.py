import pandas as pd
import matplotlib.pyplot as plt

from frequency_tables import translation

# Carregar o dataset
data = pd.read_csv('assets/rym_clean1.csv')

def plot_relation_variables():
    # Exemplo 1: Média das avaliações vs. Número de resenhas
    plt.figure(figsize=(8, 6))
    plt.scatter(data['review_count'], data['avg_rating'], alpha=0.7)
    plt.title('Média das Avaliações vs. Número de Resenhas')
    plt.xlabel('Número de Resenhas')
    plt.ylabel('Média das Avaliações')
    plt.grid(True)
    plt.savefig('outputs/Media_vs_Resenhas.png')

    # Exemplo 2: Data de lançamento vs. Média das avaliações
    plt.figure(figsize=(8, 6))
    plt.scatter(data['release_date'], data['avg_rating'], alpha=0.7)
    plt.title('Média das Avaliações vs. Data de Lançamento')
    plt.xlabel('Data de Lançamento')
    plt.ylabel('Média das Avaliações')
    plt.grid(True)
    plt.savefig('outputs/Media_vs_Data.png')

    # Exemplo 3: Gêneros primários vs. Média das avaliações (usando média por gênero)
    genre_avg = data.groupby('primary_genres')['avg_rating'].mean().sort_values()
    genre_avg.plot(kind='bar', figsize=(10, 6), color='skyblue')
    plt.title('Média das Avaliações por Gênero Primário')
    plt.xlabel('Gêneros Primários')
    plt.ylabel('Média das Avaliações')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/Media_por_Genero.png')

    # Exemplo 4: Descritores vs. Média das avaliações (usando média por descritor)
    descriptor_avg = data.groupby('descriptors')['avg_rating'].mean().sort_values()
    descriptor_avg.plot(kind='bar', figsize=(10, 6), color='lightgreen')
    plt.title('Média das Avaliações por Descritor')
    plt.xlabel('Descritores')
    plt.ylabel('Média das Avaliações')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('outputs/Media_por_Descritor.png')

    print("Gráficos de relação entre variáveis gerados com sucesso!")