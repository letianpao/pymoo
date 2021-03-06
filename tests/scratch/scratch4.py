import autograd.numpy as anp
from pymoo.model.problem import Problem


class MyProblem(Problem):

    def __init__(self):
        super().__init__(n_var=2,
                         n_obj=2,
                         n_constr=2,
                         xl=anp.array([-2, -2]),
                         xu=anp.array([2, 2]))

    def _evaluate(self, x, out, *args, **kwargs):
        f1 = x[:, 0] ** 2 + x[:, 1] ** 2
        f2 = (x[:, 0] - 1) ** 2 + x[:, 1] ** 2

        g1 = 2 * (x[:, 0] - 0.1) * (x[:, 0] - 0.9) / 0.18
        g2 = - 20 * (x[:, 0] - 0.4) * (x[:, 0] - 0.6) / 4.8

        out["F"] = anp.column_stack([f1, f2])
        out["G"] = anp.column_stack([g1, g2])


from pymoo.algorithms.nsga2 import NSGA2
from pymoo.factory import get_sampling, get_crossover, get_mutation

algorithm = NSGA2(
    pop_size=40,
    n_offsprings=10,
    sampling=get_sampling("real_random"),
    crossover=get_crossover("real_sbx", prob=0.9, eta=15),
    mutation=get_mutation("real_pm", eta=20),
    eliminate_duplicates=True
)

from pymoo.optimize import minimize
from pymoo.factory import get_termination

problem = MyProblem()

res = minimize(problem,
               algorithm,
               ('n_gen', 40),
               seed=1,
               pf=problem.pareto_front(use_cache=False),
               save_history=True,
               verbose=True)


import numpy as np
from pymoo.factory import get_decision_making, get_reference_directions


weights = np.array([0.5, 0.5])
b, pseudo_weights = get_decision_making("pseudo-weights", weights).do(res.F, return_pseudo_weights=True)
print(b)




problem = MyProblem()

print(problem.pareto_front())
print(problem.pareto_set())

F, dF = problem.evaluate(anp.array([0.1, 0.2]), return_values_of=["F", "dF"])

ps = problem.pareto_set(use_cache=False, flatten=False)
pf = problem.pareto_front(use_cache=False, flatten=False)
print(ps)
print(pf)

# Make decision
weights = np.array([0.25, 0.25, 0.25, 0.25])
a, pseudo_weights = get_decision_making("pseudo-weights", weights).do(pf, return_pseudo_weights=True)

weights = np.array([0.4, 0.20, 0.15, 0.25])
b, pseudo_weights = get_decision_making("pseudo-weights", weights).do(F, return_pseudo_weights=True)

print(b)
