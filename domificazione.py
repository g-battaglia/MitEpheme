import numpy as np
from astropy.time import Time
from astropy.coordinates import EarthLocation, AltAz, SkyCoord
from astropy.coordinates import get_sun
import astropy.units as u
from scipy.optimize import root_scalar


def calcolare_tempo_siderale(data_ora, latitudine, longitudine):
    t = Time(data_ora)
    location = EarthLocation(lat=latitudine * u.deg, lon=longitudine * u.deg)
    return t.sidereal_time('apparent', longitude=location.lon).deg


def obliquita_eclittica(data_ora):
    # Obliquità media (J2000) leggermente corretta
    return 23.4393


def ascendente(t, latitudine, longitudine):
    # Calcolo approssimato dell'ASC tramite coordinate locali
    location = EarthLocation(lat=latitudine * u.deg, lon=longitudine * u.deg)
    tempo = Time(t)
    lst = tempo.sidereal_time('apparent', longitude=location.lon)
    epsilon = np.deg2rad(obliquita_eclittica(t))
    phi = np.deg2rad(latitudine)

    tan_l = -np.cos(epsilon) * np.tan(phi)
    asc_rad = np.arctan2(tan_l, 1)
    asc_deg = np.rad2deg(asc_rad) % 360
    return asc_deg


def medium_coeli(t, latitudine, longitudine):
    location = EarthLocation(lat=latitudine * u.deg, lon=longitudine * u.deg)
    tempo = Time(t)
    lst = tempo.sidereal_time('apparent', longitude=location.lon).deg
    epsilon = obliquita_eclittica(t)

    # MC = arctan(tan(LST) / cos(epsilon))
    tan_mc = np.tan(np.deg2rad(lst)) / np.cos(np.deg2rad(epsilon))
    mc_rad = np.arctan(tan_mc)
    mc_deg = np.rad2deg(mc_rad) % 360
    return mc_deg


def placidus_cuspide(casa_num, t, latitudine, longitudine, metodo="bisezione"):
    location = EarthLocation(lat=latitudine * u.deg, lon=longitudine * u.deg)
    tempo = Time(t)
    epsilon = np.deg2rad(obliquita_eclittica(t))
    phi = np.deg2rad(latitudine)
    lst = tempo.sidereal_time('apparent', longitude=location.lon).deg

    # Convertiamo lst in radianti
    th = np.deg2rad(lst)

    # Calcolo delle cuspidi II-XII, escludendo ASC (I) e MC (X)
    if casa_num in [2, 3]:  # case notturne
        r = (3 - casa_num) * (np.pi / 6)
        sgn = -1
    elif casa_num in [11, 12]:  # case diurne
        r = (casa_num - 9) * (np.pi / 6)
        sgn = 1
    else:
        return None  # ASC e MC già gestiti a parte

    def equazione(H):
        try:
            return np.tan(th + sgn * H / 3) * np.cos(epsilon) - np.tan(phi) * np.sin(H)
        except:
            return 1e6  # fallback se diverge

    sol = root_scalar(equazione, bracket=[-np.pi/2 + 0.01, np.pi/2 - 0.01], method='bisect' if metodo=="bisezione" else "newton", xtol=1e-6)

    if not sol.converged:
        return None

    H = sol.root
    # Angolo orario => longitudine eclittica
    cuspide = (lst + np.rad2deg(H)) % 360
    return cuspide


def calcolare_cuspidi(asc, mc, t, latitudine, longitudine):
    cuspidi = {
        1: asc,
        10: mc
    }
    for casa in [2, 3, 11, 12]:
        cuspide = placidus_cuspide(casa, t, latitudine, longitudine, metodo="bisezione")
        if cuspide is not None:
            cuspidi[casa] = round(cuspide, 2)
    return cuspidi


# ======= ESEMPIO D'USO ==========
if __name__ == "__main__":
    data_ora = "2023-06-21 12:00:00"  # UTC
    latitudine = 41.9
    longitudine = 12.5

    asc = ascendente(data_ora, latitudine, longitudine)
    mc = medium_coeli(data_ora, latitudine, longitudine)
    cuspidi = calcolare_cuspidi(asc, mc, data_ora, latitudine, longitudine)

    for casa, grado in sorted(cuspidi.items()):
        print(f"Casa {casa}: {grado:.2f}°")
