"""
Módulo para geração de gráficos a partir das tabelas de frequência
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configurações gerais dos gráficos
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 12})
sns.set_palette("deep")

def plot_qualitative_graph(filename: str, title: str):
    """
    Gera um gráfico de barras para variáveis qualitativas
    
    @param nome_arquivo: Nome do arquivo CSV sem a extensão
    @param titulo: Título do gráfico
    """

    # Lê o arquivo CSV
    df = pd.read_csv(f"outputs/{filename}_table.csv")
    
    # Limita a quantidade de entradas para melhor visualização
    if len(df) > 10:
        df = df.iloc[:10].copy()  # Copia apenas as 10 primeiras linhas
    
    plt.figure(figsize=(12, 8))
    
    # Gráfico de barras
    ax = sns.barplot(x=filename, y="Frequência", data=df)
    plt.title(f"Distribuição de Frequência - {title}")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Adiciona os valores sobre as barras
    for i, v in enumerate(df["Frequência"]):
        ax.text(i, v + 5, str(v), ha='center')
    
    # Salva o gráfico
    plt.savefig(f"outputs/{filename}_grafico.png", dpi=300)
    plt.close()

def plot_quantitative_graph(filename: str, title: str):
    """
    Gera um histograma para variáveis quantitativas
    
    @param nome_arquivo: Nome do arquivo CSV sem a extensão
    @param titulo: Título do gráfico
    """

    # Lê o arquivo CSV
    df = pd.read_csv(f"outputs/{filename}_table.csv")
    
    plt.figure(figsize=(12, 8))
    
    # Extrai os intervalos e frequências
    intervals = df[filename].tolist()
    frequencies = df["Frequência"].tolist()
    
    # Gráfico de barras para representar o histograma
    ax = sns.barplot(x=intervals, y=frequencies)
    plt.title(f"Histograma - {title}")
    plt.xlabel(title)
    plt.ylabel("Frequência")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Adiciona os valores sobre as barras
    for i, v in enumerate(frequencies):
        ax.text(i, v + 5, str(v), ha='center')
    
    # Salva o gráfico
    plt.savefig(f"outputs/{filename}_grafico.png", dpi=300)
    plt.close()

def plot_release_date_graph(filename: str ="release_date"):
    """
    Gera um gráfico de linha para a variável de data de lançamento
    
    @param nome_arquivo: Nome do arquivo CSV sem a extensão
    @param titulo: Título do gráfico
    """

    # Lê o arquivo CSV
    df = pd.read_csv(f"outputs/{filename}_table.csv")
    
    plt.figure(figsize=(12, 8))
    
    # Extrai datas e frequências
    # Obtém apenas o ano do intervalo (primeiro 4 dígitos)
    years = [intervalo.split('-')[0][:4] for intervalo in df[filename]]
    frequencies = df["Frequência"].tolist()
    
    # Gráfico de linha para mostrar tendência temporal
    plt.plot(years, frequencies, marker='o', linewidth=2, markersize=8)
    plt.title(f"Tendência de Lançamentos ao Longo do Tempo")
    plt.xlabel("Ano")
    plt.ylabel("Número de Lançamentos")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Salva o gráfico
    plt.savefig(f"outputs/{filename}_grafico.png", dpi=300)
    plt.close()

def plot_all_graphs():
    """
    Função principal que gera todos os gráficos
    """

    # Cria o diretório outputs se não existir
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
        
    # Gera gráficos para variáveis qualitativas
    plot_qualitative_graph("artist_name", "Artistas")
    plot_qualitative_graph("primary_genres", "Gêneros Musicais Primários")
    plot_qualitative_graph("descriptors", "Descritores")
    
    # Gera gráficos para variáveis quantitativas
    plot_release_date_graph()
    plot_quantitative_graph("avg_rating", "Avaliação Média")
    plot_quantitative_graph("review_count", "Número de Avaliações")
    
    print("Todos os gráficos foram gerados com sucesso!")

if __name__ == "__main__":
    plot_all_graphs()