##################################################
# *.ptの名前を受け取って最適化を行うスクリプト．
# モデルのモジュールはtemplate.pyで固定．
##################################################

##################################################
# Import
##################################################
import nlopt
import os
import argparse
from distutils.util import strtobool  # argparseでboolを使うための方法の一つ
import itertools
import ctypes
import numpy as np
import subprocess
# from GPyOpt.methods import BayesianOptimization

# self-made
import modules
# 目的関数
import tools


mytimer = modules.Mytimer()
mytimer.TICK()

dirname = os.path.dirname(os.path.abspath(__file__))
print("dirname:", dirname)

# libpixel_workdirからの要請
pixel_workdir = os.path.join(dirname, "pixel_workdir")
os.makedirs(pixel_workdir, exist_ok=True)

# ##################################################
# argparseを使ったパラメータ設定
# ##################################################

parser = argparse.ArgumentParser(description="パラメータをスクリプトの引数として設定することも可能．")
# > parser.add_argument()たち
# boolean型の引数について：https://note.nkmk.me/python-argparse-bool/
parser.add_argument('--dir_main', nargs='?', default="./test/",
                    type=str, dest='dir_main',
                    help='モデルに関する結果が入るディレクトリ'
                    )
parser.add_argument('--model_id', nargs='?', default="test",
                    type=str, dest='model_id',
                    help='モデル固有の文字列'
                    )
parser.add_argument('--dir_model_pt', nargs='?', default="./test/test.pt",
                    type=str, dest='dir_model_pt',
                    help='モデルパラメータファイルのフルパス'
                    )
parser.add_argument('--dir_mu_sigma', nargs='?', default="./test/",
                    type=str, dest='dir_mu_sigma',
                    help='muとsigmaのデータがあるディレクトリ'
                    )
parser.add_argument('--experimental_subject', nargs='?', default="dist",
                    type=str, dest='experimental_subject',
                    help='実験対象（"bayes"か"cobyla"）'
                    )
parser.add_argument('--latent_dim', nargs='?', default=3,
                    type=int, dest='latent_dim',
                    help='潜在変数の次元'
                    )
parser.add_argument('--distance_switch', nargs='?', default="False",
                    type=str, dest='distance_switch',
                    help='距離を目的関数に加えるか（str型であることに注意，strtobool()）'
                    )
parser.add_argument('--x0', nargs='+', default=[0, 0, 0],
                    type=list, dest='x0',
                    help='最適化の初期値．'
                    )
parser.add_argument('--weight_min_d', nargs='?', default=0.01,
                    type=float, dest='weight_min_d',
                    help='最小のdに掛け合わせる重み'
                    )
parser.add_argument('--dx', nargs='?', default=1.5,
                    type=float, dest='dx',
                    help='初期ステップ'
                    )
parser.add_argument('--xobs_x', nargs='?', default=-0.15,
                    type=float, dest='xobs_x',
                    help='観測点のx座標'
                    )
parser.add_argument('--log_switch', nargs='?', default="False",
                    type=str, dest='log_switch',
                    help='詳細なログをとるかどうかの選択（str型であることに注意，strtobool()）'
                    )
parser.add_argument('--test_bool', nargs='?', default="True",
                    type=str, dest='test_bool',
                    help='test関数を使う場合は "True" としておく．本番の関数は激重のため．'
                    )
parser.add_argument('--comment', nargs='?', default="Nothing has set.",
                    type=str, dest='comment',
                    help='実験に対するコメント'
                    )
# <
args = parser.parse_args()

dir_model_pt = args.dir_model_pt
dir_main = args.dir_main
dir_results = os.path.join(dir_main, "results")
os.makedirs(dir_results, exist_ok=True)


# モデルのmuとsigmaを読み込み（optimization with distance用）
if strtobool(args.distance_switch):
    dir_mu_sigma = args.dir_mu_sigma
    dir_mu = os.path.join(dir_mu_sigma, "mu.npy")
    dir_sigma = os.path.join(dir_mu_sigma, "sigma.npy")
    mu_ndarray = np.load(dir_mu)
    sigma_ndarray = np.load(dir_sigma)
else:
    mu_ndarray = None
    sigma_ndarray = None


# > 設定の書き出し
# 変数記録インスタンス作成．
valcol = modules.VariableCollection(
    args.model_id + "_variables.txt", dir_main
)
valcol.print_msg(
    args.comment
)
# ループを使ってargsの内容を書き出し
for val in vars(args):
    # print(val, getattr(args, val))
    valcol.print_arg(
        getattr(args, val), val,
        parser._option_string_actions["--" + val].help
    )
valcol.__del__()
# <


############################################################
# > 最適化

# > 設定
bounds = 3  # 設計変数の範囲は[-3, 3]
sampling = 0.1  # sampling 間隔で数値確認
dimension = 1
# <

of = tools.ObjFunc(
    dir_model_pt, args.latent_dim, dir_results,
    weight_min_d=args.weight_min_d, xobs_x=args.xobs_x,
    mu_ndarray=mu_ndarray, sigma_ndarray=sigma_ndarray,
    dimension=dimension
)


def z2J(z):
    global of
    if strtobool(args.test_bool):  # test_boolの判定
        J = of.func_J_test(z, None)
    else:
        J = of.func_J(z, None)
    return J


z_list = np.arange(-bounds, bounds+0.0001, sampling)
for z in z_list:
    J = z2J(z)

of.save_log_as_csv()
of.export_iteration()

# <
############################################################

print("\n# pixel_workdir/ を\n# ", dir_main, "\n# に作成．")
obj_pixel_workdir = os.path.join(dir_main, "pixel_workdir")
os.makedirs(obj_pixel_workdir)
print(f"# mv {pixel_workdir}/* {obj_pixel_workdir}/ を実行．")
subprocess.run(f"mv {pixel_workdir}/* {obj_pixel_workdir}/", shell=True)
print("bash clean_workdir.sh を実行．")
subprocess.run(
    "bash clean_workdir.sh", shell=True, stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, text=True
)


finish = mytimer.TACK()
with open(os.path.join(dir_main, "時間.txt"), "w") as f:
    print("かかった時間：", finish/60, "min", file=f)
