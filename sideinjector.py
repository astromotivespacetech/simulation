import math
from conversions import *
from name_equals_main import imported
from matplotlib import pyplot as plt
import numpy as np



def xarea(r):
    return math.pi * r**2

def accel_from_force_mass(f, m):
    return f/m

def vel_from_dist_accel(d, a):
    return math.sqrt(2 * a * d)



if not imported(__name__):

    radiusPiston = 1 # in
    radiusPlug = 0.75 # in
    xareaPiston = xarea(radiusPiston)
    xareaPlug = xarea(radiusPlug)
    pressure = 3000 # psi
    force = lbf2newton(pressure * xareaPiston) # N
    pistonMass = 1 # kg
    accel = accel_from_force_mass(force, pistonMass) # m/s2
    displacement = inch2meter(radiusPlug)

    dists = []
    vels = []
    acts = []

    for _ in np.arange(1.0, 10.0, 0.25):

        dist = inch2meter(_)
        velocity = vel_from_dist_accel(dist, accel) # m/s
        actuation = displacement / velocity

        dists.append(dist)
        vels.append(velocity)
        acts.append(actuation)

    fig, ax1 = plt.subplots()
    fig.set_size_inches(12, 7)
    ax2 = ax1.twinx()
    ax1.plot(dists, vels, label="Velocity", color='r')
    ax2.plot(dists, acts, label="Actuation Time")
    ax1.legend(loc=0)
    ax2.legend(loc=0)
    ax1.set_xlabel("Distance (m)")
    ax1.set_ylabel("Velocity (m/s)")
    ax2.set_ylabel("Time (s)")
    plt.title("3 ksi chamber, 1 kg piston mass, 1 in piston radius")
    plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
    plt.show()


    print("Pressure: %i psi" % pressure)
    print("Cross Sectional Area: %.2f sq.in" % xareaPiston)
    print("Force: %.2f N" % force)
    print("Acceleration: %.2f m/s^2" % accel)
    print("Velocity: %.2f m/s" % velocity)
    print("Actuation Displacement: %.2f in" % meter2inch(displacement))
    print("Actuation Time: %.4f s" % actuation)
