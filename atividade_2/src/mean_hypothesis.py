import pandas as pd
from scipy import stats

# 1) Carrega os dados
df = pd.read_csv(
    'outputs/sample/rym_sample.csv',
    index_col=0
)

# 2) Filtra os álbuns cujo campo descriptors contém 'malevocals'
mask = df['descriptors'].str.contains('malevocals', case=False, na=False)
sample = df.loc[mask, 'avg_rating'].dropna()

# 3) Define média sob H0
mu0 = 3.5

# 4) Calcula estatística t e p-value (bicaudal)
t_stat, p_two = stats.ttest_1samp(sample, mu0)

# 5) Ajusta para teste unilateral (H1: média > mu0)
p_one = p_two / 2 if t_stat > 0 else 1 - p_two/2

# 6) Resultados
print(f"Número de observações: {len(sample)}")
print(f"Média amostral: {sample.mean():.3f}")
print(f"t-statistic: {t_stat:.3f}")
print(f"p-value (unilateral): {p_one:.4f}")

alpha = 0.05
if p_one < alpha:
    print("Rejeita H0 — há evidência de que a média é maior que 3.5")
else:
    print("Não rejeita H0 — sem evidência suficiente de média > 3.5")