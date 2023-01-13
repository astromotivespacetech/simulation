import math
from matplotlib import pyplot as plt
import numpy as np


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

    fig, ax1 = plt.subplots()
    fig.set_size_inches(12, 7)
    plt.plot(cds, label="Drag Coefficient")
    plt.xticks(np.arange(0, 91, 10))
    plt.ylabel("Drag Coefficient")
    plt.xlabel("Angle of Attack (deg)")
    plt.title("Hypersonic Drag Coefficient from Angle of Attack")
    plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
    plt.show()
