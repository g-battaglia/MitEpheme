from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u
import math
from datetime import datetime

# Definisci la posizione della Terra (per esempio, latitudine e longitudine)
location = EarthLocation.of_site('greenwich')  # Puoi cambiare con la tua posizione

# Ottieni l'ora corrente
now = Time.now()

# Calcola l'ora siderale
sidereal_time = now.sidereal_time('apparent', longitude=location.lon)
print(f"Sidereal Time: {sidereal_time}")

# Calcola l'ora siderale locale, Guidizzolo Italia
local_sidereal_time = now.sidereal_time('apparent', longitude=10.5815)
print(f"Local Sidereal Time: {local_sidereal_time}")

# Calcola il segno zodiacale
def zodiac_sign(degree):
    signs = [
        (0, 'Aries'), (30, 'Taurus'), (60, 'Gemini'),
        (90, 'Cancer'), (120, 'Leo'), (150, 'Virgo'),
        (180, 'Libra'), (210, 'Scorpio'), (240, 'Sagittarius'),
        (270, 'Capricorn'), (300, 'Aquarius'), (330, 'Pisces')
    ]
    for start, sign in signs:
        if degree < start + 30:
            return sign
    return None

# Calcola il segno zodiacale in base all'ora siderale locale
def calculate_zodiac_sign(sidereal_time):
    degree = sidereal_time.hour * 15  # Converti in gradi
    sign = zodiac_sign(degree)
    return sign

print(f"Zodiac Sign: {calculate_zodiac_sign(local_sidereal_time)}")


# I'm born at LMST: 4.20727
# Constants
W = 23.44  # Earth's axial tilt in degrees (obliquity of the ecliptic)
LATITUDE = 45.32  # Latitude of Guidizzolo, Italy

def calculate_10th_house(sidereal_time):
    B = math.degrees(math.atan(math.tan(math.radians(sidereal_time)) / math.cos(math.radians(W))))
    return B


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


def calculate_single_sign(degree):
    signs = [
        (0, 'Aries'), (30, 'Taurus'), (60, 'Gemini'),
        (90, 'Cancer'), (120, 'Leo'), (150, 'Virgo'),
        (180, 'Libra'), (210, 'Scorpio'), (240, 'Sagittarius'),
        (270, 'Capricorn'), (300, 'Aquarius'), (330, 'Pisces')
    ]
    for start, sign in signs:
        if degree < start + 30:
            return sign
    return None

# Esempio di utilizzo
lst_hours = 63.1090  # Local Sidereal Time in hours
latitude = LATITUDE  # Latitude of Guidizzolo, Italy
tenth_house = calculate_10th_house(lst_hours)
ascendant = calculate_ascendant(lst_hours)
aproximate_ascendant = get_ascendant_approximate(lst_hours, latitude)

print(f"------------------------------")
print(f"Local Sidereal Time: {lst_hours} hours")
print(f"Latitude: {latitude} degrees")
print(f"10th House: {tenth_house:.2f} degrees")
print(f"Ascendant: {ascendant:.2f} degrees")
print(f"Zodiac Sign 10th House: {calculate_single_sign(tenth_house)}")
print(f"Zodiac Sign Ascendant: {calculate_single_sign(ascendant)}")
print(f"Approximate Ascendant: {aproximate_ascendant:.2f} degrees")
print(f"Zodiac Sign Approximate Ascendant: {calculate_single_sign(aproximate_ascendant)}")



