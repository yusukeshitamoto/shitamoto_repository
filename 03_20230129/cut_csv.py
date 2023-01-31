# 50がいいとか言うので，カットして保存するスクリプトを用意．
import os
import pandas as pd


cut_off = 10

dirname = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(dirname, "src")
obj_dir = os.path.join(dirname, "src")
src_filename = "J_log.csv"
tmp = "_" + str(cut_off)
obj_filename = "J_log" + tmp + ".csv"

# データを消さないための保険
if src_filename == obj_filename:
    raise ValueError("src, objのファイル名が一致しているためエラー．")

df = pd.read_csv(
    os.path.join(src_dir, src_filename),
    header=None, index_col=None
)
array = df.to_numpy()
cut_array = array[:cut_off]
pd.DataFrame(cut_array).to_csv(os.path.join(obj_dir, obj_filename))
