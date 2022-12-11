from math import sqrt, pi
from constants import g_earth, T_stp, atm, R_univ
from conversions import *
from name_equals_main import imported
from matplotlib import pyplot as plt



class Propellant(object):
    def __init__(self, mol, gam, mach, r):
        self.mol = mol
        self.gam = gam
        self.mach = mach
        self.R = r

Helium = Propellant(4.0026, 1.667, 1020, 2077.1)
Air = Propellant(28.97, 1.401, 343, 287)


# choose monoprop gas
gas = Helium

R = R_univ # 8.314 J/mol K
g = g_earth # 9.80665 m/s^2


def throatTemp(Tc, gam):
    return Tc*(1/(1+(gam-1)/2))


def throatPress(Pc, gam):
    return Pc*(1+(gam-1)/2)**(-gam/(gam-1))


def calcCstar(gam, R, T):
    return sqrt(gam*R*T) / (gam * sqrt( (2/(gam+1))**((gam+1)/(gam-1)) ) )


def calcIsp(cs, gam, pe, pc):
    return (cs/g) * gam * sqrt((2/(gam-1))*(2/(gam+1))**((gam+1)/(gam-1))*(1-(pe/pc))**((gam-1)/gam))


def throatArea(Wdot, Pc, cs):
    return Wdot * cs * (1/Pc)


def mach(t, gam, r):
    return sqrt(gam * r * t)


def machNum(v, a):
    return v / a


def exitArea(At, Me, gam):
    return At/Me * ( (1+(gam-1)/2*Me**2)/((gam+1)/2) )**((gam+1)/(2*(gam-1)))


def pcns(Wdot, cs, At):
    return Wdot * cs * (1/(At))


def exitVelocity(gam, r, t, pe, pc):
    return sqrt( (2 * gam / (gam-1) ) * r * t * (1-(pe/pc)**((gam-1)/gam)) )


def exitTemp(tcns, pe, pcns, gam):
    return tcns * (pe / pcns)**((gam-1)/gam)


if not imported(__name__):

    arr_thrust = []
    arr_diameter = []

    for _ in range(100):


        Tc = 294 # K
        Pc = psi2pascal(2200)
        # T = lbf2newton( 2000 )
        T = lbf2newton( (_ * 100)+10000 )
        Pe = atm * 3 # exit pressure

        target = inch2meter(7)
        Ae = 0
        De = 0
        error = target - De
        deriv = 0
        egain = 100
        dgain = 1000
        gain = 100

        print( newton2lbf(T))


        while error > 0.0001 :

            Pe -= (error*egain + deriv*dgain) * gain

            Cstar = calcCstar(gas.gam, gas.R, Tc)
            isp = calcIsp(Cstar, gas.gam, Pe, Pc)
            Wdot = T / (isp * g)
            At = throatArea(Wdot, Pc, Cstar)
            Pcns = pcns(Wdot, Cstar, At)
            Ve = exitVelocity(gas.gam, gas.R, Tc, Pe, Pcns)
            Te = exitTemp(Tc, Pe, Pcns, gas.gam)
            ae = mach(Te, gas.gam, gas.R)
            Me = machNum(Ve, ae)
            Ae = exitArea(At, Me, gas.gam)
            Tt = throatTemp(Tc, gas.gam)
            Pt = throatPress(Pc, gas.gam)
            Dt = 2*sqrt(At/pi)
            De = 2*sqrt(Ae/pi)

            deriv = error - (target-De)
            error = target - De

            arr_thrust.append( newton2lbf(T) )
            arr_diameter.append( meter2inch(Dt) )


    plt.plot(arr_thrust, arr_diameter)
    plt.grid()
    plt.show()



    print("Chamber Temp: %.2f K" % Tc)
    print("Throat Temp: %.2f K" % Tt)
    print("Exit Temp: %.2f K" % Te)
    print("Chamber Pressure: %.2f psi" % pascal2psi(Pc))
    print("Throat Pressure: %.2f psi" % pascal2psi(Pt))
    print("Exit Pressure: %.2f psi" % pascal2psi(Pe))
    print("Cstar: %.2f m/s" % Cstar)
    print("Isp: %.2f s" % isp)
    print("Flow rate: %.2f kg/s" % Wdot)
    print("Throat Area: %.6f sq.m" % At)
    print("Throat Diameter: %.4f in" % meter2inch(Dt))
    print("Exit Velocity: %.2f m/s" % Ve)
    print("Exit Mach Number: %.2f" % Me)
    print("Speed of Sound at Exit: %.2f m/s" % (Ve/Me))
    print("Exit Area: %.6f sq.m" % Ae)
    print("Exit Diameter: %.4f in" % meter2inch(De))
    print("Area Ratio: %.2f" % (Ae/At))
