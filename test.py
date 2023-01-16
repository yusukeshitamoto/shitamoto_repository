import numpy as np


# > 設定
bounds = 3  # 設計変数の範囲は[-3, 3]
sampling = 0.1  # sampling 間隔で数値確認
# <
z_list = np.arange(-bounds, bounds+0.0001, sampling)
print(z_list)
