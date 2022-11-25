from math import sqrt, pi
from conversions import psi2pascal, pascal2psi, lbf2newton, newton2lbf

class Helium:
    mol = 4.0026 # g/mol
    gam = 1.667 # specific heat ratio
    mach = 1020 # m/s
    R = 2077.1 # J/kg K

R = 8.31453 # J/mol K
atm = 101325 # Pascals
g = 9.80665 # m/s^2

def throatTemp(Tc, gam):
    return Tc*(1/(1+(gam-1)/2))


def throatPress(Pc, gam):
    return Pc*(1+(gam-1)/2)**(-gam/(gam-1))


def calcCstar(gam, R, T):
    return sqrt(gam*R*T) / (gam * sqrt( (2/(gam+1))**((gam+1)/(gam-1)) ) )


def calcIsp(cs, gam, pe, pc):
    return (cs/g) * gam * sqrt((2/(gam-1))*(2/(gam+1))**((gam+1)/(gam-1))*(1-(pe/pc))**((gam-1)/gam))


def throatArea(Wt, Pt, Tt, gam):
    return Wt / Pt * sqrt((R*Tt)/gam)


Tc = 294
Pc = psi2pascal(1000)
Pe = atm * 0.1
T = lbf2newton(1000)

Tt = throatTemp(Tc, Helium.gam)
Pt = throatPress(Pc, Helium.gam)
Cstar = calcCstar(Helium.gam, Helium.R, Tc)
isp = calcIsp(Cstar, Helium.gam, Pe, Pc)

Wdot = T / (isp * g)
At = throatArea(Wdot, Pt, Tt, Helium.gam)
Dt = sqrt(4*At/pi)

print(Tt, Pt, Cstar, isp, Wdot, At, Dt)
