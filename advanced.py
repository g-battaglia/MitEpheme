import numpy as np
import datetime
from astropy.time import Time

# Costanti
OBLIQUITA = 23.43704  # Inclinazione dell'asse terrestre in gradi

def tempo_siderale_locale(t_astropy, lon):
    """
    Calcola il Tempo Siderale Locale (LST) in gradi.
    t_astropy: oggetto Time di Astropy
    lon: longitudine locale in gradi (positiva a est)
    """
    JD = t_astropy.jd
    T = (JD - 2451545.0) / 36525.0  # Secoli Giuliani dal J2000.0
    GMST = 280.46061837 + 360.98564736629 * (JD - 2451545) + T**2 * 0.000387933 - T**3 / 38710000.0
    GMST = GMST % 360  # Normalizza in [0, 360)
    LST = (GMST + lon) % 360
    return LST

def calc_asc_mc(lat, lon, dt_utc):
    """
    Calcola Ascendente e Medio Cielo (MC) in eclittica
    lat: latitudine dell'osservatore (gradi, positiva a nord)
    lon: longitudine dell'osservatore (gradi, positiva a est)
    dt_utc: oggetto datetime in UTC
    """
    t_astropy = Time(dt_utc)
    lst = tempo_siderale_locale(t_astropy, lon)  # in gradi
    epsilon = np.radians(OBLIQUITA)
    lst_rad = np.radians(lst)

    # Calcolo del MC: il punto in cui la meridiana interseca l'eclittica
    mc_rad = np.arctan2(np.sin(lst_rad), np.cos(lst_rad)*np.cos(epsilon))
    mc = np.degrees(mc_rad) % 360

    # Calcolo dell'Ascendente: punto orientale dove l'eclittica interseca l'orizzonte
    # Formula tradizionale con LST, latitudine e obliquità
    asc_rad = np.arctan2(
        -np.cos(np.radians(lst)),
        np.sin(np.radians(lst)) * np.cos(epsilon) + np.tan(np.radians(lat)) * np.sin(epsilon)
    )
    asc = np.degrees(asc_rad) % 360

    return asc, mc

def placidus_cusps(asc, mc, lat):
    """
    Calcola le cuspidi delle case Placidus usando le formule di divisione dell'arco diurno.
    Restituisce un dizionario con le case (1-12) in gradi.

    Il metodo:
      - Per il lato orientale (case 2 e 3): si divide l'arco tra Ascendente e MC.
      - Per il lato occidentale (case 8 e 9): si divide l'arco tra MC e Discendente.
      - Le case 11 e 12 sono gli opposti (aggiungendo 180°) di 2 e 3.
      - Le case 5 e 6 sono gli opposti di 9 e 8.
    """
    # Converte in radianti
    asc_rad = np.radians(asc)
    mc_rad = np.radians(mc)
    lat_rad = np.radians(lat)

    # Lato orientale: da Ascendente a MC
    delta = np.arctan(np.cos(lat_rad) * np.tan(mc_rad - asc_rad))
    cusp2 = asc_rad + np.arctan((1 / np.cos(lat_rad)) * np.tan(delta / 3))
    cusp3 = asc_rad + np.arctan((1 / np.cos(lat_rad)) * np.tan(2 * delta / 3))

    # Punti cardine opposti
    desc_rad = (asc_rad + np.pi) % (2 * np.pi)      # Discendente = Ascendente + 180°
    ic_rad = (mc_rad + np.pi) % (2 * np.pi)           # IC = MC + 180°

    # Lato occidentale: da MC al Discendente
    delta2 = np.arctan(np.cos(lat_rad) * np.tan(desc_rad - mc_rad))
    cusp8 = mc_rad + np.arctan((1 / np.cos(lat_rad)) * np.tan(delta2 / 3))
    cusp9 = mc_rad + np.arctan((1 / np.cos(lat_rad)) * np.tan(2 * delta2 / 3))

    # Le cuspidi opposte del lato orientale
    cusp11 = (cusp2 + np.pi) % (2 * np.pi)
    cusp12 = (cusp3 + np.pi) % (2 * np.pi)

    # Le cuspidi opposte del lato occidentale (case 5 e 6)
    cusp5 = (cusp9 + np.pi) % (2 * np.pi)
    cusp6 = (cusp8 + np.pi) % (2 * np.pi)

    # Organizza le case in un dizionario:
    # Casa 1: Ascendente
    # Casa 2: cuspide calcolata (lato orientale)
    # Casa 3: cuspide calcolata (lato orientale)
    # Casa 4: IC (Imum Coeli)
    # Casa 5: opposto della cuspide 9
    # Casa 6: opposto della cuspide 8
    # Casa 7: Discendente
    # Casa 8: cuspide calcolata (lato occidentale)
    # Casa 9: cuspide calcolata (lato occidentale)
    # Casa 10: MC (Medium Coeli)
    # Casa 11: opposto della cuspide 2
    # Casa 12: opposto della cuspide 3
    houses_rad = {
        1: asc_rad,
        2: cusp2,
        3: cusp3,
        4: ic_rad,
        5: cusp5,
        6: cusp6,
        7: desc_rad,
        8: cusp8,
        9: cusp9,
        10: mc_rad,
        11: cusp11,
        12: cusp12
    }

    # Converte le cuspidi in gradi e normalizza in [0, 360)
    houses_deg = {k: np.degrees(v) % 360 for k, v in houses_rad.items()}
    return houses_deg

# -------------------------------
# ESEMPIO DI UTILIZZO
# -------------------------------
if __name__ == '__main__':
    # Parametri dell'osservatore (es. Montichiari, Brescia)
    latitudine = 45.41317     # gradi (latitudine)
    longitudine = 10.39799    # gradi (longitudine)

    # Data e ora di interesse (ora locale)
    # Ad esempio: 10 giugno 1993, ore 12:30 (UTC+1)
    dt_local = datetime.datetime(1993, 6, 10, 12, 15)
    fuso_orario = 1  # Italia: UTC+1
    # Convertiamo in UTC:
    dt_utc = dt_local - datetime.timedelta(hours=fuso_orario)

    # Calcola Ascendente e MC
    asc, mc = calc_asc_mc(latitudine, longitudine, dt_utc)

    # Calcola tutte le cuspidi Placidus
    houses = placidus_cusps(asc, mc, latitudine)

    # Determina anche il segno zodiacale per ciascuna cuspide (ogni 30°)
    def trova_segno_zodiacale(long_deg):
        segni = [
            ("Ariete", 0, 30),
            ("Toro", 30, 60),
            ("Gemelli", 60, 90),
            ("Cancro", 90, 120),
            ("Leone", 120, 150),
            ("Vergine", 150, 180),
            ("Bilancia", 180, 210),
            ("Scorpione", 210, 240),
            ("Sagittario", 240, 270),
            ("Capricorno", 270, 300),
            ("Acquario", 300, 330),
            ("Pesci", 330, 360)
        ]
        for segno, min_deg, max_deg in segni:
            if min_deg <= long_deg < max_deg:
                return segno
        return "Errore"

    # Stampa i risultati
    print("Data/ora (UTC):", dt_utc.isoformat())
    print(f"Ascendente: {asc:.2f}° → {trova_segno_zodiacale(asc)}")
    print(f"MC (Medium Coeli): {mc:.2f}° → {trova_segno_zodiacale(mc)}")
    for i in range(1, 13):
        print(f"Casa {i}: {houses[i]:.2f}° → {trova_segno_zodiacale(houses[i])}")
