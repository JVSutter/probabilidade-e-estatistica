"""
Script para criar uma amostra aleatória de linhas de um arquivo CSV.
"""

import csv
import random


def sample_csv(input_file, output_file, sample_size):
    """
    Extrai uma amostra aleatória de linhas de um arquivo CSV.

    @param input_file: Caminho para o arquivo CSV de entrada
    @param output_file: Caminho para o arquivo CSV de saída
    @param sample_size: Número de linhas para amostrar
    """

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)  # Preservar o cabeçalho
        rows = list(reader)

        # Selecionar linhas aleatoriamente
        sampled_rows = random.sample(rows, sample_size)

        # Escrever a amostra no arquivo de saída
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(sampled_rows)

        print(f"Amostra de {sample_size} linhas criada com sucesso em '{output_file}'")


sample_csv("./dataset/rym_clean1.csv", "./outputs/sample/rym_sample.csv", 360)
