# ギャラリーを作る．
import cv2
import numpy as np
import sys
import os


def png(filename):
    return filename + ".png"


# source
# foldername = "data_high"
foldername = "data_shape_high"
# 出力画像の名前
out_filename = "gallery_of_dataset_high_res"


# 画像周りに枠を追加する関数．
def add_frame(img, border_width):
    """画像周りに枠を追加する関数．

    Args:
        img (_type_): _description_
        border_width (_type_): _description_

    Returns:
        _type_: _description_
    """
    img = np.pad(img, border_width, "constant")
    return img


def make_gallery(dir_src, n_x, n_y, border_width, border_color, offset=0):
    """[summary]

    Args:
        dir_src ([type]): ギャラリーに使う画像の保存場所．データは 01.png, 02.png...という名前である必要がある．
        n_x ([type]): 横の枚数
        n_y ([type]): 縦の枚数
        border_width (int): [description]
        border_color (int): 画像間の線の色．255->白，0->黒

    Returns:
        ndarray: numpyの配列．一枚の絵．
    """
    img = cv2.imread(
        os.path.join(dir_src, png(str(1).zfill(2))), cv2.IMREAD_GRAYSCALE
    )
    height, width = img.shape
    print("画像の高さは", height, "で，幅は", width, "です．")

    gallery = np.full(
        (n_y*height + (n_y+1)*border_width, n_x*width + (n_x+1)*border_width),
        border_color, "int"
        )
    for i in range(n_y):
        for j in range(n_x):
            print("Now: ", str(n_x*i+j+1).zfill(2))
            filename = png(str(n_x*i+j+1+offset).zfill(2))
            img = cv2.imread(
                os.path.join(dir_src, filename), cv2.IMREAD_GRAYSCALE
            )
            gallery[
                i*height + (i+1)*border_width:(i+1)*height + (i+1)*border_width,
                j*width + (j+1)*border_width:(j+1)*width + (j+1)*border_width
                ] = img
    return gallery


if __name__ == "__main__":
    print('basename:    ', os.path.basename(__file__))
    print('dirname:     ', os.path.dirname(__file__))
    dirname = os.path.dirname(__file__)

    # src_path = os.path.join(dirname, "data/")
    src_path = os.path.join(dirname, foldername)

    obj_path = os.path.join(dirname, "results/")
    os.makedirs(obj_path, exist_ok=True)

    if not os.path.exists(src_path):
        print("パス", src_path, "が見つかりませんでした．終了します．")
        sys.exit()
    # 横の枚数
    n_x = 4
    # 縦の枚数
    n_y = 1
    # pixel, 画像間の線の太さ
    border_width = 0
    # 画像間の線の色．255->白，0->黒
    border_color = 255
    gallery = make_gallery(src_path, n_x, n_y, border_width, border_color)
    cv2.imwrite(os.path.join(obj_path, png(out_filename)), gallery)
