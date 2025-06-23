"""
Hipótese: o ano de lançamento do álbum afeta a média das avaliações.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

df = pd.read_csv("outputs/sample/rym_sample.csv")
df["release_date"] = pd.to_datetime(df["release_date"])
df["release_year"] = df["release_date"].dt.year  # Trabalha apenas com o ano

# Basic visualization to see the relationship
plt.figure(figsize=(12, 6))
plt.scatter(df["release_year"], df["avg_rating"], alpha=0.5)
plt.title("Média das Avaliações vs. Ano de Lançamento")
plt.xlabel("Ano de Lançamento")
plt.ylabel("Média das Avaliações")
plt.grid(True, alpha=0.3)

# Adiciona uma linha de tendência
z = np.polyfit(
    df["release_year"], df["avg_rating"], 1
)  # Quadrados mínimos para a linha de tendência
p = np.poly1d(z)
plt.plot(df["release_year"], p(df["release_year"]), "r--", alpha=0.8)
plt.savefig("outputs/graphs/rating_vs_year.png")
plt.close()

# Aplica regressão linear usando statsmodels
X = df["release_year"]
X = sm.add_constant(X)
y = df["avg_rating"]
model = sm.OLS(y, X).fit()

# Extrai os resultados do modelo
slope = model.params.iloc[1]
p_value = model.pvalues.iloc[1]
r_squared = model.rsquared

# Cria coeficiente de correlação
correlation = df["release_year"].corr(df["avg_rating"])

# Exibe os resultados
print("\nResultados da análise:")
print(f"Coeficiente de correlação: {correlation:.4f}")
print(f"Inclinação: {slope:.6f} (mudança na avaliação por ano)")
print(f"P-valor: {p_value:.20f}")
print(f"R²: {r_squared:.6f}")

if p_value < 0.05:
    print(
        "\nO p-valor é menor que 0.05, sugerindo uma relação estatisticamente significativa entre a data de lançamento e a média das avaliações."
    )

    if slope > 0:
        print(
            f"A inclinação positiva ({slope:.6f}) indica que álbuns mais novos tendem a ter avaliações mais altas."
        )
    else:
        print(
            f"A inclinação negativa ({slope:.6f}) indica que álbuns mais antigos tendem a ter avaliações mais altas."
        )
    print(
        f"\nNo entanto, o valor de R² de {r_squared:.6f} sugere que apenas {r_squared*100:.2f}% da variação nas avaliações é explicada pelo ano de lançamento."
    )

else:
    print(
        "\nO p-valor é maior que 0.05, sugerindo que não há evidências suficientes para concluir que a data de lançamento afeta significativamente a média das avaliações."
    )
