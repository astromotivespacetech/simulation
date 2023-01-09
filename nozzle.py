from math import sqrt, pi
from constants import g_earth, T_stp, atm, R_univ
from conversions import *
from name_equals_main import imported
from matplotlib import pyplot as plt
import numpy as np

R = R_univ # 8.314 J/mol K
g = g_earth # 9.80665 m/s^2



class Propellant(object):
    def __init__(self, mol, gam, mach, r):
        self.mol = mol
        self.gam = gam
        self.mach = mach
        self.R = r

Hydrogen = Propellant(2.01, 1.405, 1320, 4124)
Helium = Propellant(4.0026, 1.667, 1020, 2077.1)
Air = Propellant(28.97, 1.401, 343, 287)




class Nozzle(object):

    def __init__(self, gas, Tc, Pc, Pe, T):
        self.gas = gas
        self.Tc = Tc
        self.Pc = Pc
        self.Pe = Pe
        self.T = T
        self.Cstar = self.calcCstar(gas.gam, gas.R, Tc)
        self.isp = self.calcIsp(self.Cstar, gas.gam, Pe, Pc)
        self.Wdot = T / (self.isp * g)
        self.At = self.throatArea(self.Wdot, Pc, self.Cstar)
        self.Pcns = self.pcns(self.Wdot, self.Cstar, self.At)
        self.Ve = self.exitVelocity(gas.gam, gas.R, self.Tc, Pe, self.Pcns)
        self.Te = self.exitTemp(Tc, Pe, self.Pcns, gas.gam)
        self.ae = self.mach(self.Te, gas.gam, gas.R)
        self.Me = self.machNum(self.Ve, self.ae)
        self.Ae = self.exitArea(self.At, self.Me, gas.gam)
        self.Tt = self.throatTemp(self.Tc, gas.gam)
        self.Pt = self.throatPress(Pc, gas.gam)
        self.Dt = 2*sqrt(self.At/pi)
        self.De = 2*sqrt(self.Ae/pi)


    def throatTemp(self, Tc, gam):
        return Tc*(1/(1+(gam-1)/2))


    def throatPress(self, Pc, gam):
        return Pc*(1+(gam-1)/2)**(-gam/(gam-1))


    def calcCstar(self, gam, R, T):
        return sqrt(gam*R*T) / (gam * sqrt( (2/(gam+1))**((gam+1)/(gam-1)) ) )


    def calcIsp(self, cs, gam, pe, pc):
        return (cs/g) * gam * sqrt((2/(gam-1))*(2/(gam+1))**((gam+1)/(gam-1))*(1-(pe/pc))**((gam-1)/gam))


    def throatArea(self, Wdot, Pc, cs):
        return Wdot * cs * (1/Pc)


    def mach(self, t, gam, r):
        return sqrt(gam * r * t)


    def machNum(self, v, a):
        return v / a


    def exitArea(self, At, Me, gam):
        return At/Me * ( (1+(gam-1)/2*Me**2)/((gam+1)/2) )**((gam+1)/(2*(gam-1)))


    def pcns(self, Wdot, cs, At):
        return Wdot * cs * (1/(At))


    def exitVelocity(self, gam, r, t, pe, pc):
        return sqrt( (2 * gam / (gam-1) ) * r * t * (1-(pe/pc)**((gam-1)/gam)) )


    def exitTemp(self, tcns, pe, pcns, gam):
        return tcns * (pe / pcns)**((gam-1)/gam)





if not imported(__name__):

    # choose monoprop gas
    gas = Helium

    arr_thrust = []
    arr_diameter = []
    arr_exit = []

    for _ in range(1, 501):

        Tc = 294 # K
        Pc = psi2pascal(3000)
        # T = lbf2newton(100000)
        T = lbf2newton( (_ * 1000) )
        Pe = atm # exit pressure



        print( newton2lbf(T))

        nozzle = Nozzle(gas, Tc, Pc, Pe, T)
        arr_thrust.append( newton2lbf(T) )
        arr_diameter.append( meter2inch(nozzle.Dt) )
        arr_exit.append( meter2inch(nozzle.De) )

        # target = inch2meter(5 + (_ * 0.1))
        # Ae = 0
        # De = 0
        # error = target - De
        # deriv = 0
        # egain = 100
        # dgain = 1000
        # gain = 100

        # while error > 0.0001 :
        #
        #     Pe -= (error*egain + deriv*dgain) * gain
        #
        #     nozzle = Nozzle(gas, Tc, Pc, Pe, T)
        #
        #     deriv = error - (target-nozzle.De)
        #     error = target - nozzle.De
        #
        #     arr_thrust.append( newton2lbf(T) )
        #     arr_diameter.append( meter2inch(nozzle.Dt) )




    f = plt.figure()
    f.set_figwidth(12)
    f.set_figheight(9)
    plt.xticks(np.arange(0, 550000, 50000))
    plt.yticks(np.arange(0, 40, 1))
    plt.plot(arr_thrust, arr_diameter, label="Throat Diameter")
    plt.plot(arr_thrust, arr_exit, label="Exit Diameter")
    plt.legend()
    plt.ylabel("Inches")
    plt.xlabel("Thrust (lbf)")
    plt.title("1 Atm exit pressure, 3000 psi chamber")
    plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
    plt.show()



    # print("Chamber Temp: %.2f K" % nozzle.Tc)
    # print("Throat Temp: %.2f K" % nozzle.Tt)
    # print("Exit Temp: %.2f K" % nozzle.Te)
    # print("Chamber Pressure: %.2f psi" % pascal2psi(nozzle.Pc))
    # print("Throat Pressure: %.2f psi" % pascal2psi(nozzle.Pt))
    # print("Exit Pressure: %.2f psi" % pascal2psi(nozzle.Pe))
    # print("Cstar: %.2f m/s" % nozzle.Cstar)
    # print("Isp: %.2f s" % nozzle.isp)
    # print("Flow rate: %.2f kg/s" % nozzle.Wdot)
    # print("Throat Area: %.6f sq.m" % nozzle.At)
    # print("Throat Diameter: %.4f in" % meter2inch(nozzle.Dt))
    # print("Exit Velocity: %.2f m/s" % nozzle.Ve)
    # print("Exit Mach Number: %.2f" % nozzle.Me)
    # print("Speed of Sound at Exit: %.2f m/s" % (nozzle.Ve/nozzle.Me))
    # print("Exit Area: %.6f sq.m" % nozzle.Ae)
    # print("Exit Diameter: %.4f in" % meter2inch(nozzle.De))
    # print("Area Ratio: %.2f" % (nozzle.Ae/nozzle.At))
