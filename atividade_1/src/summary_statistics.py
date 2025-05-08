import math
from collections import Counter
from typing import Iterable
import csv
import numpy as np

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

def calculate_mean(data, key):
    """Retorna a média da lista de dados."""
    if key == "release_date":
        data_array = np.array(data, dtype='datetime64[s]').view('i8')
        mean = (data_array
            .mean()
            .astype('datetime64[s]'))
        return mean
    data = list(map(float, data))  # Converte os dados para float
    return sum(data) / len(data)

def calculate_median(data, key):
    """Retorna a mediana da lista de dados."""
    if key == "release_date":
        median = np.datetime64(
            int(np.median(np.array(data, dtype='datetime64[s]').view('i8'))), 's'
        )
        return median
    data = list(map(float, data))  # Converte os dados para float
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]

def calculate_mode(data, key):
    """Retorna a(s) moda(s) da lista de dados como uma lista.
    Se todos os números ocorrerem igualmente, retorna toda a lista ordenada."""
    if key != "release_date" and key not in qualitative_vars:
        data = list(map(float, data))
    count = Counter(data)
    max_occurrence = max(count.values())
    modes = [x for x, occ in count.items() if occ == max_occurrence]
    return sorted(modes)

def calculate_percentile(data, percentile, key):
    """Retorna o percentil informado da lista de dados.
    Utiliza interpolação linear entre posições mais próximas."""
    if not 0 <= percentile <= 100:
        raise ValueError("O percentil deve estar entre 0 e 100")
    if key == "release_date":
        value = np.datetime64(
            int(np.percentile(np.array(data, dtype='datetime64[s]').view('i8'), percentile)), 's'
        )
        return value
    data = list(map(float, data))  # Converte os dados para float
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

def calculate_quartiles(data, key):
    """Retorna o primeiro (Q1), segundo (Q2/Mediana) e terceiro (Q3) quartis da lista de dados."""
    if key == "release_date":
        Q1 = np.datetime64(
            int(np.percentile(np.array(data, dtype='datetime64[s]').view('i8'), 25)), 's'
        )
        Q2 = calculate_median(data, key)
        Q3 = np.datetime64(
            int(np.percentile(np.array(data, dtype='datetime64[s]').view('i8'), 75)), 's'
        )
        return Q1, Q2, Q3

    Q1 = calculate_percentile(data, 25, key)
    Q2 = calculate_median(data, key)
    Q3 = calculate_percentile(data, 75, key)
    return Q1, Q2, Q3

def calculate_decil(data, decil_index, key):
    """Retorna o decil informado da lista de dados.
    
    @param data: Lista de dados numéricos.
    @param decil_index: Índice do decil (inteiro de 1 a 9).
    @return: Valor do decil calculado utilizando o percentil correspondente.
    """
    if not 1 <= decil_index <= 9:
        raise ValueError("O índice do decil deve estar entre 1 e 9")
    # O decil 1 corresponde ao percentil 10, o decil 2 ao percentil 20, e assim por diante.
    return calculate_percentile(data, decil_index * 10, key)

def calculate_range(data, key):
    """Retorna a amplitude (máximo - mínimo) da lista de dados."""
    if key == "release_date":
        data_array = np.array(data, dtype='datetime64[s]')
        return data_array.max() - data_array.min()
    data = list(map(float, data))  # Converte os dados para float
    return max(data) - min(data)

def calculate_variance(data, key):
    """Retorna a variância populacional da lista de dados."""
    if key == "release_date":
        data_array = np.array(data, dtype='datetime64[s]').view('i8')
        mean = data_array.mean()
        if mean == 0:
            return float('inf')
        std = data_array.std()
        return std / mean
    data = list(map(float, data))  # Converte os dados para float
    mean_value = calculate_mean(data, key)
    return sum((x - mean_value) ** 2 for x in data) / len(data)

def calculate_standard_deviation(data, key):
    """Retorna o desvio padrão populacional da lista de dados."""
    if key == "release_date":
        data_array = np.array(data, dtype='datetime64[s]').view('i8')
        std_seconds = np.std(data_array)
        return np.timedelta64(int(std_seconds), 's') 
    data = list(map(float, data))  # Converte os dados para float
    return math.sqrt(calculate_variance(data, key))

def calculate_interquartile_range(data, key):
    """Retorna o intervalo interquartílico (IQR) da lista de dados."""
    if key == "release_date":
        data_array = np.array(data, dtype='datetime64[s]').view('i8')
        Q1 = np.percentile(data_array, 25)
        Q3 = np.percentile(data_array, 75)
        return np.timedelta64(int(Q3 - Q1), 's')
    Q1, _, Q3 = calculate_quartiles(data, key)
    return Q3 - Q1

def calculate_coefficient_of_variation(data, key):
    """Retorna o coeficiente de variação (desvio padrão / média) da lista de dados."""
    mean_value = calculate_mean(data, key)
    if mean_value == 0 or mean_value == "1970-01-01T00:00:00":
        return float('inf')
    if key == "release_date":
        data_array = np.array(data, dtype='datetime64[s]').view('i8')
        mean = data_array.mean()
        if mean == 0:
            return float('inf')
        std = data_array.std()
        return std / mean  
    return calculate_standard_deviation(data, key) / mean_value

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
    get_csv_data()
    total_data = {}
    variables = quantitative_vars + qualitative_vars
    for i in range(len(variables)):
        total_data[variables[i]] = []
    for key, value in data_occurences.items():
        for data_key, dataset in data.items():
            if key in dataset:
                key_aux = key
                if ",..." in key:
                    key_aux = key[:-(len(",..."))]
                for i in range(value):
                    total_data[data_key].append(key_aux)

    for key, dataset in total_data.items():
        print(f"\nEstatísticas para {key}:")
        # Se o dado for qualitativo, calcula apenas a moda
        if key in qualitative_vars:
            dataset_list = list(dataset)
            mode_values = calculate_mode(dataset_list, key)
            print(f"Moda(s): {mode_values}")
            continue
        # Se o dado for qualitativo, não faz sentido calcular média, mediana, etc.
        dataset_list = list(dataset)  # Converte os dados para float
        #if key == "release_date":
        mean_value = calculate_mean(dataset_list, key)
        median_value = calculate_median(dataset_list, key)
        mode_values = calculate_mode(dataset_list, key)
        Q1, Q2, Q3 = calculate_quartiles(dataset_list, key)
        data_range = calculate_range(dataset_list, key)
        variance_value = calculate_variance(dataset_list, key)
        std_deviation = calculate_standard_deviation(dataset_list, key)
        iqr = calculate_interquartile_range(dataset_list, key)
        coefficient_of_variation = calculate_coefficient_of_variation(dataset_list, key)
        print(f"Média: {mean_value}")
        print(f"Mediana: {median_value}")
        print(f"Moda(s): {mode_values}")
        print(f"Quartis: Q1 = {Q1}, Q2 (Mediana) = {Q2}, Q3 = {Q3}")
        print(f"Amplitude: {data_range}")
        print(f"Variância: {variance_value}")
        print(f"Desvio Padrão: {std_deviation}")
        print(f"Intervalo Interquartílico (IQR): {iqr}")
        print(f"Coeficiente de Variação: {coefficient_of_variation}")
        # Percentil e decil dependem do index desejado

if __name__ == "__main__":
    get_summary_statistics()