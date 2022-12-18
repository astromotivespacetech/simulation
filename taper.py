import math
from name_equals_main import imported
from conversions import inch2meter, psi2pascal, lbf2newton
from constants import g_earth, T_stp, atm, R_univ
from nozzle import Nozzle, Propellant
from idealgas import solve_n


R = R_univ # 8.314 J/mol K
g = g_earth # 9.80665 m/s^2



def transit_duration(velocity, length):
    return length/velocity

def taper_half_angle(len, rad):
    return math.atan(rad/len)




if not imported(__name__):

    Air = Propellant(28.97, 1.401, 343, 287)
    gas = Air
    Tc = 294 # K
    Pc = psi2pascal(2000)
    T = lbf2newton(1500)
    Pe = atm
    nozzle = Nozzle(gas, Tc, Pc, Pe, T)

    exhaust_velocity = nozzle.Ve # m/s

    rad = inch2meter(2) # m
    len = inch2meter(12) # m

    vel = 1000 # m/s

    dt = transit_duration(vel, len)
    vt = transit_duration(exhaust_velocity, rad)
    transit_flow = nozzle.Wdot * dt

    vol = nozzle.Ae * inch2meter(24)
    moles = solve_n(Pc, vol, Tc)
    mass = moles * nozzle.gas.mol * 0.001


    print("Projectile Velocity: %i m/s" % vel)
    print("Projectile Radius: %.4f m" % rad)
    print("Projectile Tail Length: %.4f m" % len)
    print("Taper Angle: %.2f deg" % math.degrees(taper_half_angle(len,rad)))
    print("Projectile Transit Duration: %.7f s" % dt)
    print("Exhaust Velocity: %i m/s" % exhaust_velocity)
    print("Exhaust Transit Time: %.7f s" % vt)
    print("Flow Rate: %.2f kg/s" % nozzle.Wdot)
    print("Transit Mass Flow: %.5f kg" % transit_flow)
    print("Nozzle Volume: %.5f cu.m" % vol)
    print("Moles: %.4f" % moles)
    print("Mass: %.4f kg" % mass)
