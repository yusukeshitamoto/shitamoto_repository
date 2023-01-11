# ##################################################
# 
# 形状リスト：
# 
# まる
# →　半径40px（面積約5027px^2）
# 
# 三角形（頂点右向き）
# →　一辺の長さ100px（面積約4330px^2）
# 
# 三角形（頂点左向き）
# →　一辺の長さ100px（面積約4330px^2）
# 
# 四角形
# →　一辺の長さ80px（面積6400px^2）
# 
# ##################################################
import numpy as np
import os
import subprocess

# 自作
import gen_utils.fundamental_shapes as fnd_shapes  # fnd_shapes.
import gen_utils.save_shape as save_shape  # save_shape.


print('basename:    ', os.path.basename(__file__))
print('dirname:     ', os.path.dirname(__file__))
dirname = os.path.dirname(__file__)

obj_path = os.path.join(dirname, "data_shape")
try:
    os.mkdir(obj_path)
except:
    print("ディレクトリがすでに存在しているので，上書きしませんでした．")


if __name__ == "__main__":
    # キャンバスの大きさ指定．
    L = 128

    # 円を保存
    img = fnd_shapes.generate_circle(L, 40, center=[L/2+0.5, L/2+0.5])
    save_shape.save_shape(obj_path, img, "01")


    # 左むき三角形を保存
    img = fnd_shapes.generate_triangle_at_center(L, 100)
    img = np.rot90(img)
    save_shape.save_shape(obj_path, img, "02")

    # 右向き三角形を保存
    img = fnd_shapes.generate_triangle_at_center(L, 100)
    img = np.rot90(img, 3)
    save_shape.save_shape(obj_path, img, "03")

    # 正方形を保存
    img = fnd_shapes.generate_square_at_center(L, 80)
    save_shape.save_shape(obj_path, img, "04")

    subprocess.run("cp " + obj_path + "/* " + os.path.join(dirname, "../20_train_vae/dataset_shape/data/"), shell=True)
