import math
from matplotlib import pyplot as plt


# http://www.aerospaceweb.org/design/waverider/theory.shtml

def drag_coeff(a):
    return 2 * math.sin(a)**3



def calc_drag(cd, r, rho, v):
    return 0.5 * rho * v*v * cd * math.pi*r*r




if __name__=="__main__":

    cds = []

    for _ in range(90):

        ax = math.radians(_)
        cd = drag_coeff(ax)
        cds.append(cd)


    plt.plot(cds)
    plt.show()
