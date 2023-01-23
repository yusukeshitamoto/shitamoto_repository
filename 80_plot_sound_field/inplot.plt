
reset

x_min = -3.0
x_max =  3.0
y_min = -2.0
y_max =  4.0
x_y_ratio = (y_max - y_min)/(x_max - x_min)

set xrange [x_min:x_max]
set yrange [y_min:y_max]
set size ratio x_y_ratio

set cbtics scale 0

set lmargin at screen 0.15
set rmargin at screen 0.80

# /=* でフォントサイズいじれる．
set xlabel '{/=30 {/Times-Italic x}}'
set ylabel '{/=30 {/Times-Italic y}}'
# set zlabel '{/=30 {/Times-Italic z}}'
set cblabel '{/=30 {/Times-Italic |u|}}'

# メモリのフォント．
set tics font ",20"

# フォントでかくしたバージョン用オフセット
set cblabel offset 3,0

set dgrid 128

set term png font 'arial' enhanced
# set terminal pngcairo enhanced

# ######################################################################
# いじるところ
file_in = sprintf("./out.txt")
file_out = sprintf("./incal.png")
# ######################################################################

set output file_out

# カラーマップのスケール設定：
set cbrange[0.0:4.0]

# # obs_point.txtを読み込んで，obsポイントを書き込んだバージョン．
plot file_in u 1:2:5 w image, "./obs_point.txt" pt 3 ps 2 lc 'green' notitle  # title を消してみた．

# set output file_out
# replot

