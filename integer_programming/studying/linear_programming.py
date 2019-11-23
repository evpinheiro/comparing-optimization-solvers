import pyomo.environ as pyo


def create_model():
    model = pyo.AbstractModel()
    model.dual = pyo.Suffix(direction=pyo.Suffix.IMPORT)
    model.I = pyo.Set()
    model.J = pyo.Set()

    model.c = pyo.Param(model.J)
    model.A = pyo.Param(model.I, model.J)
    model.b = pyo.Param(model.I)

    model.x = pyo.Var(model.J, within=pyo.NonNegativeReals)

    def objective(model):
        return pyo.summation(model.c, model.x)

    model.obj = pyo.Objective(rule=objective, sense=pyo.maximize)

    def constraint_rule(model, i):
        return sum(model.A[i, j] * model.x[j] for j in model.J) <= model.b[i]

    model.constraint = pyo.Constraint(model.I, rule=constraint_rule)

    return model
