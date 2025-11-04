import math
import re

# ---- Metric prefix parser ----
def parse_value(val_str):
    """
    Convert strings like '5u', '10m', '2n', '6p' into float (SI units).
    Supports:
        T, G, M, k, m, u (or µ), n, p, f
    """
    val_str = val_str.strip().lower().replace("µ", "u")
    match = re.match(r"([0-9.]+)\s*([tgmkmunpf]?)", val_str)
    if not match:
        raise ValueError(f"Invalid value format: {val_str}")
    num, prefix = match.groups()
    num = float(num)
    scale = {
        "t": 1e12,
        "g": 1e9,
        "m": 1e-3,
        "k": 1e3,
        "u": 1e-6,
        "n": 1e-9,
        "p": 1e-12,
        "f": 1e-15,
        "": 1.0
    }[prefix]
    return num * scale

# ---- Spectral weighting tables (400–500 nm) ----
R_TABLE = {
    400: 2.0, 410: 2.0, 420: 2.0, 430: 2.0, 440: 2.0,
    450: 2.0, 455: 2.0, 460: 2.0, 470: 2.0, 480: 2.0,
    490: 2.0, 500: 2.0
}
B_TABLE = {
    400: 0.060, 410: 0.180, 420: 0.900, 430: 0.980, 440: 0.970,
    450: 0.940, 455: 0.900, 460: 0.800, 470: 0.630, 480: 0.550,
    490: 0.420, 500: 0.320
}

def nearest_nm(nm, table_keys=R_TABLE.keys()):
    """Nearest valid wavelength key"""
    return min(table_keys, key=lambda k: abs(k - nm))

def iso15004_smallspot(wavelength_nm, power_pupil_W, dwell_time_s,
                       rep_rate_Hz=59e6, pulse_duration_s=6e-12):
    """ISO 15004-2:2025 small-spot (≤0.03 mm) laser safety evaluation"""
    
    nm = nearest_nm(wavelength_nm)
    R = R_TABLE[nm]
    B = B_TABLE[nm]

    # ---- Apply R(λ) substitution rules ----
    if pulse_duration_s < 1e-11 and R < 1.0:
        R = 1.0
    if dwell_time_s > 10.0 and R > 1.0:
        R = 1.0

    # ---- Fixed small-spot aperture ----
    d_mm = 0.03
    r_cm = (d_mm / 2) / 10.0
    A_cm2 = math.pi * r_cm**2  # ≈ 7.07 × 10⁻⁶ cm²

    # ---- Single-pulse energy ----
    E_pulse = power_pupil_W / rep_rate_Hz
    E_pulse_eff = R * E_pulse
    single_limit = 40e-9  # J
    single_margin = single_limit / E_pulse_eff if E_pulse_eff > 0 else float('inf')

    # ---- Thermal hazard (t > 6.2e-4 s) ----
    E_eff = R * power_pupil_W * dwell_time_s
    thermal_limit = None
    thermal_margin = None
    if dwell_time_s > 6.2e-4:
        thermal_limit = 1.7 * (dwell_time_s**0.75) * 1e-3  # mJ→J
        thermal_margin = thermal_limit / E_eff if E_eff > 0 else float('inf')

    # ---- Photochemical hazard (t > 6.2e-4 s) ----
    photo_limit = 2.2  # J/cm²
    E_photo = (power_pupil_W * B) / A_cm2
    H_photo = None
    photo_margin = None
    if dwell_time_s > 6.2e-4:
        H_photo = E_photo * dwell_time_s
        photo_margin = photo_limit / H_photo if H_photo > 0 else float('inf')

    # ---- Determine governing hazard ----
    if dwell_time_s <= 6.2e-4:
        governing = "Thermal only (photochemical not applicable)"
    else:
        if thermal_margin and photo_margin:
            governing = "Photochemical" if photo_margin < thermal_margin else "Thermal"
        elif thermal_margin:
            governing = "Thermal"
        elif photo_margin:
            governing = "Photochemical"
        else:
            governing = "Indeterminate"

    # ---- Safe stopped-beam time ----
    t_safe_photo = photo_limit / E_photo if E_photo > 0 else float('inf')

    # ---- Print formatted output ----
    print("\n=== ISO 15004-2:2025 Small-Spot Laser Safety Evaluation ===")
    print(f"Wavelength (nm):           {nm}")
    print(f"Pulse duration (s):        {pulse_duration_s:.2e}")
    print(f"Exposure time (s):         {dwell_time_s:.3g}")
    print(f"Power at pupil (W):        {power_pupil_W:.3g}")
    print(f"Repetition rate (Hz):      {rep_rate_Hz:.3g}")
    print(f"Spot diameter (mm):        0.03 (fixed small-spot)")
    print(f"\n--- Spectral weighting ---")
    print(f"R(λ):                      {R}")
    print(f"B(λ):                      {B}")
    print(f"\n--- Single-pulse check ---")
    print(f"Pulse energy (J):          {E_pulse:.3e}")
    print(f"Weighted pulse (J):        {E_pulse_eff:.3e}")
    print(f"Limit (J):                 4.00e-8")
    print(f"Margin:                    {single_margin:.1f} × below limit")
    if dwell_time_s > 6.2e-4:
        print(f"\n--- Thermal hazard ---")
        print(f"Weighted energy (J):       {E_eff:.3e}")
        print(f"Thermal limit (J):         {thermal_limit:.3e}")
        print(f"Margin:                    {thermal_margin:.1f} × below limit")
        print(f"\n--- Photochemical hazard ---")
        print(f"E_photo (W/cm²):           {E_photo:.3e}")
        print(f"Dose (J/cm²):              {H_photo:.3e}")
        print(f"Limit (J/cm²):             2.20")
        print(f"Margin:                    {photo_margin:.1f} × below limit")
        print(f"\nGoverning hazard:          {governing}")
        print(f"Safe stopped-beam time(s): {t_safe_photo:.3e}")
    else:
        print("\nExposure below 6.2 × 10⁻⁴ s → Photochemical hazard not applicable")
        print(f"Governing hazard:          {governing}")
    print("============================================================\n")

# --- Interactive prompt ---
if __name__ == "__main__":
    λ = float(input("Enter wavelength (nm, 400–500): "))
    P_str = input("Enter power at pupil (e.g., 5u for 5 µW): ")
    t_str = input("Enter exposure duration (e.g., 100m for 100 ms): ")
    P = parse_value(P_str)
    t = parse_value(t_str)
    iso15004_smallspot(λ, P, t)
