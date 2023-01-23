// ファイル名に_outを添えて，音圧の行を追加するプログラム．

// 単品で，月の内側を黒く塗りつぶす（音圧の値を0（任意の値）に書き換えられる）ように修正．（20220803）


/*
検討：

incalは 128 * 128 行のデータを出力する．そこから含まれる座標は割り出せる．

月のピクセルデータを読み込む
→　x軸方向にスライスして，一行ずつ見ていく（check_line()→start_point, end_point）
→　もし1が見つかったら，"一続き"で一番長い１のかたまりを黒く塗りつぶすことを考える（fill_line()）
→　あとはループ．

注意：
離れ小島（ちぎれた要素）はぬらない．

*/

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>

#define PIXEL_FILE_PATH "./shape.txt"
#define INCAL_FILE_PATH "./incal.txt"

void check_line(char *line, int num, double *start_point, double *end_point, int *flag, double dx, int debug);
double fill_line(double start_point, double end_point);


int main(){
    int debug = 0;
    int num = 128;
    int num_data = num*num;
    int flag;  // 塗りつぶし発生→１，塗りつぶしなし→０
    int flags[128];
    double x, y, re, im, p;
    double lx = 2.0, ly = 2.0;
    double dx = lx/(num-1), dy = ly/(num-1);
    double start_point, end_point;
    double start_points[128], end_points[128];
    double lx_2 = 6, ly_2 = 6;
    double dx_2 = lx_2/(num-1), dy_2 = ly_2/(num-1);
    double origin_x = -3, origin_y = 4;

    // 一行の0, 1データを保持
    char one_line[256];
    // char型配列の先頭の要素のポインタを，charポインタに格納して，それを関数に渡している．
    char *one_line_ptr = &(one_line[0]);
    // in, out ファイルの名前
    char pixelfile[256];
    sprintf(pixelfile, PIXEL_FILE_PATH);
    FILE *moon_infile = fopen(pixelfile, "r");
    if (debug) printf("%s\n", pixelfile);

    for (int i=0; i <= num; i++){
        fgets(one_line, 150, moon_infile);
        check_line(one_line_ptr, num, &start_point, &end_point, &flag, dx, debug);
        if (debug){
            if (flag == 1){
                printf("# # # %d:\tstart_point = %lf, end_point = %lf\n", i, start_point, end_point);
            }
        }
        start_points[i] = start_point;
        end_points[i] = end_point;
        flags[i] = flag;
    }

    // printf("start_point = %lf, end_point = %lf\n", start_point, end_point);

    fclose(moon_infile);
    // fclose(moon_outfile);

    // printf("\nFinished the points\n\n");


    char OUT_FILE[256], IN_FILE[256];
    // sprintf(IN_FILE, "src/11_incal_001.txt");
    sprintf(IN_FILE, INCAL_FILE_PATH);
    sprintf(OUT_FILE, "./out.txt");
    FILE *my_fp;
    my_fp = fopen(OUT_FILE, "w");
    FILE *fp_2 = fopen(IN_FILE, "r");

    if (fp_2 == NULL) {
        printf("Fail to open %s. Exit.\n", "incal.txt");
        exit(1);
    }

    int row = 0;
    for (int i = 0; i < num; i++){
        if (debug) printf("# # # i = %d\n", i);
        if ((origin_y - i*dy_2) > (2.0 + dx/2)){
            if (debug) printf("# Case 1:\n");
            for (int j = 0; j < num; j++){
                fscanf(fp_2, "%le %le %le %le", &x, &y, &re, &im);
                p = sqrt(re*re + im*im);
                fprintf(my_fp, "%15.7e %15.7e  %15.7e %15.7e %15.7e\n", x, y, re, im, p);
            }
        }
        else if ((origin_y - i*dy_2) <= (0.0 - dx/2)){
            if (debug) printf("# Case 2:\n");
            for (int j = 0; j < num; j++){
                fscanf(fp_2, "%le %le %le %le", &x, &y, &re, &im);
                p = sqrt(re*re + im*im);
                fprintf(my_fp, "%15.7e %15.7e  %15.7e %15.7e %15.7e\n", x, y, re, im, p);
            }
        }
        else{
            if (debug) printf("# Case 3:\n");
            // j のループで使うstart_points etc... の行を決定
            int k = 0;
            while (((k*dy - dy/2) < (origin_y - i*dy_2)) && ((k*dy + dy/2) <= (origin_y - i*dy_2))){
                ++k;
            }
            row = k;
            if (debug) printf("# # # # row = %d\n", row);
            if (flags[row] == 1){
                for (int j = 0; j < num; j++){
                    fscanf(fp_2, "%le %le %le %le", &x, &y, &re, &im);
                    p = sqrt(re*re + im*im);
                    // 入ってたら0を代入し直す
                    if ((start_points[row] < x) && (x < end_points[row])){
                        p = 0;
                    }
                    fprintf(my_fp, "%15.7e %15.7e  %15.7e %15.7e %15.7e\n", x, y, re, im, p);
                }
            }
            else{
                for (int j = 0; j < num; j++){
                    fscanf(fp_2, "%le %le %le %le", &x, &y, &re, &im);
                    p = sqrt(re*re + im*im);
                    fprintf(my_fp, "%15.7e %15.7e  %15.7e %15.7e %15.7e\n", x, y, re, im, p);
                }
            }
        }
    }


    fclose(my_fp);
    fclose(fp_2);


    // test();



    return 0;
}


void check_line(char *line, int num, double *start_point, double *end_point, int *flag, double dx, int debug){
    // printf("%s", line);
    int j = 0;
    // カウンター
    int counter = 0;
    // maxの値を保持
    int max = 0;
    // int tmp;
    // 読み込んだdigitを保持
    int d;
    // 一番長い連続の1の両端のピクセル番号
    int start_pixel = 0, end_pixel = 0;
    int tmp_start_pixel = 0;
    // 終端まで位置文字づつ扱うwhile loop．
    // printf("\n");
    while(line[j] != '\0'){
        int d = line[j] - '0';  // 最後，line[j]が'\0'だったとき，d = -38となるっぽい．
        if (debug) printf("%d", d);
        if (d == 1){
            if (counter == 0){  // 0 -> 1 のタイミングでの処理
                tmp_start_pixel = j;
            }
            counter += 1;
        }
        else{
            if (counter > 0){  // 1 -> 0 のタイミングでの処理
                if (max < counter){  // 記録更新時の処理
                    max = counter;  // max の値更新
                    start_pixel = tmp_start_pixel;
                    end_pixel = j;
                }
            }
            counter = 0;  // counter 初期化
        }
        j++;
    }

    // start_point, end_pointの計算
    if (max >= 4){
        *flag = 1;
        start_pixel = start_pixel + 1;
        end_pixel = end_pixel - 1;
        *start_point = start_pixel * dx;
        *end_point = end_pixel * dx;
    }
    else{
        *flag = 0;
        *start_point = 0;
        *end_point = 0;
    }
    if (debug) printf("\nmax = %d\n", max);
    if (debug) printf("\n");
}


double fill_line(double start_point, double end_point){
    return 1;
}

