import numpy as np
from scipy.optimize import bisect
from astropy.time import Time
import datetime

# Costante: obliquità (possiamo anche calcolarla dinamicamente se necessario)
OBLIQUITA = 23.43704  # Valore medio in gradi

def ecliptic_to_equatorial(L_deg, epsilon_deg=OBLIQUITA):
    """
    Trasforma una coordinata eclittica (lon = L_deg, lat = 0) in coordinate equatoriali (RA, Dec).
    """
    L = np.radians(L_deg)
    epsilon = np.radians(epsilon_deg)
    # Calcola RA e Dec per β = 0
    ra = np.degrees(np.arctan2(np.sin(L) * np.cos(epsilon), np.cos(L))) % 360
    dec = np.degrees(np.arcsin(np.sin(L) * np.sin(epsilon)))
    return ra, dec

def horizontal_coords(ra_deg, dec_deg, lat_deg, lst_deg):
    """
    Converte coordinate equatoriali (RA, Dec) in coordinate orizzontali (altitudine, azimut)
    per un osservatore in latitudine lat_deg e con tempo siderale locale lst_deg.
    """
    ra = np.radians(ra_deg)
    dec = np.radians(dec_deg)
    lat = np.radians(lat_deg)
    lst = np.radians(lst_deg)
    # Calcola l'angolo orario (HA)
    HA = lst - ra
    # Altezza: formula dell'altitudine
    alt = np.degrees(np.arcsin(np.sin(lat)*np.sin(dec) + np.cos(lat)*np.cos(dec)*np.cos(HA)))
    # Azimut: formula (si noti che qui l'azimut è calcolato in modo standard, con 0° = nord)
    az = np.degrees(np.arctan2(-np.sin(HA),
                                np.cos(lat)*np.tan(dec) - np.sin(lat)*np.cos(HA))) % 360
    return alt, az

def altitude_for_ecliptic_longitude(L_deg, lat_deg, lst_deg, epsilon_deg=OBLIQUITA):
    """
    Data una eclittica longitudine L_deg (con latitudine eclittica = 0),
    calcola l'altitudine e l'azimut corrispondenti per un osservatore con latitudine lat_deg e LST lst_deg.
    """
    ra, dec = ecliptic_to_equatorial(L_deg, epsilon_deg)
    alt, az = horizontal_coords(ra, dec, lat_deg, lst_deg)
    return alt, az

def objective(L_deg, lat_deg, lst_deg, epsilon_deg=OBLIQUITA):
    """
    Funzione obiettivo: restituisce l'altitudine (in gradi) per una data eclittica longitudine L_deg.
    Vogliamo trovare L tale che altitudine(L) = 0.
    """
    alt, _ = altitude_for_ecliptic_longitude(L_deg, lat_deg, lst_deg, epsilon_deg)
    return alt

def find_ascendant(lat_deg, lst_deg, epsilon_deg=OBLIQUITA):
    """
    Cerca lungo l'eclittica il punto (longitudine L) per cui l'altitudine è 0.
    Tra tutte le soluzioni, restituisce quella per cui l'azimut è più vicino a 90° (est).
    """
    # Campiona l'eclittica da 0 a 360° in modo fine
    L_values = np.linspace(0, 360, 1000)
    roots = []

    alt_values = [altitude_for_ecliptic_longitude(L, lat_deg, lst_deg, epsilon_deg)[0] for L in L_values]

    # Trova intervalli in cui l'altitudine cambia segno
    for i in range(len(L_values)-1):
        if alt_values[i] * alt_values[i+1] < 0:
            try:
                L_root = bisect(lambda L: objective(L, lat_deg, lst_deg, epsilon_deg),
                                L_values[i], L_values[i+1])
                alt_root, az_root = altitude_for_ecliptic_longitude(L_root, lat_deg, lst_deg, epsilon_deg)
                roots.append((L_root, alt_root, az_root))
            except ValueError:
                continue

    if not roots:
        return None, None

    # Seleziona il root con azimut più vicino a 90° (rising point)
    best = min(roots, key=lambda r: abs(r[2] - 90))
    return best[0] % 360, best[2]

# Funzione per calcolare il tempo siderale locale (LST) in gradi
def tempo_siderale_locale(t_astropy, lon_deg):
    """
    Calcola il Tempo Siderale Locale (LST) in gradi.
    t_astropy: oggetto Time di Astropy
    lon_deg: longitudine in gradi (positiva a est)
    """
    JD = t_astropy.jd
    T = (JD - 2451545.0) / 36525.0  # Secoli dal J2000.0
    GMST = 280.46061837 + 360.98564736629 * (JD - 2451545) + T**2 * 0.000387933 - T**3 / 38710000.0
    GMST = GMST % 360
    LST = (GMST + lon_deg) % 360
    return LST


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
    fuso_orario = 2  # Italia: UTC+1

    # Convertiamo in UTC:
    dt_utc = dt_local - datetime.timedelta(hours=fuso_orario)

    # Crea un oggetto Time per Astropy
    t_astropy = Time(dt_utc)

    # Calcola il tempo siderale locale (LST) in gradi
    lst = tempo_siderale_locale(t_astropy, longitudine)

    # Trova l'ascendente con il metodo iterativo
    L_asc, az_asc = find_ascendant(latitudine, lst)
    if L_asc is not None:
        print("Data/ora (UTC):", dt_utc.isoformat())
        print(f"Tempo siderale locale: {lst:.2f}°")
        print(f"Ascendente (longitudine eclittica): {L_asc:.2f}°")
        print(f"Azimut associato: {az_asc:.2f}°")
        print(f"Segno zodiacale: {trova_segno_zodiacale(L_asc)}")
    else:
        print("Non è stato possibile determinare l'ascendente.")
