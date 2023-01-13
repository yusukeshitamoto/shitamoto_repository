# --- Load GPyOpt
from GPyOpt.methods import BayesianOptimization
import numpy as np


# --- Define your problem
def f(x): return (6*x-2)**2*np.sin(12*x-4)
domain = [{'name': 'var_1', 'type': 'continuous', 'domain': (0,1)}]

# --- Solve your problem
myBopt = BayesianOptimization(f=f, domain=domain)
myBopt.run_optimization(max_iter=15)


print(myBopt.x_opt)  #[ 2.05769988]
print(myBopt.fx_opt)  #[-0.79271554]


# myBopt.plot_acquisition()
