from mpl_toolkits.mplot3d import Axes3D
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pulp
import sys

def plot_by_value(inclination):
    c1 = 2
    c2 = -3
    a11 = 3
    a12 = -inclination
    b1 = 1


    axis=range(0,20)
    comb = pulp.combination(axis,2)

    xy = []
    for c in comb:
    #    print(type(c))
        xy.append(c)  
        xy.append((c[1],c[0]))

    for i in axis:
        xy.append((i,i))

    def constraint_left_hand(index):
         return a11*xy[index][0] + a12*xy[index][1]

    constraint = []
    objective = []
    for index in range(0,len(xy)):
        if constraint_left_hand(index) >= b1:
            constraint.append(xy[index])
            objective.append(c1*xy[index][0] + c2*xy[index][1])

    opt_index = -1
    opt_min = sys.maxsize
    for index, value in enumerate(objective):
        if value < opt_min:
            opt_index = index 
            opt_min = value

        

    print(xy)
    #print(constraint)
    #print(objective)
    #print(constraint[opt_index], objective[opt_index], constraint_left_hand(opt_index))

    #fig, ax = plt.subplots()
    fig = plt.figure()
    ax = Axes3D(fig)

    xt = [x[0] for x in xy]
    yt = [y[1] for y in xy]

    xf = [c[0] for c in constraint]
    yf = [c[1] for c in constraint]

    #ax.plot(xt, yt, "+",xf,yf, "*")

    z = objective

    ax.plot(xs=xf, ys=yf, zs=z, marker="*", zdir='z', label='ys=0')
    xLabel = ax.set_xlabel('x1', linespacing=3.2)
    yLabel = ax.set_ylabel('x2', linespacing=3.1)
    zLabel = ax.set_zlabel('z', linespacing=3.4)

    #plt.show()


plot_by_value(4)
