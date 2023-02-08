import math

def xarea(r):
    return math.pi * r**2


tensile_stress_area = {
    'eight_thirtytwo': ['8-32', 0.014],
    'quarter_twenty': ['1/4-20', 0.0318],
    'three_eights_sixteen': ['3/8-16', 0.0775]
}


grade_8_min_tensile = 150000 # psi
bolt = 'quarter_twenty'
stress_area = tensile_stress_area[bolt][1] # sq. in
shear_strength_factor = 0.6 # 60% of tensile strength [https://www.portlandbolt.com/technical/faqs/calculating-shear-strength-of-grade-8-bolts/]
grade_8_shear_strength = grade_8_min_tensile * shear_strength_factor
shear = grade_8_shear_strength * stress_area
num_bolts = 6
max_force = num_bolts * shear
pressure = 1000 # psi
radiusPiston = 1 # in
radiusChamber = 2 # in
xareaPiston = xarea(radiusPiston)
xareaChamber = xarea(radiusChamber)
xareaChamberCap = xareaChamber - xareaPiston
pressureChamberCap = xareaChamberCap * pressure

print("Bolt: %s" % tensile_stress_area[bolt][0])
print("Bolt Stress Area: %.3f sq.in" % stress_area)
print("Grade 8 Shear Strength %i lbf" % grade_8_shear_strength)
print("Bolt Shear Strength: %i lbf" % shear)
print("Chamber Cap Cross-Sectional Area: %.2f sq.in" % xareaChamberCap)
print("Chamber Cap Load: %i lbf" % pressureChamberCap)
print("Max Force: %i lbf" % max_force)
