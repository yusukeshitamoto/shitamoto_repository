# optimization.pyに送りこむargparseを羅列したテキストファイルを作成する．
import os


dirname = os.path.dirname(os.path.abspath(__file__))

# # いじるところ：
# 日付
date = "20230118"
# モデルパラメータが入ったディレクトリ
dir_model = os.path.join(dirname, "model_parameters")
comment = "With_distance"

# 通し番号と実験条件のリスト
log_file = "_実験条件のリスト.txt"
exp_list = [
    # [experimental_subject]
    "cobyla"
]

with open(os.path.join(dirname, date + log_file), "w") as f:
    f.write(
        str(
            ["distance_switch", "weight_min_d", "xobs_x"]
        ) + "\n"
    )
    for exp in exp_list:
        f.write(str(exp) + "\n")

name = date + "_args"
filename = name + ".txt"

with open(os.path.join(dirname, filename), "w") as f:
    model = "model"
    for i, experimental_subject in enumerate(exp_list):
        # boolに関しては distutils.util の strtobool(args.distance_switch) を使うこと．
        dir_main = os.path.join(
            os.path.join(
                dirname, date
            ), experimental_subject
        )
        model_id = model
        dir_model_pt = os.path.join(dir_model, model + ".pt")
        dir_mu_sigma = dir_model
        latent_dim = 8
        distance_switch = False
        x0 = ""
        for i in range(latent_dim):
            x0 += "0 "
        weight_min_d = 0
        dx = "1.5"
        xobs_x = -0.25
        log_switch = "False"
        test_bool = False
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
--test_bool {test_bool} \
--comment {comment}\
""",
                file=f
        )
