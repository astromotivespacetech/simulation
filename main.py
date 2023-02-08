import math
from vector import Vector
from standard_atmosphere import Atmosphere
from earth import Earth
from rk4 import *
from matplotlib import pyplot as plt
from drag import *
from constants import EARTH_RADIUS, g_earth
import numpy as np
from orbit import Orbit, keplerian_elements
from dv import *
import simplekml


def calc_gravity(a):
    return g_earth * (EARTH_RADIUS / (EARTH_RADIUS+a))**2



def simulate_launch(angle):


    # start of new simulation
    position     = Vector(0, 0, EARTH_RADIUS)
    velocity     = Vector(0, 0, 7000)
    acceleration = Vector(0, 0, -g_earth)

    kml = simplekml.Kml()
    trajectory = kml.newlinestring(name="Trajectory")
    trajectory.altitudemode = simplekml.AltitudeMode.relativetoground

    launch_angle = math.radians(90-angle) # up angle from horizontal
    axis = Vector(-1,0,0)
    velocity.rotate(axis, launch_angle)

    projectile = StateVector(position, velocity)

    elapsed = 0
    time = []
    altitude = []
    x = [projectile.vector[1].p]
    y = [projectile.vector[2].p]

    dragforce = []
    velocities = []


    # numerical integration loop
    for i in range( int(duration/dt) ):

        try:
            alt = altitude[i]
        except:
            alt = position.magnitude() - EARTH_RADIUS

        # calculate acceleration due to gravity
        g = calc_gravity(alt)

        # reinitialize acceleration each iteration
        acceleration = position.copy().unit()
        acceleration.scale(g)
        acceleration.inverse()

        # get magnitude of velocity vector
        vel = velocity.magnitude()

        # get atmospheric density at current altitude
        rho = Atmosphere.calc_rho(alt)

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
        dragforce.append(force)
        velocities.append(velocity.magnitude())
        lat, lon, a = Earth.get_lat_lon(position)
        trajectory.coords.addcoordinates([(math.degrees(lon),math.degrees(lat),round(a))])


        if alt < altitude[i-1]:
            print(alt, altitude[i-1])

            # angles.append(angle)
            # velocities.append(velocity.magnitude())
            # altitudes.append(alt)
            break


    #plot_telemetry(time, velocities, altitude, dragforce)
    kml.save("trajectory.kml")

    return x, y, position, velocity, trajectory




def align_yaxis(a1, v1, a2, v2):
    """adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
    _, y1 = a1.transData.transform((0, v1))
    _, y2 = a2.transData.transform((0, v2))
    adjust_yaxis(a2,(y1-y2)/2,v2)
    adjust_yaxis(a1,(y2-y1)/2,v1)

def adjust_yaxis(ax,ydif,v):
    """shift axis ax by ydiff, maintaining point v at the same location"""
    inv = ax.transData.inverted()
    _, dy = inv.transform((0, 0)) - inv.transform((0, ydif))
    miny, maxy = ax.get_ylim()
    miny, maxy = miny - v, maxy - v
    if -miny>maxy or (-miny==maxy and dy > 0):
        nminy = miny
        nmaxy = miny*(maxy+dy)/(miny+dy)
    else:
        nmaxy = maxy
        nminy = maxy*(miny+dy)/(maxy+dy)
    ax.set_ylim(nminy+v, nmaxy+v)



def plot_telemetry(time, velocities, altitude, dragforce):

    fig, ax1 = plt.subplots()
    fig.subplots_adjust(right=0.75)

    fig.set_size_inches(15, 8)
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    ax3.spines["right"].set_position(("axes", 1.2))
    ax1.plot(time, velocities, label="Velocity", color='b')
    ax2.plot(time, altitude, label="Altitude", color='g')
    ax3.plot(time, dragforce, label="Drag Force", color='r')

    ax1.set_ylim([6000, 7000])
    # ax2.set_ylim([0, 350000])

    ax1.set_ylabel("Velocity (m/s)")
    ax2.set_ylabel("Altitude (m")
    ax3.set_ylabel("Drag Force (N)")

    # ax1.legend(loc='upper left')
    # ax2.legend(loc='upper center')
    # ax3.legend(loc='upper right')

    align_yaxis(ax2, 0, ax3, 0)

    ax1.set_xlabel("Time (s)")
    fig.legend(loc=2)
# fig.subplots_adjust(right=0.75)
    plt.grid(color='#bbb', linestyle='-', linewidth=0.5)

    plt.show()







if __name__=="__main__":

    # initial params
    dt = 0.5 # [s]
    duration = 2000.0 # [s]
    mass = 1000 # kg
    rad = 0.1 # m
    cd = drag_coeff(math.radians(15))

    angle = 12


    x, y, pos, vel, trajectory = simulate_launch(angle)




    orbit = Orbit(*keplerian_elements(pos, vel))
    orbit_circ = Orbit(orbit.apogee.altitude, orbit.apogee.altitude)
    dv = orbit_circ.apogee.velocity-orbit.apogee.velocity
    isp = 250
    mf = calc_mf(mass, dv, isp)


    # print("VELOCITY: %.2f m/s" % vel.magnitude())
    # print("ALTITUDE: %.2f m" % (pos.magnitude()-EARTH_RADIUS) )
    # print("APOGEE: %.2f m" % (orbit.apogee.altitude - EARTH_RADIUS))
    # print("PERIGEE: %.2f m" % (orbit.perigee.altitude - EARTH_RADIUS))
    # print("CIRC VELOCITY: %.2f m/s" % dv)
    # print("PROP MASS: %.2f kg" % (mass-mf))
    # print("DRY MASS: %.2f kg" % mf)
    # print("MASS RATIO: %.2f" % (mass/mf))





    # velocities = []
    # altitudes = []
    # angles = []
    #
    # for angle in np.arange(1, 15, 0.5):
    #     x, y, pos, vel = simulate_launch(angle)
    #     angles.append(angle)
    #     altitudes.append(pos.magnitude()-EARTH_RADIUS)
    #     velocities.append(vel.magnitude())


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
