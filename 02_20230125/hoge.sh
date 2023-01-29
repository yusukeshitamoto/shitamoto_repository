exp_list=(
    "bayes_d2"
    "cobyla_d2"
    "bayes_d4"
    "cobyla_d4"
    "bayes_d6"
    "cobyla_d6"
    "bayes_d8"
    "cobyla_d8"
)
DATE=20230125
tmp=${DATE}_archive/${DATE}
for exp in "${exp_list[@]}"
do
    cp ${tmp}/${exp}/J_log.png ./${exp}_J_log.png
done
