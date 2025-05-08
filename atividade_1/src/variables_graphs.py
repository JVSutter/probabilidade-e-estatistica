"""
Módulo para geração de gráficos a partir das tabelas de frequência
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from frequency_tables import quantitative_vars, qualitative_vars, translation

# Configurações gerais dos gráficos
plt.style.use('ggplot')
plt.rcParams.update({'font.size': 12})
sns.set_palette("deep")

def plot_qualitative_graph(filename: str):
    """
    Gera um gráfico de barras para variáveis qualitativas
    
    @param nome_arquivo: Nome do arquivo CSV sem a extensão
    @param titulo: Título do gráfico
    """

    # Lê o arquivo CSV
    df = pd.read_csv(f"outputs/{filename}_table.csv")
    
    # Limita a quantidade de entradas para melhor visualização
    if len(df) > 15:
        df = df.iloc[:15].copy()  # Copia apenas as 10 primeiras linhas
    
    plt.figure(figsize=(12, 8))
    
    # Gráfico de barras
    ax = sns.barplot(x=filename, y="Frequência", data=df)
    plt.title("Mostrando apenas as 15 maiores frequências")
    plt.xlabel(filename)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Adiciona os valores sobre as barras
    max_value = df["Frequência"].max()
    for i, v in enumerate(df["Frequência"]):
        ax.text(i, v + 0.01 * max_value, str(v), ha='center')
    
    # Salva o gráfico
    plt.savefig(f"outputs/{filename}_grafico.png", dpi=300)
    plt.close()

def plot_quantitative_graph(filename: str):
    """
    Gera um histograma para variáveis quantitativas
    
    @param nome_arquivo: Nome do arquivo CSV sem a extensão
    @param titulo: Título do gráfico
    """

    # Lê o arquivo CSV
    path = f"outputs/{filename}_table.csv"
    if filename == "Número de resenhas":
        path = f"outputs/{filename}_ajustado_table.csv"
    df = pd.read_csv(path)
    
    plt.figure(figsize=(12, 8))
    
    # Extrai os intervalos e frequências
    intervals = df[filename].tolist()
    frequencies = df["Frequência"].tolist()
    
    # Gráfico de barras para representar o histograma
    ax = sns.barplot(x=intervals, y=frequencies)
    plt.xlabel(filename)
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
    years = [interval.split('-')[0][:4] for interval in df[filename]]
    frequencies = df["Frequência"].tolist()
    
    # Gráfico de linha para mostrar tendência temporal
    plt.plot(years, frequencies, marker='o', linewidth=2, markersize=8)
    plt.xlabel("Ano")
    plt.ylabel("Número de Lançamentos")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Salva o gráfico
    plt.savefig(f"outputs/{filename}_grafico.png", dpi=300)
    plt.close()

 #Distribuicao da media das avaliacoes
def plot_boxplot(filename: str = "Média das avaliações",
                 graphname: str = "boxplot"
                 ):

    df = pd.read_csv(f"outputs/{filename}_table.csv")
    
    plt.figure(figsize=(12, 8))
    
    # 1. Converter intervalos para valores numéricos (usando o ponto médio)
    df['Ponto Médio'] = df[filename].apply(lambda x: np.mean([float(i) for i in x.split(' - ')]))
    
    # 2. Ajeita os dados 
    stats = {
        'med': 2.54,    # Mediana (Q2)
        'q1': 3.28,     # Primeiro quartil (25%)
        'q3': 3.80,     # Terceiro quartil (75%)
        'whislo': 2.5, # Mínimo (sem outliers)
        'whishi': 4.58  # Máximo (sem outliers)
    }
    
    
    # 4. Criar o boxplot com os dados simulados
    a = sns.boxplot(x=df['Ponto Médio'],
                          showfliers = True,
                       color = 'skyblue',
                        vert= False)    

    # Salva o gráfico
    plt.savefig(f"outputs/{graphname}_grafico.png", dpi=300, bbox_inches='tight')
    plt.close()


def plot_all_graphs():
    """
    Função principal que gera todos os gráficos
    """

    # Cria o diretório outputs se não existir
    if not os.path.exists("outputs"):
        os.makedirs("outputs")
        
    # Gera gráficos para variáveis qualitativas
    for variable in qualitative_vars:
        plot_qualitative_graph(translation[variable])
    
    # Gera gráficos para variáveis quantitativas
    plot_release_date_graph(translation["release_date"])
    plot_quantitative_graph(translation["avg_rating"])
    plot_quantitative_graph(translation["review_count"])
    plot_boxplot()
    
    print("Todos os gráficos foram gerados com sucesso!")

if __name__ == "__main__":
    plot_all_graphs()
