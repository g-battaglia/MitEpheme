from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, get_sun
from astropy import units as u

# Example: Let's use a time and a place (latitude, longitude)
latitude = 52.5200  # Example latitude (Berlin)
longitude = 13.4050  # Example longitude (Berlin)
time = '2025-04-03 12:00:00'  # Example time (UTC)

# Create a Time object
t = Time(time)

# Define the observer's location
location = EarthLocation(lat=latitude*u.deg, lon=longitude*u.deg)

# Get the Sun's position at that time
sun = get_sun(t)

# Convert the Sun's position to AltAz coordinates
altaz_frame = AltAz(obstime=t, location=location)
sun_altaz = sun.transform_to(altaz_frame)

print(f"Sun's altitude: {sun_altaz.alt}")
print(f"Sun's azimuth: {sun_altaz.az}")
