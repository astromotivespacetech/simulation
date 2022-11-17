import math
from conversions    import *
from functions      import normalize
from vector         import Vector
from constants      import g_earth, EARTH_RAD



class Atmosphere(object):


    def calc_rho(self, alt):
        ''' Calculates atmospheric density.
            Arguments:
                alt: altitude [km].
            Returns:
                atmospheric density [kg/m^3].
         '''

        a             = alt / 1000                                              # convert to [ km ]
        geopot_height = self.get_geopotential(a)                                # [ km ]
        temp          = self.get_standard_temperature(geopot_height)            # [ Kelvin ]
        standard_p    = self.get_standard_pressure(geopot_height, temp)         # [ Pascals ]
        R             = 287.5                                                   # specific gas constant for dry air

        return standard_p / (R * temp) if standard_p > 0 else 0.0


    def calc_ambient_pressure(self, alt):
        ''' Setup function for get_standard_pressure.
            Arguments:
                altitude [km]
            Returns:
                atmospheric pressure [Pascals].
        '''

        a             = alt / 1000                                              # convert to [ km ]
        geopot_height = self.get_geopotential(a)                                # [ km ]
        temp          = self.get_standard_temperature(geopot_height)            # [ Kelvin ]
        standard_p    = self.get_standard_pressure(geopot_height, temp)         # [ Pascals ]

        return standard_p if standard_p > 0 else 0.0



    def get_standard_pressure(self, geo, t):                                      # returns atmospheric pressure in Pascals
        ''' Calculates standard atmosphere pressure up to 84.85 km.
            Arguments:
                g: geopotential height [km].
                t: temperature [Kelvin].
            Returns:
                pressure [Pascals].
        '''


        if geo <= 11:
            return 101325   * math.pow(288.15 / t, -5.255877)
        elif geo <= 20:
            return 22632.06 * math.exp(-0.1577 * (geo - 11))
        elif geo <= 32:
            return 5474.889 * math.pow(216.65 / t, 34.16319)
        elif geo <= 47:
            return 868.0187 * math.pow(228.65 / t, 12.2011)
        elif geo <= 51:
            return 110.9063 * math.exp(-0.1262 * (geo - 47))
        elif geo <= 71:
            return 66.93887 * math.pow(270.65 / t, -12.2011)
        elif geo <= 84.85:
            return 3.956420 * math.pow(214.65 / t, -17.0816)
        else:
            return 0



    def get_standard_temperature(self, geo):
        ''' Calculates standard temperature.
            Arguments:
                g: geopotential [km].
            Returns:
                temperature [Kelvin].
        '''

        if   geo <= 11:
            return 288.15 - (6.5 * geo)
        elif geo <= 20:
            return 216.65
        elif geo <= 32:
            return 196.65 + geo
        elif geo <= 47:
            return 228.65 + 2.8 * (geo - 32)
        elif geo <= 51:
            return 270.65
        elif geo <= 71:
            return 270.65 - 2.8 * (geo - 51)
        elif geo <= 84.85:
            return 214.65 - 2 * (geo - 71)
        else:
            return 0



    def get_geopotential(self, altitude_km):
        ''' Calculates geopotential height.
            Arguments:
                altitude_km: altitude [km].
            Returns:
                geopotential height [km].
        '''
        
        return EARTH_RAD * 0.001 * altitude_km / (EARTH_RAD * 0.001 + altitude_km)




    def speed_of_sound(self, alt):
        ''' Calculates the speed of sound at a given altitude.
            Arguments:
                alt: altitude [m].
            Returns:
                speed [m/s].
        '''

        a_km          = alt / 1000
        geopot_height = self.get_geopotential(a_km)
        temperature_k = self.get_standard_temperature(geopot_height)
        C             = kelvin2celcius(temperature_k)

        return 331.5 + 0.60 * C







if __name__ == "__main__":

    a = Atmosphere()

    for x in range(100):

        print( a.calc_rho(x*1000) )
