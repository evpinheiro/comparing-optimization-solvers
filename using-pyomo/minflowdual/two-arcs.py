#abstract1.py
from pyomo.environ import *

def abstract_model():
    model = AbstractModel()

    model.Nodes = Set()
    model.Arcs = Set()

    model.a = Param(model.Nodes, model.Arcs)
    model.b = Param(model.Nodes)
    model.c = Param(model.Arcs)

    model.dual = Suffix(direction=Suffix.IMPORT)

    # the next line declares a variable indexed by the set J
    model.x = Var(model.Arcs, within=NonNegativeReals)

    def obj_expression(model):
        return summation(model.c, model.x)

    model.OBJ = Objective(rule=obj_expression, sense=minimize)

    def flow_constraint_rule(model, i):
        # return the expression for the constraint for i
        return sum(model.a[i,j] * model.x[j] for j in model.Arcs) == model.b[i]

    # the next line creates one constraint for each member of the set model.I
    model.flowConstraint = Constraint(model.Nodes, rule=flow_constraint_rule)

    def capacity_constraint_rule(model, j):
        return model.x[j] <= model.c[j]

    model.capacityConstraint = Constraint(model.Arcs, rule=capacity_constraint_rule)

    return model

m = abstract_model()
instance = m.create_instance('/home/eder/workspace/comparing-optimization-solvers/using-pyomo/minflowdual/two-arcs.dat')
opt = SolverFactory('cbc')
opt.solve(instance)
instance.dual.display()
instance.dual.pprint()
instance.display()
instance.pprint()



