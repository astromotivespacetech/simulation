from math import pi, atan2



F = 200 # N


inf = float('inf')

GPa = 1000 # MPa
e1 = 210*GPa # GPa
e2 = 210*GPa # GPa
v1 = 0.28
v2 = 0.28
r1 = 6.35 * 0.5 # mm [0.25"]
r2 = inf

def area(f, e1, v1, r1, e2, v2, r2):

    x = 3*f/8
    numerator = ((1-v1**2)/e1)+((1-v2**2)/e2)
    denominator = 1/(2*r1)+1/(2*r2)

    return ( x*(numerator/denominator) ) ** (1./3)


def omegax(pmax, z, a, v):

    za = abs(z/a)

    return -pmax * ( (1 - za * atan2(1,za) ) * (1+v) - (1 / (2 * (1 + (z**2/a**2) ) ) )  )

def omegaz(pmax, z, a):
    return -pmax / (1 + (z**2/a**2))




a = area(F,e1,v1,r1,e2,v2,r2)
z = 0.48*a
Pmax = (3*F) / (2*pi*a**2)
omx = omegax(Pmax, z, a, v2)
omz = omegaz(Pmax, z, a)
maxstress = (omx-omz)/2



print(a)
print(Pmax)
print(omx, omz)
print(maxstress)
