# 変数PYTHONの設定
# $(uname)には"Darwin"か"Linux"あたりが入っている．
if [ "$(uname)" == 'Darwin' ]
then
    OS='Mac'
    PYTHON=/usr/local/bin/python3
elif [ "$(uname)" == 'Linux' ]
then
    OS='Linux'
    PYTHON=/usr/bin/python3
else
    echo "Your platform ($(uname -a)) is not supported."
    exit 1
fi
SCRIPT=optimization.py

# いじるところ：
DATE=20230117  # handlerのdateと一致してないと動かない

arr=()   # 空の配列
echo "${arr[@]}"

while read line
do
    # echo $line
    arr+=("$line")
done < ./${DATE}_args.txt

# Read the array values with space
# " "で囲むとスペースでちぎれない．
for val in "${arr[@]}"; do
    ${PYTHON} ${SCRIPT} ${val}
done

cp ./計算の条件.txt ./${DATE}_計算の条件.txt
