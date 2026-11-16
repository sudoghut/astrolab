"""Hand-transcribed inputs (README section 3; verified against the papers on 2026-11-15)."""

# Naidu et al. 2026 (OJAp 9, arXiv:2505.11263 v2), Sec. 4.1
N26 = {
    "n_sources": 2,
    "area_arcmin2": 136.0 + 243.0 + 9.0,      # PRIMER-COSMOS + PRIMER-UDS + JOF
    "volume_mpc3": 462648.0,                  # differential comoving volume, z = 14-15
    "z_lo": 14.0, "z_hi": 15.0,
    "m_lo": -21.0, "m_hi": -20.0,
    "log_phi": -5.36, "err_hi": 0.37, "err_lo": 0.45,
    "ratio": 182.0, "ratio_hi": 329.0, "ratio_lo": 105.0,
    "sigma_uv_required": (1.5, 2.0),
}

# Bouwens et al. 2021 (AJ 162, 47, arXiv:2102.07775), Table 5: Schechter parameters;
# phi_star in Mpc^-3 mag^-1
BOUWENS21 = {
    "z8": {"z": 7.9, "m_star": -20.93, "phi_star": 0.09e-3, "alpha": -2.23},
    "z7": {"z": 6.8, "m_star": -21.15, "phi_star": 0.19e-3, "alpha": -2.06},
}

# Harikane et al. 2025 (ApJ 980, 138), Table 2, z ~ 14 bin (13.5-15.0)
H25_Z14 = {"m_uv": -20.8, "phi": 3.7e-5, "err_hi": 8.7e-5, "err_lo": 3.6e-5, "area_arcmin2_approx": 10.0}

# Shen et al. 2023 (MNRAS 525, 3254) abstract: required sigma_UV
S23_SIGMA = {"z9": 0.75, "z12": 2.0, "z16": 2.5}


# R2/R3-POST (README section 2, addendum 2026-11-16), verified 2026-11-16 against the PDF tables.
# Rows: (M_1600, phi, err_hi, err_lo) in Mpc^-3 mag^-1.
# Bouwens et al. 2021 (arXiv:2102.07775) Table 4, z ~ 8 column (blank fields), all 7 rows.
BINNED_Z8_BLANK = [
    (-21.85, 0.000003, 0.000002, 0.000002),
    (-21.35, 0.000012, 0.000004, 0.000004),
    (-20.85, 0.000041, 0.000011, 0.000011),
    (-20.10, 0.000120, 0.000040, 0.000040),
    (-19.35, 0.000657, 0.000233, 0.000233),
    (-18.60, 0.001100, 0.000340, 0.000340),
    (-17.60, 0.003020, 0.001140, 0.001140),
]
# Bouwens et al. 2022 (arXiv:2205.11526) Table 4, z ~ 8 column (HFF cluster fields), rows brighter
# than -15.0 (primary fit).
BINNED_Z8_LENS = [
    (-18.75, 0.0018, 0.0006, 0.0006),
    (-18.25, 0.0016, 0.0007, 0.0007),
    (-17.75, 0.0037, 0.0012, 0.0012),
    (-17.25, 0.0058, 0.0023, 0.0020),
    (-16.75, 0.0063, 0.0040, 0.0030),
    (-16.25, 0.019, 0.013, 0.008),
    (-15.75, 0.016, 0.018, 0.011),
    (-15.25, 0.014, 0.026, 0.011),
]
# the four fainter rows (sensitivity fit only); -14.75 is a 1-sigma upper limit
BINNED_Z8_LENS_FAINT = [
    (-14.25, 0.11, 0.23, 0.09),
    (-13.75, 0.53, 1.03, 0.39),
    (-13.25, 0.20, 0.99, 0.16),
]
BINNED_Z8_LENS_LIMITS = [(-14.75, 0.068)]
