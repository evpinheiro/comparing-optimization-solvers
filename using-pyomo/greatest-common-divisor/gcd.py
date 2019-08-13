import pyomo.environ as pe
from pyomo.opt import SolverFactory

b = 3
a = 127


model = pe.ConcreteModel()

bound = max(3,127)
model.x = pe.Var(domain=pe.Integers, bounds=(-bound,bound))
model.y = pe.Var(domain=pe.Integers, bounds=(-bound,bound))



def obj_rule(model):
    return a*model.x + b*model.y

model.OBJ = pe.Objective(rule=obj_rule, sense=pe.minimize)

def const_rule(model):
    return a*model.x + b*model.y >= 1

model.higherone = pe.Constraint(rule=const_rule)

opt = SolverFactory('cbc')
opt.solve(model)

print("x", model.x.value)
print("y", model.y.value)

model.display()
model.pprint()
