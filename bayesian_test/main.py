import GPy
import GPyOpt
import numpy as np 

def f(x):
    '''
    今回最適化する非線形関数
    '''
    return np.cos(1.5*x) + 0.1*x

bounds = [{'name': 'x', 'type': 'continuous', 'domain': (0,10)}]
myBopt = GPyOpt.methods.BayesianOptimization(f=f, domain=bounds,initial_design_numdata=5,acquisition_type='LCB')

myBopt.run_optimization(max_iter=15)

print(myBopt.x_opt) #[ 2.05769988]
print(myBopt.fx_opt) #[-0.79271554]
