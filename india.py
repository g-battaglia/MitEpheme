import math
from datetime import datetime

# Constants
W = 23.44  # Earth's axial tilt in degrees (obliquity of the ecliptic)
LATITUDE = 28.6139  # Example: New Delhi latitude (in degrees)
LONGITUDE = 77.2090  # Example: New Delhi longitude (in degrees)

# Function to compute sidereal time in degrees
def calculate_sidereal_time(date_time, longitude):
    # Calculate the number of days since the standard epoch (J2000)
    jd = (date_time - datetime(2000, 1, 1, 12, 0)).days + 2451545.0
    t = (jd - 2451545.0) / 36525.0  # Julian centuries
    sidereal_time = 280.46061837 + 360.98564736629 * (jd - 2451545) / 365.25  # Mean Sidereal Time
    sidereal_time += (0.000387933 * t**2) - (t**3 / 38710000)  # Adjustments for sidereal time
    sidereal_time = sidereal_time % 360  # Normalize to 0-360 degrees
    sidereal_time += longitude  # Adjust by the local longitude
    return sidereal_time % 360  # Ensure value stays within 0-360 degrees

# Function to compute 10th house (Mid-Heaven) from sidereal time
def calculate_10th_house(sidereal_time):
    B = math.degrees(math.atan(math.tan(math.radians(sidereal_time)) / math.cos(math.radians(W))))
    return B

# Function to compute Ascendant from sidereal time
def calculate_ascendant(sidereal_time):
    A = sidereal_time + 90  # Ascendant computation adds 90 degrees to sidereal time
    B = math.degrees(math.atan(math.tan(math.radians(A)) * math.cos(math.radians(W))))

    # Declination and angle between meridian and ecliptic
    D = math.asin(math.sin(math.radians(A)) * math.sin(math.radians(W)))
    q = math.asin(math.sin(math.radians(W)) * math.cos(math.radians(LATITUDE)))

    # Final ascendant computation
    E = math.degrees(math.atan(math.sin(D) * math.tan(math.radians(LATITUDE + q))))
    ascendant = B + E
    return ascendant % 360

# Example usage: Calculate sidereal time, 10th house, and ascendant
date_time = datetime(2025, 4, 11, 12, 0)  # Example date and time (April 11, 2025, noon)

sidereal_time = calculate_sidereal_time(date_time, LONGITUDE)
print(f"Sidereal Time: {sidereal_time:.2f} degrees")

tenth_house = calculate_10th_house(sidereal_time)
print(f"10th House (Mid-Heaven): {tenth_house:.2f} degrees")

ascendant = calculate_ascendant(sidereal_time)
print(f"Ascendant: {ascendant:.2f} degrees")
