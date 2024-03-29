from constants import g_earth
import numpy as np
from matplotlib import pyplot as plt
from name_equals_main import imported


def dist_from_accel_time(v, a, t):
    return v*t + 0.5*a*t**2

def vel_from_time(v, a, t):
    return v + a*t

def accel_from_vel_dist(v, d, v0):
    return (v**2 - v0**2) / (2*d)

def dist_from_accel_vel(a, v):
    return v**2 / (2*a)


if not imported(__name__):


    v = 3700 # target velocity

    gs = []
    dists = []

    for x in np.arange(500, 3000, 100):
        a = x * g_earth
        d = dist_from_accel_vel(a, v)
        gs.append(x)
        dists.append(d)

    f = plt.figure()
    f.set_figwidth(12)
    f.set_figheight(9)
    plt.plot(dists, gs)
    plt.ylabel("Acceleration (g)")
    plt.xlabel("Distance (m)")
    plt.title("Launch tube length given constant acceleration, 7 km muzzle velocity")
    plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
    plt.show()







    # get the average acceleration for a given delta-v (from zero) and total displacement
    # v = 7000
    # d = 1250
    # a = accel_from_vel_dist(v,d,0)
    # print(a/g_earth)
    # exit()



    # t = 0.1
    # v = 0
    # a = g_earth * 5000
    #
    # distances = []
    # velocities = []
    # times = []
    #
    # for t in np.arange(0.0001, 0.02, 0.0001):
    #
    #     dist = dist_from_accel_time(v, a, t)
    #     vel = vel_from_time(v, a, t)
    #
    #     times.append(t)
    #     distances.append(dist)
    #     velocities.append(vel)
    #
    # plt.plot(times, distances, label="Length of Launch Track")
    # plt.plot(times, velocities, label="Projectile Velocity")
    # plt.legend()
    # plt.ylabel("Meters")
    # plt.xlabel("Seconds")
    # plt.title("2000 g's")
    # plt.grid()
    # plt.show()
