# optimization.pyに送りこむargparseを羅列したテキストファイルを作成する．
import os


dirname = os.path.dirname(os.path.abspath(__file__))

# # いじるところ：
# 日付
date = "20230129"
# モデルパラメータが入ったディレクトリ
dir_model = os.path.join(dirname, "model_parameters")
comment = "Experiments_with_dimensions_4_8_2_6"

# 通し番号と実験条件のリスト
log_file = "_実験条件のリスト.txt"
exp_list = [
    # [experimental_subject, dimension]
    ["bayes", 4],
    ["cobyla", 4],
    ["bayes", 8],
    ["cobyla", 8],
    ["bayes", 2],
    ["cobyla", 2],
    ["bayes", 6],
    ["cobyla", 6]
]

with open(os.path.join(dirname, date + log_file), "w") as f:
    f.write(
        str(
            ["experimental_subject", "dimension"]
        ) + "\n"
    )
    for exp in exp_list:
        f.write(str(exp) + "\n")

name = date + "_args"
filename = name + ".txt"

with open(os.path.join(dirname, filename), "w") as f:
    with open(os.path.join(dirname, date + log_file), "w") as f2:
        for i, exp in enumerate(exp_list):
            # boolに関しては distutils.util の strtobool(args.distance_switch) を使うこと．
            experimental_subject, dimension = exp
            exp_id = experimental_subject + "_d" + str(dimension)
            dir_main = os.path.join(
                os.path.join(
                    dirname, date
                ), exp_id
            )
            dir_model_pt = os.path.join(dir_model, "model.pt")
            dir_mu_sigma = dir_model
            # experimental_subject =
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
            max_iter = 300
            # dimension =
            print(
                    f"""\
--dir_main {dir_main} \
--exp_id {exp_id} \
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
--comment {comment} \
--max_iter {max_iter} \
--dimension {dimension}\
""",
                    file=f
            )
            print(
                f"# # {experimental_subject}\tdimensino: {dimension}",
                file=f2
            )
            print(
                    f"""\
--dir_main: {dir_main}\n\
--exp_id: {exp_id}\n\
--dir_model_pt: {dir_model_pt}\n\
--dir_mu_sigma: {dir_mu_sigma}\n\
--experimental_subject: {experimental_subject}\n\
--latent_dim: {latent_dim}\n\
--distance_switch: {distance_switch}\n\
--x0: {x0}\n\
--weight_min_d: {weight_min_d}\n\
--dx: {dx}\n\
--xobs_x: {xobs_x}\n\
--log_switch: {log_switch}\n\
--test_bool: {test_bool}\n\
--comment: {comment}\n\
--max_iter {max_iter}\n\
--dimension {dimension}\n\
""",
                    file=f2
            )
