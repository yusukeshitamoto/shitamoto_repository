import os
import torch
import ctypes
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt

# self-made
import process_data
from modules import png
import distance
# モデル
import model_template as model


class ObjFunc():
    def __init__(
            self, dir_model_pt, latent_dim, dir_results,
            weight_min_d=0, xobs_x=-0.20,
            mu_ndarray=None, sigma_ndarray=None
            ):
        self.iteration = 0
        self.J_log = []
        self.z_log = []
        self.dir_results = dir_results
        # > 共有ライブラリの準備
        LIB_PATH = './libpixel_GCC631.so'
        self.lib = ctypes.cdll.LoadLibrary(LIB_PATH)
        # 戻り値の型を指定
        self.lib.pixel_objfunc.restype = ctypes.c_double
        lx = 2.0
        self.c_lx = ctypes.c_double(lx)
        ly = 2.0
        self.c_ly = ctypes.c_double(ly)
        # xobs_x = -0.20
        self.c_xobs_x = ctypes.c_double(xobs_x)
        xobs_y = ly/2
        self.c_xobs_y = ctypes.c_double(xobs_y)
        cndfile = b"test.cnd"
        self.c_cndfile = ctypes.c_char_p(cndfile)
        infile = b"test.in"
        self.c_infile = ctypes.c_char_p(infile)
        # <
        self.vae = model.VariationalAutoencoder(latent_dim)
        print(dir_model_pt)
        self.vae.load_state_dict(torch.load(dir_model_pt))

        # distに関わる変数
        self.weight_min_d = weight_min_d
        self.mu_ndarray = mu_ndarray
        self.sigma_ndarray = sigma_ndarray

    def setup(self, x):
        """iterationのカウントアップと，xからの画像生成
        """
        self.iteration += 1
        print("# # # Iteration =", self.iteration)
        self.z_log.append(list(x))
        input = torch.Tensor(x)
        img = self.vae.decoder(input)
        img = img.detach().numpy().reshape(128, 128)*-1
        img = (img > 0.) * 1.
        img = process_data.filter(img)/255
        self.save_shape(img, str(self.iteration).zfill(3))
        return img

    def func_J(self, x, _):
        img = self.setup(x)
        ##############################################
        # 目的関数の値を計算するパート
        # # 音圧計算パート
        J = self.calc_J_from_img(img)
        ##############################################
        self.J_log.append(J)
        return J

    def func_J_dist(self, x, _):
        img = self.setup(x)
        ##############################################
        # 目的関数の値を計算するパート

        # # 距離計算パート
        min_d = self.check_min_d(x)

        # # 音圧計算パート
        J = self.calc_J_from_img(img)

        # 距離に乗じるウェイト
        weight_min_d = self.weight_min_d
        J_total = J - weight_min_d * min_d
        print(f"{min_d = }, {weight_min_d = }, {weight_min_d * min_d = }")
        ##############################################
        self.J_log.append([J, weight_min_d * min_d, J_total])
        return J_total

    def func_J_test(self, x, _):
        img = self.setup(x)
        ##############################################
        # 目的関数の値を計算するパート
        # # 音圧計算パート（testバージョン）
        J = self.calc_J_from_img_test(img, x)
        ##############################################
        self.J_log.append(J)
        return J

    def func_J_dist_test(self, x, _):
        img = self.setup(x)
        ##############################################
        # 目的関数の値を計算するパート

        # # 距離計算パート
        min_d = self.check_min_d(x)

        # # 音圧計算パート（testバージョン）
        J = self.calc_J_from_img_test(img, x)

        # 距離に乗じるウェイト
        weight_min_d = self.weight_min_d

        J_total = J - weight_min_d * min_d
        ##############################################
        self.J_log.append([J, weight_min_d * min_d, J_total])
        return J_total

    def calc_J_from_img(self, img):
        img = img.astype(int)
        np.savetxt("./moon_optimized.txt", img, delimiter="", fmt='%d')
        c_iteration = ctypes.c_int(self.iteration)
        J = self.lib.pixel_objfunc(
            c_iteration, self.c_lx, self.c_ly, self.c_xobs_x,
            self.c_xobs_y, self.c_cndfile, self.c_infile
        )
        print(f"戻り値（目的関数）は{J}です．")
        return J

    def calc_J_from_img_test(self, img, x):
        img = img.astype(int)
        np.savetxt("./moon_optimized.txt", img, delimiter="", fmt='%d')
        # testでは，漸近的に1に近づく関数を設定しておく．
        J = 10 - np.sum(x * x)
        with open(
                    "./pixel_workdir/CHECK_TEST"
                    + str(self.iteration).zfill(3) + ".txt",
                    "w"
                ) as f:
            f.write("0")
        with open(
                    "./pixel_workdir/CHECK_U_INCAL"
                    + str(self.iteration).zfill(3) + ".txt",
                    "w"
                ) as f:
            f.write("0")
        print(f"戻り値（目的関数）は{J}です．")
        return J

    def check_min_d(self, x):
        if self.mu_ndarray is None:
            raise ValueError("distなのにmuが設定されてない")
        if self.sigma_ndarray is None:
            raise ValueError("distなのにsigmaが設定されてない")
        min_d = 1000.
        for i in range(4):
            mu = self.mu_ndarray[i]
            sigma = self.sigma_ndarray[i]
            d = distance.measure_d(x, mu, sigma)
            if min_d > d:
                min_d = d
        return min_d

    def reset_iteration(self):
        print("iterationをリセットしました．")
        self.iteration = 0

    def save_shape(self, img, filename):
        L = 128
        img = np.full((L, L), 1) - img
        img = img*255
        img = img.astype(int)
        cv2.imwrite(os.path.join(self.dir_results, png(filename)), img)
        print("# # ", os.path.join(self.dir_results, png(filename)), "保存完了")

    def save_log(self, x):
        plt.close("all")
        plt.plot(self.J_log)
        plt.xlabel("Step")
        plt.ylabel("$J$")
        plt.savefig(os.path.join(self.dir_results, "J_log.png"))
        input = torch.Tensor(x)
        img = self.vae.decoder(input)
        img = img.detach().numpy().reshape(128, 128)*-1
        img = (img > 0.) * 1.
        img = process_data.filter(img)/255
        self.save_shape(img, "opt_shape")

    def save_log_as_csv(self):
        obj_path = os.path.join(self.dir_results, "J_log.csv")
        df = pd.DataFrame(self.J_log)
        df.to_csv(obj_path, header=False, index=False)
        obj_path_z = os.path.join(self.dir_results, "z_log.csv")
        df_z = pd.DataFrame(self.z_log)
        df_z.to_csv(obj_path_z, header=False, index=False)

    def export_iteration(self):
        file = "total_iteration.txt"
        with open(os.path.join(self.dir_results, file), "w") as f:
            print(self.iteration, file=f)
