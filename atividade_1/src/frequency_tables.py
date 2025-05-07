"""
Módulo para construção das tabelas de frequência
"""

import csv
from datetime import datetime, timedelta
from typing import Iterable

import numpy as np
import pandas as pd

TABLE_SIZE_LIMIT = 15
qualitative_vars = ["artist_name", "primary_genres", "descriptors"]
quantitative_vars = ["release_date", "avg_rating", "review_count"]
data: dict[str, set[str]] = {
    column: set() for column in (qualitative_vars + quantitative_vars)
}  # Mapeia coluna -> conjunto de dados lidos
data_occurences: dict[str, int] = {}  # Mapeia dado -> número de ocorrências
translation = {
    "artist_name": "Nome do artista",
    "primary_genres": "Gêneros primários",
    "descriptors": "Descritores",
    "release_date": "Data de lançamento",
    "avg_rating": "Média das avaliações",
    "review_count": "Número de resenhas",
}


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


def sturges_rule(n: int) -> int:
    """
    Regra de Sturges para determinar o número de classes de uma variável quantitativa

    @param n: Número total de observações
    """

    return int(np.ceil(1 + 3.322 * np.log10(n)))


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


def add_relative_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona uma coluna de frequência relativa a uma tabela de frequência

    @param df: DataFrame com a tabela de frequência
    """

    total_frequency = df["Frequência"].sum()
    df["Frequência Relativa (%)"] = (df["Frequência"] / total_frequency * 100).round(2)
    return df


def generate_qualitative_tables() -> None:
    """
    Função que gera as tabelas de frequência para variáveis qualitativas
    """

    for variable in qualitative_vars:
        translated_variable = translation[variable]
        table = {translated_variable: [], "Frequência": []}

        # Ordena por frequência decrescente. Em caso de empate, ordena alfabeticamente
        sorted_entries = sorted(
            [
                (data_entry, data_occurences[data_entry])
                for data_entry in data[variable]
            ],
            key=lambda x: (-x[1], x[0]),
        )

        for i, (data_entry, frequency) in enumerate(sorted_entries):
            if i < TABLE_SIZE_LIMIT:
                table[translated_variable].append(data_entry)
                table["Frequência"].append(frequency)
            else:
                break

        if len(sorted_entries) > TABLE_SIZE_LIMIT:
            others_sum = sum(freq for _, freq in sorted_entries[TABLE_SIZE_LIMIT:])
            table[translated_variable].append("Others")
            table["Frequência"].append(others_sum)

        df = pd.DataFrame(table)
        df = add_relative_frequency(df)
        df.to_csv(f"outputs/{translated_variable}_table.csv", index=False)


def generate_quantitative_tables() -> None:
    """
    Função que gera as tabelas de frequência para variáveis quantitativas

    Esta função processa cada variável quantitativa, dividindo os dados em classes
    de acordo com a regra de Sturges.
    """

    for variable in quantitative_vars:
        # Coleta os valores e frequências para a variável atual
        values = collect_variable_values(variable)

        if not values:
            continue

        # Determina os limites e configurações para as classes
        min_val, max_val = get_min_max_values(values)
        total_frequency = sum(freq for _, freq in values)
        nbins = sturges_rule(total_frequency)

        # Cria as bordas dos intervalos para as classes
        bin_edges = create_bin_edges(variable, min_val, max_val, nbins)

        
        if variable == "review_count":
            bin_edges = bin_edges.tolist()
            bin_edges.insert(1, 70)
            last = bin_edges[-1]
            bin_edges = bin_edges[:8]
            bin_edges[-1] = last
            nbins = len(bin_edges) - 1

        # Cria rótulos descritivos para as classes
        labels = create_class_labels(variable, bin_edges, nbins)

        # Calcula a frequência para cada classe
        freq_bins = calculate_class_frequencies(variable, values, bin_edges, nbins)

        # Cria a tabela e salva como CSV
        create_and_save_table(variable, labels, freq_bins)


def collect_variable_values(variable: str) -> list[tuple]:
    """
    Coleta todos os valores e suas frequências para uma variável.

    @param variable: Nome da variável a ser processada
    @return: Lista de tuplas (valor_numérico, frequência)
    """

    values = []
    for entry in data[variable]:
        if variable == "release_date":
            # Converte a string de data para um objeto datetime
            date_obj = datetime.strptime(entry, "%Y-%m-%d")
            num_value = date_obj
        else:
            # Para outras variáveis quantitativas, converte para float
            num_value = float(entry)

        freq = data_occurences.get(entry, 0)
        values.append((num_value, freq))

    return values


def get_min_max_values(values: list[tuple]) -> tuple:
    """
    Determina os valores mínimo e máximo dentre os dados.

    @param values: Lista de tuplas (valor, frequência)
    @return (valor_mínimo, valor_máximo)
    """

    val_nums = [val for val, _ in values]
    return min(val_nums), max(val_nums)


def create_bin_edges(variable: str, min_val, max_val, nbins: int) -> list:
    """
    Cria as bordas dos intervalos para as classes.

    @param variable: Nome da variável
    @param min_val: Valor mínimo
    @param max_val: Valor máximo
    @param nbins: Número de classes

    @return: Lista com as bordas dos intervalos
    """

    if variable == "release_date":
        # Para datas, precisamos ajustar para garantir que a data máxima seja incluída
        # Adicionamos um dia ao valor máximo para garantir que ele fique na última classe
        adjusted_max = max_val + timedelta(days=1)
        time_delta = adjusted_max - min_val
        return [min_val + (time_delta / nbins) * i for i in range(nbins + 1)]
    else:
        # Para valores numéricos, usamos o linspace do numpy
        return np.linspace(min_val, max_val, nbins + 1)


def create_class_labels(variable: str, bin_edges: list, nbins: int) -> list:
    """
    Cria rótulos descritivos para cada classe.

    @param variable: Nome da variável
    @param bin_edges: Lista com as bordas dos intervalos
        nbins: Número de classes

    @return: Lista de rótulos para as classes
    """

    labels = []
    for i in range(nbins):
        low = bin_edges[i]
        high = bin_edges[i + 1]

        if variable == "release_date":
            # Para datas, subtraímos um dia do limite superior para evitar sobreposição
            upper_date = high - timedelta(days=1)
            labels.append(
                f"{low.strftime('%Y-%m-%d')} - {upper_date.strftime('%Y-%m-%d')}"
            )
        elif variable == "review_count":
            # Para contagens, usamos valores inteiros
            if i < nbins - 1:
                labels.append(f"{int(low)} - {int(high) - 1}")
            else:
                labels.append(f"{int(low)} - {int(high)}")
        elif variable == "avg_rating":
            # Para ratings, mantemos duas casas decimais
            if i < nbins - 1:
                labels.append(f"{low:.2f} - {high - 0.01:.2f}")
            else:
                labels.append(f"{low:.2f} - {high:.2f}")

    return labels


def calculate_class_frequencies(variable: str, values: list[tuple], bin_edges: list, nbins: int) -> list:
    """
    Calcula a frequência para cada classe.

    @param variable: Nome da variável
    @param values: Lista de tuplas (valor, frequência)
    @param bin_edges: Lista com as bordas dos intervalos
    @param nbins: Número de classes

    @return Lista com as frequências de cada classe
    """

    freq_bins = [0] * nbins

    for val, freq in values:
        if variable == "release_date":
            # Para datas, verificamos explicitamente cada intervalo
            bin_index = 0
            for j in range(nbins):
                if j == nbins - 1:
                    # Último bin inclui o limite superior
                    if bin_edges[j] <= val <= bin_edges[j + 1]:
                        bin_index = j
                        break
                else:
                    # Demais bins excluem o limite superior
                    if bin_edges[j] <= val < bin_edges[j + 1]:
                        bin_index = j
                        break
        else:
            # Para valores numéricos, calculamos o índice baseado na posição relativa
            if val == max(val for val, _ in values):
                # Se for o valor máximo, garantimos que fique na última classe
                bin_index = nbins - 1
            else:
                # O índice da frequência a ser incrementada é o índice que representa
                # o intervalo ao qual o valor pertence
                for i, (low, high) in enumerate(zip(bin_edges, bin_edges[1:])):
                    if low <= val <= high:
                        bin_index = i
                        break

                # Proteção contra valores fora dos limites
                bin_index = min(bin_index, nbins - 1)

        freq_bins[bin_index] += freq

    return freq_bins


def create_and_save_table(variable: str, labels: list, freq_bins: list) -> None:
    """
    Cria a tabela de frequência e salva como CSV.

    @param variable: Nome da variável
    @param labels: Lista de rótulos para as classes
    @param freq_bins: Lista com as frequências de cada classe
    """

    variable = translation[variable]
    table = {variable: labels, "Frequência": freq_bins}
    df = pd.DataFrame(table)
    df = add_relative_frequency(df)
    df.to_csv(f"outputs/{variable}_table.csv", index=False)


def generate_frequency_tables() -> None:
    """
    Função que gera as tabelas de frequência para as variáveis de interesse
    """

    get_csv_data()
    generate_qualitative_tables()
    generate_quantitative_tables()


if __name__ == "__main__":
    generate_frequency_tables()
