from math import sin, cos, pi, degrees, radians
from matplotlib import pyplot as plt

angles = []
forces = []

pressure = 2000 # psi
radius_piston = 3 # in
xarea_piston = pi * radius_piston**2 # sq.in
force_piston = pressure * xarea_piston
angle = radians(48.7)
force_sleeve = force_piston * cos(angle)
force_stop = force_piston * sin(angle)

print("Piston Force: %i lb" % force_piston)
print("Sleeve Force: %i lb" % force_sleeve)
print("Stop Force: %i lb" % force_stop)



for i in range(90):
    forces.append( force_sleeve * sin(radians(i)) )
    angles.append(i)



fig, ax1 = plt.subplots()
fig.set_size_inches(12, 7)
ax1.plot(angles, forces, label="s", color='r')
ax1.set_xlabel("angle (deg)")
ax1.set_ylabel("force (lbf)")
plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
plt.show()
