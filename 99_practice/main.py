# --- Load GPyOpt
from GPyOpt.methods import BayesianOptimization
import numpy as np


# --- Define your problem
class MyClass():
    def __init__(self, a):
        self.a = a
        self.iteration = 0

    def say_hello(self):
        print(f"# I said hello {str(self.iteration).zfill(3)} times.")

    def f(self, x):
        self.iteration += 1
        self.say_hello()
        J = (6*x-self.a)**self.a*np.sin(12*x-4)
        return J


domain = [{'name': 'var_1', 'type': 'continuous', 'domain': (0, 1)}]

# --- Solve your problem
mc = MyClass(2)
myBopt = BayesianOptimization(f=mc.f, domain=domain)
myBopt.run_optimization(max_iter=15)


print(myBopt.x_opt)  # [0.75622342]
print(myBopt.fx_opt)  # -6.020180295391553
