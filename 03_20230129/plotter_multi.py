import os
import matplotlib.pyplot as plt
import math
import numpy as np


class MyPlotter():
    def __init__(
                self,
                obj_dir, obj_filename,
                step_xticks, step_yticks,
                x_min=None, x_max=None, y_min=None, y_max=None,
                FIG_SIZE=None,
                legend=False,
                column_plotted=None,
                y_label="$J$",
                legend_list=None
            ):
        """こいつの仕事は，yとかxありきの，fig, ax管理．

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
        self.obj_dir = obj_dir
        self.obj_filename = obj_filename
        self.step_xticks = step_xticks
        self.step_yticks = step_yticks
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.FIG_SIZE = FIG_SIZE
        self.multi_y = False
        self.legend = legend
        self.column_plotted = column_plotted
        self.legend_list = legend_list
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
        self.FONT_LEGENDS = 18

        # Figure size settings:
        if self.FIG_SIZE is not None:
            self.FIG_SIZE = self.FIG_SIZE
        else:
            self.FIG_SIZE = (8, 5)

        # pathの作成
        self.obj_path = os.path.join(self.obj_dir, self.obj_filename)

        # ファイル，フォルダチェック
        self.exist_obj_dir()

    def prepare_fig_ax(self):
        # fig, axインスタンス
        self.fig, self.ax = plt.subplots(figsize=self.FIG_SIZE)
        self.ax.tick_params(axis='both', labelsize=self.FONT_TICKLABELS)
        self.ax.set_xlabel(self.xlabel, fontsize=self.FONT_LABELS)
        self.ax.set_ylabel(self.ylabel, fontsize=self.FONT_LABELS)

    def set_everything(self):
        # > y axis
        step_yticks = self.step_yticks  # 最大値，最小値を元に設定
        # y_min_rounded = self.my_round(self.y_min, step_yticks, floor=True)
        # y_max_rounded = self.my_round(self.y_max, step_yticks)
        # y_lim = [
        #     y_min_rounded,
        #     y_max_rounded
        # ]
        y_lim = [0, 4]
        ndarray_for_yticks = np.arange(
            y_lim[0], y_lim[1] + step_yticks, step=step_yticks
        )
        # <

        # > x axis
        step_xticks = self.step_xticks  # 最大値，最小値を元に設定
        # ndarray_for_xticks = np.arange(0, len(x)+1, step=step_xticks)[1:]
        # ndarray_for_xticks = np.insert(ndarray_for_xticks, 0, 1)  # 0番目に1を挿入
        # x_rounded = self.my_round(len(self.x)+1, step_xticks)
        ndarray_for_xticks = np.arange(self.x_min, self.x_max+1, step_xticks)
        x_lim = [self.x_min, self.x_max]
        # <

        # sets
        self.ax.set_xlim(x_lim)
        self.ax.set_ylim(y_lim)
        self.ax.set_yticks(ndarray_for_yticks)
        self.ax.set_xticks(ndarray_for_xticks)
        plt.grid(True)

        # legend
        if self.legend:
            # 苦労の末，$J_{\text{sp}}の出力に成功．$
            if self.legend_list is None:
                self.ax.legend(
                    fontsize=self.FONT_LEGENDS,
                    framealpha=1.0,
                    loc='lower right'
                )
            else:
                self.ax.legend(
                    self.legend_list,
                    fontsize=self.FONT_LEGENDS,
                    framealpha=1.0,
                    loc='lower right'
                )

    def save_fig(self):
        self.fig.savefig(
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

    def x_for_y(self, y):
        return np.arange(1, len(y) + 1, 1)

    def plot_y(self, y, label=None):
        x = self.x_for_y(y)
        self.ax.plot(x, y, marker='o', markersize=3, linewidth=1, label=label)

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
