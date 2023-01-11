# optimization.pyに送りこむargparseを羅列したテキストファイルを作成する．
import os


dirname = os.path.dirname(os.path.abspath(__file__))

# # いじるところ：
# 日付
date = "20220106"
# date = "2099"
# モデル訓練の日付
model_date = "20221226"
# 最適化を行うモデルのリスト．
model_list = [
    "3420",
    "4228",
    "4230"
]
comment = "With_distance"

# 通し番号と実験条件のリスト
log_file = "_実験条件のリスト.txt"
exp_list = [
    # [sequencial_num, distance_switch, weight_min_d, xobs_x]
    [1, True, 0.02, -0.30],
    [2, True, 0.03, -0.30],
    [3, True, 0.04, -0.30],
]

with open(os.path.join(dirname, date + log_file), "w") as f:
    f.write(
        str(
            ["sequencial_num", "distance_switch", "weight_min_d", "xobs_x"]
        ) + "\n"
    )
    for exp in exp_list:
        f.write(str(exp) + "\n")

name = date + "_args"
filename = name + ".txt"

with open(os.path.join(dirname, filename), "w") as f:
    for exp in exp_list:
        # boolに関しては distutils.util の strtobool(args.distance_switch) を使うこと．
        sequencial_num, distance_switch, weight_min_d, xobs_x = exp
        for model in model_list:
            dir_main = os.path.join(
                os.path.join(
                    dirname, date + "_" + str(sequencial_num).zfill(2)
                ), model
            )
            dir_tmp = os.path.join(os.path.join(dirname, model_date), model)
            model_id = model
            dir_model_pt = os.path.join(dir_tmp, model + ".pt")
            dir_mu_sigma = dir_tmp
            experimental_subject = "dist"
            latent_dim = 8
            # distance_switch = distance_switch
            x0 = ""
            for i in range(latent_dim):
                x0 += "0 "
            # weight_min_d = weight_min_d
            dx = "1.5"
            # xobs_x = xobs_x
            log_switch = "False"
            print(
                    f"""\
--dir_main {dir_main} \
--model_id {model_id} \
--dir_model_pt {dir_model_pt} \
--dir_mu_sigma {dir_mu_sigma} \
--experimental_subject {experimental_subject} \
--latent_dim {latent_dim} \
--distance_switch {distance_switch} \
--x0 {x0} \
--weight_min_d {weight_min_d} \
--dx {dx} \
--xobs_x {xobs_x} \
--log_switch {log_switch} \
--comment {comment}\
""",
                    file=f
            )
