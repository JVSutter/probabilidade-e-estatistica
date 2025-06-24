import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm


file_path = "atividade_2/outputs/sample/rym_sample.csv"
df = pd.read_csv(file_path)
# Cálculo dos parâmetros do teste
n = len(df)
x = df['primary_genres'].str.contains('Rock', case=False, na=False).sum()


p_hat = x / n
p0 = 0.20
SE = np.sqrt(p0 * (1 - p0) / n)
z = (p_hat - p0) / SE
p_value = 1 - norm.cdf(z)


# Criar o gráfico
x_vals = np.linspace(-4, 40, 1000)  # Geração de valores de z para a curva
y_vals = norm.pdf(x_vals, 0, 1)     # Densidade da distribuição normal padrão

plt.figure(figsize=(10, 6))
sns.lineplot(x=x_vals, y=y_vals, color='blue')  # Curva da distribuição normal

# Área do p-valor (cauda direita)
x_fill = np.linspace(z, 40, 500)
y_fill = norm.pdf(x_fill, 0, 1)
plt.fill_between(x_fill, y_fill, color='red', alpha=0.5, label='Região do p-valor (cauda direita)')

# Linha vertical indicando o valor de z
plt.axvline(x=z, color='red', linestyle='--', label=f'Estatística z = {z:.2f}')

# Configuração dos eixos e legendas
plt.title('Distribuição Normal Padrão - Região do p-valor (Teste de Proporção)')
plt.xlabel('z')
plt.ylabel('Densidade de probabilidade')
plt.legend()
plt.grid(True)
plt.show()

print(f'Tamanho da amostra (n): {n}')
print(f'Número de álbuns de Rock (x): {x}')
print(f'Proporção amostral (p̂): {p_hat:.4f}')
print(f'Estatística z: {z:.4f}')
print(norm.cdf(z))  
print(f'p-valor: {p_value:.15f}')