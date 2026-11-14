# Hubble tension: SH0ES distance ladder and host selection

> Sections 1-4 were written on 2026-11-14 BEFORE run.py and before any data were fetched
> (pre-registration; derived from part 3 of the wiki article
> [Study-003](https://github.com/sudoghut/astrolab/blob/main/docs/wiki/Study-003-hubble-tension-host-selection.md)
> and design plan 012). Later edits to them must carry a dated note.

## 1. Question

Riess et al. 2024 (arXiv:2408.11770) argue that the lower H0 found by the CCHP JWST program
(Freedman et al. 2025, arXiv:2408.06153) is "entirely consistent with differences in sample
selection": the same SH0ES Cepheid ladder, restricted to the CCHP-selected supernova hosts and the
NGC 4258 anchor, already gives a lower H0. Using the public SH0ES matrices of Riess et al. 2022
(R22, arXiv:2112.04510, section 2.1, Eq. 6):

1. **R1.** Does our generalised least squares (GLS) fit of the public y, L, C reproduce the
   authors' own solution (`lstsq_results.txt`) and, secondarily, R22's H0 = 73.04 ± 1.01?
2. **R2 (the test).** How much does H0 move, in 5 log H0, when (a) the anchors are reduced to
   NGC 4258 alone and (b) the Cepheid hosts are then reduced to the 10 CCHP-selected hosts? Is
   the host step significant, and is its size what the 2024 paper reports?
3. **R3 (descriptive).** On the same 10 hosts and 11 SNe Ia, how far apart are the SH0ES Cepheid
   ladder and the CCHP JWST TRGB distances (per host and in 5 log H0)?
4. **R4 (descriptive).** Where does the CCHP selection fall among random 10-host subsets?
5. **Cross-paper comparison (descriptive).** Published H0 values side by side.

The Lean argument (`argument/`) is about the paper's reasoning. This study tests one input of it
(the host-selection shift, R2) and explores the rest; it does not test the inference rule
`gap_rule`.

## 2. Hypotheses and decision criteria

All shifts and criteria are defined in **5 log H0 (mag)**: the GLS estimate is linear in y there,
so variances are exact (aᵀCa); km/s/Mpc values (H0 = 10^(q/5)) are illustrative only.
Tolerances are fixed here and are not changed after results are seen. Each criterion reports a
verdict, the numbers, and our explanation of any failure.

**Fit validity (before any criterion).** Every GLS fit must have full column rank after dropping
all-zero columns (`infer.gls` raises otherwise) and finite errors. The host-identification and
anchor rules of section 4 must pass their structural checks; if a check fails, every criterion
that depends on it is reported as **not evaluable**, with the reason.

**R1 (reproduction).**
- Primary: all 47 parameters agree with `lstsq_results.txt` to |Δq| ≤ 1×10⁻³ and
  |Δσ| ≤ 1×10⁻³ (same data and method, so this is an exact check of `infer.gls`, the FITS
  decoding and the column reading). Verdict: **reproduced** / **not reproduced** (with the worst
  parameter).
- Secondary: our 5 log H0 against R22's 9.318 (73.04). Not expected to match exactly: the public
  file's last entry is 9.32599 (about 73.3), a slightly different fit from the printed baseline
  (plan 012, section 2). Reported with the difference; nothing is tuned to close it.

**R2 (the test of the paper's selection claim).**
- *Anchor step* (all anchors → NGC 4258 only, all 37 hosts):
  Δ_a = 5 log H0(NGC 4258 only) − 5 log H0(baseline). Target: R22 Table 5 fit 10 (72.51 ± 1.54
  against 73.04), i.e. −0.0158 mag. **Reproduced** if |Δ_a − (−0.0158)| ≤ 0.005 mag; this also
  validates the anchor rule. arXiv:2408.11770 Table 4 (73.17 → 72.54, −0.0188) is a secondary
  reference, reported only.
- *Host step* (NGC 4258 only: 37 hosts → the 10 CCHP hosts): Δ_h = aᵀy with
  a = (A_sub S − A_full)ᵀ e (A: the GLS estimator matrices; S: the row selection; e: the last
  parameter), and σ_h² = aᵀCa exactly. Null hypothesis: host selection does not move H0
  (Δ_h = 0). Reference: 5 log10(71.2 / 72.54) = −0.0405 mag (our conversion of arXiv:2408.11770
  section III.2; that paper uses 2024 data and its Eq. 6 approximation, so the agreement tolerance
  adds 0.02 mag). Exactly one row applies:

  | Condition | Verdict |
  |---|---|
  | Δ_h/σ_h ≤ −2 and \|Δ_h − (−0.0405)\| ≤ 2σ_h + 0.02 | host selection significantly lowers H0, by the size the paper reports (supports the paper) |
  | Δ_h/σ_h ≤ −2, otherwise | host selection significantly lowers H0, but by a different size |
  | \|Δ_h/σ_h\| < 2 | no host-selection effect detected in these data (does not support the paper's quantitative claim) |
  | Δ_h/σ_h ≥ 2 | host selection raises H0 (contradicts the paper) |

**R3 (descriptive; no significance verdict).** CCHP's error budget was not mapped term by term
before data, so R3 stays descriptive (plan 012, section 4). Reported: per-host differences
Δμ_i = μ_Ceph,i − μ_TRGB,i (Cepheid distances from our NGC 4258-only fit on the 10 hosts; TRGB
from CCHP Table 2) with their χ² under Cov(z); and d = 5 log H0,SH0ES − 5 log H0,CCHP on the same
10 hosts, both from the joint estimator on z = (y, t) (section 4), with σ_d = √(bᵀ Cov(z) b) as an
indicative uncertainty. Before d is reported, our CCHP-side estimate is compared with CCHP's own
TRGB + Pantheon+ value 69.29 (arXiv:2408.06153 section X.5 and Table 5; 5 log H0 = 9.2034):
**matched** if within 0.02 mag; otherwise d is still reported, with the mismatch stated.
Sensitivity (reported only): CCHP's CSP-based 68.81.

**R4 (descriptive).** With NGC 4258 only, draw 10 of the 37 hosts without replacement
(`PARAMS["r4_draws"]` = 10,000, seed 0), refit each, and record Δ = 5 log H0(subset) −
5 log H0(37 hosts) and the number of calibrator SNe. Report the percentile of the CCHP selection's
Δ_h: between the 5th and 95th percentile → "consistent with random-subset fluctuations"; below
the 5th → "the selection itself is systematically low"; above the 95th → "systematically high".
Every outcome is compatible with the paper, so R4 is not a test of it.

**Cross-paper comparison (descriptive).** Pairwise differences over √(σa² + σb²) are interpreted
only for roughly independent pairs (distance ladder vs CMB, TDCOSMO vs ladder, TDCOSMO vs CMB);
the early-universe reference is the CMB-only 67.19 ± 0.38 (arXiv:2506.20707); TDCOSMO's
asymmetric error is taken on the side facing the other value. SH0ES, H0DN and CCHP share data:
their values are listed as "not independent, not interpreted" and are not averaged.

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| C (covariance, 3492 × 3492, big-endian float32 FITS) | `https://media.githubusercontent.com/media/PantheonPlusSH0ES/DataRelease/main/SH0ES_Data/allc_shoes_ceph_topantheonwt6.0_112221.fits` (Git LFS) via `ctx.http` | whole file; assert 48,781,440 bytes and SHA-256 `a42778672d25df7a559bd2949b1e412b99b2e35dd9a36895f6b38828be019172` | 46.5 MiB |
| L (equation matrix, 3492 × 47) | `https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/SH0ES_Data/alll_shoes_ceph_topantheonwt6.0_112221.fits` | whole file; assert shape | 0.66 MB |
| y (data vector, 3492) | same folder, `ally_shoes_ceph_topantheonwt6.0_112221.fits` | whole file; assert shape | 17 kB |
| Authors' least-squares solution | same folder, `lstsq_results.txt` | 47 rows "value error" | 0.7 kB |
| R22 Table 6 (42 SNe: host, SN, m⁰_B, μ_Ceph) | typed into `run.py` from arXiv:2112.04510 (PDF p. 30) | host-identification checks | 42 rows |
| CCHP Table 2 (JWST TRGB μ and σ_T; 10 hosts, 11 SNe) | typed into `run.py` from arXiv:2408.06153 v3 | R3 | 11 rows |

Total about 47.2 MiB: under the 200 MB study budget, and the largest file is under the 50 MiB
single-download limit. If an LFS download returns a pointer or an error page (size or hash
mismatch), the run stops. No TAP queries.

## 4. Method

**Parameter order** (R22 Eq. 6; checked against `lstsq_results.txt` in plan 012): columns 0–36 are
the host distance moduli μ₀,i in R22 Table 6 order (alphabetical: M101, M1337, N0105, …, U9391),
then ΔμN4258 (37), M^W_H,1 (38), ΔμLMC (39), μM31 (40), b_W (41), M⁰_B (42), Z_W (43), an extra
parameter (44; 0.00000 in the file), Δzp (45) and 5 log H0 (46).

**GLS.** `astrolab.infer.gls`: q̂ = (LᵀC⁻¹L)⁻¹LᵀC⁻¹y with Cholesky factors (no explicit inverse),
all-zero columns dropped, full column rank required; C is converted to native float64. A
subsystem takes the selected rows of y and L and the rows and columns of C (the marginal of a
Gaussian).

**Host identification (structural checks; all required).** Calibrator SN rows have a non-zero in
column 42 and in exactly one host column; Hubble-flow SN rows have non-zeros in columns 42 and 46
and in no host column. Required: 42 calibrator rows with per-host counts equal to Table 6 (2 in
N1448, 3 in N3147, 2 in N5468, 2 in N5643, 1 elsewhere); 277 Hubble-flow rows; and, within each
host, the sorted y values of its SN rows within 0.05 mag of the sorted Table 6 m⁰_B (Table 6
note d: those are approximations). Reported only: each host's fitted μ against Table 6 μ_Ceph.

**Anchor rule (NGC 4258 only; R22 section 6.2: drop the other anchors' geometric distances, keep
their Cepheids).** Drop the LMC detached-eclipsing-binary row (its only non-zero is in column 39)
and the Milky Way parallax rows (the rows with a non-zero in column 45, Δzp, the Gaia parallax
zero point, which only MW parallax rows carry; column 45 then drops out). Required: exactly one
LMC row and at least one MW row found, and the NGC 4258 maser row (its only non-zero is in
column 37) kept. Validated by the R2 anchor target.

**Host step.** From the NGC 4258-only system, drop every row with a non-zero in a host column
outside the CCHP set {M101, N1365, N2442, N3972, N4038, N4424, N4536, N4639, N5643, N7250}
(the Cepheids and SNe of the other 27 hosts); anchor and Hubble-flow rows are kept. Δ_h and σ_h
as in section 2, from `infer.gls(..., return_estimator=True)`.

**R3 joint estimator.** z = (y, t), t = the CCHP Table 2 μ_TRGB of the 10 hosts (one value per
host; N5643's two SNe share it). Cov(z): the y block is C; the t block is diag(σ_T²) plus
0.025² + 0.032² on every entry (the TRGB tip measurement in NGC 4258, 0.025 mag, and the maser
distance, 0.032 mag, both fully correlated across hosts; arXiv:2408.06153 sections V, VII.2 and
X); the y–t block is zero except Cov(t_i, maser row) = that row's variance in C (both carry the
same maser error, with the same sign). H0,SH0ES comes from the host-step subsystem; H0,CCHP from
the same subsystem with the 10 hosts' Cepheid rows removed and rows μ₀,i = t_i added. Both are
linear in z, so d = bᵀz and σ_d² = bᵀ Cov(z) b exactly; σ_d is indicative only (section 2).

**R4.** Random host subsets as in section 2, on the NGC 4258-only system, one GLS per draw.

**Parameters (`PARAMS` in `run.py`, saved with the results):** `cchp_hosts`, `r4_draws` (10,000),
`r4_seed` (0), `sn_match_tol` (0.05 mag), `trgb_tip_sys` (0.025 mag), `maser_sys` (0.032 mag; the
cross term uses the maser row's variance in C). Changing a committed `PARAMS` value amends this
pre-registration and needs a dated note.

**Systematics and limits.** The public matrices are not exactly the printed R22 baseline (R1).
The 2024 paper's numbers use newer data (SMC anchor, more Cepheids) and its Eq. 6 approximation,
hence the 0.02 mag allowance in R2. R3's covariance omits SN-photometry differences between the
two analyses: CCHP's 69.29 uses the same Pantheon+ magnitudes inside the R22 framework (Table 5
note d), so this term is expected to be small.

## 5. Results

Filled after running. Link to `web/index.html` and key numbers in `results/`.

## 6. Referee notes

Independent critique: selection effects, systematics, alternative explanations.

## 7. Open questions

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| TODO | | | |

- Rerun with an override: `python -m astrolab explore 003-m02-hubble-tension-distance-ladder --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about N s from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 003-m02-hubble-tension-distance-ladder --tag <topic> --script explore/<name>.py`.
- Results files and keys: TODO (`results/<file>.json`: key - meaning).
- Example questions: TODO (question -> knob or script an agent would use).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

