import os
import torch
import argparse
import numpy as np
from distutils.util import strtobool  # argparseでboolを使うための方法の一つ
from tqdm import tqdm

# 自作
import modules
import process_data
import configures
import distance
# モデル
import model_template as model


dirname = os.path.dirname(os.path.abspath(__file__))
print(dirname)

# Device
device = torch.device(
    "cuda:0" if (torch.cuda.is_available()) else "cpu"
)
print("Using device: ", device)


# > argparse

parser = argparse.ArgumentParser(description="パラメータをスクリプトの引数として設定することも可能．")

parser.add_argument('--dir_main', nargs='?', default="",
                    type=str, dest='dir_main',
                    help='モデル固有のディレクトリ．自由に設定可能．'
                    )
parser.add_argument('--dir_pt', nargs='?', default="hoge",
                    type=str, dest='dir_pt',
                    help='モデルパラメータファイルのフルパス．\
torch.load(args.dir_pt)のように直接読み込みに使う．'
                    )
parser.add_argument('--latent_dim', nargs='?', default=3,
                    type=int, dest='latent_dim',
                    help='潜在変数の次元'
                    )
parser.add_argument('--check_depth', nargs='?', default=2,
                    type=int, dest='check_depth',
                    help='モデルの出力を確認する際の潜在変数の深さ（2が最小）'
                    )
parser.add_argument('--check_gallery_switch', nargs='?', default="False",
                    type=str, dest='check_gallery_switch',
                    help='check_gallery()関数を実行するかどうかを決める'
                    )
parser.add_argument('--check_ms_switch', nargs='?', default="False",
                    type=str, dest='check_ms_switch',
                    help='check_ms()関数を実行するかどうかを決める'
                    )

args = parser.parse_args()

# <


dir_results = os.path.join(args.dir_main, "results")
os.makedirs(dir_results, exist_ok=True)


# > 設定の書き出し
# 変数記録インスタンス作成．
print("変数記録インスタンス作成")
valcol = modules.VariableCollection(
    "variables.txt", args.dir_main
)
# ループを使ってargsの内容を書き出し
for val in vars(args):
    # print(val, getattr(args, val))
    valcol.print_arg(
        getattr(args, val), val,
        parser._option_string_actions["--" + val].help
    )
# <


# vaeインスタンス作成
vae = model.VariationalAutoencoder(args.latent_dim)
print("dir_pt:", args.dir_pt)
vae.load_state_dict(torch.load(args.dir_pt))
use_model = process_data.UseModel(vae, args.latent_dim)


# > 潜在変数を変更しながら出力を確認

def replacer(s, newstring, index):
    if index < 0:  # add it to the beginning
        raise ValueError("indexがおかしい．")
    if index > len(s):  # add it to the end
        raise ValueError("indexがおかしい．")

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]


# # つまり，潜在変数の次元を超えないcheck_depth変数によって関数を分けることにすればいいのではないかということ．
def check_gallery(use_model, dir_results, check_depth, sample_point=1.5):
    ld = use_model.latent_dim
    print(f"# 潜在変数の次元：{ld}，深さ：{check_depth}")
    unit = np.array([-sample_point, 0, sample_point])
    m = check_depth - 2  # 深さに応じた行方向のループ数
    if m == 0:
        z = [0 for v in range(ld)]
        filename = 'gallery'
        use_model.make_gallery(
            z, dir_results, filename
        )
    else:
        num_loop = 3 ** m
        for i in tqdm(range(num_loop)):
            # print(f"\n{i = }")
            z = [0 for v in range(ld)]
            filename = "0" * m
            for j in range(m):
                # print(f"{j = }")
                # Dividend ÷ Divisor = Quotient
                if j == 0:
                    index = i % 3
                    # print(f"{index = }")
                else:
                    # それぞれのquotientを，さらに3で割って，その"余り"をindexとしなければならない．
                    divisor = 3 ** j  # それぞれのjにおける割る数
                    # print(f"{divisor = }")
                    quotient = i // divisor
                    index = quotient % 3
                    # print(f"{index = }")
                z[1 + m - j] = unit[index]
                inv_j = m - j - 1
                filename = replacer(filename, str(index), inv_j)
            # print("#", f"{filename = }")
            use_model.make_gallery(
                z, dir_results, filename
            )


if strtobool(args.check_gallery_switch):
    # check_depthとlatent_dimがうまく設定されているかどうかの確認
    if args.check_depth <= 1:
        raise ValueError("args.check_depthが1より小さいのでストップ．")
    if args.check_depth > args.latent_dim:
        raise ValueError("args.check_depthがargs.latent_dimより大きいのでストップ．")

    check_gallery(use_model, dir_results, args.check_depth)

# <


# > meanとstandard deviationを確認．

def check_ms():
    csv_distance = os.path.join(dirname, "distances.csv")
    num_dataset = 4  # しばらくは4
    dir_dataset = configures.dir_of_dataset_shape
    my_dataset = modules.SimpleDataset(4, dir_dataset)

    for x, _ in my_dataset.dataloader:
        for m in range(num_dataset):
            arr = x[m][0].numpy()
            arr = np.logical_and(arr > 0, True)*1.0
            arr = arr.astype(int)*255
        x = x.to(device)  # GPU
        _ = vae.encoder(x)
        mu = vae.encoder.mu.detach().numpy()
        sigma = vae.encoder.sigma.detach().numpy()
        valcol.print_arg(mu, "mu", "平均")
        valcol.print_arg(sigma, "sigma", "標準偏差")
        np.save(os.path.join(args.dir_main, "mu"), mu)
        np.save(os.path.join(args.dir_main, "sigma"), sigma)
        with open(csv_distance, "a") as f:
            flag = "1"
            for i in range(num_dataset):
                mu_i = mu[i]
                sigma_i = sigma[i]
                z = np.full(mu_i.shape, 0)
                d = distance.measure_d(z, mu_i, sigma_i)  # 原点と各データセットとの距離
                valcol.print_arg(d, "d"+str(i+1), "画像"+str(i+1)+"の0からの距離")
                f.write(str(d)+",")
                if d > 500:
                    flag = "0"
            f.write(flag)
            f.write("\n")


if strtobool(args.check_ms_switch):
    check_ms()

# <


valcol.__del__()
