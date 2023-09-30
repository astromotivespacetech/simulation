import math
from conversions import inch2meter


throat_radius = inch2meter(3) # in

projectile_velocity = 3700 # m/s

tail_length = 4 # m

pct_tail_coverage = 0.65

margin_of_error_len = tail_length * (1-pct_tail_coverage)

margin_of_error_duration = margin_of_error_len/projectile_velocity * 1e+6

# print(margin_of_error_len)
# print(margin_of_error_duration)


target_actuation_duration = 500 * 1e-6
print("Target actuation duration: %0.6f s" % target_actuation_duration)

plug_velocity = throat_radius / target_actuation_duration

print("Plug Velocity: %.4f m/s" % plug_velocity)

piston_actuation_distance = inch2meter(4)

piston_vel = 10

piston_acceleration = piston_vel**2 / (2*piston_actuation_distance)

print("Acceleration: %.5f m/s2" % piston_acceleration)
