import math
from math import pi, sqrt


# Acceleration due to gravity at Earth's surface [units: meter second**-2]
g_earth = 9.80665

# Gravitational Parameter [units: cubic meter per second squared ]
_u = 3.9860044e+14

# Universal gravitational constant
G_const = 6.67259e-11




class Vector(object):

    def __init__(self, *args):
        if len(args) == 0:
            self.data = [0,0,0]
        elif len(args) == 1:
            self.data = args[0]
        elif len(args) == 2:
            self.data = [args[0], args[1], 0]
        elif len(args) == 3:
            self.data = [args[0], args[1], args[2]]
        self.x      = self.data[0]
        self.y      = self.data[1]
        self.z      = self.data[2]


    def sum(self, vector):
        new = [x+y for x, y in zip(self.data, vector.data)]
        return Vector(new)


    def difference(self, vector):
        new = [x-y for x, y in zip(self.data, vector.data)]
        return Vector(new)


    def add(self, vector):
        for i, x in enumerate(vector.data):
            self.data[i] += x
        self.__init__(self.data)


    def subtract(self, vector):
        for i, x in enumerate(vector.data):
            self.data[i] -= x
        self.__init__(self.data)

    def mult(self, scalar):
        new = [x*scalar for x in self.data]
        return Vector(new)


    def scale(self, scalar):
        for x in range(len(self.data)):
            self.data[x] *= scalar
        self.__init__(self.data)


    def divide(self, scalar):
        for x in range(len(self.data)):
            self.data[x] /= scalar
        self.__init__(self.data)


    def dot(self, vector):
        new = sum([x*y for x, y in zip(self.data, vector.data)])
        return new



    def cross(self, vector):
        x = self.y * vector.z - self.z * vector.y
        y = self.z * vector.x - self.x * vector.z
        z = self.x * vector.y - self.y * vector.x
        return Vector(x,y,z)


    def copy(self):
        return Vector(self.data)


    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2 + self.z**2)


    def unit(self):
        m = self.magnitude()
        if m == 0:
            new = [0, 0, 0]
        else:
            new = [1/m * self.x, 1/m * self.y, 1/m * self.z]
        return Vector(new)


    def inverse(self):
        new = [-1 * x for x in self.data]
        self.__init__(new)


    def angle(self, vector):
        m1      = self.magnitude()
        m2      = vector.magnitude()
        dot     = self.dot(vector)

        if dot / (m1 * m2) > 1.0:
            n   = 1.0
        elif dot / (m1 * m2) < -1.0:
            n   = -1.0
        else:
            n   = dot / (m1 * m2)
        return math.acos(n)


    def rotate(self, axis, angle):
        vrot = self.mult(math.cos(angle))
        v2 = axis.cross(self)
        v2 = v2.mult(math.sin(angle))
        v3 = axis.mult(axis.dot(self))
        v3 = v3.mult(1 - math.cos(angle))
        vrot.add(v2)
        vrot.add(v3)
        self.__init__(vrot.data)



    def update(self, array):
        self.__init__(array)




class Earth(object):

    radius_equator          = 6378137  # meters (at equator)
    f                       = 1/298.257223563
    radius_poles            = radius_equator * (1-f)  # 6356752.314245179 meters (at poles)
    radius                  = 6371008 # mean radius
    omega                   = 7.2921159e-5 # angular velocity [radians/second]
    center                  = Vector([0,0,0])
    mass                    = 5.97237e+24 # [kg]
    e                       = math.sqrt((radius_equator**2-radius_poles**2)/radius_equator**2)
    e_prime                 = math.sqrt((radius_equator**2-radius_poles**2)/radius_poles**2)
    circumference           = 2 * math.pi * radius_equator
    day                     = 86164


    @classmethod
    def calc_gravity(cls, distance):
        ''' Given an altitude, returns force of gravity in m/s^2 '''

        return G_const * Earth.mass / distance ** 2




    @classmethod
    def get_cartesian(cls, lat, lon, alt):

        a       = Earth.radius_equator
        b       = Earth.radius_poles

        N       = a / math.sqrt(1 - Earth.e ** 2 * math.sin(math.radians(lat))**2)

        x       = (N + alt) * math.cos(math.radians(lat)) * math.cos(math.radians(lon))
        y       = (N + alt) * math.cos(math.radians(lat)) * math.sin(math.radians(lon))
        z       = ((b**2/a**2) * N + alt) * math.sin(math.radians(lat))

        v       = Vector([x, y, z])

        return v



    @classmethod
    def get_lat_lon(cls, vector):

        x       = vector.x
        y       = vector.y
        z       = vector.z

        a       = Earth.radius_equator
        b       = Earth.radius_poles
        p       = math.sqrt(x**2 + y**2)

        lon     = math.atan2(y,x)

        theta   = math.atan2((z*a),(p*b))

        num     = z + Earth.e_prime**2 * b * math.sin(theta)**3
        den     = p - Earth.e**2 * a * math.cos(theta)**3

        lat     = math.atan2(num,den)

        N       = a / math.sqrt(1 - Earth.e ** 2 * math.sin(lat)**2)

        h       = p / math.cos(lat) - N


        return lat, lon, h




    @classmethod
    def velocity_at_latitude(cls, lat):
        ''' Given a latitude in degrees, returns the tangential velocity at sea-level. '''

        return Earth.radius * Earth.omega * math.cos(math.radians(lat))



    @classmethod
    def surface_speed(cls, vector):

        x               = vector.x
        y               = vector.y
        radius          = math.sqrt(x**2 + y**2)

        circumference   = 2 * math.pi * radius
        speed           = circumference / Earth.day

        return speed



    @classmethod
    def radius_at_latitude(cls, lat):

        r1       = Earth.radius_equator
        r2       = Earth.radius_poles
        n        = (r1**2 * math.cos(lat))**2 + (r2**2 * math.sin(lat))**2
        d        = (r1 * math.cos(lat))**2 + (r2 * math.sin(lat))**2
        r        = math.sqrt(n/d)

        return r




