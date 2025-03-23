"""
Módulo para construção das tabelas de frequência
"""

from typing import Iterable
import csv

import pandas as pd
import numpy as np


qualitative_vars = ["artist_name", "primary_genres", "descriptors"]
quantitative_vars = ["release_date", "avg_rating", "review_count"]
data: dict[str, set[str]] = {
    column: set() for column in (qualitative_vars + quantitative_vars)
}  # Mapeia coluna -> conjunto de dados lidos
data_occurences: dict[str, int] = {}  # Mapeia dado -> número de ocorrências


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
    Regra de Sturges para determinar o número de classes de uma variável quantitativa
    """

    return int(np.ceil(1 + 3.322 * np.log10(n)))


def get_csv_data() -> None:
    """
    Função que lê o arquivo CSV e armazena os dados relevantes
    """

    with open("assets/rym_clean1.csv", "r") as file:
        reader = csv.reader(file)
        column_numbers = get_column_numbers(
            reader=reader, variables=(qualitative_vars + quantitative_vars)
        )

        for row in reader:
            for column_name, column_number in column_numbers.items():
                row_data = row[column_number]
                row_data = row_data.split(", ")  # Algumas entradas contêm múltiplos valores separados por vírgula

                for data_entry in row_data:
                    data[column_name].add(data_entry)
                    data_occurences[data_entry] = data_occurences.get(data_entry, 0) + 1


def generate_qualitative_tables() -> str:
    """
    Função que gera as tabelas de frequência para variáveis qualitativas
    """

    for variable in qualitative_vars:
        table = {variable: [], "Frequência": []}

        for data_entry in data[variable]:
            table[variable].append(data_entry)
            table["Frequência"].append(data_occurences[data_entry])

        df = pd.DataFrame(table).sort_values(by="Frequência", ascending=False)
        df.to_csv(f"outputs/{variable}_table.csv", index=False)


def generate_quantitative_tables() -> None:
    """
    Função que gera as tabelas de frequência para variáveis qualitativas
    """
    #  TODO
    # 1 - Usar a regra de Sturges para determinar o número de classes
    # 2 - Preencher a tabela com a frequência de cada classe
    # OBS: Lidar com release_date vai ser um pouco mais complicado
    pass


def generate_frequency_tables() -> None:
    """
    Função que gera as tabelas de frequência para as variáveis de interesse
    """

    get_csv_data()
    generate_qualitative_tables()
    # generate_quantitative_tables()


if __name__ == "__main__":
    generate_frequency_tables()
