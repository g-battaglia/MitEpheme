import math
from datetime import datetime, timedelta
import juliandate
import pytz
from astropy.coordinates.earth_orientation import obliquity as calculate_obliquity


# Constants
VERY_SMALL = 1e-10
DEGTORAD = math.pi / 180.0
RADTODEG = 180.0 / math.pi

def normalize_degree(deg: float) -> float:
    """
    Normalize degree to a value between 0 and 360.

    Args:
        deg (float): The degree to normalize.

    Returns:
        float: The normalized degree.
    """
    return deg % 360.0

def sine_degrees(deg: float) -> float:
    """
    Sine of an angle in degrees.

    Args:
        deg (float): Angle in degrees.

    Returns:
        float: Sine of the angle.
    """
    return math.sin(deg * DEGTORAD)

def cosine_degrees(deg: float) -> float:
    """
    Cosine of an angle in degrees.

    Args:
        deg (float): Angle in degrees.

    Returns:
        float: Cosine of the angle.
    """
    return math.cos(deg * DEGTORAD)

def tangent_degrees(deg: float) -> float:
    """
    Tangent of an angle in degrees.

    Args:
        deg (float): Angle in degrees.

    Returns:
        float: Tangent of the angle.
    """
    return math.tan(deg * DEGTORAD)

def arcsine_degrees(value: float) -> float:
    """
    Arcsine in degrees.

    Args:
        value (float): The value to calculate arcsine for.

    Returns:
        float: Arcsine in degrees.
    """
    return math.asin(value) * RADTODEG

def arctangent_degrees(value: float) -> float:
    """
    Arctangent in degrees.

    Args:
        value (float): The value to calculate arctangent for.

    Returns:
        float: Arctangent in degrees.
    """
    return math.atan(value) * RADTODEG

def degree_difference(p1: float, p2: float) -> float:
    """
    Calculate the difference between two degrees, normalized to a value between 0 and 360.

    Args:
        p1 (float): The first degree.
        p2 (float): The second degree.

    Returns:
        float: The normalized degree difference.
    """
    difference = p1 - p2
    return (difference + 360.0) % 360.0

def calculate_ascendant(x1: float, latitude: float, sine: float, cosine: float) -> float:
    """
    Calculate the ascendant based on given parameters.

    Args:
        x1 (float): The angle in degrees.
        latitude (float): The geographic latitude in degrees.
        sine (float): Obliquity of the ecliptic sine.
        cosine (float): Obliquity of the ecliptic cosine.

    Returns:
        float: The calculated ascendant in degrees.
    """
    quadrant = int((x1 / 90) + 1)  # Determine the quadrant (1 to 4)
    x1 = normalize_degree(x1)
    if abs(90 - latitude) < VERY_SMALL:
        return 180.0
    if abs(90 + latitude) < VERY_SMALL:
        return 0.0
    if quadrant == 1:
        ascendant = calculate_auxiliary_ascendant(x1, latitude, sine, cosine)
    elif quadrant == 2:
        ascendant = 180.0 - calculate_auxiliary_ascendant(180.0 - x1, -latitude, sine, cosine)
    elif quadrant == 3:
        ascendant = 180.0 + calculate_auxiliary_ascendant(x1 - 180.0, -latitude, sine, cosine)
    else:
        ascendant = 360.0 - calculate_auxiliary_ascendant(360.0 - x1, latitude, sine, cosine)
    ascendant = normalize_degree(ascendant)
    return ascendant

def calculate_auxiliary_ascendant(x: float, latitude: float, sine: float, cosine: float) -> float:
    """
    Auxiliary function for calculating the ascendant.

    Args:
        x (float): The angle in degrees.
        latitude (float): The geographic latitude in degrees.
        sine (float): Obliquity of the ecliptic sine.
        cosine (float): Obliquity of the ecliptic cosine.

    Returns:
        float: The calculated auxiliary ascendant in degrees.
    """
    auxiliary_ascendant = -tangent_degrees(latitude) * sine + cosine * cosine_degrees(x)
    if abs(auxiliary_ascendant) < VERY_SMALL:
        auxiliary_ascendant = 0.0
    sinx = sine_degrees(x)
    if abs(sinx) < VERY_SMALL:
        sinx = 0.0
    if sinx == 0:
        if auxiliary_ascendant < 0:
            auxiliary_ascendant = -VERY_SMALL
        else:
            auxiliary_ascendant = VERY_SMALL
    elif auxiliary_ascendant == 0:
        if sinx < 0:
            auxiliary_ascendant = -90.0
        else:
            auxiliary_ascendant = 90.0
    else:
        auxiliary_ascendant = arctangent_degrees(sinx / auxiliary_ascendant)
    if auxiliary_ascendant < 0:
        auxiliary_ascendant = 180.0 + auxiliary_ascendant
    return auxiliary_ascendant


if __name__ == "__main__":
    # Calculate for J2000 (June 10, 1993, 12:15 GMT+1)
    j2000 = datetime(1993, 6, 10, 12, 15)
    j2000 = juliandate.from_gregorian(j2000.year, j2000.month, j2000.day, j2000.hour, j2000.minute, j2000.second)
    obliquity_j2000 = calculate_obliquity(j2000)
    print(f"Obliquity of the ecliptic for J2000: {obliquity_j2000}")

    #45.41317 10.39799
    latitude = 45.41317  # Example latitude
    longitude = 10.39799  # Example longitude
    sine = sine_degrees(obliquity_j2000)
    cosine = cosine_degrees(obliquity_j2000)

    ascendant = calculate_ascendant(longitude, latitude, sine, cosine)
    print(f"Ascendant: {ascendant}")
