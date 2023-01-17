# incalから，tar.gz作成しつつのアーカイブフォルダの用意まで，post processのすべてが詰まっている．

# いじるところ：
DATE=20220106_1
DATE_MODEL=20221226
ar1=(
    "3420"
)  # モデルの名前のリスト
# ファイル処理をするかどうか
PROCESS=false
# アーカイブを作成するかどうか
MAKE_ARCHIVE=true
LOOP=`seq -f '%02g' 3`  # ループの設定


# ID，最適解，最適値などを記録するフォルダ
OBJ=${PWD}/${DATE}_obj.csv

# # columnを設定．
# latent_dim=2  # <------------------ 潜在変数の次元を設定する必要がある!!
# echo head,`seq -s, -f 'z%1g' ${latent_dim}`,J >> ${OBJ}

TOP=${PWD}  # optimization.pyのあるディレクトリ

PIC=pixel_workdir
IN=CHECK_U_INCAL
ITER=total_iteration.txt
RES=results
PP=post_process
OPT=opt_shape.png
SRC=src
GZS=${DATE}_gzips
ARCHIVE=archive
PLT=80_plot_sound_field
ABS_VAE_WITH_OPT=${HOME}/Desktop/vae_with_opt
OBS_TXT=obs_point.txt

FAIL=fail.txt  # 失敗した時に生成されるファイル

num1=991
num2=992

mkdir ${TOP}/${GZS}

# 各実験条件の各モデルディレクトリに潜ってファイル操作．
if ${PROCESS}
then
    rm ${OBJ}
    for exp in ${LOOP}; do
        if ! [ -e ./${DATE}_${exp} ]
        then
            echo "# # # "${DATE}_${exp}は存在しない！！
        else
            cd ${DATE}_${exp}
            for model in "${ar1[@]}"; do
                echo ${DATE}_${exp}: ${model}
                cd ${model}
                    if [ -f "${FAIL}" ]
                    then
                        echo ${DATE}_${exp}: ${model}は最適化失敗している．>> ${TOP}/${DATE}_failures.txt

                        # イテレーション数の取り出し
                        TOTAL_ITER=`head -n 1 ${RES}/${ITER}`
                        echo ${TOTAL_ITER}

                        # pixel_workdirのgzipファイル化と移動
                        if [ -e ${PIC} ]
                        then
                            echo gzipファイルの処理．．．
                            tar -zcf ${DATE}_${exp}_${model}.tar.gz ${PIC}
                            rm -r ${PIC}
                            # gzipファイル専用フォルダへの移動
                            mv ${DATE}_${exp}_${model}.tar.gz ${TOP}/${GZS}
                        fi
                    else
                        # イテレーション数の取り出し
                        TOTAL_ITER=`head -n 1 ${RES}/${ITER}`
                        echo ${TOTAL_ITER}

                        # pixel_workdirのgzipファイル化と移動
                        if [ -e ${PIC} ]
                        then
                            echo gzipファイルの処理．．．
                            tar -zcf ${DATE}_${exp}_${model}.tar.gz ${PIC}
                            rm -r ${PIC}
                            # gzipファイル専用フォルダへの移動
                            mv ${DATE}_${exp}_${model}.tar.gz ${TOP}/${GZS}
                        fi

                        # obs_pointに出力する値の用意
                        row=28  # xobs_xに関する情報の行数
                        val=`head -n ${row} ${model}_variables.txt | tail -n 1`
                        echo 観測点の座標：${val}
                        val=`echo ${val} | tr -d '観測点の座標： xobs_x = '`
                        val2=1
                        rm ${ABS_VAE_WITH_OPT}/${PLT}/${OBS_TXT}
                        echo ${val} ${val2} >> ${ABS_VAE_WITH_OPT}/${PLT}/${OBS_TXT}

                        # incal用のsrcフォルダ作成
                        mkdir ${SRC}
                        cp ${RES}/${num1}.png ${SRC}/init.png
                        cp ${RES}/${num2}.png ${SRC}/opt.png
                        cp ${PP}/${IN}${num1}.txt ${SRC}/init.txt
                        cp ${PP}/${IN}${num2}.txt ${SRC}/opt.txt

                        # post_processのgzipファイル化と移動
                        if [ -e ${PP} ]
                        then
                            echo gzipファイルの処理．．．
                            tar -zcf ${DATE}_${exp}_${model}_pp.tar.gz ${PP}
                            rm -r ${PP}
                            # gzipファイル専用フォルダへの移動
                            mv ${DATE}_${exp}_${model}_pp.tar.gz ${TOP}/${GZS}
                        fi

                        # incalの実行と結果のコピー
                        rm -r obj/
                        cp -r ${SRC}/ ${ABS_VAE_WITH_OPT}/${PLT}/
                        TMP=${PWD}
                        cd ${ABS_VAE_WITH_OPT}/${PLT}
                            echo ${PWD}
                            rm -r obj
                            . go.sh
                        cd ${TMP}
                        mv ${ABS_VAE_WITH_OPT}/${PLT}/obj/ ./

                        # logファイルの最終行の取り出し
                        z=`tail -n 1 ${RES}/z_log.csv`
                        J=`tail -n 1 ${RES}/J_log.csv`
                        echo ${DATE}_${exp},${model},${z},${J} >> ${OBJ}

                        # opt_shape.pngの取り出し
                        cp -v ${RES}/opt_shape.png ../${model}_opt_shape.png
                    fi
                cd ..
            done
            cd ..
        fi
    done
fi

# 実験に関わるファイル・フォルダを一括で移動
if ${MAKE_ARCHIVE}
then
    echo アーカイブ作成（${DATE}_${ARCHIVE}）
    DST=${DATE}_${ARCHIVE}
    mkdir ${DST}
    mv ${TOP}/${GZS}/ ${DST}
    mv ${OBJ} ${DST}
    mv ${DATE}_計算の条件.txt ${DST}
    mv ${DATE}_実験条件のリスト.txt ${DST}
    for exp in ${LOOP}; do
        mv ${DATE}_${exp} ${DST}
    done
    cp -r ${DATE_MODEL} ${DST}
fi
