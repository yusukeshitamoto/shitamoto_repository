# incalから，tar.gz作成しつつのアーカイブフォルダの用意まで，post processのすべてが詰まっている．

# いじるところ：
DATE=20230116
DATE_MODEL=20221226
ar1=(
    "sample"
)  # モデルの名前のリスト
# ファイル処理をするかどうか
PROCESS=false
# アーカイブを作成するかどうか
MAKE_ARCHIVE=true
# LOOP=`seq -f '%02g' 3`  # ループの設定

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

# 各実験条件の各モデルディレクトリに潜ってファイル操作．
if ${PROCESS}
then
    if ! [ -e ./${DATE} ]
    then
        echo "# # # "${DATE}は存在しない！！
    else
        cd ${DATE}
        for model in "${ar1[@]}"; do
            echo ${DATE}: ${model}
            cd ${model}
                # イテレーション数の取り出し
                TOTAL_ITER=`head -n 1 ${RES}/${ITER}`
                echo ${TOTAL_ITER}

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
                for i in `seq -f '%03g' 60`
                do
                    echo ${IN}${i}
                    cp -v ${PIC}/${IN}${i}.txt ${SRC}/${i}.txt
                    cp -v ${RES}/${i}.png ${SRC}/${i}.png
                done

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

                # pixel_workdirのgzipファイル化と移動
                if [ -e ${PIC} ]
                then
                    echo gzipファイルの処理．．．
                    tar -zcf ${DATE}_${model}.tar.gz ${PIC}
                    # rm -r ${PIC}
                    # gzipファイル専用フォルダへの移動
                    mv ${DATE}_${model}.tar.gz ${TOP}/${GZS}
                fi
            cd ..
        done
        cd ..
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
    mv -v ${DATE} ${DST}
    cp -r ${DATE_MODEL} ${DST}
fi
