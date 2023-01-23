# pngをテキストに変換することはこんなに簡単．
# カプセル化（？）の恩恵．
import os
import argparse
# 自作
import process_data


dirname = os.path.dirname(os.path.abspath(__file__))

process_data.voxel2txt_path(
    dirname, dirname, "shape"
)
