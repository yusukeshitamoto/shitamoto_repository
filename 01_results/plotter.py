import os
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np

<<<<<<< HEAD
# 設定ファイル
import plot_setting as ps


# 各種関数
def my_round(a, unit, floor=False):
    """unitで指定した単位で数字を丸める．プロットの際のlimを設定するために使える．

    Args:
        a (float): 対象
        unit (float): ユニット
        floor (bool): Trueの場合，下側に切り捨て（正でも負でも）

    Returns:
        _type_: 丸められた数値
    """
    tmp = a/unit
    if a >= 0:  # 正
        if floor:
            tmp = math.floor(tmp)
        else:
            tmp = math.ceil(tmp)
    else:  # 負
        if floor:
            tmp = math.floor(tmp)
        else:
            tmp = math.ceil(tmp)
    return tmp * unit


def return_step(y):
    x = np.arange(1, len(y.T) + 1, 1)
    return x


# ファイル，フォルダチェック
if not os.path.exists(ps.src_path):
    raise FileNotFoundError(
        f"ファイル：{ps.src_path}がないので終了します．"
    )

if not os.path.exists(ps.obj_dir):
    print(f"ディレクトリ：{ps.obj_dir}がないので作成します．")
    os.makedirs(ps.obj_dir)


# csvファイルの読み込み
df = pd.read_csv(
    ps.src_path, header=ps.header,
    index_col=ps.index_col
)
print(df.head())

# ndarrayへの変換
y = df.to_numpy()[:205].T
print(f"ndarray: {y.shape = }, {len(y) = }")

# yに対応するndarrayの生成
if not len(y) == 1:
    print(f"# {ps.column_plotted + 1}列目についてプロット")
    y = y[ps.column_plotted]
    print(f"ndarray: {y.shape = }, {len(y) = }")

# xに対応するndarrayの生成
x = return_step(y)

# x, yの最大値と最小値を確認
y_max = np.amax(y)
y_min = np.amin(y)
x_max = np.amax(x)
x_min = np.amin(x)
print(f"{y_max = }, {y_min = }")
print(f"{x_max = }, {x_min = }")

# fig, axインスタンス
fig, ax = plt.subplots(figsize=ps.FIG_SIZE)
ax.tick_params(axis='both', labelsize=ps.FONT_TICKLABELS)
ax.set_xlabel(ps.xlabel, fontsize=ps.FONT_LABELS)
ax.set_ylabel(ps.ylabel, fontsize=ps.FONT_LABELS)

# > y axis
step_yticks = 0.5  # 最大値，最小値を元に設定
y_min_rounded = my_round(y_min, step_yticks, floor=True)
y_max_rounded = my_round(y_max, step_yticks)
y_lim = [
    y_min_rounded,
    y_max_rounded
]
ndarray_for_yticks = np.arange(
    y_lim[0], y_lim[1] + step_yticks, step=step_yticks
)
# <

# > x axis
step_xticks = 25  # 最大値，最小値を元に設定
ndarray_for_xticks = np.arange(0, len(x)+1, step=step_xticks)[1:]
ndarray_for_xticks = np.insert(ndarray_for_xticks, 0, 1)  # 0番目に1を挿入
# ndarray_for_xticks = np.arange(1, len(x)+1, step_xticks)
x_lim = [1, len(x)]
# <

# プロット:
ax.plot(x, y.T, marker='o', markersize=3, linewidth=1)

# sets
ax.set_xlim(x_lim)
ax.set_ylim(y_lim)
ax.set_yticks(ndarray_for_yticks)
ax.set_xticks(ndarray_for_xticks)
plt.grid(True)

# Save image:
fig.savefig(
    ps.obj_path,
    bbox_inches="tight", pad_inches=0.2
)
=======

