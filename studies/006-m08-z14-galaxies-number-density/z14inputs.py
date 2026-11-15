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
