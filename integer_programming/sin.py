#import matplotlib
import matplotlib.pyplot as plt
import math

axis_max = 10

axis1 = []
for x in range(0, 100*axis_max):
    if math.sin(0.05*x) >= 0:
        axis1.append(0.05*x)

y1 = [math.sin(x) for x in axis1]

axis2 = [(k+0.5)*math.pi for k in range(0, axis_max)]

y2 = [math.sin(x) for x in axis2]

y3 = [math.sin(x) for x in range(0, axis_max*10)]

print(axis2)

fig, ax = plt.subplots()

ax.plot(axis1, y1, "-", axis2, y2, "*", range(0, axis_max*10), y3, "+")

plt.show()