class MyPlotter():
    def __init__(
                self,
                src_dir, src_filename, obj_dir, obj_filename,
                header, index_col, step_xticks, step_yticks,
                column_plotted=None,
                x_min=None, x_max=None, y_min=None, y_max=None,
                y_range=None
            ):
        self.src_dir = src_dir
        self.src_filename = src_filename
        self.obj_dir = obj_dir
        self.obj_filename = obj_filename
        self.header = header
        self.index_col = index_col
        self.step_xticks = step_xticks
        self.step_yticks = step_yticks
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        print("# #", self.obj_filename)
        print("#", self.step_xticks)

        # ラベル
        self.xlabel = "Number of evaluation"
        self.ylabel = "Objective function"

        # Font setting:
        _font = 'Times New Roman'
        plt.rcParams["font.family"] = _font   # Before fig, ax =...
        print("# Font:", _font, "(Linuxでは無効になる;_;)")
        plt.rcParams["mathtext.fontset"] = 'stix'   # Before fig, ax =　...

        # Font size:
        self.FONT_LABELS = 28
        self.FONT_LABELS = 28
        self.FONT_TICKLABELS = 20
        self.FONT_LEGENDS = 16

        # Figure size settings:
        self.FIG_SIZE = (8, 5)
        # self.FIG_SIZE = (10, 5)

        # pathの作成
        self.src_path = os.path.join(self.src_dir, self.src_filename)
        self.obj_path = os.path.join(self.obj_dir, self.obj_filename)

        # ファイル，フォルダチェック
        self.exist_src_path()
        self.exist_obj_dir()

        # csvファイルの読み込み
        self.df = pd.read_csv(
            self.src_path, header=self.header,
            index_col=self.index_col
        )
        # print(self.df.head())
        print(f"{len(self.df.columns) = }")
        self.num_column = len(self.df.columns)

        # ndarrayへの変換
        self.y = self.df.to_numpy()  # もし1次元配列なら，転置が必要ない．
        print(f"ndarray: {self.y.shape = }, {len(self.y) = }")
        if not self.num_column == 1:
            self.y = self.y.T
        print(f"ndarray: {self.y.shape = }, {len(self.y) = }")

        # yに対応するndarrayの生成
        self.column_plotted = column_plotted
        if not self.num_column == 1:
            print(f"# {self.column_plotted + 1}列目についてプロット")
            self.y = self.y[self.column_plotted]
            print(f"ndarray: {self.y.shape = }, {len(self.y) = }")

        # yのスライス
        if y_range is not None:
            self.y = self.y[y_range[0]:y_range[1]]

        # xに対応するndarrayの生成
        self.x = self.return_step(self.y)

        # x, yの最大値と最小値を確認
        # min, maxがNoneのままなら自動で決定．
        self.check_min_max()

        # fig, axインスタンス
        fig, ax = plt.subplots(figsize=self.FIG_SIZE)
        ax.tick_params(axis='both', labelsize=self.FONT_TICKLABELS)
        ax.set_xlabel(self.xlabel, fontsize=self.FONT_LABELS)
        ax.set_ylabel(self.ylabel, fontsize=self.FONT_LABELS)

        # > y axis
        step_yticks = self.step_yticks  # 最大値，最小値を元に設定
        y_min_rounded = self.my_round(self.y_min, step_yticks, floor=True)
        y_max_rounded = self.my_round(self.y_max, step_yticks)
        y_lim = [
            y_min_rounded,
            y_max_rounded
        ]
        ndarray_for_yticks = np.arange(
            y_lim[0], y_lim[1] + step_yticks, step=step_yticks
        )
        # <

        # > x axis
        step_xticks = self.step_xticks  # 最大値，最小値を元に設定
        # ndarray_for_xticks = np.arange(0, len(x)+1, step=step_xticks)[1:]
        # ndarray_for_xticks = np.insert(ndarray_for_xticks, 0, 1)  # 0番目に1を挿入
        x_rounded = self.my_round(len(self.x)+1, step_xticks)
        ndarray_for_xticks = np.arange(0, x_rounded+1, step_xticks)
        x_lim = [0, x_rounded]
        # <

        # プロット:
        ax.plot(self.x, self.y, marker='o', markersize=3, linewidth=1)

        # sets
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        ax.set_yticks(ndarray_for_yticks)
        ax.set_xticks(ndarray_for_xticks)
        plt.grid(True)

        # Save image:
        fig.savefig(
            self.obj_path,
            bbox_inches="tight", pad_inches=0.2
        )

    def exist_src_path(self):
        if not os.path.exists(self.src_path):
            raise FileNotFoundError(
                f"ファイル：{self.src_path}がないので終了します．"
            )

    def exist_obj_dir(self):
        if not os.path.exists(self.obj_dir):
            print(f"ディレクトリ：{self.obj_dir}がないので作成します．")
            os.makedirs(self.obj_dir)

    # 各種関数
    def my_round(self, a, unit, floor=False):
        """unitで指定した単位で数字を丸める．プロットの際のlimを設定するために使える．

        Args:
            a (float): 対象
            unit (float): ユニット
            floor (bool): Trueの場合，下側に切り捨て（正でも負でも）

        Returns:
            _type_: 丸められた数値
        """
        tmp = a/unit
        if a >= 0:  # 正
            if floor:
                tmp = math.floor(tmp)
            else:
                tmp = math.ceil(tmp)
        else:  # 負
            if floor:
                tmp = math.floor(tmp)
            else:
                tmp = math.ceil(tmp)
        return tmp * unit

    def return_step(self, y):
        x = np.arange(1, len(self.y) + 1, 1)
        return x

    def check_min_max(self):
        if self.y_max is None:
            self.y_max = np.amax(self.y)
        if self.y_min is None:
            self.y_min = np.amin(self.y)
        if self.x_max is None:
            self.x_max = np.amax(self.x)
        if self.x_min is None:
            self.x_min = np.amin(self.x)
        print(f"{self.x_max = }")
        print(f"{self.x_min = }")
        print(f"{self.y_max = }")
        print(f"{self.y_min = }")
>>>>>>> f8a29e9b4c428f40e73278b96a728e229aa44522
