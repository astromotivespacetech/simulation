from math import pi
from matplotlib import pyplot as plt



tensile_cf = 250000 # psi
pressure = 2000
radius_plug = 3 # in
xarea_plug = pi * radius_plug**2
force_plug = xarea_plug * pressure
min_xarea_rod = force_plug / tensile_cf
min_radius_rod = (min_xarea_rod / pi) ** 0.5

diameter_rod = 0.75
radius_rod = diameter_rod * 0.5
xarea_rod = pi * radius_rod**2
tensile_rod = xarea_rod * tensile_cf


od_steel_tube = diameter_rod + 0.25
id_steel_tube = diameter_rod
tensile_steel = 70000 # psi
od_xarea_steel_tube = pi * (od_steel_tube*0.5)**2
id_xarea_steel_tube = pi * (id_steel_tube*0.5)**2
xarea_steel_tube = od_xarea_steel_tube = id_xarea_steel_tube
tensile_steel_tube = xarea_steel_tube * tensile_steel


print("Plug Force: %.2f lbf" % force_plug)
print("Min Rod Diameter: %.2f in" % (min_radius_rod*2))
print("Rod Diameter: %.2f in" % diameter_rod)
print("Rod Tensile Strength: %.2f lbf" % tensile_rod)
print("Steel Tube Tensile Strength: %.2f lbf" % tensile_steel_tube)
print("Plug Shaft Tensile Stength: %.2f lbf" % (tensile_rod+tensile_steel_tube))
print("Tensile Margin: %.2f lbf" % ((tensile_rod+tensile_steel_tube)-force_plug))

#Master_Bond_EP31_shear = 4600 # psi
Master_Bond_10AOHT_shear = 3500 # psi

min_bond_surface_area = force_plug / Master_Bond_10AOHT_shear

print("Minimum bonding surface area: %.2f sq.in" % min_bond_surface_area)

h = min_bond_surface_area / (2 * pi * radius_rod)

print("Minimum bond length: %.2f in" % h)

bond_length = 25.5 # in

bond_surface_area = bond_length * 2 * pi * radius_rod

print("Bond surface area: %.2f sq.in" % bond_surface_area)

bond_shear_strength = Master_Bond_10AOHT_shear * bond_surface_area

print("Bond shear strength: %.2f lbf" % bond_shear_strength)


vel = 40 # m/s

dt = 0.00025

accel = vel / dt

print("Acceleration: %i m/s2" % accel)

plug_mass = 3.45 # kg
piston_mass = 19.6 # kg

F = plug_mass * accel # N

force = F * 0.224809

print("Force: %.2f lbf" % force)


# pressures = []
# radii = []

# for i in range(100):
#     pressure = 1500 + i * 10 # psi
#     force_plug = xarea_plug * pressure
#     xarea_rod = force_plug / tensile_cf
#     radius_rod = (xarea_rod / pi) ** 0.5
#     pressures.append(pressure)
#     radii.append(radius_rod)
#
# fig, ax1 = plt.subplots()
# fig.set_size_inches(12, 7)
# ax1.plot(radii, pressures, label="Rod Radius vs Pressure", color='r')
# ax1.set_xlabel("Rod Radius (in)")
# ax1.set_ylabel("Pressure (psi)")
# plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
# plt.show()
#
# pressure = 2000
# radii_plug = []
# radii_rod = []
#
# for i in range(100):
#     radius_plug = 1 + i*0.1 # in
#     xarea_plug = pi * radius_plug**2
#     force_plug = xarea_plug * pressure
#     xarea_rod = force_plug / tensile_cf
#     radius_rod = (xarea_rod / pi) ** 0.5
#     radii_plug.append(radius_plug)
#     radii_rod.append(radius_rod)
#
# fig, ax1 = plt.subplots()
# fig.set_size_inches(12, 7)
# ax1.plot(radii_rod, radii_plug, label="Rod Radius vs Plug Radius", color='r')
# ax1.set_xlabel("Rod Radius (in)")
# ax1.set_ylabel("Plug Radius (in)")
# plt.grid(color='#bbb', linestyle='-', linewidth=0.5)
# plt.show()















#
