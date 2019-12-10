from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
import numpy as np


def linear_funtion(a,b, x_range):
    return a*x+b

fig = plt.figure()
#ax = plt.axes(projection="3d")
x = np.linspace(0,2,100)
plt.plot(x, linear_funtion(-1,1,x), label='linear')
plt.show()


