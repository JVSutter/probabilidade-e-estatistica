"""
Módulo para construção das tabelas de frequência
"""

from typing import Iterable
import csv

import matplotlib.pyplot as plt
import numpy as np


qualitative_columns = ["artist_name", "primary_genres", "descriptors"]
quantitative_columns = ["release_date", "avg_rating", "review_count"]
data: dict[str, set[str]] = {column: set() for column in (qualitative_columns + quantitative_columns)}  # Mapeia coluna -> lista de dados lidos
occurences: dict[str, int] = {}  # Mapeia dado -> número de ocorrências


def get_column_numbers(reader: Iterable[list[str]], variables: list) -> dict[str, int]:
    """
    Função que dinamicamente obtém os números das colunas relevantes
    """

    column_numbers = {}  # Mapeia nome da coluna -> número da coluna
    for i, column in enumerate(next(reader)):
        if column in variables:
            column_numbers[column] = i
    return column_numbers


def sturges_rule(n: int) -> int:
    """
    Regra de Sturges para determinar o número de classes de um histograma
    """

    return int(np.ceil(1 + 3.322 * np.log10(n)))


def get_csv_data() -> None:
    """
    Função que lê o arquivo CSV e constrói as tabelas de frequência
    """

    with open('assets/rym_clean1.csv', 'r') as file:
        reader = csv.reader(file)
        column_numbers = get_column_numbers(reader=reader, variables=(qualitative_columns + quantitative_columns))

        for row in reader:
            for column_name, column_number in column_numbers.items():
                row_data = row[column_number]
                row_data = row_data.split(", ")  # Algumas entradas contêm múltiplos valores separados por vírgula

                for data_entry in row_data:
                    data[column_name].add(data_entry)
                    occurences[data_entry] = occurences.get(data_entry, 0) + 1


if __name__ == "__main__":
    get_csv_data()
