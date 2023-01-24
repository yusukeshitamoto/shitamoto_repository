import plotter
import os


dirname = os.path.dirname(os.path.abspath(__file__))

J_log_csv = "J_log.csv"
J_log_png = "J_log.png"
J_log_2_png = "J_log_2.png"


def make_list(test=True):
    plot_setting_list = []

    # ##############################
    # # bayes_1
    # ##############################
    # パス関連
    folder = "bayes_1"
    src_dir = os.path.join(dirname, folder)
    src_filename = J_log_csv
    if test:
        obj_dir = os.path.join(dirname, "test")
        obj_filename = folder + "_" + J_log_png
    else:
        obj_dir = os.path.join(dirname, folder)
        obj_filename = J_log_png

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None
    # header = 0
    # index_col = 0

    # step_*ticks
    step_xticks = 1
    step_yticks = 0.5

    plot_setting_list.append(
        [
            src_dir, src_filename, obj_dir, obj_filename,
            header, index_col, step_xticks, step_yticks,
            0, None,
            None
        ]
    )

    # ##############################
    # # bayes_2
    # ##############################
    # パス関連
    folder = "bayes_2"
    src_dir = os.path.join(dirname, folder)
    src_filename = J_log_csv
    if test:
        obj_dir = os.path.join(dirname, "test")
        obj_filename = folder + "_" + J_log_png
    else:
        obj_dir = os.path.join(dirname, folder)
        obj_filename = J_log_png

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None
    # header = 0
    # index_col = 0

    # step_*ticks
    step_xticks = 20
    step_yticks = 0.5

    plot_setting_list.append(
        [
            src_dir, src_filename, obj_dir, obj_filename,
            header, index_col, step_xticks, step_yticks,
            0, None,
            None
        ]
    )

    # ##############################
    # # cobyla_1
    # ##############################
    # パス関連
    folder = "cobyla_1"
    src_dir = os.path.join(dirname, folder)
    src_filename = J_log_csv
    if test:
        obj_dir = os.path.join(dirname, "test")
        obj_filename = folder + "_" + J_log_2_png
    else:
        obj_dir = os.path.join(dirname, folder)
        obj_filename = J_log_2_png

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None
    # header = 0
    # index_col = 0

    # step_*ticks
    step_xticks = 50
    step_yticks = 0.5

    plot_setting_list.append(
        [
            src_dir, src_filename, obj_dir, obj_filename,
            header, index_col, step_xticks, step_yticks,
            0, None,
            None
        ]
    )

    # ##############################
    # # cobyla_2
    # ##############################
    # パス関連
    folder = "cobyla_2"
    src_dir = os.path.join(dirname, folder)
    src_filename = J_log_csv
    if test:
        obj_dir = os.path.join(dirname, "test")
        obj_filename = folder + "_" + J_log_2_png
    else:
        obj_dir = os.path.join(dirname, folder)
        obj_filename = J_log_2_png

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None
    # header = 0
    # index_col = 0

    # step_*ticks
    step_xticks = 50
    step_yticks = 0.5

    plot_setting_list.append(
        [
            src_dir, src_filename, obj_dir, obj_filename,
            header, index_col, step_xticks, step_yticks,
            0, None,
            None
        ]
    )

    # ##############################
    # # cobyla_1
    # ##############################
    # パス関連
    folder = "cobyla_1"
    src_dir = os.path.join(dirname, folder)
    src_filename = J_log_csv
    if test:
        obj_dir = os.path.join(dirname, "test")
        obj_filename = folder + "_" + J_log_png
    else:
        obj_dir = os.path.join(dirname, folder)
        obj_filename = J_log_png

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None
    # header = 0
    # index_col = 0

    # step_*ticks
    step_xticks = 10
    step_yticks = 0.5

    plot_setting_list.append(
        [
            src_dir, src_filename, obj_dir, obj_filename,
            header, index_col, step_xticks, step_yticks,
            0, None,
            [0, 50]
        ]
    )

    # ##############################
    # # cobyla_2
    # ##############################
    # パス関連
    folder = "cobyla_2"
    src_dir = os.path.join(dirname, folder)
    src_filename = J_log_csv
    if test:
        obj_dir = os.path.join(dirname, "test")
        obj_filename = folder + "_" + J_log_png
    else:
        obj_dir = os.path.join(dirname, folder)
        obj_filename = J_log_png

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None
    # header = 0
    # index_col = 0

    # step_*ticks
    step_xticks = 10
    step_yticks = 0.5

    plot_setting_list.append(
        [
            src_dir, src_filename, obj_dir, obj_filename,
            header, index_col, step_xticks, step_yticks,
            0, None,
            [0, 50]
        ]
    )

    return plot_setting_list


plot_setting_list = make_list(False)


# plot_setting_listに従ってプロット
for plot_setting in plot_setting_list:
    src_dir, src_filename, obj_dir, obj_filename, header, index_col, step_xticks, step_yticks, y_min, y_max, y_range = plot_setting
    mp = plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        y_min=y_min, y_max=y_max,
        y_range=y_range
    )
