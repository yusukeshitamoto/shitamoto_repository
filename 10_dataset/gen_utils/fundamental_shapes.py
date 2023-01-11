# ##################################################
# 基本的な図形生成のプログラムをまとめておく．
# ##################################################
import numpy as np
import sys
import os
import math


print('basename:    ', os.path.basename(__file__))
print('dirname:     ', os.path.dirname(__file__))
dirname = os.path.dirname(__file__)


def generate_circle(L, r, center=[3, 3]):
    """
    白埋めの正方形（1辺L）に中心の座標center，半径r，の円形を入れ込んだ配列を返す．
    L, rはピクセル．Lはキャンバスの一辺の長さ，rは半径．
    もしも中心座標がピクセルの間である場合は，
    0.5を加えたものにすればよい．
    """
    img = np.full((L, L), 0)
    # numpy.mgrid()を使う．
    yy, xx = np.mgrid[:L, :L]
    # print("xx= ", xx)
    # print("yy= ", yy)
    # circleはxx, yyと同じ次元（L, L）をもつ．要素は中心からの距離の関数になっている．
    circle = (xx + 1 - center[0]) ** 2 + (yy + 1 - center[1]) ** 2
    circle = np.logical_and(circle < (r**2), True)
    img = img + circle*1
    img = img.astype(int)
    return img


def generate_square_at_center(L, r):
    """中心に位置する一辺の長さr[px]の正方形を，
    一辺の長さL[px]のキャンバスに入れ込んだ配列を返す．

    Args:
        L (int): キャンバスの一辺の長さ，偶数のみ対応
        r (int): 正方形の一辺の長さ，偶数のみ対応
    """
    if r%2 == 1:
        print("# # (エラー) 正方形の一辺の長さが偶数でないので終了します．")
        sys.exit()
    if L%2 == 1:
        print("# # (エラー) キャンバスの一辺の長さが偶数でないので終了します．")
        sys.exit()
    # 方針は，徐々に周囲を剥がすイメージ．
    img = np.full((L, L), 1)
    yy, xx = np.mgrid[:L, :L]
    img = np.logical_and(yy < int(L - (L - r)/2), img)
    # print(img)
    img = np.logical_and(xx < int(L - (L - r)/2), img)
    # print(img)
    img = np.logical_and(yy >= int(L - r)/2, img)
    # print(img)
    img = np.logical_and(xx >= int(L - r)/2, img)
    # print(img)
    return img


def generate_triangle_at_center(L, a):
    """重心がキャンバスの中心に位置する一辺の長さa[px]の正三角形を，
    一辺の長さL[px]のキャンバスに入れ込んだ配列を返す．

    Args:
        L (int): キャンバスの一辺の長さ，偶数のみ対応
        a (int): 正三角形の一辺の長さ，偶数のみ対応
    """
    if L%2 == 1:
        print("# # (エラー) 正方形の一辺の長さが偶数でないので終了します．")
        sys.exit()
    # 計算については，研究のフォルダにまとまっている．
    img = np.full((L, L), 1)
    yy, xx = np.mgrid[:L, :L] + 0.5
    # yyを上下反転させる（座標軸方向を一致させるため）
    yy = np.flip(yy, 0)
    # print(yy)
    # print(L/2 - math.sqrt(3) * a / 12)
    sqrt_3 = math.sqrt(3)
    img = np.logical_and(yy >= (L/2 - sqrt_3 * a / 6), True)
    img = np.logical_and(yy <= (sqrt_3 * xx - (sqrt_3 - 1)*L/2 + sqrt_3 * a / 3), img)
    img = np.logical_and(yy <= (-1 * sqrt_3 * xx + (sqrt_3 + 1)*L/2 + sqrt_3 * a / 3), img)
    return img


def generate_oval(L, r, phi, center=[3, 3]):
    """
    白埋めの正方形（1辺L）に中心の座標center，半径r，
    円盤の回転角phiの楕円を入れ込んだ配列を返す．
    縦長限定．phiは単位deg．
    L, rはピクセル．
    もしも中心座標がピクセルの間である場合は，
    0.5を加えたものにすればよい．
    """
    if phi > 90:
        print("# # generate_oval()に90[deg]以上の角度が渡されました．処理を終了します．")
        sys.exit()
    pi = math.pi
    phi = phi/180*pi  # radian
    img = np.full((L, L), 0)
    # numpy.mgrid()を使う．
    yy, xx = np.mgrid[:L, :L]
    oval = ((xx + 1 - center[0])/math.cos(phi)) ** 2 + (yy + 1 - center[1]) ** 2
    oval = np.logical_and(oval < (r**2), True)
    img = img + oval*1
    img = img.astype(int)
    return img


if __name__ == "__main__":
    # 自作
    import save_shape

    # img = generate_square_at_center(32, 28)
    # save_shape.save_shape(dirname, img, "hoge")

    img = generate_triangle_at_center(128, 80)
    save_shape.save_shape(dirname, img, "hoge")
