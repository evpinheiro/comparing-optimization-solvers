def lagrange_function(x, u, c, A, b):
    return objective_function(c, x) + inner_product(u, subgradient(x, A, b))


def subgradient(x, A, b):
    return [b[i] - inner_product(A[i], x) for i in range(len(b))]


def inner_product(vector1, vector2):
    product = 0
    for i, vi in enumerate(vector1):
        product = product + vi * vector2[i]
    return product


def objective_function(c, x):
    return inner_product(c, x)


def LR(u, c, A, b):
    best_x = [0 for i in range(len(c))]
    for j, cj in enumerate(c):
        aux = 0
        for i in range(len(u)):
            aux = aux + u[i] * A[i][j]
        if cj - aux > 0:
            best_x[j] = 1
    max_value = lagrange_function(best_x, u, c, A, b)
    return max_value, best_x


def subgradient_method(c, A, b, u0, mi0=0.1, pho=0.95, max_iterations=100):
    results_zk = []
    results_xuk = []
    k = 1
    while k < max_iterations:
        (zuk, xuk) = LR(u0, c, A, b)
        results_xuk.append(xuk)
        results_zk.append(zuk)
        dk = subgradient(xuk, A, b)
        u0 = [u0[i] - mi0 * dk[i] for i in range(len(dk))]
        mi0 = pho * mi0
        print(k, [round(u0[k], 4) for k in range(len(u0))], round(zuk, 4), dk, xuk, objective_function(c, xuk))
        k = k + 1


subgradient_method(c=[10, 4, 14], A=[[3, 1, 4]], b=[4], u0=[0], max_iterations=200)
