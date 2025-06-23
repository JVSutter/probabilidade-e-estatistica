import numpy as np
import pandas as pd
from scipy import stats

quantitative_vars = ["release_year", "avg_rating", "rating_count"]
qualitative_vars = ["primary_genres", "descriptors"]

sample_df = pd.read_csv('outputs/sample/rym_sample.csv')

# Converter datas para ano
sample_df['release_date'] = pd.to_datetime(sample_df['release_date'], errors='coerce')
sample_df['release_year'] = sample_df['release_date'].dt.year

# Função para estatísticas descritivas com IC para média
def quantitative_statistics(col):
    data = sample_df[col].dropna()
    n = len(data)
    mean = data.mean()
    median = data.median()
    std_dev = data.std()
    min_val = data.min()
    max_val = data.max()
    q1 = data.quantile(0.25)
    q3 = data.quantile(0.75)
    
    # Intervalo de confiança para a média (95%)
    ic = stats.t.interval(0.95, df=n-1, loc=mean, scale=stats.sem(data))

    return {
        'n': n,
        'média': mean,
        'mediana': median,
        'desvio padrão': std_dev,
        'mínimo': min_val,
        'máximo': max_val,
        'Q1': q1,
        'Q3': q3,
        'IC 95% média': ic
    }

# Função para estatísticas descritivas de variáveis qualitativas
def qualitative_statistics(col, top_n=10):
    data = sample_df[col].dropna()
    
    # Separar múltiplos valores (assumindo separação por vírgula, comum nesse tipo de dataset)
    all_values = data.str.split(', ').explode()
    
    freq_abs = all_values.value_counts()
    freq_rel = freq_abs / len(data)

    # Para a mais frequente: IC 95% para proporção
    most_common = freq_abs.idxmax()
    p_hat = freq_rel[most_common]
    n = len(data)
    erro = np.sqrt(p_hat * (1 - p_hat) / n)
    ic = (p_hat - 1.96 * erro, p_hat + 1.96 * erro)

    return {
        'n': n,
        'categorias distintas': all_values.nunique(),
        'top categorias (frequência absoluta)': freq_abs.head(top_n).to_dict(),
        'top categorias (frequência relativa)': freq_rel.head(top_n).to_dict(),
        'categoria mais comum': most_common,
        'proporção': p_hat,
        'IC 95% proporção': ic
    }


print(f"{'-' * 8} QUANTITATIVAS {'-' * 8}")
for var in quantitative_vars:
    print(f'{var.upper()}:')
    for key, value in quantitative_statistics(var).items():
        print(f"\t{key}: {value}")
        
    print()
    
print(f"{'-' * 8} QUALITATIVAS {'-' * 8}")
for var in qualitative_vars:
    print(f'{var.upper()}:')
    for key, value in qualitative_statistics(var).items():
        print(f"\t{key}: {value}")
        
    print()
    