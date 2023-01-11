# tmp.txtを順に実行するコード．
# 先にextract_model.pyを実行しておく必要がある．
PYTHON=/usr/bin/python3
SCRIPT=optimization.py

# SCRIPT=z2j.py

echo ${SCRIPT}

# いじるところ：
DATE=20220100  # handlerのdateと一致してないと動かない


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
