import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar os dados
df = pd.read_csv('outputs/sample/rym_sample.csv')  # ajuste o nome se necessário

# Gerar o gráfico de dispersão
plt.figure(figsize=(8,6))
sns.scatterplot(
    x='rating_count',
    y='avg_rating',
    data=df,
    color='blue',
    alpha=0.6
)

# Título e rótulos
plt.xlabel('Número de avaliações')
plt.ylabel('Nota média')
plt.grid(True)

# Salvar como PNG
plt.savefig('outputs/graphs/scatter_ratings_vs_avg_rating.png', dpi=300)

# Mostrar o gráfico
plt.show()
