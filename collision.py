from matplotlib import pyplot as plt
import numpy as np


m2 = 1
v = 1

v2 = []
m = []

for m1 in np.arange(1, 100, 1):

    vf1 = (m1 - m2) * v / (m1 + m2)
    vf2 = 2*m1*v / (m1 + m2)
    m.append(m1)
    v2.append(vf2)


fig, ax1 = plt.subplots()
fig.set_size_inches(12, 7)

ax1.plot(m, v2, label="Velocity", color='r')
plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
plt.show()
