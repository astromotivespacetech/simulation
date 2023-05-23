import math

def xarea(r):
    return math.pi * r**2

# https://www.almabolt.com/pages/catalog/bolts/proofloadtensile.htm
tensile_stress_area = {
    'eight_thirtytwo': ['8-32', 0.014],
    'quarter_twenty': ['1/4-20', 0.0318],
    'three_eights_sixteen': ['3/8-16', 0.0775],
    'one_half_thirteen': ['1/2-14', 0.141],
    'five_eights_eighteen': ['5/8-18', 0.256]
}


grade_8_min_tensile = 170000 # psi
bolt = 'five_eights_eighteen'
stress_area = tensile_stress_area[bolt][1] # sq. in
shear_strength_factor = 0.6 # 60% of tensile strength [https://www.portlandbolt.com/technical/faqs/calculating-shear-strength-of-grade-8-bolts/]
grade_8_shear_strength = grade_8_min_tensile * shear_strength_factor
shear = grade_8_shear_strength * stress_area
num_bolts = 12
max_force = num_bolts * shear
pressure = 2000 # psi
radiusPiston = 3 # in
radiusChamber = 4.913 # in
xareaPiston = xarea(radiusPiston)
xareaChamber = xarea(radiusChamber)
xareaChamberCap = xareaChamber - xareaPiston
pressureChamberCap = xareaChamberCap * pressure
pressureNozzle = xareaChamber * pressure
pressurePiston = xareaPiston * pressure

print("Bolt: %s" % tensile_stress_area[bolt][0])
print("Bolt Stress Area: %.3f sq.in" % stress_area)
print("Grade 8 Shear Strength %i lbf" % grade_8_shear_strength)
print("Bolt Shear Strength: %i lbf" % shear)
print("Nozzle Cross-Sectional Area: %.2f sq.in" % xareaChamber)
print("Nozzle Load: %i lbf" % pressureNozzle)
print("Number of Bolts: %i" % num_bolts)
print("Max Force: %i lbf" % max_force)
print("Chamber Cap Load: %i lbf" % pressureChamberCap)
print("Piston Load: %i lbf" % pressurePiston)
