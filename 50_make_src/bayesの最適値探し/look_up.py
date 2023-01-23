import pandas as pd
import os


dirname = os.path.dirname(os.path.abspath(__file__))

if False:
    for i in range(2):
        j_log_filename = "J_log_bayes_" + str(i+1) + ".csv"
        z_log_filename = "z_log_bayes_" + str(i+1) + ".csv"
        df_j = pd.read_csv(os.path.join(dirname, j_log_filename), index_col=None, header=None)
        df_z = pd.read_csv(os.path.join(dirname, z_log_filename), index_col=None, header=None)
        # print(df_j.head())
        # print(df_z.head())
        # j_ndarray = df_j.to_numpy()
        # z_ndarray = df_z.to_numpy()
        # print(j_ndarray.shape)
        df_j["1"] = df_z
        df_j.columns = ["J", "z_1"]
        df_j.to_csv(os.path.join(dirname, "log_bayes_" + str(i+1) + ".csv"))

if True:
    max_index = []
    for i in range(2):
        log_filename = "log_bayes_" + str(i+1) + ".csv"
        df = pd.read_csv(os.path.join(dirname, log_filename), index_col=None, header=0)
        df_sorted = df.sort_values(by="J", ascending=False)
        df_sorted.columns = ["index", "J", "z_1"]
        print(df_sorted.head())
        df_sorted.to_csv(os.path.join(dirname, "log_bayes_sorted_" + str(i+1) + ".csv"))
        max_index.append(df_sorted["index"].to_numpy()[0] + 1)

print("# 1始まりのインデックス")
print(f"{max_index = }")
