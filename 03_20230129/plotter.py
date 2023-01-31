import os
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np


class MyPlotter():
    def __init__(
                self,
                src_dir, src_filename, obj_dir, obj_filename,
                header, index_col, step_xticks, step_yticks,
                x_min=None, x_max=None, y_min=None, y_max=None,
                FIG_SIZE=None,
                legend=False,
                column_plotted=None,
                y_label="$J$",
                legend_list=None,
                dual_scale=False,
                multi_y=False
            ):
        """_summary_

        Args:
            src_dir (_type_): _description_
            src_filename (_type_): _description_
            obj_dir (_type_): _description_
            obj_filename (_type_): _description_
            header (_type_): _description_
            index_col (_type_): _description_
            step_xticks (_type_): _description_
            step_yticks (_type_): _description_
            x_min (_type_, optional): _description_. Defaults to None.
            x_max (_type_, optional): _description_. Defaults to None.
            y_min (_type_, optional): _description_. Defaults to None.
            y_max (_type_, optional): _description_. Defaults to None.
            FIG_SIZE (_type_, optional): _description_. Defaults to None.
            legend (bool, optional): _description_. Defaults to False.
            column_plotted (list, optional): _description_. Defaults to None.

        Raises:
            ValueError: _description_
        """
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
        self.FIG_SIZE = FIG_SIZE
        self.multi_y = multi_y
        self.legend = legend
        self.column_plotted = column_plotted
        self.legend_list = legend_list
        self.dual_scale = dual_scale
        print("# #", self.obj_filename)
        print("#", self.step_xticks)

        # ラベル
        self.xlabel = "Number of evaluation"
        self.ylabel = y_label

        # ##################################################
        # LaTeX有効にする設定？？
        plt.rcParams["text.usetex"] = True
        # ##################################################

        # Font setting:
        _font = 'Times New Roman'
        plt.rcParams["font.family"] = _font   # Before fig, ax =...
        print("# Font:", _font, "(Linuxでは無効になる;_;)")
        plt.rcParams["mathtext.fontset"] = 'stix'   # Before fig, ax =　...

        # 解像度
        plt.rcParams["savefig.dpi"] = 500

        # Font size:
        self.FONT_LABELS = 28
        self.FONT_LABELS = 28
        self.FONT_TICKLABELS = 20
        self.FONT_LEGENDS = 20

        # Figure size settings:
        if self.FIG_SIZE is not None:
            self.FIG_SIZE = self.FIG_SIZE
        else:
            self.FIG_SIZE = (8, 5)

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
        self.len_data = len(self.y)
        print(f"ndarray: {self.y.shape = }, {len(self.y) = }")
        if not self.num_column == 1:
            self.multi_y = True
            self.y = self.y.T
        print(f"ndarray: {self.y.shape = }, {len(self.y) = }")

        # yに対応するndarrayの生成
        if self.multi_y:
            if column_plotted is None:
                raise ValueError("multi_yかつcolumn_plottedがNoneなのでエラー．")
            self.y = self.y[self.column_plotted]
            print(f"# 以下の列: {self.column_plotted}についてプロット")
            print(f"ndarray: {self.y.shape = }, {len(self.y) = }")
            if self.dual_scale:
                if self.column_plotted != [0, 1, 2]:
                    raise ValueError("column_plottedがおかしいのでエラー．")
                self.y_2 = self.y[[1]]
                self.y = self.y[[0, 2]]

        # xに対応するndarrayの生成
        self.x = self.return_step()

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
        if self.dual_scale:
            lns1 = ax.plot(self.x, self.y[0], marker='o', markersize=3, linewidth=1)
            # lns2 = ax.plot(self.x, self.y[1], marker='o', markersize=3, linewidth=1)

            ax2 = ax.twinx()  # instantiate a second axes that shares the same x-axis
            ax2.tick_params(axis='both', labelsize=self.FONT_TICKLABELS)
            ax2.set_ylabel(r'$J_{\Large \textnormal{sim}}$', fontsize=self.FONT_LABELS)
            lns3 = ax2.plot(self.x, self.y_2[0], marker='o', markersize=3, linewidth=1, color='#2ca02c')
            ax2.tick_params(axis='y')

            lns2 = ax.plot(self.x, self.y[1], marker='o', markersize=3, linewidth=1)
            # added these three lines
            lns = lns1+lns3+lns2
        else:
            if self.multi_y:
                for i in range(len(self.y)):
                    ax.plot(self.x, self.y[i], marker='o', markersize=3, linewidth=1)
            else:
                ax.plot(self.x, self.y, marker='o', markersize=3, linewidth=1)

        # sets
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        ax.set_yticks(ndarray_for_yticks)
        ax.set_xticks(ndarray_for_xticks)
        if self.dual_scale:
            step_yticks = 10
            y_lim_2 = [0, 70]
            ndarray_for_yticks_2 = np.arange(
                y_lim_2[0], y_lim_2[1] + step_yticks, step=step_yticks
            )
            ax2.set_yticks(ndarray_for_yticks_2)
            ax2.set_ylim(y_lim_2)
        plt.grid(True)

        # legend
        if self.legend:
            # 苦労の末，$J_{\text{sp}}の出力に成功．$
            if self.legend_list is None:
                raise ValueError("legend_listを設定してください．")
            if self.dual_scale:
                ax2.legend(
                    lns, self.legend_list, fontsize=self.FONT_LEGENDS,
                    loc='lower right',
                    framealpha=0.8,
                    borderaxespad=0.7
                )
            else:
                ax.legend(
                    self.legend_list,
                    fontsize=self.FONT_LEGENDS,
                    borderaxespad=0.7
                )

        # Save image:
        fig.savefig(
            self.obj_path,
            bbox_inches="tight",
            pad_inches=0.2
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

    def return_step(self):
        x = np.arange(1, self.len_data + 1, 1)
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
