import os
import matplotlib.pyplot as plt


# パス関連
dirname = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(dirname, "cobyla_1")
obj_dir = os.path.join(dirname, "cobyla_1")
tmp = "J_log"
src_filename = tmp + ".csv"
obj_filename = tmp + ".png"
src_path = os.path.join(src_dir, src_filename)
obj_path = os.path.join(obj_dir, obj_filename)

# 何列目をプロットするか
column_plotted = 0

# ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
header = None
index_col = None
# header = 0
# index_col = 0

# ラベル
xlabel = "Step"
ylabel = "Objective function"

# ticks
y_ticks = "auto"
x_ticks = "auto"

# Font setting:
_font = 'Times New Roman'
plt.rcParams["font.family"] = _font   # Before fig, ax =...
print("# Font:", _font, "(Linuxでは無効になる;_;)")
plt.rcParams["mathtext.fontset"] = 'stix'   # Before fig, ax =　...

# Font size:
FONT_LABELS = 28
FONT_LABELS = 28
FONT_TICKLABELS = 20
FONT_LEGENDS = 16

# Figure size settings:
FIG_SIZE = (8, 5)
# FIG_SIZE = (10, 5)
