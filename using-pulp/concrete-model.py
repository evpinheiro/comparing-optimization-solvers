from pulp import LpProblem, LpVariable, LpMinimize, value

prob = LpProblem("Dedication Model", LpMinimize)

X1 = LpVariable("X1", 0, None, cat='Integer')
X2 = LpVariable("X2", 0, None, cat='Integer')

prob += 2 * X1 - 3 * X2
prob += 30 * X1 - 45 * X2 >= 10

prob.solve()
print("Optimal total cost is: ", value(prob.objective))
print("X1 :", X1.varValue, "X2 :", X2.varValue)
