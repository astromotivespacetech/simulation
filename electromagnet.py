from math import pi
from matplotlib import pyplot as plt



def circumference(d):
    return pi * d

def xarea(d):
    return pi * (d*0.5)**2

def num_turns(l, c):
    return l / c

def force(N, I, A, g):
    return (N * I)**2 * mu * A / (2 * g**2)


mu = 4 * pi * 1e-7
# mu = 0.000001256637061
gap = 0.088 # in
coil_diameter = 10 # in
len = 1136
coil_len = len * 12 # in
awg22 = 16.14 # ohms per 1000 ft
resistance = len / 1000 * awg22
I = 2 # amps

print(mu)
print(coil_len)
print(resistance)

forces = []
diameters = []

for i in range(100):
    diameter = 5 + i/10
    c = circumference(diameter)
    xa = xarea(diameter)
    n = num_turns(coil_len, c)
    F = force(n, I, xa, gap)

    diameters.append(diameter)
    forces.append(F)

fig, ax1 = plt.subplots()
fig.set_size_inches(12, 7)

ax1.plot(diameters, forces, label="Force", color='r')
plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
plt.show()
