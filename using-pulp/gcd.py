import pulp

a = 3
b = 2

c = max(3, 2, 100)

prob = pulp.LpProblem("Dedication Model", pulp.LpMinimize)

X1 = pulp.LpVariable("X1", cat='Integer')
X2 = pulp.LpVariable("X2", cat='Integer')

prob += a * X1 + b * X2
prob += a * X1 + b * X2 >= 1

print('status', prob.solve())
print("Optimal total cost is: ", pulp.value(prob.objective))
print("X1 :", X1.varValue, "X2 :", X2.varValue)
