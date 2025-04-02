"""
Módulo para construção das tabelas de frequência
"""

import csv
from typing import Iterable

import numpy as np
import pandas as pd

TABLE_SIZE_LIMIT = 15
qualitative_vars = ["artist_name", "primary_genres", "descriptors"]
quantitative_vars = ["avg_rating", "review_count"]
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
                if column_name in ["primary_genres", "descriptors"]:
                    row_data = row_data.split(
                        ", "
                    )  # Algumas entradas contêm múltiplos valores separados por vírgula
                else:
                    row_data = [row_data]

                for data_entry in row_data:
                    data[column_name].add(data_entry)
                    data_occurences[data_entry] = data_occurences.get(data_entry, 0) + 1


def add_relative_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adiciona uma coluna de frequência relativa a uma tabela de frequência
    """

    total_frequency = df["Frequência"].sum()
    df["Frequência Relativa (%)"] = (df["Frequência"] / total_frequency * 100).round(2)
    return df


def generate_qualitative_tables() -> str:
    """
    Função que gera as tabelas de frequência para variáveis qualitativas
    """

    for variable in qualitative_vars:
        table = {variable: [], "Frequência": []}

        sorted_entries = sorted(
            [
                (data_entry, data_occurences[data_entry])
                for data_entry in data[variable]
            ],
            key=lambda x: (-x[1], x[0]),
        )

        for i, (data_entry, frequency) in enumerate(sorted_entries):
            if i < TABLE_SIZE_LIMIT:
                table[variable].append(data_entry)
                table["Frequência"].append(frequency)
            else:
                break

        if len(sorted_entries) > TABLE_SIZE_LIMIT:
            others_sum = sum(freq for _, freq in sorted_entries[TABLE_SIZE_LIMIT:])
            table[variable].append("Others")
            table["Frequência"].append(others_sum)

        df = pd.DataFrame(table)
        df = add_relative_frequency(df)
        df.to_csv(f"outputs/{variable}_table.csv", index=False)


def generate_quantitative_tables() -> None:
    """
    Função que gera as tabelas de frequência para variáveis quantitativas
    """

    #  TODO
    # 1 - Usar a regra de Sturges para determinar o número de classes
    # 2 - Preencher a tabela com a frequência de cada classe
    # OBS: Lidar com release_date vai ser um pouco mais complicado (tirei por enquanto)

    for variable in quantitative_vars:
        # Lista com tuplas (valor numérico, frequência)
        values = []
        for entry in data[variable]:
            try:
                # Para release_date pode ser necessário converter para int,
                # mas usaremos float para tratamento unificado.
                num_value = float(entry)
            except ValueError:
                continue
            freq = data_occurences.get(entry, 0)
            values.append((num_value, freq))

        if not values:
            continue

        # Determinar os limites mínimo e máximo dos valores
        val_nums = [val for val, _ in values]
        min_val, max_val = min(val_nums), max(val_nums)

        # Se todos os valores forem iguais, cria apenas uma classe
        if min_val == max_val:
            nbins = 1
            bin_edges = [min_val, max_val]
        else:
            # Para o número de classes, usamos total de ocorrências (sum dos freqs)
            total_frequency = sum(freq for _, freq in values)
            nbins = sturges_rule(total_frequency)
            bin_edges = np.linspace(min_val, max_val, nbins + 1)

        # Define os rótulos para as classes no formato "limite_inferior - limite_superior"
        labels = []
        for i in range(nbins):
            low = bin_edges[i]
            high = bin_edges[i + 1]

            if variable == "review_count":
                if i < nbins - 1:
                    labels.append(f"{int(low)} - {int(high) - 1}")
                else:
                    labels.append(f"{int(low)} - {int(high)}")
            elif variable == "avg_rating":
                if i < nbins - 1:
                    labels.append(f"{low:.2f} - {high - 0.01:.2f}")
                else:
                    labels.append(f"{low:.2f} - {high:.2f}")

        # Inicializa os contadores de frequência para cada classe
        freq_bins = [0] * nbins
        for val, freq in values:
            # Se o valor for o máximo, garantimos que seja incluido na última classe
            if val == max_val:
                bin_index = nbins - 1
            else:
                # Define o índice da classe baseado na posição relativa
                bin_index = int((val - min_val) / (max_val - min_val) * nbins)
            freq_bins[bin_index] += freq

        # Cria a tabela e gera o CSV
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
