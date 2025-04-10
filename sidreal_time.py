from astropy.time import Time
from astropy.coordinates import EarthLocation
from axes import calcola_punti_cardinali

t = Time.now()  # Tempo attuale
location = EarthLocation(lat=45.0, lon=12.0)  # Esempio: Venezia, Italia

lst = t.sidereal_time("mean", longitude=location.lon)
gmst = t.sidereal_time("mean", longitude=0.0)

print(f"UTC: {t.iso}")
print(f"Tempo siderale locale (LST): {lst.to_string(unit='hour')}")
print(f"Tempo siderale di Greenwich (GMST): {gmst.to_string(unit='hour')}")

####################
punti = calcola_punti_cardinali(
    ora_siderale_locale=lst.hour,
    latitudine=location.lat.deg,
    obliquita=23.4367  # Obliquità eclittica (J2000)
)

print("--------------------------")
print("Ascendente (ASC):", punti["ASC"])
print("Discendente (DSC):", punti["DSC"])
print("Medio Cielo (MC):", punti["MC"])
print("Fondo Cielo (IC):", punti["IC"])
