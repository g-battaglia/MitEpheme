import math

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

def calcola_punti_cardinali(ora_siderale_locale, latitudine, obliquita=23.43):
    """
    Calcola ASC, DSC, MC e IC in modo preciso.

    Args:
        ora_siderale_locale (float): Ore (0-24).
        latitudine (float): Gradi decimali (Nord +, Sud -).
        obliquita (float): Obliquità dell'eclittica (default 23.43°).

    Returns:
        dict: ASC, DSC, MC, IC in gradi zodiacali (0-360°).
    """
    RAMC = ora_siderale_locale * 15  # Converti ore in gradi (0-360)
    RAMC_rad = math.radians(RAMC)
    lat_rad = math.radians(latitudine)
    obl_rad = math.radians(obliquita)

    # 1. Calcola il Medio Cielo (MC) in longitudine eclittica
    MC_rad = math.atan2(
        math.sin(RAMC_rad) * math.cos(obl_rad),
        math.cos(RAMC_rad)
    )
    MC = math.degrees(MC_rad) % 360

    # 2. Calcola l'Ascendente (ASC)
    ASC_rad = math.atan2(
        math.cos(RAMC_rad),
        - (math.sin(RAMC_rad) * math.cos(lat_rad) +
          math.tan(lat_rad) * math.sin(lat_rad))
    )
    ASC = math.degrees(ASC_rad) % 360

    # 3. Calcola Discendente (DSC) e Fondo Cielo (IC)
    DSC = (ASC + 180) % 360
    IC = (MC + 180) % 360

    return {"ASC": ASC, "DSC": DSC, "MC": MC, "IC": IC}


ora_siderale_locale = 4.20727  # Ore
latitudine = 45.0  # Gradi Nord
longitudine = 10.58  # Gradi Est
obliquita = 23.4367    # Obliquità eclittica (J2000)

punti_cardinali = calcola_punti_cardinali(ora_siderale_locale, latitudine, obliquita)

print("Ascendente (ASC):", punti_cardinali["ASC"])
print("Discendente (DSC):", punti_cardinali["DSC"])
print("Medio Cielo (MC):", punti_cardinali["MC"])
print("Fondo Cielo (IC):", punti_cardinali["IC"])

print("Segno Ascendente:", calculate_single_sign(punti_cardinali["ASC"]))
print("Segno Discendente:", calculate_single_sign(punti_cardinali["DSC"]))
print("Segno Medio Cielo:", calculate_single_sign(punti_cardinali["MC"]))
print("Segno Fondo Cielo:", calculate_single_sign(punti_cardinali["IC"]))
