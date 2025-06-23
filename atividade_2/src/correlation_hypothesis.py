import pandas as pd
from scipy.stats import pearsonr

# Carregar os dados
df = pd.read_csv('outputs/sample/rym_sample.csv')  # ajuste o nome se precisar

# Selecionar as colunas
rating_count = df['rating_count']
avg_rating = df['avg_rating']

# Calcular a correlação de Pearson
corr_coef, p_value = pearsonr(rating_count, avg_rating)

print('Coeficiente de correlação de Pearson:', corr_coef)
print('P-valor do teste:', p_value)

# Interpretação do resultado
alpha = 0.05
if (p_value < alpha) and (corr_coef > 0):
    print('Conclusão: Existe evidência estatística para afirmar que há correlação positiva entre o número de avaliações e a nota média do álbum.')
else:
    print('Conclusão: Não há evidência suficiente para afirmar que existe correlação positiva entre o número de avaliações e a nota média do álbum.')
