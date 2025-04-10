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

def calcola_punti_cardinali(ora_siderale_locale, latitudine, longitudine):
    """
    Calcola ASC, DSC, MC e IC a partire da:
    - ora_siderale_locale: in ore (0-24)
    - latitudine: in gradi decimali
    - longitudine: in gradi decimali (positiva per Est, negativa per Ovest)

    Restituisce un dizionario con i 4 punti cardinali in gradi zodiacali (0-360°)
    """
    # Converti l'ora siderale locale in gradi
    RAMC = ora_siderale_locale * 15  # Right Ascension of Medium Coeli

    # Calcolo del Medio Cielo (MC) - già in gradi zodiacali
    MC = RAMC

    # Calcolo del Fondo Cielo (IC) - opposto al MC
    IC = (MC + 180) % 360

    # Calcolo dell'Ascendente (ASC)
    # Converti la latitudine in radianti per i calcoli
    lat_rad = math.radians(latitudine)

    # Formula per l'ASC
    asc_rad = math.atan2(math.cos(RAMC * math.pi / 180),
                        -math.sin(RAMC * math.pi / 180) * math.cos(lat_rad) -
                        math.tan(lat_rad) * math.sin(lat_rad))
    ASC = math.degrees(asc_rad) % 360

    # Calcolo del Discendente (DSC) - opposto all'ASC
    DSC = (ASC + 180) % 360

    return {
        "ASC": ASC,
        "DSC": DSC,
        "MC": MC,
        "IC": IC
    }

# Esempio di utilizzo
ora_siderale_locale = 4.20727  # Ore
latitudine = 45.0  # Gradi Nord
longitudine = 9.0  # Gradi Est

punti_cardinali = calcola_punti_cardinali(ora_siderale_locale, latitudine, longitudine)

print("Ascendente (ASC):", punti_cardinali["ASC"])
print("Discendente (DSC):", punti_cardinali["DSC"])
print("Medio Cielo (MC):", punti_cardinali["MC"])
print("Fondo Cielo (IC):", punti_cardinali["IC"])

print("Segno Ascendente:", calculate_single_sign(punti_cardinali["ASC"]))
print("Segno Discendente:", calculate_single_sign(punti_cardinali["DSC"]))
print("Segno Medio Cielo:", calculate_single_sign(punti_cardinali["MC"]))
print("Segno Fondo Cielo:", calculate_single_sign(punti_cardinali["IC"]))
