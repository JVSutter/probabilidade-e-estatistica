import pandas as pd
import scipy.stats as stats


df = pd.read_csv("outputs/sample/rym_sample.csv")

print(df["artist_name"].describe())