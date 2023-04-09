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
    pressure = 1000 # psi
    force = lbf2newton(pressure * xareaPiston) # N
    pistonMass = 1.48 # kg
    plugMass = 0.176 # kg
    accel = accel_from_force_mass(force, pistonMass) # m/s2
    displacement = inch2meter(radiusPlug) * 2

    dists = []
    vpiston = []
    vplug = []
    acts = []

    for _ in np.arange(1.0, 10.0, 0.25):

        dist = inch2meter(_)
        velocity = vel_from_dist_accel(dist, accel) # m/s
        vf1 = (pistonMass - plugMass) * velocity / (pistonMass + plugMass)
        vf2 = 2*pistonMass*velocity / (pistonMass + plugMass)

        dists.append(dist)
        vpiston.append(velocity)
        vplug.append(vf2)
        acts.append(displacement/vf2)

    fig, ax1 = plt.subplots()
    fig.set_size_inches(12, 7)
    ax2 = ax1.twinx()
    # ax3 = ax1.twinx()
    ax1.plot(dists, vpiston, label="Piston Velocity", color='r')
    ax2.plot(dists, acts, label="Actuation Time")
    ax1.plot(dists, vplug, label="Plug Velocity", color='g')
    ax1.legend(loc=0)
    ax2.legend(loc=0)
    # ax3.legend(loc=0)
    ax1.set_xlabel("Distance (m)")
    ax1.set_ylabel("Velocity (m/s)")
    ax2.set_ylabel("Time (s)")
    # ax3.set_ylabel("Velocity (m/s)")
    plt.title("1 ksi chamber, 1 kg piston mass, 1 in piston radius")
    plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
    plt.show()


    print("Pressure: %i psi" % pressure)
    print("Cross Sectional Area: %.2f sq.in" % xareaPiston)
    print("Force: %.2f N" % force)
    print("Acceleration: %.2f m/s^2" % accel)
    print("Velocity: %.2f m/s" % velocity)
    print("Actuation Displacement: %.2f in" % meter2inch(displacement))
    # print("Actuation Time: %.4f s" % actuation)