r_e = Earth.radius_equator






class Orbit(object):

    def __init__(self, apogee, perigee):

        self.semi_major_axis       = Orbit.calc_semi_major_axis(apogee+r_e, perigee+r_e)
        self.perigee               = self.Apsis(min(apogee, perigee), self.semi_major_axis)
        self.apogee                = self.Apsis(max(apogee, perigee), self.semi_major_axis)




    class Apsis(object):

        def __init__(self, altitude, sMajAxis):

            self.altitude = altitude
            self.dist = altitude+r_e
            self.velocity = Orbit.calc_velocity(sMajAxis, self.dist)


    @classmethod
    def calc_semi_major_axis(cls, apogee, perigee):
        ''' Calculates the semi-major axis given an apogee and perigee. '''

        return 0.5 * (perigee + apogee)


    @classmethod
    def calc_velocity(cls, sMajAxis, altitude):
        ''' Calculates the velocity at altitude in an elliptical orbit with a given semi-major axis. '''

        return sqrt( (G_const * Earth.mass) * (2.0 / altitude - 1/sMajAxis) )




def keplerian_elements(p, v):

    ''' Converts orbital state vector to Keplerian elements. Returns instance of Orbit object. '''

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

    return Orbit(apogee-r_e, perigee-r_e)

    



def calc_hohmann_dv(init, final):
    ''' Computes the delta-v required to transfer from one circular orbit to
        another circular orbit in the same orbital plane. A new Orbit instance is
        created for the elliptical transfer orbit, using the apogees of the two
        circular orbits given. The required delta-v is the sum of the two burns
        that place the rocket in the elliptical transfer orbit, and the circularize
        the orbit.

        Args:
            init: can be either the initial circular altitude, or an Orbit instance
            final: can be either the final circular altitude, or an Orbit instance

        Returns:
            required change in velocity [m/s].
    '''


    init_orbit      = init  if isinstance(init, Orbit)  else Orbit(init, init)
    final_orbit     = final if isinstance(final, Orbit) else Orbit(final, final)
    transfer_orbit  = Orbit(min(init_orbit.apogee.altitude, final_orbit.apogee.altitude), max(init_orbit.apogee.altitude, final_orbit.apogee.altitude))

    if final_orbit.apogee.altitude > init_orbit.apogee.altitude:
        burn_1      = transfer_orbit.perigee.velocity - init_orbit.perigee.velocity
        burn_2      = final_orbit.apogee.velocity - transfer_orbit.apogee.velocity
    else:
        burn_1      = transfer_orbit.apogee.velocity - init_orbit.apogee.velocity
        burn_2      = final_orbit.perigee.velocity - transfer_orbit.perigee.velocity
    dv              = burn_1 + burn_2

    return abs(dv), burn_1, burn_2



if __name__ == '__main__':

    # apogee = 500000 # in meters
    # perigee = 200000
    #
    # orbit1 = Orbit(apogee, perigee)
    #
    # print(orbit1.apogee.altitude, orbit1.apogee.velocity)
    # print(orbit1.perigee.altitude, orbit1.perigee.velocity)
    #
    # pos = Vector(orbit1.apogee.dist, 0, 0)
    # vel = Vector(0, orbit1.apogee.velocity, 0)
    #
    # orbit2 = keplerian_elements(pos, vel)
    #
    # print(orbit2.apogee.altitude, orbit2.apogee.velocity)
    # print(orbit2.perigee.altitude, orbit2.perigee.velocity)

    orb1 = Orbit(500000, 500000)
    orb2 = Orbit(500000, 150000)
    hohmann_transfer = calc_hohmann_dv(orb1, orb2)

    print("Orbit 1 Apogee Altitude: %d m" % orb1.apogee.altitude)
    print("Orbit 1 Apogee Velocity: %d m/s" % orb1.apogee.velocity)
    print("Orbit 1 Perigee Altitude: %d m" % orb1.perigee.altitude)
    print("Orbit 1 Perigee Velocity: %d m/s" % orb1.perigee.velocity)
    print("--")
    print("Orbit 2 Apogee Altitude: %d m" % orb2.apogee.altitude)
    print("Orbit 2 Apogee Velocity: %d m/s" % orb2.apogee.velocity)
    print("Orbit 2 Perigee Altitude: %d m" % orb2.perigee.altitude)
    print("Orbit 2 Perigee Velocity: %d m/s" % orb2.perigee.velocity)
    print("--")
    print("Hohmann Transfer Burn 1: %d m/s" % hohmann_transfer[1])
    print("Hohmann Transfer Burn 2: %d m/s" % hohmann_transfer[2])
    print("Hohmann Transfer Total DV: %d m/s" % hohmann_transfer[0])
