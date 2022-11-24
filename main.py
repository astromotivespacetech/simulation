import math
from vector import Vector
from standard_atmosphere import Atmosphere
from rk4 import *
from matplotlib import pyplot as plt
from drag import *
from constants import EARTH_RADIUS, g_earth
import numpy as np
from orbit import Orbit, keplerian_elements



def calc_gravity(a):
    return g_earth * (EARTH_RADIUS / (EARTH_RADIUS+a))**2




def simulate_launch(angle):

    # start of new simulation
    position     = Vector(0, 0, EARTH_RADIUS)
    velocity     = Vector(0, 0, 7000)
    acceleration = Vector(0, 0, -g_earth)

    launch_angle = math.radians(90-angle) # up angle from horizontal
    axis = Vector(-1,0,0)
    velocity.rotate(axis, launch_angle)

    projectile = StateVector(position, velocity)

    elapsed = 0
    time = [elapsed]
    altitude = [position.magnitude() - EARTH_RADIUS]
    x = [projectile.vector[1].p]
    y = [projectile.vector[2].p]


    # numerical integration loop
    for i in range( int(duration/dt) ):

        # calculate acceleration due to gravity
        g = calc_gravity(altitude[i])

        # reinitialize acceleration each iteration
        acceleration = position.copy().unit()
        acceleration.scale(g)
        acceleration.inverse()

        # get magnitude of velocity vector
        vel = velocity.magnitude()

        # get atmospheric density at current altitude
        rho = Atmosphere.calc_rho(altitude[i])

        # calculate drag force
        force = calc_drag(cd, rad, rho, vel)

        # calculate acceleration from drag force and projectile mass
        accel = force / mass

        # copy velocity vector and normalize
        drag = velocity.copy().unit()

        # scale copy by acceleration from drag
        drag.scale(accel)

        # drag is in opposite direction of velocity vector
        drag.inverse()

        # add to acceleration
        acceleration.add(drag)

        for s, a in zip(projectile.vector, acceleration.data):
            rk4(s, a, dt)

        elapsed += dt
        time.append(elapsed)
        pv = projectile.vector
        x.append(pv[1].p)
        y.append(pv[2].p)
        position.update([pv[0].p, pv[1].p, pv[2].p])
        velocity.update([pv[0].v, pv[1].v, pv[2].v])
        alt = position.magnitude() - EARTH_RADIUS
        altitude.append(alt)

        if alt < altitude[i-1]:

            # angles.append(angle)
            # velocities.append(velocity.magnitude())
            # altitudes.append(alt)
            break

    return position, velocity




if __name__=="__main__":

    # initial params
    dt = 0.5 # [s]
    duration = 2000.0 # [s]
    mass = 1000 # kg
    rad = 0.1 # m
    cd = drag_coeff(math.radians(15))

    angle = 10
    pos, vel = simulate_launch(angle)

    orbit = Orbit(*keplerian_elements(pos, vel))
    orbit_circ = Orbit(orbit.apogee.altitude, orbit.apogee.altitude)

    print("VELOCITY: %.2f m/s" % vel.magnitude())
    print("ALTITUDE: %.2f m" % (pos.magnitude()-EARTH_RADIUS) )
    print("APOGEE: %.2f m" % (orbit.apogee.altitude - EARTH_RADIUS))
    print("PERIGEE: %.2f m" % (orbit.perigee.altitude - EARTH_RADIUS))
    print("CIRC VELOCITY: %.2f m/s" % (orbit_circ.apogee.velocity-orbit.apogee.velocity))




    # velocities = []
    # altitudes = []
    # angles = []
    #
    # for angle in np.arange(1, 15, 0.5):
    #     pos, vel = simulate_launch(angle)
    #     angles.append(angle)
    #     altitudes.append(pos.magnitude()-EARTH_RADIUS)
    #     velocities.append(vel.magnitude())
    #
    #
    # fig, ax1 = plt.subplots()
    # ax2 = ax1.twinx()
    # fig.set_size_inches(10, 7)
    # ax1.plot(angles,velocities, color='r')
    # ax2.plot(angles,altitudes, color='b')
    # ax2.ticklabel_format(useOffset=False,style='plain')
    # ax1.grid(color='#aaa', linestyle='-', linewidth=0.5)
    # ax2.grid(color='#f77', linestyle='-', linewidth=0.5)
    # plt.show()




    # fig, ax = plt.subplots()
    # fig.set_size_inches(10, 7)
    # circle1 = plt.Circle((0, 0), EARTH_RADIUS, color='b', fill=False)
    # ax.add_patch(circle1)
    #
    # plt.plot(x, y)
    # plt.axis('equal')
    # plt.show()
