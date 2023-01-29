mkdir obj
PYTHON=/usr/bin/python3

make

# arr=(
#     "10_ld3bs16_034"
#     "11_ld2bs8_020"
#     "11_ld4bs8_016"
#     "12_ld6bs4_012"
#     "15_ld2bs8_020"
#     "16_ld5bs4_008"
# )
# arr=(
#     "1"
# )
arr=(
    "bayes_d2_init"
    "bayes_d2_opt"
    "bayes_d4_init"
    "bayes_d4_opt"
    "bayes_d6_init"
    "bayes_d6_opt"
    "bayes_d8_init"
    "bayes_d8_opt"
    "cobyla_d2_init"
    "cobyla_d2_opt"
    "cobyla_d4_init"
    "cobyla_d4_opt"
    "cobyla_d6_init"
    "cobyla_d6_opt"
    "cobyla_d8_init"
    "cobyla_d8_opt"
)
echo "${arr[@]}"

for val in "${arr[@]}"; do
    # ファイル操作．．．
    echo "# ${val} を実行中．．．"
    cp ./src/${val}.png ./shape.png
    cp ./src/${val}.txt ./incal.txt
    ${PYTHON} png2txt.py
    # echo "fill_black.cを実行（a.out）．"
    ./a.out
    gnuplot -e "load 'inplot.plt'"
    # ファイル操作．．．
    cp ./incal.png ./obj/${val}_incal.png
    cp ./shape.png ./obj/${val}_shape.png
done

rm ./incal.png
rm ./shape.png
rm ./incal.txt
rm ./shape.txt
