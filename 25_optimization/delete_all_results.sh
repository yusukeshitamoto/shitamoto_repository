
readonly switch=true

if [ "${switch}" ]
then
    read -n1 -p "本当に結果の全削除を行いますか？ (y/N): " yn
    if [[ $yn = [yY] ]]; then

        # topディレクトリの削除
        date_rm=20230125
        read -n1 -p "y押したら./${date_rm}消す (y/N): " yn
        if [[ $yn = [yY] ]]; then
            rm -r ./${date_rm}
        else
            echo abort
        fi

        # その他
        rm -r pixel_workdir
        rm moon_optimized.txt
        rm obj_fnc.txt
        rm -r z_viewer

    else
        echo abort
    fi
else
    echo Skiped all operations.
fi
