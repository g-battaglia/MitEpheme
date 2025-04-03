from skyfield.api import load
from datetime import datetime, timezone

def trova_segno_zodiacale(longitudine):
    """Restituisce il segno zodiacale corrispondente alla longitudine eclittica."""
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
        if min_deg <= longitudine < max_deg:
            return segno
    return "Errore"

# Carica le effemeridi della NASA
eph = load('de421.bsp')
pianeti = {
    "Sole": eph['sun'],
    "Luna": eph['moon'],
    "Mercurio": eph['mercury'],
    "Venere": eph['venus'],
    "Marte": eph['mars'],
    "Giove": eph['jupiter barycenter'],
    "Saturno": eph['saturn barycenter'],
    "Urano": eph['uranus barycenter'],
    "Nettuno": eph['neptune barycenter'],
    "Plutone": eph['pluto barycenter'],
}
terra = eph['earth']

# Ottieni il tempo UTC attuale
t = load.timescale().utc(datetime.now(timezone.utc))

# Calcola il segno zodiacale di ogni pianeta
print(f"UTC: {t.utc_iso()}\n")
for nome, corpo in pianeti.items():
    astro = terra.at(t).observe(corpo).apparent()
    lat, lon, distance = astro.ecliptic_latlon()
    segno = trova_segno_zodiacale(lon.degrees)
    print(f"{nome}: {lon.degrees}° → {segno}")
