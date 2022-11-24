import math
from math       import pi, sqrt
from earth      import Earth
from constants  import G_const, _u
from vector     import Vector




def keplerian_elements(p, v):

    ''' Converts orbital state vector to Keplerian elements. Returns apogee and perigee. '''

    GM = G_const * Earth.mass
    h = p.cross(v)
    e = v.cross(h)
    e.divide(GM)
    r = p.copy()
    r.divide(p.magnitude())
    e.subtract(r)
    # n = Vector(-h.y, h.x, 0)
    # if p.dot(v) >= 0:
    #     v_ = math.acos( e.dot(p) / (e.magnitude() * p.magnitude()) )
    # else:
    #     v_ = math.pi*2 - math.acos( e.dot(p) / (e.magnitude() * p.magnitude()) )
    eccentricity = e.magnitude()
    a = 1 / ( 2/p.magnitude() - (v.magnitude()**2)/GM )
    apogee = a * (1+eccentricity)
    perigee = a * (1-eccentricity)

    return apogee, perigee








class Orbit(object):

    def __init__(self, perigee, apogee):

        self.semi_major_axis       = Orbit.calc_semi_major_axis(apogee, perigee)
        self.perigee               = self.Apsis(min(apogee, perigee), self.semi_major_axis)
        self.apogee                = self.Apsis(max(apogee, perigee), self.semi_major_axis)




    class Apsis(object):

        def __init__(self, altitude, sMajAxis):

            self.altitude = altitude
            self.velocity = Orbit.calc_velocity(sMajAxis, self.altitude)


    @classmethod
    def calc_semi_major_axis(cls, apogee, perigee):
        ''' Calculates the semi-major axis given an apogee and perigee. '''

        return 0.5 * (perigee + apogee)


    @classmethod
    def calc_velocity(cls, sMajAxis, altitude):
        ''' Calculates the velocity at altitude in an elliptical orbit with a given semi-major axis. '''

        return sqrt( (G_const * Earth.mass) * (2.0 / altitude - 1/sMajAxis) )




if __name__ == '__main__':

    R_e = Earth.radius_equator

    orbit1 = Orbit(R_e + 500000, R_e + 200000 )

    print(orbit1.apogee.altitude-R_e, orbit1.apogee.velocity)
    print(orbit1.perigee.altitude-R_e, orbit1.perigee.velocity)

    pos = Vector(orbit1.apogee.altitude, 0, 0)
    vel = Vector(0, orbit1.apogee.velocity, 0)

    orbit2 = Orbit(*keplerian_elements(pos, vel))

    print(orbit2.apogee.altitude-R_e, orbit2.apogee.velocity)
    print(orbit2.perigee.altitude-R_e, orbit2.perigee.velocity)
