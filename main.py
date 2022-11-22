import math
from vector import Vector
from standard_atmosphere import Atmosphere
from rk4 import *
from matplotlib import pyplot as plt
from drag import *
from constants import EARTH_RADIUS, g_earth


def calc_gravity(a):
    return g_earth * (EARTH_RADIUS / (EARTH_RADIUS+a))**2


if __name__=="__main__":

    # initial params
    dt           = 0.1 # [s]
    duration     = 200.0 # [s]

    position     = Vector(0, 0, EARTH_RADIUS)
    velocity     = Vector(0, 0, 8000)
    acceleration = Vector(0, 0, -g_earth)

    mass = 500 # kg
    rad = 0.1 # m
    cd = drag_coeff(math.radians(15))
    angle = 15
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
        altitude.append( position.magnitude() - EARTH_RADIUS )



    fig, ax = plt.subplots()
    fig.set_size_inches(10, 7)
    circle1 = plt.Circle((0, 0), EARTH_RADIUS, color='b', fill=False)
    ax.add_patch(circle1)

    plt.plot(x, y)
    plt.axis('equal')
    plt.show()
