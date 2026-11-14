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
  decoding and the column reading). A column that is all zero in L (expected: column 44, printed
  as 0.00000 ± 0.000) is not fitted; it passes if the file's value and error are both 0 within
  the same tolerance. Verdict: **reproduced** / **not reproduced** (with the worst parameter).
- Secondary: our 5 log H0 against R22's 9.318 (73.04). Not expected to match exactly: the public
  file's last entry is 9.32599 (about 73.3), a slightly different fit from the printed baseline
  (plan 012, section 2). Reported with the difference; nothing is tuned to close it.

**R2 (the test of the paper's selection claim).**
- *Anchor step* (all anchors → NGC 4258 only, all 37 hosts):
  Δ_a = 5 log H0(NGC 4258 only) − 5 log H0(baseline). Target: R22 Table 5 fit 10 (72.51 ± 1.54
  against 73.04), i.e. −0.0158 mag. **Reproduced** if |Δ_a − (−0.0158)| ≤ 0.005 mag **and** the
  NGC 4258-only σ(5 log H0) is within 15% of fit 10's 5 log10(e) × 1.54 / 72.51 = 0.0461 mag
  (Table 5's errors, like the baseline's 73.04 ± 1.01, are fit-only errors without the
  analysis-variant systematics; a
  fit that kept another anchor would have a clearly smaller σ; 15% allows for the public file
  not being the printed baseline). Both together validate the anchor rule. If the anchor step is
  not reproduced, the host step is still computed but its verdict is reported as **conditional
  (anchor rule not validated)**. arXiv:2408.11770 Table 4 (73.17 → 72.54, −0.0188) is a secondary
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
**matched** if within 0.02 mag; otherwise d is still reported, with the mismatch stated. The
per-host Δμ table does not depend on this step and is reported unchanged either way.
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
single-download limit. `ctx.http` follows the media.githubusercontent.com redirect; if an LFS
download returns a pointer or an error page, for example after the LFS bandwidth quota is
exhausted (size or hash mismatch), the run stops. No TAP queries.

## 4. Method

**Parameter order** (R22 Eq. 6; checked against `lstsq_results.txt` in plan 012): columns 0–36 are
the host distance moduli μ₀,i in R22 Table 6 order (alphabetical: M101, M1337, N0105, …, U9391),
then ΔμN4258 (37), M^W_H,1 (38), ΔμLMC (39), μM31 (40), b_W (41), M⁰_B (42), Z_W (43), an extra
parameter (44; 0.00000 in the file), zp (45; R22 section 4.2: "the difference between the ground
and HST zeropoints", carried by ground-based Cepheid rows and constrained by "0 = zp ± σgrnd") and
5 log H0 (46). In R22 Eq. 6 the anchors enter as external-constraint rows: y = M^W_H,1,HST
(−5.810, σ 0.054) and y = M^W_H,1,Gaia (−5.903, σ 0.024) for the Milky Way (R22 Table 4), and
rows y = 0 for ΔμN4258, ΔμLMC and zp; the NGC 4258 and LMC Cepheid rows carry
y = m − μ₀,anchor and a +1 in their Δμ column. There are no per-Cepheid Milky Way rows.

**GLS.** `astrolab.infer.gls`: q̂ = (LᵀC⁻¹L)⁻¹LᵀC⁻¹y with Cholesky factors (no explicit inverse),
all-zero columns dropped, full column rank required; C is converted to native float64. A
subsystem takes the selected rows of y and L and the rows and columns of C (the marginal of a
Gaussian).

**Row classes (reported, must sum to 3492).** Calibrator SN rows: a non-zero in column 42 and in
exactly one host column. R22 section 4.8 uses "77 sets in all for 42 SNe Ia" (several light-curve
sets per SN), so 77 such rows are expected, not 42. Hubble-flow SN rows: non-zeros in columns 42
and 46 and in no host column (R22: 277 SNe; the count is reported, and nothing depends on it, since
these rows are kept in every subsystem). Single-non-zero constraint rows (expected 5: two in
column 38, one each in columns 37, 39, 45). The rest are Cepheid rows.

**Host identification (structural checks; all required).** (i) 77 calibrator rows, every host
column 0–36 having at least one; (ii) within each host, every SN row's y is within
`sn_match_tol` = 0.15 mag of some Table 6 m⁰_B of that host, and every Table 6 SN of that host is
matched by at least one row (the tolerance is wider than the Table 6 errors, 0.07–0.20 mag,
because Table 6 note d gives a simple average over surveys while each row is one survey's light
curve). In hosts with several SNe (N1448, N3147, N5468, N5643) rows are matched to the host, not
to individual SNe; no criterion needs a per-SN assignment (R2 and R4 select by host; R3 uses one
TRGB distance per host). (iii) Each host's fitted μ₀,i in the baseline fit within
3σ_Ceph + 0.02 mag of Table 6 μ_Ceph (column a; Table 6 prints no full-fit distance: column a
excludes that host's SNe and column b all SNe, so the 3σ allowance also covers the pull of the
host's own SNe). (iv) Each host's Cepheid row count (rows with a non-zero in that host column and
in column 38) within 2 of R22 Table 3's "fit" count (e.g. M101 259, N1448 73, N5643 251; 2150 in
all), typed into `run.py`; the allowance covers the public file not being exactly the printed
fit. (v) **Swap test**: for every pair of host columns, swap their labels and re-apply (ii)–(iv);
if any swapped labelling also passes all of them, the identification of that pair is ambiguous.
An ambiguous pair that involves a CCHP host makes R2's host step, R3 and R4 **not evaluable**;
other ambiguous pairs are reported (they affect only R4's random subsets, which treat all
non-CCHP hosts alike, and only through which non-CCHP host carries which label). Reported: the
worst host for each check and the list of ambiguous pairs.

**Anchor rule (NGC 4258 only; R22 section 6.2: drop the other anchors' geometric distances, keep
their Cepheids).** Drop the LMC detached-eclipsing-binary row (only non-zero in column 39, y = 0)
and the two Milky Way rows (only non-zero in column 38, y within 0.2 mag of −5.85). Keep the
NGC 4258 maser row (only non-zero in column 37, y = 0), the zp constraint row and every row with
a non-zero in column 45. Required: exactly one LMC row, exactly two MW rows and exactly one maser
row found. ΔμLMC is then fixed by the LMC Cepheids relative to NGC 4258, as in R22's fit 10.
Validated by the R2 anchor target (shift and σ).

**Host step.** From the NGC 4258-only system, drop every row with a non-zero in a host column
outside the CCHP set {M101, N1365, N2442, N3972, N4038, N4424, N4536, N4639, N5643, N7250}
(the Cepheids and SNe of the other 27 hosts); anchor and Hubble-flow rows are kept. Δ_h and σ_h
as in section 2, from `infer.gls(..., return_estimator=True)`.

**R3 joint estimator.** z = (y, t), t = the CCHP Table 2 μ_TRGB of the 10 hosts (one value per
host; N5643's two SNe share it). Cov(z): the y block is C; the t block is diag(σ_T²) plus
0.025² + σ_m² on every entry, where 0.025 mag is the TRGB tip measurement in NGC 4258 and σ_m² is
the maser row's variance in C (R22's 0.032 mag), both fully correlated across hosts
(arXiv:2408.06153 sections V, VII.2 and X; we read Table 2's σ_T as excluding these zero-point
terms, since CCHP section X adds them separately "for each SN Ia-host distance average"). The y–t
block is zero except Cov(t_i, maser row) = k·c·σ_m², where k is the maser row's column-37 entry and
c the NGC 4258 Cepheid rows' column-37 entry (both must be ±1, else R3 is not evaluable). Derivation:
a maser modulus too high by ε makes every t_i too high by ε, the fitted ΔμN4258 low by ε through
the NGC 4258 Cepheid rows (y = m − μ₀,N4258, coefficient c), and the maser row's error k·c·ε; with
k = c = +1 the cross term is +σ_m².
H0,SH0ES comes from the host-step subsystem. H0,CCHP is a GLS on the same subsystem with the 10
hosts' Cepheid rows removed and the rows μ₀,i = t_i added, weighted by the matching block of
Cov(z) (C for the y rows, the t block, and the cross term). Both are linear in z, so d = bᵀz and
σ_d² = bᵀ Cov(z) b exactly; σ_d is indicative only (section 2). Sensitivity (reported only): d
and the CCHP-side H0 with the t-block zero-point terms removed.

**R4.** Random host subsets as in section 2, on the NGC 4258-only system, one GLS per draw.
Runtime estimate: each draw factorises a C sub-block of roughly 1500–2500 rows (0.05–0.2 s), so
10,000 draws take roughly 10–30 min; the subsystem's row indices are precomputed per host. An
exploration that changes `r4_draws` reruns all draws.

**Parameters (`PARAMS` in `run.py`, saved with the results):** `cchp_hosts`, `r4_draws` (10,000),
`r4_seed` (0), `sn_match_tol` (0.15 mag), `trgb_tip_sys` (0.025 mag). The maser variance is read
from C. Changing a committed `PARAMS` value amends this pre-registration and needs a dated note.

**Systematics and limits.** The public matrices are not exactly the printed R22 baseline (R1).
The 2024 paper's numbers use newer data (SMC anchor, more Cepheids) and its Eq. 6 approximation,
hence the 0.02 mag allowance in R2. R3's covariance omits SN-photometry differences between the
two analyses: CCHP's 69.29 uses the same Pantheon+ magnitudes inside the R22 framework (Table 5
note d), so this term is expected to be small. Our CCHP-side estimate fits all 77 light-curve rows
of the 11 SNe with C, whereas CCHP applied one peak m_B per SN to R22's NGC 4258 fit (fit 10,
M_B = −19.269); the 0.02 mag "matched" tolerance in R3 is the guard for this difference.

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

