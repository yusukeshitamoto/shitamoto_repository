# incalから，tar.gz作成しつつのアーカイブフォルダの用意まで，post processのすべてが詰まっている．

# いじるところ：
DATE=20230129
DATE_MODEL=model_parameters
# exp_list=(
#     "bayes_d2"
#     "cobyla_d2"
#     "bayes_d4"
#     "cobyla_d4"
#     "bayes_d6"
#     "cobyla_d6"
#     "bayes_d8"
#     "cobyla_d8"
# )

exp="bayes_d4"

# テストを実行：
TEST=false
# ファイル処理をするかどうか
PROCESS=true
# アーカイブを作成するかどうか
MAKE_ARCHIVE=false
# LOOP=`seq -f '%02g' 3`  # ループの設定

# 設定：
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

mkdir ${TOP}/${GZS}

# 観測点の情報
x_obs_x=-0.25
# incal用のsrcフォルダの絶対パス
ABS_SRC=${TOP}/src
mkdir ${ABS_SRC}

# 各実験条件の各モデルディレクトリに潜ってファイル操作．
if ${PROCESS}
then
    if ! [ -e ./${DATE} ]
    then
        echo "# # # "${DATE}は存在しない！！
    else
        cd ${DATE}  # DATE

        echo ${DATE}: ${exp}

        cd ${exp}  # exp
            # echo 2. ${PWD}
            # イテレーション数の取り出し
            TOTAL_ITER=`head -n 1 ${ITER}`
            echo ${TOTAL_ITER}

            # 目的関数の最大値の取り出し
            f_opt=`head -n 1 f_opt.txt`
            echo ${f_opt}

            # pixel_workdirのgzipファイル化と移動
            if [ -e ${PIC} ]
            then
                echo gzipファイルの処理．．．
                tar -zcf ${DATE}_${exp}.tar.gz ${PIC}
                rm -r ${PIC}
                # gzipファイル専用フォルダへの移動
                mv ${DATE}_${exp}.tar.gz ${TOP}/${GZS}
            fi

            # topディレクトリにlog.csvをコピー
            cp -v J_log.csv ../${exp}_J_log.csv
            cp -v z_log.csv ../${exp}_z_log.csv

            # incal用のsrcフォルダにコピー
            cp -v ${PP}/${IN}991.txt ${ABS_SRC}/${exp}_init.txt
            cp -v ${PP}/${IN}992.txt ${ABS_SRC}/${exp}_opt.txt
            cp -v ${RES}/991.png ${ABS_SRC}/${exp}_init.png
            cp -v ${RES}/992.png ${ABS_SRC}/${exp}_opt.png

            # # incalの実行と結果のコピー
            # rm -r obj/
            # cp -r ${SRC}/ ${ABS_VAE_WITH_OPT}/${PLT}/
            # TMP=${PWD}
            # cd ${ABS_VAE_WITH_OPT}/${PLT}
            #     echo ${PWD}
            #     rm -r obj
            #     . go.sh
            # cd ${TMP}
            # mv ${ABS_VAE_WITH_OPT}/${PLT}/obj/ ./

        cd ..  # exp
    

        cd ..  # DATE
    fi
fi

# 実験に関わるファイル・フォルダを一括で移動
if ${MAKE_ARCHIVE}
then
    echo アーカイブ作成（${DATE}_${ARCHIVE}）
    DST=${DATE}_${ARCHIVE}
    mkdir ${DST}
    mv -v ${TOP}/${GZS}/ ${DST}
    mv -v ${DATE}_計算の条件.txt ${DST}
    mv -v ${DATE}_実験条件のリスト.txt ${DST}
    mv -v ${DATE}_args.txt ${DST}
    mv -v ${DATE} ${DST}
    cp -r ${DATE_MODEL} ${DST}
fi
