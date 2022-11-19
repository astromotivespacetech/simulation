import math
from vector import Vector
from standard_atmosphere import Atmosphere
from rk4 import *
from matplotlib import pyplot as plt
from drag import *


if __name__=="__main__":

    # initial params
    dt           = 0.1 # [ms]
    duration     = 100.0 # [s]

    position     = Vector(0, 0, 0)
    velocity     = Vector(0, 0, 7000)
    acceleration = Vector(0, 0, -9.8)

    mass = 100 # kg
    rad = 0.05 # m
    cd = drag_coeff(math.radians(15))
    launch_angle = math.radians(30) # up angle from horizontal
    axis = Vector(1,0,0)
    velocity.rotate(axis, -launch_angle)

    projectile = StateVector(position, velocity)


    elapsed = 0
    time = [elapsed]
    altitude = [projectile.vector[2].p]


    # numerical integration loop
    for x in range( int(duration/dt) ):

        # reinitialize acceleration each iteration
        acceleration = Vector(0, 0, -9.8)

        # get magnitude of velocity vector
        vel = velocity.magnitude()

        # get atmospheric density at current altitude
        rho = Atmosphere.calc_rho(altitude[x])

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
        altitude.append(pv[2].p)
        velocity.update([pv[0].v, pv[1].v, pv[2].v])



    plt.plot(time, altitude)
    plt.show()
