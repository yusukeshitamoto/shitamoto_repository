import pandas as pd


df = pd.read_csv("./z_log_copy.csv")
print(df.head())

ar = df.to_numpy()
print(ar)
