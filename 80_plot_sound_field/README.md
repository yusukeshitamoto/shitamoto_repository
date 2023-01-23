# 80_plot_sound_field

プログラムで，srcファイルをいじって，黒で埋めた．

## 使い方:

1. src/以下に散乱体の画像データ，CHECK_U_INCAL.txtを保存し，plot_sound_field/以下にobs_point.txtを用意する．
2. 散乱体の画像データとCHECK_U_INCALは同じ名前にしておく．例：CHECK_U_INCAL001.txt -> 001.txt
3. go.shのリスト：arrを適宜書き換える．
4. go.shを実行．

* src/png2txt.py を使えば，バイナリ画像データからtxtのバイナリデータを作れる．

## Future Work

ファイル名をプログラムの引数として渡したい（.c, .plt両方）．
そうすれば手間が1/3になる．
