import os
# import plotter_70 as plotter
import plotter
import matplotlib.pyplot as plt


dirname = os.path.dirname(os.path.abspath(__file__))

J_log_csv = "J_log.csv"
J_log_png = "J_log.png"

large_step_xticks = 50


def execute(test=True):
    src_dir = os.path.join(dirname, "src")
    obj_dir = os.path.join(dirname, "obj")

    # > single
    tmp = "single"
    src_filename = tmp + ".csv"
    obj_filename = tmp + ".png"
    if test:
        obj_dir = obj_dir
    else:
        obj_dir = obj_dir

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None

    # step_*ticks
    step_xticks = 10
    step_yticks = 1.0

    # min_max
    y_min = -4
    y_max = 3

    plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        y_min=y_min, y_max=y_max,
        FIG_SIZE=(10, 5),
        legend=False,
        column_plotted=[0, 1, 2],
        y_label=r'$J_{\Large \textnormal{sp}}$, $J_{\Large \textnormal{total}}$',
        legend_list=[
                    r'$J_{\Large \textnormal{sp}}$',
                    r'$J_{\Large \textnormal{sim}}$',
                    r'$J_{\Large \textnormal{total}}$'
                ],
        dual_scale=False
    )

    # <

    # > single_with_header_index
    tmp = "single_with_header_index"
    src_filename = tmp + ".csv"
    obj_filename = tmp + ".png"
    if test:
        obj_dir = obj_dir
    else:
        obj_dir = obj_dir

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = 0
    index_col = 0

    # step_*ticks
    step_xticks = 10
    step_yticks = 200

    plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        FIG_SIZE=(10, 5),
        legend=False,
        column_plotted=[0, 1, 2],
        y_label=r'$J_{\Large \textnormal{sp}}$, $J_{\Large \textnormal{total}}$',
        legend_list=[
                    r'$J_{\Large \textnormal{sp}}$',
                    r'$J_{\Large \textnormal{sim}}$',
                    r'$J_{\Large \textnormal{total}}$'
                ],
        dual_scale=False
    )

    # <

    # > select_col
    tmp = "select_col"
    src_filename = tmp + ".csv"
    obj_filename = tmp + ".png"
    if test:
        obj_dir = obj_dir
    else:
        obj_dir = obj_dir

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = 0
    index_col = 0

    # step_*ticks
    step_xticks = 10
    step_yticks = 1.0

    # min_max
    y_min = -4
    y_max = 3

    plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        y_min=y_min, y_max=y_max,
        FIG_SIZE=(10, 5),
        legend=False,
        column_plotted=[0, 1, 2],
        y_label=r'$J_{\Large \textnormal{sp}}$, $J_{\Large \textnormal{total}}$',
        # legend_list=[
        #             r'$J_{\Large \textnormal{sp}}$',
        #             r'$J_{\Large \textnormal{sim}}$',
        #             r'$J_{\Large \textnormal{total}}$'
        #         ],
        dual_scale=False,
        multi_y=True
    )

    # <

    # > dual_scale
    tmp = "dual_scale"
    src_filename = tmp + ".csv"
    obj_filename = tmp + ".png"
    if test:
        obj_dir = obj_dir
    else:
        obj_dir = obj_dir

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None

    # step_*ticks
    step_xticks = 10
    step_yticks = 1.0

    # min_max
    y_min = -4
    y_max = 3

    plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        y_min=y_min, y_max=y_max,
        FIG_SIZE=(10, 5),
        legend=True,
        column_plotted=[0, 1, 2],
        y_label=r'$J_{\Large \textnormal{sp}}$, $J_{\Large \textnormal{total}}$',
        legend_list=[
                    r'$J_{\Large \textnormal{sp}}$',
                    r'$J_{\Large \textnormal{sim}}$',
                    r'$J_{\Large \textnormal{total}}$'
                ],
        dual_scale=True
    )

    # <

    src_dir = os.path.join(dirname, "20230129")
    obj_dir_test = os.path.join(dirname, "20230129_test")
    obj_dir = os.path.join(dirname, "20230129")

    y_max = 3
    y_min = 0

    # > bayes_d4_J_log
    tmp = "bayes_d4_J_log"
    src_filename = tmp + ".csv"
    obj_filename = tmp + ".png"
    if test:
        obj_dir = obj_dir_test
    else:
        obj_dir = obj_dir

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None

    # step_*ticks
    step_xticks = large_step_xticks
    step_yticks = 0.5

    # min_max
    y_min = y_min
    y_max = y_max

    plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        y_min=y_min, y_max=y_max,
        FIG_SIZE=(8, 5),
    )

    # <

    # > bayes_d8_J_log
    tmp = "bayes_d8_J_log"
    src_filename = tmp + ".csv"
    obj_filename = tmp + ".png"
    if test:
        obj_dir = obj_dir_test
    else:
        obj_dir = obj_dir

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None

    # step_*ticks
    step_xticks = large_step_xticks
    step_yticks = 0.5

    # min_max
    y_min = y_min
    y_max = y_max

    plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        y_min=y_min, y_max=y_max,
        FIG_SIZE=(8, 5),
    )

    # <

    # > cobyla_d4_J_log
    tmp = "cobyla_d4_J_log"
    src_filename = tmp + ".csv"
    obj_filename = tmp + ".png"
    if test:
        obj_dir = obj_dir_test
    else:
        obj_dir = obj_dir

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None

    # step_*ticks
    step_xticks = large_step_xticks
    step_yticks = 0.5

    # min_max
    y_min = y_min
    y_max = y_max

    plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        y_min=y_min, y_max=y_max,
        FIG_SIZE=(8, 5),
    )

    # <

    # > cobyla_d8_J_log
    tmp = "cobyla_d8_J_log"
    src_filename = tmp + ".csv"
    obj_filename = tmp + ".png"
    if test:
        obj_dir = obj_dir_test
    else:
        obj_dir = obj_dir

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None

    # step_*ticks
    step_xticks = large_step_xticks
    step_yticks = 0.5

    # min_max
    y_min = y_min
    y_max = y_max

    plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        y_min=y_min, y_max=y_max,
        FIG_SIZE=(8, 5),
    )

    # <

    # > cobyla_d4_J_log_50
    tmp = "cobyla_d4_J_log_50"
    src_filename = tmp + ".csv"
    obj_filename = tmp + ".png"
    if test:
        obj_dir = obj_dir_test
    else:
        obj_dir = obj_dir

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None

    # step_*ticks
    step_xticks = 10
    step_yticks = 0.5

    # min_max
    y_min = y_min
    y_max = y_max

    plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        y_min=y_min, y_max=y_max,
        FIG_SIZE=(8, 5),
    )

    # <

    # > cobyla_d8_J_log_50
    tmp = "cobyla_d8_J_log_50"
    src_filename = tmp + ".csv"
    obj_filename = tmp + ".png"
    if test:
        obj_dir = obj_dir_test
    else:
        obj_dir = obj_dir

    # ヘッダとインデックスのタイプ（該当の行・列がなければNoneとする）
    header = None
    index_col = None

    # step_*ticks
    step_xticks = 10
    step_yticks = 0.5

    # min_max
    y_min = y_min
    y_max = y_max

    plotter.MyPlotter(
        src_dir, src_filename, obj_dir, obj_filename,
        header, index_col, step_xticks, step_yticks,
        y_min=y_min, y_max=y_max,
        FIG_SIZE=(8, 5),
    )

    # <

    return


if __name__ == "__main__":
    execute(test=False)
    plt.close('all')
