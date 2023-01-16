# Import Modules
# GPyOpt - Cases are important, for some reason
import GPyOpt
from GPyOpt.methods import BayesianOptimization

# numpy
import numpy as np
from numpy.random import multivariate_normal  # For later example

import pandas as pd

import os
from tqdm import tqdm

# Plotting tools
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
from numpy.random import multivariate_normal



dirname = os.path.dirname(os.path.abspath(__file__))

plot_func = False  # obj_funcのグラフ作成するか否か
maximize = True  # 最大化の練習かどうか


# Objective functionのクラス
class MyClass():
    def __init__(self, maximize=False):
        """_summary_

        Args:
            maximize (bool, optional): _description_. Defaults to False.
        """
        self.iteration = 0
        if maximize:
            self.func = self.obj_func_max
        else:
            self.func = self.obj_func_min
        self.mute = True

    def say_iteration(self):
        if self.mute:
            pass
        else:
            print(f"# Now {str(self.iteration).zfill(3)} times.")

    def obj_func_max(self, x):
        self.iteration += 1
        self.say_iteration()
        out = -x**4 - 2*x**3 + 12*x**2 + 2*x + 6
        return out

    def obj_func_min(self, x):
        self.iteration += 1
        self.say_iteration()
        out = x**4 + 2*x**3 - 12*x**2 - 2*x + 6
        return out

    def reset_iteration(self):
        print("# Reset the iteration.")
        self.iteration = 0


# インスタンス作成
mc = MyClass(maximize)


# > Plot the function
def plot_function():
    x = pd.Series(np.linspace(-5, 4, 1000))
    f_x = pd.Series.apply(x, mc.func)
    fig, ax = plt.subplots()
    ax.plot(x, f_x, 'b-')
    fig.savefig(os.path.join(dirname, "figs/obj_func.png"))
    mc.reset_iteration()


if plot_func:
    plot_function()
# <


def optimization(max_iter):
    # > Make the instance of Bopt
    domain = [{'name': 'var_1', 'type': 'continuous', 'domain': (-5, 4)}]
    myBopt_1d = BayesianOptimization(
        f=mc.func, domain=domain, maximize=maximize
    )
    myBopt_1d.run_optimization(max_iter=max_iter)
    # myBopt_1d.plot_acquisition()  # <------ This method doesn't work...
    # <

    ins = myBopt_1d.get_evaluations()[1].flatten()
    outs = myBopt_1d.get_evaluations()[0].flatten()
    evals = pd.DataFrame(ins, outs)
    print(evals.sort_index())

    total_iteration = len(ins)

    print("The minumum (or maximum) value obtained by the function was %.4f (x = %.4f)" % (myBopt_1d.fx_opt, myBopt_1d.x_opt))
    return myBopt_1d.fx_opt, myBopt_1d.x_opt, total_iteration


m = 10
n = 200
opt_list = []
for i in tqdm(range(n)):
    max_iter = m * (i + 1)
    f_opt, x_opt, total_iter = optimization(max_iter)
    x_opt = x_opt[0]
    opt_list.append([max_iter, f_opt, x_opt, total_iter])
    mc.reset_iteration()
print(opt_list)
col = ["max_iter", "f_opt", "x_opt", "total_iter"]
df = pd.DataFrame(opt_list, columns=col)
df.to_csv(os.path.join(dirname, "test_change_max_iter.csv"))
