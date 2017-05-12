import csv
import math

path = 'data.csv'

inhg = 30.02
temperature = 21.11
prop_diameter = 16
rpm = 8364
pitch = 6
airspeed = 8

weight = 23
num_motors = 8

voltage = 25

if __name__ == '__main__':
    file=open(path, "r")
    reader = csv.reader(file)
    for line_data in reader:
        power = float(line_data[1]) * voltage
        rpm_dynamic = ((2 * power / 0.772127488)**0.5) * 60 / (2 * math.pi)

        rpm = rpm_dynamic
        density_calc = (inhg * 3386.39) / (287.05 * (temperature + 273.15))
        coefficient_1 = math.pi * 0.25 * (0.0254 * prop_diameter)**2
        coefficient_2 = (rpm * 0.0254 * pitch / 60)**2
        coefficient_3 = coefficient_2 - ((rpm * 0.0254 * pitch / 60) * airspeed)
        coefficient_4 = (prop_diameter / (3.29546 * pitch))**1.5
        thrust = density_calc * coefficient_1 * coefficient_3 * coefficient_4
        thrust_ounces = thrust * 1000 * 0.035274 / 9.81
        total_thrust_lbs = num_motors * thrust_ounces / 16

        print("Throttle:", line_data[0], "Thrust:", total_thrust_lbs)
