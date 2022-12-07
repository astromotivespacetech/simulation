import math


def transit_duration(velocity, length):
    return length / velocity

def taper_half_angle(len, rad):
    return math.atan( rad/len )


if __name__=="__main__":

    exhaust_velocity = 667 # m/s

    rad = 1.62 # m
    len = 7 # m

    vel = 1000 # m/s

    # dt = transit_duration(vel, len)
    # vt = transit_duration(exhaust_velocity, rad)
    #
    # print(dt > vt)


    print( math.degrees(taper_half_angle(len,rad)) )
