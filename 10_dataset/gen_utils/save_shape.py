import numpy as np
import sys
import os
import cv2


def save_shape(path, img, filename):
    """imgなる画像をpath/以下にstr_num/という名前で保存するコード．
    正方形のみ対応．

    Args:
        path (_type_): パス
        img (ndarray): 画像
        filename (str): ファイル名
    """
    _L = len(img)
    img = np.full((_L, _L), 1) - img
    img = img*255
    img = img.astype(int)
    if (os.path.exists(path)):
        cv2.imwrite(os.path.join(path, filename + ".png"), img)
    else:
        print("# # パス", path, "がないので終了．")
        sys.exit()
    print("# # filename:", filename, "保存完了")
