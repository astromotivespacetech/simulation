import math
from matplotlib import pyplot as plt
import numpy as np
from conversions import inch2meter


def accel_from_force_mass(f, m):
    return f/m

def vel_from_dist_accel(d, a):
    return math.sqrt(2 * a * d)



#
# m2 = 1
# v = 1
#
# v2 = []
# m = []
#
# for m1 in np.arange(1, 10, 0.1):
#
#     vf1 = (m1 - m2) * v / (m1 + m2)
#     vf2 = 2*m1*v / (m1 + m2)
#     m.append(m1)
#     v2.append(vf2)
#
#
# fig, ax1 = plt.subplots()
# fig.set_size_inches(12, 7)
#
# ax1.plot(m, v2, label="Velocity", color='r')
# plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
# plt.show()


m = []
v2 = []

mass_plug = 10 # kg

actuator_force = 15000 # N

dist = inch2meter(4)

for mass_piston in np.arange(1, mass_plug*2, 1):

    accel = actuator_force / mass_piston
    v = vel_from_dist_accel(dist, accel)

    vf1 = (mass_piston - mass_plug) * v / (mass_piston + mass_plug)
    vf2 = 2*mass_piston*v / (mass_piston + mass_plug)
    m.append(mass_piston)
    v2.append(vf2)


fig, ax1 = plt.subplots()
fig.set_size_inches(12, 7)

ax1.plot(m, v2, label="Velocity", color='r')
plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
plt.show()
