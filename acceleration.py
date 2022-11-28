from constants import g_earth
import numpy as np
from matplotlib import pyplot as plt



def dist_from_accel_time(v, a, t):
    return v*t + 0.5*a*t*t

def vel_from_time(v, a, t):
    return v + a*t


if __name__=="__main__":

    t = 0.1
    v = 0
    a = g_earth * 2000

    distances = []
    velocities = []
    times = []

    for t in np.arange(0.001, 0.05, 0.001):

        dist = dist_from_accel_time(v, a, t)
        vel = vel_from_time(v, a, t)

        times.append(t)
        distances.append(dist)
        velocities.append(vel)

    plt.plot(times, distances, label="Length of Launch Track")
    plt.plot(times, velocities, label="Projectile Velocity")
    plt.legend()
    plt.ylabel("Meters")
    plt.xlabel("Seconds")
    plt.title("1000 g's")
    plt.grid()
    plt.show()