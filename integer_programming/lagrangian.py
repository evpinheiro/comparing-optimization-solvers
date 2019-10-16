#A = [[2, 1, 6, 5]]
#c = [10, 7, 25, 24]
#b = [7]

A = [[5, 4, 4], [9, 3, 5]]
b = [10, 11]
c = [4, 5, 7]


def lagrange_function(x, u):
    return objective_function(x) + inner_product(u, subgradient(x))


def subgradient(x):
    return [b[i] - inner_product(A[i], x) for i in range(len(b))]


def inner_product(vector1, vector2):
    product = 0
    for i, vi in enumerate(vector1):
        product = product + vi*vector2[i]
    return product


def objective_function(x):
    return inner_product(c, x)


def LR(u):
    best_x = [0, 0, 0, 0]
    for j, cj in enumerate(c):
        aux = 0
        for i in range(len(u)):
            aux = aux + u[i]*A[i][j]
        if cj - aux > 0:
            best_x[j] = 1
        #elif c()[i]-u*A()[i] == 0 and
    max_value = lagrange_function(best_x, u)
    return max_value, best_x


def subgradient_method(uk, mik = 0.1, pho=0.95, max_iterations=100):
    results_zk = []
    results_xuk = []
    k = 1
    while k < max_iterations:
        (zuk, xuk) = lr(uk)
        results_xuk.append(xuk)
        results_zk.append(zuk)
        dk = subgradient(xuk)
        uk = [uk[i] - mik*dk[i] for i in range(len(dk))]
        mik = pho*mik
        k = k + 1
        print(k, [round(uk[k],4) for k in range(len(uk))], round(zuk,4), dk, xuk, objective_function(xuk))


subgradient_method([0, 0])
