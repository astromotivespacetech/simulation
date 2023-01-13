import math
from name_equals_main import imported
from conversions import *
from constants import g_earth, T_stp, atm, R_univ
from nozzle import Nozzle, Propellant
from idealgas import solve_n
import numpy as np
from matplotlib import pyplot as plt

R = R_univ # 8.314 J/mol K
g = g_earth # 9.80665 m/s^2



def transit_duration(velocity, length):
    return length/velocity

def taper_half_angle(len, rad):
    return math.atan(rad/len)




if not imported(__name__):

    Air = Propellant(28.97, 1.401, 343, 287)
    Helium = Propellant(4.0026, 1.667, 1020, 2077.1)

    gas = Air
    Tc = 294 # K
    Pc = psi2pascal(2000)
    T = lbf2newton(1500)
    Pe = atm
    nozzle = Nozzle(gas, Tc, Pc, Pe, T)

    exhaust_velocity = nozzle.Ve # m/s

    # rad = inch2meter(1) # m
    # len = inch2meter(2) # m

    rad = 1
    len = 1

    vel = 7000 # m/s

    dt = transit_duration(vel, len)
    vt = transit_duration(exhaust_velocity, rad)
    transit_flow = nozzle.Wdot * dt

    vol = nozzle.Ae * inch2meter(24)
    moles = solve_n(Pc, vol, Tc)
    mass = moles * nozzle.gas.mol * 0.001

    lens = []
    lds = []
    angles = []
    dts = []
    vts = []
    vels = []



    for _ in np.arange(1, 20, 0.5):
        len = _
        vel = len/vt
        dt = transit_duration(vel, len)
        angles.append( math.degrees(taper_half_angle(len,rad)) )
        lds.append(len/rad)
        lens.append(len)
        dts.append(dt)
        vts.append(vt)
        vels.append(vel)



    f = plt.figure()
    f.set_figwidth(12)
    f.set_figheight(9)
    plt.plot(vels, angles, label="Velocity")
    plt.xticks(np.arange(0, 35000, 2500))
    plt.yticks(np.arange(0, 46, 1))
    # plt.plot(vts, angles, label="Transit Duration")
    # plt.plot(dts, angles, label="Firing Duration")
    plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
    plt.legend()
    plt.ylabel("Taper half-angle (deg)")
    plt.xlabel("Velocity (m/s)")
    plt.title("Exhaust Velocity " + str(round(exhaust_velocity, 0)) + " m/s, Projectile Rad 1 m")
    plt.show()





    print("Chamber Temp: %.2f K" % nozzle.Tc)
    print("Throat Temp: %.2f K" % nozzle.Tt)
    print("Exit Temp: %.2f K" % nozzle.Te)
    print("Chamber Pressure: %.2f psi" % pascal2psi(nozzle.Pc))
    print("Throat Pressure: %.2f psi" % pascal2psi(nozzle.Pt))
    print("Exit Pressure: %.2f psi" % pascal2psi(nozzle.Pe))
    print("Cstar: %.2f m/s" % nozzle.Cstar)
    print("Isp: %.2f s" % nozzle.isp)
    print("Flow rate: %.2f kg/s" % nozzle.Wdot)
    print("Throat Area: %.6f sq.m" % nozzle.At)
    print("Throat Diameter: %.4f in" % meter2inch(nozzle.Dt))
    print("Exit Velocity: %.2f m/s" % nozzle.Ve)
    print("Exit Mach Number: %.2f" % nozzle.Me)
    print("Speed of Sound at Exit: %.2f m/s" % (nozzle.Ve/nozzle.Me))
    print("Exit Area: %.6f sq.m" % nozzle.Ae)
    print("Exit Diameter: %.4f in" % meter2inch(nozzle.De))
    print("Area Ratio: %.2f" % (nozzle.Ae/nozzle.At))

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
