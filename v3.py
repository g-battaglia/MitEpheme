from skyfield.api import load, Topos
import math

def calculate_astrological_ascendant(year, month, day, hour, minute, lat_deg, lon_deg):
    # Carica efemeridi e tempo
    eph = load('de421.bsp')
    ts = load.timescale()
    t = ts.utc(year, month, day, hour, minute)

    # Calcola il tempo siderale locale in gradi
    gst = t.gmst * 15  # Greenwich sidereal time in degrees
    lst = (gst + lon_deg) % 360  # Local sidereal time

    # Obliquità dell’eclittica (approssimata, può anche essere calcolata)
    epsilon_deg = 23.4393
    epsilon = math.radians(epsilon_deg)

    # Converti in radianti
    lst_rad = math.radians(lst)
    lat_rad = math.radians(lat_deg)

    # Formula astronomica per il punto ascendente (longitudine eclittica)
    tan_lambda = (
        math.cos(epsilon) * math.tan(lat_rad) +
        math.sin(epsilon) * math.sin(lst_rad)
    ) / math.cos(lst_rad)

    lambda_rad = math.atan(tan_lambda)

    # Correzione di quadrante
    if math.cos(lst_rad) < 0:
        lambda_rad += math.pi
    lambda_deg = math.degrees(lambda_rad) % 360

    # Converti in segno zodiacale (ciclo di 30° per segno)
    zodiac_sign = int(lambda_deg // 30)
    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    ascendant_sign = signs[zodiac_sign]
    return lambda_deg, ascendant_sign

# Esempio: Roma, 10 aprile 2025, 14:30 locali (12:30 UTC)
asc, ascendant = calculate_astrological_ascendant(1993, 6, 10, 10, 15, 45.5, 10.4)
print(f"Ascendente astronomico (longitudine eclittica): {asc:.2f}°, Segno: {ascendant}")
