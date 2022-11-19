import math
from vector import Vector
from standard_atmosphere import Atmosphere
from rk4 import *



if __name__=="__main__":

    # initial params
    timestep     = 0.1 # [ms]
    duration     = 2.0 # [s]

    position     = Vector([0.0, 0.0, 0.0])
    velocity     = Vector([0.0, 0.0, 0.0])
    acceleration = Vector([0.0, 0.0, -9.8])


    projectile = StateVector(position, velocity)
    mass = 100 # kg
    launch_angle = math.radians(30)




    # numerical integration loop
    for x in range( int(duration/timestep) ):
        #
        # could implement a function to vary acceleration here
        #
        for s, a in zip(state.vector, acceleration.points):
            rk4(s, a, timestep)
