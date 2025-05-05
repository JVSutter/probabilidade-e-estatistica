import math
from collections import Counter
from typing import Iterable
import csv

#!/usr/bin/env python3
"""
Este script calcula estatísticas descritivas para um conjunto de dados.
Calcula medidas de tendência central (média, mediana, moda),
medidas posicionais (quartis, percentis)
e medidas de dispersão (amplitude, variância, desvio padrão, intervalo interquartílico e coeficiente de variação).
"""

qualitative_vars = ["artist_name", "primary_genres", "descriptors"]
quantitative_vars = ["release_date", "avg_rating", "review_count"]
data: dict[str, set[str]] = {
column: set() for column in (qualitative_vars + quantitative_vars)
}  # Mapeia coluna -> conjunto de dados lidos
data_occurences: dict[str, int] = {}  # Mapeia dado -> número de ocorrências

def calculate_mean(data):
    """Retorna a média da lista de dados."""
    return sum(data) / len(data)

def calculate_median(data):
    """Retorna a mediana da lista de dados."""
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]

def calculate_mode(data):
    """Retorna a(s) moda(s) da lista de dados como uma lista.
    Se todos os números ocorrerem igualmente, retorna toda a lista ordenada."""
    count = Counter(data)
    max_occurrence = max(count.values())
    modes = [x for x, occ in count.items() if occ == max_occurrence]
    return sorted(modes)

def calculate_percentile(data, percentile):
    """Retorna o percentil informado da lista de dados.
    Utiliza interpolação linear entre posições mais próximas."""
    if not 0 <= percentile <= 100:
        raise ValueError("O percentil deve estar entre 0 e 100")
    sorted_data = sorted(data)
    n = len(sorted_data)
    # Calcula a posição do ranking
    rank = (n - 1) * (percentile / 100)
    lower = math.floor(rank)
    upper = math.ceil(rank)
    # Se o ranking for inteiro, retorna o valor diretamente
    if lower == upper:
        return sorted_data[int(rank)]
    # Caso contrário, interpola entre os dois valores vizinhos
    lower_value = sorted_data[lower]
    upper_value = sorted_data[upper]
    weight = rank - lower
    return lower_value + weight * (upper_value - lower_value)

def calculate_quartiles(data):
    """Retorna o primeiro (Q1), segundo (Q2/Mediana) e terceiro (Q3) quartis da lista de dados."""
    Q1 = calculate_percentile(data, 25)
    Q2 = calculate_median(data)
    Q3 = calculate_percentile(data, 75)
    return Q1, Q2, Q3

def calculate_decil(data, decil_index):
    """Retorna o decil informado da lista de dados.
    
    @param data: Lista de dados numéricos.
    @param decil_index: Índice do decil (inteiro de 1 a 9).
    @return: Valor do decil calculado utilizando o percentil correspondente.
    """
    if not 1 <= decil_index <= 9:
        raise ValueError("O índice do decil deve estar entre 1 e 9")
    # O decil 1 corresponde ao percentil 10, o decil 2 ao percentil 20, e assim por diante.
    return calculate_percentile(data, decil_index * 10)

def calculate_range(data):
    """Retorna a amplitude (máximo - mínimo) da lista de dados."""
    return max(data) - min(data)

def calculate_variance(data):
    """Retorna a variância populacional da lista de dados."""
    mean_value = calculate_mean(data)
    return sum((x - mean_value) ** 2 for x in data) / len(data)

def calculate_standard_deviation(data):
    """Retorna o desvio padrão populacional da lista de dados."""
    return math.sqrt(calculate_variance(data))

def calculate_interquartile_range(data):
    """Retorna o intervalo interquartílico (IQR) da lista de dados."""
    Q1, _, Q3 = calculate_quartiles(data)
    return Q3 - Q1

def calculate_coefficient_of_variation(data):
    """Retorna o coeficiente de variação (desvio padrão / média) da lista de dados."""
    mean_value = calculate_mean(data)
    if mean_value == 0:
        return float('inf')
    return calculate_standard_deviation(data) / mean_value

def get_column_numbers(reader: Iterable[list[str]], variables: list) -> dict[str, int]:
    """
    Função que dinamicamente obtém os números das colunas relevantes

    @param reader: Objeto CSV reader
    @param variables: Lista de variáveis cujas colunas queremos mapear
    """

    column_numbers = {}  # Mapeia nome da coluna -> número da coluna
    for i, column in enumerate(next(reader)):
        if column in variables:
            column_numbers[column] = i
    return column_numbers

def get_csv_data() -> None:
    """
    Função que lê o arquivo CSV e armazena os dados relevantes nos dicionários (data e data_occurences)
    """

    with open("assets/rym_clean1.csv", "r") as file:
        reader = csv.reader(file)
        column_numbers = get_column_numbers(
            reader=reader, variables=(qualitative_vars + quantitative_vars)
        )

        for row in reader:
            for column_name, column_number in column_numbers.items():
                row_data = row[column_number]  # Obtém o dado da coluna correspondente

                if column_name in ["primary_genres", "descriptors"]:
                    row_data = row_data.split(
                        ", "
                    )  # Algumas entradas contêm múltiplos valores separados por vírgula
                else:
                    row_data = [row_data]

                for data_entry in row_data:
                    data[column_name].add(
                        data_entry
                    )  # Adiciona o dado ao conjunto correspondente (evitando duplicatas)
                    data_occurences[data_entry] = (
                        data_occurences.get(data_entry, 0) + 1
                    )  # Atualiza o número de ocorrências do dado


def get_summary_statistics():
    # Exemplo de conjunto de dados; modifique ou estenda com seus próprios dados.
    #data = [12, 15, 14, 10, 8, 11, 15, 12, 9, 10, 16, 15]
    get_csv_data()
    #print("Conjunto de dados:", data["avg_rating"])
    for key, dataset in data.items():
        if key in qualitative_vars or key == "release_date":
            continue
        dataset_list = list(map(float, dataset))  # Converte os dados para float
        print(f"\nEstatísticas para {key}:")
        
        mean_value = calculate_mean(dataset_list)
        median_value = calculate_median(dataset_list)
        mode_values = calculate_mode(dataset_list)
        Q1, Q2, Q3 = calculate_quartiles(dataset_list)
        data_range = calculate_range(dataset_list)
        variance_value = calculate_variance(dataset_list)
        std_deviation = calculate_standard_deviation(dataset_list)
        iqr = calculate_interquartile_range(dataset_list)
        coefficient_of_variation = calculate_coefficient_of_variation(dataset_list)
        
        print(f"Média: {mean_value:.2f}")
        print(f"Mediana: {median_value:.2f}")
        print(f"Moda(s): {mode_values}")
        print(f"Quartis: Q1 = {Q1:.2f}, Q2 (Mediana) = {Q2:.2f}, Q3 = {Q3:.2f}")
        print(f"Amplitude: {data_range:.2f}")
        print(f"Variância: {variance_value:.2f}")
        print(f"Desvio Padrão: {std_deviation:.2f}")
        print(f"Intervalo Interquartílico (IQR): {iqr:.2f}")
        print(f"Coeficiente de Variação: {coefficient_of_variation:.2f}")
        # Percentil e decil dependem do index desejado

if __name__ == "__main__":
    get_summary_statistics()