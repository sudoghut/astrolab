"""theta_* and r_drag from CAMB for the R2-CAMB sensitivity check (README section 2, addendum
2026-11-16). Settings are pre-registered there: camb package defaults except the calls below.
Helper module: does not import run; callers pass every value as an argument."""
import camb

N_EFF = 3.044
T_CMB = 2.7255


def _params(H0, ombh2, omch2, w0, wa, mnu):
    p = camb.CAMBparams()
    p.set_cosmology(H0=H0, ombh2=ombh2, omch2=omch2, mnu=mnu, num_massive_neutrinos=1,
                    nnu=N_EFF, TCMB=T_CMB, YHe=None)
    p.set_dark_energy(w=w0, wa=wa, dark_energy_model="ppf")
    return p


def theta_rdrag(H0, ombh2, omch2, w0, wa, mnu):
    """(theta_*, r_drag [Mpc]) from the CAMB background; theta_* = thetastar / 100."""
    d = camb.get_background(_params(H0, ombh2, omch2, w0, wa, mnu)).get_derived_params()
    return d["thetastar"] / 100.0, d["rdrag"]


def settings(mnu):
    """What the results must record about the CAMB configuration."""
    p = _params(67.32, 0.022383, 0.12011, -1.0, 0.0, mnu)
    return {"camb_version": camb.__version__, "recombination": type(p.Recomb).__name__,
            "bbn_predictor": type(p.bbn_predictor).__name__, "YHe_at_reference": float(p.YHe),
            "nnu": N_EFF, "TCMB": T_CMB, "num_massive_neutrinos": 1,
            "neutrino_hierarchy": "degenerate (set_cosmology default)", "dark_energy_model": "ppf"}
