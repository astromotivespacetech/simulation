import math
from conversions import inch2meter, psi2pascal, lbf2newton


def xarea(r):
    return math.pi * r**2

def accel_from_force_mass(f, m):
    return f/m

def vel_from_dist_accel(d, a):
    return math.sqrt(2 * a * d)



if __name__=="__main__":

    radiusPiston = 1 # in
    radiusPlug = 0.75 # in
    xareaPiston = xarea(radiusPiston)
    xareaPlug = xarea(radiusPlug)
    pressure = 2000 # psi
    force = lbf2newton(pressure * (xareaPiston - xareaPlug)) # N
    pistonMass = 1 # kg
    accel = accel_from_force_mass(force, pistonMass) # m/s2
    dist = inch2meter(3.25)
    velocity = vel_from_dist_accel(dist, accel) # m/s
    displacement = inch2meter(1.25)
    actuation = displacement / velocity


    print("Pressure: %i psi" % pressure)
    print("Cross Sectional Area: %.2f sq.in" % (xareaPiston - xareaPlug))
    print("Force: %.2f N" % force)
    print("Acceleration: %.2f m/s^2" % accel)
    print("Velocity: %.2f m/s" % velocity)
    print("Actuation Displacement: %.2f m" % displacement)
    print("Actuation Time: %.4f s" % actuation)
