import math
from conversions import *



fr = 1/240

in_per_frame = 4

in_per_sec = in_per_frame / fr

ft_per_sec = in_per_sec / 12

m_per_sec = ft_per_sec * 0.3048

actuation_time = inch2meter(1) / m_per_sec

piston_base = 0.931 # kg

piston_tube = 0.349 # kg

piston_cap = 0.217 # kg


print(in_per_sec)

print(ft_per_sec)

print(m_per_sec)

print(actuation_time)
