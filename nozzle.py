from math import sqrt, pi
from constants import g_earth, T_stp, atm_1, R_univ
from conversions import *


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
atm = atm_1 # 101325 # Pascals
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


def exitMachNum(Pc, gam):
    return sqrt( (2/(gam-1)) * ((Pc/atm)**((gam-1)/gam) - 1) )


def exitArea(At, Me, gam):
    return At/Me * ( (1+(gam-1)/2*Me**2)/((gam+1)/2) )**((gam+1)/(2*(gam-1)))


def pcns(Wdot, cs, At):
    return Wdot * cs * (1/(At))


def exitVelocity(gam, r, t, pe, pc):
    return sqrt( (2 * gam / (gam-1) ) * r * 1000 * t * (1-(pe/pc)**((gam-1)/gam)) )



Tc = 294 # K
Pc = psi2pascal(2000)
Pe = atm
T = lbf2newton(1500)

Tt = throatTemp(Tc, gas.gam)
Pt = throatPress(Pc, gas.gam)
Cstar = calcCstar(gas.gam, gas.R, Tc)
isp = calcIsp(Cstar, gas.gam, Pe, Pc)

Wdot = T / (isp * g)
At = throatArea(Wdot, Pc, Cstar)
Dt = 2*sqrt(At/pi)
Me = exitMachNum(Pc, gas.gam)
Ae = exitArea(At, Me, gas.gam)
De = 2*sqrt(Ae/pi)
Pcns = pcns(Wdot, Cstar, At)
Ve = exitVelocity(gas.gam, R, Tc, Pe, Pcns)

print("Chamber Temp: %.2f K" % Tc)
print("Throat Temp: %.2f K" % Tt)
print("Chamber Pressure: %.2f psi" % pascal2psi(Pc))
print("Throat Pressure: %.2f psi" % pascal2psi(Pt))
print("Cstar: %.2f m/s" % Cstar)
print("Isp: %.2f s" % isp)
print("Flow rate: %.2f kg/s" % Wdot)
print("Throat Area: %.6f sq.m" % At)
print("Throat Diameter: %.4f m" % Dt)
print("Exit Velocity: %.2f m/s" % Ve)
print("Exit Mach Number: %.2f" % Me)
print("Speed of Sound at Exit: %.2f m/s" % (Ve/Me))
print("Exit Area: %.6f sq.m" % Ae)
print("Exit Diameter: %.4f m" % De)
print("Area Ratio: %.2f" % (Ae/At))
