# Hubble tension: SH0ES distance ladder and host selection

> 中文：[README.zh.md](README.zh.md)

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
all-zero columns (`infer.gls` raises otherwise: the smallest eigenvalue of the column-normalised
LᵀC⁻¹L must exceed `rank_rtol` = 10⁻¹² times the largest) and finite errors. The host-identification and
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

### Addendum 2026-11-16: R2-RE, host step with a host-level random effect (T-023, plan 021), pre-registered before any random-effect fit

*Why.* R2's host step uses errors propagated from C. Across random 10-host subsets (R4) the ratio
Δ/σ scatters by 1.33 rather than 1, which suggests that C understates host-to-host scatter; with
σ inflated by that factor the verdict table would flip (referee point 1, section 6). Inflating by
an empirical spread is post hoc; this addendum fixes a model-based test in advance.

*Seen before this addendum.* All results in sections 5 and 6 (R1-R4, the 1.33 spread, the CCHP
host shift −0.0730 ± 0.0331 mag, z = −2.21), so the direction is known: more host scatter weakens
the host-step significance. REML (below) was chosen over ML knowing this; it is the standard
estimator for a variance component and gives the larger τ than ML. No random-effect variance has
been estimated or tried, and the section 7 leave-one-host-out χ² exploration has not been run.

*Model.* In the NGC 4258-only system (R2's anchor-step rows: all rows except the LMC and the two
Milky Way constraint rows, about 3489), each calibrator host j gets an additive offset shared by
all its calibrator SN rows (rows with a non-zero in the M⁰_B column and in exactly one host
column, `row_classes`' `calib`), Gaussian with variance τ²:
V(τ) = C + τ² Σ_j h_j h_jᵀ, where h_j is the indicator of host j's calibrator SN rows. τ is one
number for all 37 hosts (the minimal one-parameter model; with 37 groups τ̂ is poorly constrained,
hence the interval below). Other rows are unchanged. Placement: a random effect on the host
distance μ₀,j itself is not identifiable (μ₀,j is a free parameter and absorbs it); the same
offset on host j's Cepheid rows instead of its SN rows is a different covariance direction and is
reported as a sensitivity check (estimated and applied in the same way), not used for the verdict.
A per-SN effect is not available (the light-curve rows are matched to hosts, not to SNe,
section 4) and would equal the per-host one for single-SN hosts. For single-SN hosts τ is
indistinguishable from extra scatter of calibrator SNe relative to their Cepheid distance; that is
what τ measures.

- **Estimate.** τ̂ by restricted maximum likelihood (REML) on that
  system: −2ℓ_R(τ) = log det V + log det(Xᵀ V⁻¹ X) + rᵀ V⁻¹ r, with X the columns of L fitted in
  that system (`infer.gls`'s `kept`) on those rows, r the GLS residual under V, and all constraint
  rows kept (their τ-independent terms are constants). Search: a grid τ = 0, 0.01, …, 0.50 mag,
  then `scipy.optimize.minimize_scalar` (method "bounded", xatol 10⁻⁵) on the grid interval around
  the grid's global minimum (at an end point, the one adjacent interval); τ̂ is the better of the
  refined and the grid minimum (the grid minimum if the refinement fails). Other local minima of
  the grid are reported. τ̂ < 10⁻³ counts as zero (V = C; R2-RE then equals R2). τ̂ > 0.5 − 10⁻³ is
  "at the upper bound": R2-RE is **not evaluable (bound)**.
- **Interval.** The 68% interval is where −2ℓ_R exceeds its minimum by 1, found by root finding
  (`brentq`) on each side of τ̂, at the crossing nearest to τ̂ (scanning the grid outward from τ̂ to
  the first grid point above the threshold, then `brentq` within that grid interval); the lower end is 0 if −2ℓ_R(0) is within 1 of the minimum; the
  upper end is reported as "> 0.5" if not reached by 0.5, and as "not determined" if the root
  search fails.
- **Host step under V(τ̂).** As R2's host step with C replaced by V(τ̂) in both fits and in the
  shift variance: Δ_h' = 5 log H0(10 CCHP hosts) − 5 log H0(37 hosts), σ_h'² = a'ᵀ V a', z' = Δ_h'/σ_h',
  with the host labelling of the 2026-11-14 run (amended, section 4 note); R2-RE inherits R2's
  labels (amended post-data labelling) and its anchor-step status rule.
- **Rule.** R2's verdict table unchanged (z' ≤ −2 with |Δ_h' − (−0.0405)| ≤ 2σ_h' + 0.02 → "supports
  the paper"; z' ≤ −2 otherwise → "different size"; |z'| < 2 → "no host-selection effect
  detected"; z' ≥ 2 → "raises H0").
- **Validity.** V positive definite numerically (Cholesky succeeds) and both GLS fits succeed; else
  R2-RE is **not evaluable (fit)**.
- **Headline, fixed now.** The R2-RE verdict row, whatever it is, becomes the headline host-step
  verdict in section 5, `summary.json` (`R2_host`) and the claim, and replaces the inflated-σ
  sentence in the public `verdict` of `r2.json` and on the web page. R2 (C errors) stays recorded as the pre-registered
  outcome of 2026-11-14 (`criterion_outcome`, `R2_host_preregistered`). The inflated-σ figure and
  the diagnostics below are labelled descriptive and cannot override R2-RE. If R2-RE is not
  evaluable, the headline stays R2 with its existing qualification, labelled as such.
- **Reported, not decisive.** z' at the upper end of the τ interval (if finite); R4 rerun under
  V(τ̂) with exactly the draws R4 ends with (same seed, same count): the 37-host system is fitted
  once under V and each draw refits only its subset under V, σ'² = σ²_sub,V − σ²_full,V. Derivation:
  both are GLS estimators under the same V (the subset uses V's sub-block), the full one is the
  best linear unbiased estimator on the full data and the subset one is another linear unbiased
  estimator on the same data, so Cov(full, sub) = Var(full) and Var(sub − full) = Var(sub) −
  Var(full) for any V; checked exactly with a'ᵀ V a' on the R2-RE host step and on the first draw, the spread of Δ/σ' (near 1 if τ absorbs the excess) and the CCHP percentile of z'; the
  host-level χ² of the 37 leave-one-host-out SN residuals under C and under V(τ̂): for each host j,
  refit the 37-host system without host j's calibrator SN rows (its Cepheids kept), predict those
  rows, and form r_jᵀ S_j⁻¹ r_j with S_j = W_jj + X_j Cov(q̂) X_jᵀ (W = C or V); report the sum and its
  number of SN rows, compared with χ² with that many degrees of freedom.
- **Runtime.** One REML evaluation is a Cholesky of a 3489 × 3489 matrix (about 0.3 s); the grid,
  refinement and interval take about 1 min. R4 under V costs about as much as R4 (8-15 min).

### Addendum 2026-11-17: R2-RE-ROB, robustness of R2-RE to single hosts and under the null (T-032), pre-registered before any of these fits

Revised the same day after the gate-1 review, still before any of these fits.

*Why.* The R2-RE referee (section 6) found that τ̂ may rest on a few non-CCHP hosts (largest
leave-one-out χ² terms N5584, N2525, N1015) and that neither τ̂ nor R4's 1.33 spread was calibrated
against the null of no host-level scatter. *Seen before this addendum:* all of section 5 and the
R2-RE results (τ̂ = 0.077 mag, interval 0.048–0.105, Δ(−2ℓ_R) = 3.50 at τ = 0, z' = −1.53, the
per-host leave-one-out χ² terms, the 1.33 spread under C and 1.005 under V). From Δ(−2ℓ_R) = 3.50 the
asymptotic boundary likelihood-ratio p-value is 0.5 · P(χ²₁ > 3.5) ≈ 0.031, so B's τ part is expected
to land near 0.03; the three-way label below exists because of that. At a true p of 0.031 the τ label
comes out "undetermined" with probability about 0.6 and "unusual" about 0.4; "undetermined" is
therefore the expected outcome, and more simulations after the run would need a new pre-registration. No fit without a host and no
simulation has been run (dated note 2026-11-17: a code smoke run later showed part of A before the
formal run; disclosed in log.md, the rules unchanged). These checks attach descriptive labels to R2-RE; they do not change the
R2-RE headline row.

Common settings: hosts are the 37 calibrator hosts with the column labels of the amended (post-data)
host labelling (`col_host`), as in R2-RE; τ̂ is found by R2-RE's REML procedure (grid 0, 0.01, …,
0.50 mag, then the bounded refinement; no interval), τ̂ < 10⁻³ counts as zero (V = C) and
τ̂ > 0.5 − 10⁻³ is "at the upper bound".

*A. Leave one host out.* For each host j, the rows with a non-zero in host j's column (its Cepheid
and calibrator SN rows) are removed from the NGC 4258-only system, and τ̂_j is estimated with the
other 36 hosts' groups. Then:
- **τ route (the label).** R2-RE's original host step (all 37 hosts against the 10 CCHP hosts, all
  data) under V = C + τ̂_j² Σ h h ᵀ over all 37 hosts' calibrator groups on the full NGC 4258-only system, and its verdict row (R2's table, unchanged). Label: **"verdict robust to single
  hosts' influence on τ̂"** if this row equals R2-RE's row for every j; otherwise **"verdict
  sensitive to single hosts' influence on τ̂"**, naming the hosts. The label is about the verdict
  row, not about τ̂ itself: τ̂_j and its range are reported, and a host whose removal moves τ̂ a lot
  while the row holds is named in section 5. A τ̂_j at the upper bound, a failed REML fit or a failed host-step fit counts as "sensitive" for
  that j. If R2-RE itself is not evaluable (no verdict row to compare), A is not evaluable.
- **Data route (reported).** On the reduced system: the host step at τ = 0 (C) and under V(τ̂_j),
  each with z and the verdict row; when j is a CCHP host the CCHP subset has 9 hosts and the entry is
  marked "changes the tested selection".
Reported: τ̂_j, the three z values and rows for every host, and their ranges.

*B. Null simulations.* Under C, fit the NGC 4258-only system (R2's anchor-step rows, `rows_a`) and
take ŷ = L q̂ on those rows. Simulation s draws y_s = ŷ + K ε_s, with K the lower Cholesky factor of
C restricted to `rows_a` and ε_s = `numpy.random.default_rng(10_000 + s).standard_normal(len(rows_a))`.
(Under C both statistics below have the same null distribution for any q̂: REML uses only residual
contrasts, and each Δ_k/σ_k is exactly N(0, 1).)
- **τ part.** s = 0, …, 399: τ̂_s by the procedure above. n_τ = simulations whose fit succeeded;
  k_τ = those with τ̂_s ≥ τ̂_obs (R2-RE's τ̂); p_τ = (1 + k_τ) / (1 + n_τ), with a 95% Clopper–Pearson
  interval for k_τ / n_τ (two-sided, equal-tailed: 2.5% in each tail). Labels: interval entirely below 0.05 → **"τ̂ unusual under C (excess
  calibrator scatter)"**; entirely above 0.05 → **"τ̂ not unusual under C"**; containing 0.05 →
  **"undetermined (Monte Carlo)"**. More than 20 failed fits → not evaluable; with 20
  or fewer, p_τ and the interval use the n_τ successful fits.
- **Spread part.** The first 1,000 of R4's random 10-host subsets (R4's own draws: same seed, in
  order; all of them if R4 ended with fewer). For subset k the shift Δ_k = a_kᵀ y is linear in y with
  a fixed σ_k (σ_k² = σ²_subset − σ²_37 under C, as in R4); the rows a_k are computed once. spread =
  the standard deviation of Δ_k/σ_k over the subsets (`numpy.std`, ddof = 0, as in R4); spread_obs on
  the real data with the same subsets. s = 0, …, 1,999: spread_s; p_spread = (1 + k_s) / 2,001 with
  k_s = #{spread_s ≥ spread_obs}. Labels, with the same 95% Clopper–Pearson interval for k_s / 2,000: entirely below 0.05 → **"the R4
  excess spread is unusual under C"**; entirely above → **"the R4 spread is consistent with C"**;
  containing 0.05 → **"undetermined (Monte Carlo)"**.
- If R2-RE is not evaluable, the τ part is not evaluable; if R4 has no draws, the spread part is not
  evaluable.

*Reading, fixed now.* The R2-RE headline row stands as pre-registered. The labels are reported next
to it in section 5 and the claim, read as follows: "verdict robust" with "τ̂ unusual under C" →
the null result rests on excess calibrator scatter that the data show, and no single host's effect
on τ̂ changes the verdict; "verdict robust" with "not unusual" or "undetermined" → the null result
rests on a τ the data do not clearly require; "verdict sensitive" → the null result depends on the
named hosts' effect on τ̂. The spread label says
whether R4's 1.33 is itself evidence of excess scatter under C. "Unusual under C" means more scatter
among calibrator SN rows than C allows (for example a host-level effect, an under-scaled SN block or
one outlying host); it does not identify the cause.

*Runtime (estimates).* A: 37 REML fits plus about 222 host-step fits, about 25 minutes. B: 400 REML
fits (about 20–35 s each, about 3.5 hours; up to about 6 hours if another long run shares the CPU)
and 1,000 subset fits once (about 2 minutes). `PARAMS["rob_check"]`
turns both off.

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| C (covariance, 3492 × 3492, big-endian float32 FITS) | `https://media.githubusercontent.com/media/PantheonPlusSH0ES/DataRelease/main/SH0ES_Data/allc_shoes_ceph_topantheonwt6.0_112221.fits` (Git LFS) via `ctx.http` | whole file; assert 48,781,440 bytes and SHA-256 `a42778672d25df7a559bd2949b1e412b99b2e35dd9a36895f6b38828be019172` | 46.5 MiB |
| L (equation matrix, 3492 × 47) | `https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/main/SH0ES_Data/alll_shoes_ceph_topantheonwt6.0_112221.fits` | whole file via `ctx.http`; assert shape | 0.66 MB (about 0.69 × 10⁶ bytes; exact size recorded in the provenance) |
| y (data vector, 3492) | same folder, `ally_shoes_ceph_topantheonwt6.0_112221.fits` | whole file via `ctx.http`; assert shape | 17 kB (about 1.7 × 10⁴ bytes; exact size recorded in the provenance) |
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
column 38, one each in columns 37, 39, 45). The rest are Cepheid rows: rows with a non-zero in
column 38 and in no column 42; those with a host column are SN-host Cepheids, expected
2149 ± 37 (sum of R22 Table 3's per-host "fit" counts; see the dated note below; the allowance is check (iv)'s ±1 per host on average), and the
count is asserted.

**Host identification (structural checks; all required).** (i) 77 calibrator rows, every host
column 0–36 having at least one; (ii) within each host, every SN row's y is within
`sn_match_tol` = 0.15 mag of some Table 6 m⁰_B of that host, and every Table 6 SN of that host is
matched by at least one row (the tolerance is wider than the Table 6 errors, 0.07–0.20 mag,
because Table 6 note d gives a simple average over surveys while each row is one survey's light
curve). In hosts with several SNe (N1448, N3147, N5468, N5643) rows are matched to the host, not
to individual SNe; no criterion needs a per-SN assignment (R2 and R4 select by host; R3 uses one
TRGB distance per host). Check (ii) validates host membership only: the 77 light-curve rows are
not expected to map one-to-one onto the 42 SNe, and several rows may match the same SN. (iii) Each host's fitted μ₀,i in the baseline fit within
3σ_Ceph + 0.02 mag of Table 6 μ_Ceph (column a; Table 6 prints no full-fit distance: column a
excludes that host's SNe and column b all SNe, so the 3σ allowance also covers the pull of the
host's own SNe). (iv) Each host's Cepheid row count (rows with a non-zero in that host column and
in column 38) within 2 of R22 Table 3's "fit" count (e.g. M101 259, N1448 73, N5643 251; 2149 in
all), typed into `run.py` from the rendered table (the PDF text layer misaligns its columns), with
an assertion that the typed counts sum to 2149; the allowance covers the public file not being
exactly the printed fit. (v) **Uniqueness of the labelling (global assignment)**, run only after
(i)–(iv) pass under the labelling of this section (if they fail, the fit-validity rule applies:
not evaluable). Checks (ii)–(iv) each compare one column with one Table 3/6 host, so they define
a bipartite compatibility graph between the 37 columns and the 37 hosts. The labelling of this
section is one perfect matching in it. For every compatible off-diagonal edge (column j, host h),
we test with `scipy.optimize.linear_sum_assignment` (cost 0 for compatible edges, 1 otherwise;
edge (j, h) forced) whether another perfect matching of cost 0 exists. Every alternative matching
is found this way, whatever its cycle length. If an alternative exists that changes which
columns are CCHP hosts, R2's host step, R3 and R4 are **not evaluable**. If the alternatives only
permute CCHP hosts among themselves, only R3's per-host Δμ table and its χ² are affected
(reported with that caveat). If they only permute non-CCHP hosts, nothing is affected (R4 treats
non-CCHP hosts alike). Reported: the worst host for each check and every compatible off-diagonal
edge.

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

**R3 joint estimator.** z = (y, t), where t has exactly 10 entries, one μ_TRGB per host from CCHP
Table 2 (Table 2 lists SNe, so it prints N5643's single host distance twice, for 2013aa and
2017cbv; that is one measurement and enters t once). Cov(z): the y block is C; the t block is diag(σ_T²) plus
0.025² + σ_m² on every entry, where 0.025 mag is the TRGB tip measurement in NGC 4258 and σ_m² is
the maser row's variance in C (R22's 0.032 mag), both fully correlated across hosts
(arXiv:2408.06153 sections V, VII.2 and X; we read Table 2's σ_T as excluding these zero-point
terms, since CCHP section X adds them separately "for each SN Ia-host distance average"). The y–t
block is zero except Cov(t_i, maser row) = k·c·σ_m², where k is the maser row's column-37 entry and
c the NGC 4258 Cepheid rows' column-37 entry (both must be ±1, else R3 is not evaluable). Derivation:
a maser modulus too high by ε makes every t_i too high by ε, the fitted ΔμN4258 low by ε through
the NGC 4258 Cepheid rows (y = m − μ₀,N4258, coefficient c), and the maser row's error k·c·ε; with
k = c = +1 the cross term is +σ_m².
Both estimators are written as linear maps on the full z (length 3492 + 10).
H0,SH0ES comes from the host-step subsystem: its coefficient vector b_S is e_Hᵀ A_sub placed on that
subsystem's y rows, zero elsewhere (A_sub from `infer.gls(..., return_estimator=True)`, e_H the
5 log H0 row). H0,CCHP is a GLS on the same subsystem with the 10 hosts' Cepheid rows removed and
the 10 rows μ₀,i = t_i added (L rows with a single 1 in host column i), weighted by the matching
sub-block of Cov(z) (C for the y rows, the t block, and the y–t cross term): its coefficient vector
b_C is e_Hᵀ A_CCHP placed on those y rows and the t entries, zero elsewhere. Then
d = bᵀz with b = b_S − b_C, and σ_d² = bᵀ Cov(z) b exactly; this includes their covariance through
the shared y rows (anchors, SNe, Hubble flow) and the maser cross term. σ_d is indicative only
(section 2). The per-host Δμ_i use the same construction (b for μ₀,i of the SH0ES fit minus e_i on t). Sensitivity (reported only): d
and the CCHP-side H0 with the t-block zero-point terms removed.

**R4.** Random host subsets as in section 2, on the NGC 4258-only system, one GLS per draw.
Runtime, measured before any data on this machine with `infer.gls` on synthetic dense matrices
(sub-block extraction included): 0.021 s at 1500 rows, 0.046 s at 2000, 0.081 s at 2500. A draw
has about 980 anchor Cepheid rows, ten hosts' Cepheids (about 600), 277 Hubble-flow rows and the
constraint rows, so about 1900 rows and 0.05 s: 10,000 draws take about 8 min. Guard
(pre-registered): the first 100 draws are timed; if the projection for all draws exceeds 60 min,
`r4_draws` drops to the largest multiple of 1000 that fits in 60 min, and the change is recorded
in the results. If even 2000 draws would exceed 60 min, R4 is not run and is reported as
**not evaluated (runtime)**. The subsystem's row indices are precomputed per host. An
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

> **Dated note (2026-11-14, before any data were fetched).** Transcribing R22 Table 3 from the
> rendered PDF table showed that its per-host "fit" counts sum to 2149, while the printed
> "SN Total" is 2150; 2149 + 443 + 55 + 339 + 143 = 3129 equals the printed "Total All", so 2150
> is the table's own inconsistency. The expected SN-host Cepheid count and the assertion in
> `run.py` use 2149 (section 4). No criterion or tolerance changed.

> **Dated amendment (2026-11-14, AFTER the first run; a deviation from the pre-registration).**
> The first run showed that the columns of L are not in R22 Table 6 order (check (ii) failed for
> most hosts; for example the column assumed to be N1365 holds SN magnitudes 12.254 and 11.752,
> which are N1448's two SNe). As pre-registered, the R2 host step, R3 and R4 are therefore
> **not evaluable** under the labelling of section 4, and that verdict is reported. Amendment:
> the columns are relabelled by the perfect matching of the compatibility graph of checks
> (ii)–(iv) (`scipy.optimize.linear_sum_assignment`), accepted only if every matched edge passes
> (ii)–(iv), checks (i) and the Cepheid total pass, and check (v) finds no alternative matching
> that changes the CCHP set. In this amended labelling, check (ii) compares the mean of a column's
> SN rows with the mean of the host's Table 6 m⁰_B (tolerance unchanged, 0.15 mag): Table 6 note d
> says its m⁰_B is a simple average over surveys, and a per-row comparison failed for one host only
> (N1015: rows 13.499, 13.124, 13.427 against 13.350; their mean is 13.350). Ties among compatible
> labellings are broken by the smallest summed |μ_fit − μ_Ceph(a)|/σ(a) (implemented as a tiny
> cost, far below 1, added to every compatible edge). The relabelling uses only SN magnitudes, Cepheid counts and host
> distances, never an H0 result. Results under it are reported separately and labelled
> "amended (post-data labelling)". The decision criteria and tolerances of section 2 are unchanged;
> the identification check (ii) is changed as described. (The shift printed by
> the first run under the wrong labelling is meaningless and is not used.)

## 5. Results

Run of 2026-11-14 (`python -m astrolab run 003`; inputs 47.2 MiB, size and SHA-256 checks
passed; page: [`web/index.html`](web/index.html); numbers in `results/*.json`).

| Criterion | Ours | Target | Verdict |
|---|---|---|---|
| R1 primary: 47 parameters vs `lstsq_results.txt` | max \|Δq\| 0.050 (column 3, which holds N1015) | ≤ 0.001 | **not reproduced** |
| R1 secondary: R22 printed baseline | 5 log H0 = 9.3179 ± 0.0299 (H0 73.04); χ²/dof = 3552.8/3445 = 1.031 | 9.318 (73.04); 1.03 | matches |
| R2 anchor step | −0.0184 mag; σ(5 log H0) 0.0461 | −0.0158 ± 0.005; 0.0461 ± 15% | **reproduced** |
| R2 host step, pre-registered labelling | — | — | **not evaluable** (host identification) |
| R2 host step, amended labelling | Δ_h = −0.0730 ± 0.0331 mag (−2.21σ); H0 72.42 → 70.03 | −0.0405 ± (2σ + 0.02) | significantly lowers H0, by the size the paper reports — **amended, post-data** (labelling and check (ii) changed); 2.2σ with C-propagated errors, about 1.7σ on the random-subset scale (itself uncertain) |
| **R2-RE host step (headline since 2026-11-16)** | Δ_h' = −0.0618 ± 0.0404 mag (z' = −1.53) with τ̂ = 0.077 mag | R2's table | **no host-selection effect detected** — amended labelling; see the R2-RE subsection |
| R3 CCHP-side H0, same 10 hosts (amended) | 69.70 (Δ = +0.013 mag) | 69.29 ± 0.02 mag | matched |
| R3 d = SH0ES − CCHP, same hosts (amended) | +0.010 ± 0.048 mag (≈ +0.3 km/s/Mpc); per-host χ² 5.1 / 10 | — | descriptive |
| R4 percentile of the CCHP host shift (amended) | 5.7th of 10,000 draws (spread σ = 0.046 mag); 4.7th in Δ/σ | 5th–95th | consistent with random-subset fluctuations |

- **R1.** Our GLS reproduces R22's printed baseline to rounding (5 log H0, M⁰_B −19.2529,
  Z_W −0.2166, ΔμN4258 −0.0127, ΔμLMC 0.0101, χ²/dof 1.031). The public `lstsq_results.txt` is a
  different fit (5 log H0 9.326, about 73.3, host distances off by up to 0.05 mag), so the
  pre-registered primary target was the wrong one; the pre-registered verdict stands.
- **Host identification.** The columns of L are not in R22 Table 6 order (for example, N0976 is
  the second-to-last host column). Under the pre-registered labelling the R2 host step, R3 and R4
  are not evaluable. Under the dated amendment (section 4 note) every host gets a column; the CCHP
  set is unique. Six compatible edges lie in alternative matchings; they form three pairwise swaps
  (N4038 ↔ N4639, both CCHP hosts, which only touches R3's per-host table; N2608 ↔ N5728 and
  N3021 ↔ N5917, both non-CCHP), so 7 alternative labellings exist, none changing the CCHP set.
  The SN means decide N4038 against N4639 outright (offsets 0.000 and 0.045 mag), as does the
  tie-break. Under the chosen labelling every column's mean SN magnitude is within 0.001 mag of
  Table 6, every Cepheid count equals Table 3 except N1365 (46 against 45), and every
  |Δμ/σ(a)| ≤ 1.71.
- **Row classes vs section 4.** Section 4 expected 5 single-non-zero constraint rows; the data have
  8: the extra three constrain Z_W (y = −0.215), b_W (y = 0) and column 44 (y = 0). Column 44 is
  therefore fitted (σ 3 × 10⁻⁵), not all-zero as section 2 assumed for R1; it still passes R1's
  tolerance. The anchor rule selects rows by column and is unaffected.
- **R2.** Under the amended labelling the pre-registered table gives "significantly lowers H0, by
  the size the paper reports": dropping to NGC 4258 costs −0.6 km/s/Mpc and restricting to the
  CCHP hosts a further −2.4 km/s/Mpc (illustrative), a 2.2σ shift. Two qualifications. (1) Our
  shift is 1.8 times the paper's (−0.073 against −0.0405 mag, −2.4 against −1.3 km/s/Mpc); it is
  consistent only within the wide pre-registered tolerance (±0.086 mag). (2) The 2.2σ uses the
  C-propagated σ. Across random 10-host subsets (R4) the same ratio Δ/σ has a spread of 1.33, not
  1, which suggests that C may understate host-to-host scatter (the draws share one data set and
  37 hosts, so the 1.33 is itself uncertain); the CCHP ratio (−2.21) sits at the 4.7th percentile
  of that empirical distribution, about 1.7σ on that scale (a descriptive diagnostic added after the
  first results, at the gate-1 review). With σ inflated by that factor the pre-registered verdict
  table would give "no host-selection effect detected" (referee point 1; a pre-registered test with
  a host-level random effect is T-023). **Overall (2026-11-14): in R22's data the CCHP hosts give a
  lower H0, by about 2σ at most; the evidence that the selection effect is significant is marginal.**
  **Headline since 2026-11-16 (R2-RE, pre-registered): no host-selection effect detected** once a
  host-level random effect is modelled (next subsection); the 2026-11-14 verdict above stays recorded.
- **R3.** On the same 10 hosts the SH0ES Cepheid ladder and CCHP's JWST TRGB distances give the
  same H0 within 0.01 mag (0.3 km/s/Mpc); no host deviates by more than 1.2σ.
- **R4.** The CCHP selection sits at the low edge (5.7th percentile) of random 10-host subsets:
  a large but not exceptional draw. Random subsets scatter by 0.046 mag (about 1.5 km/s/Mpc), more
  than the CCHP set's own σ_h = 0.033 (its Cepheid-rich hosts M101, N5643 and N2442 make it more
  precise than a typical subset); in units of each draw's own σ the CCHP set is at the 4.7th
  percentile (spread of Δ/σ: 1.33).
- **Cross-paper (descriptive).** SH0ES R22 vs CMB-only 5.3σ; TDCOSMO vs SH0ES −0.4σ; TDCOSMO vs
  CMB-only 1.3σ; CCHP TRGB vs CMB-only 1.6σ (`results/cross_paper.json`).

### R2-RE (addendum 2026-11-16, T-023)

Run of 2026-11-16 (`python -m astrolab run 003`, 1678 s; R1, the anchor and host steps with C, R3,
R4 and the host identification reproduce the 2026-11-14 numbers exactly). Numbers:
`results/r2_re.json`.

| Quantity | Value |
|---|---|
| τ̂ (REML, host-level random effect on calibrator SN rows) | 0.077 mag, 68% interval 0.048–0.105 (grid minimum refined; no other local minimum) |
| Host step under V(τ̂) | Δ_h' = −0.0618 ± 0.0404 mag, z' = −1.53 (H0 shift −2.0 km/s/Mpc) |
| Verdict row (R2's table, unchanged) | **no host-selection effect detected in these data (does not support the paper's quantitative claim)** — the headline host-step verdict, with the amended (post-data) host labelling |
| At the upper end of the τ interval (0.105) | z' = −1.25 |
| Same offset on the Cepheid rows | τ̂ and z' identical to 10⁻¹¹: an identity, not a sensitivity check (the two indicators add up to the host-distance column, so REML and the H0 estimate cannot tell them apart; referee, below) |
| R4 under V(τ̂), same 10,000 draws | spread of Δ/σ' = 1.005 (was 1.33 under C); CCHP z' at the 6.9th percentile, shift at the 7.6th |
| Leave-one-host-out χ² of the 77 calibrator SN rows | 64.9 under C, 52.4 under V (approximate, see note in the results) |

- The random effect accounts for the excess host-to-host scatter seen in R4: under V the random
  subsets' Δ/σ' spread is 1.005, as expected for correctly scaled errors. With that scatter included
  the CCHP shift is −0.062 ± 0.040 mag, 1.5σ, and the pre-registered table gives "no host-selection
  effect detected". The shift keeps its sign and roughly its size (−2.0 against −2.4 km/s/Mpc under
  C), so the data still lean the way the paper says; what fails is significance.
- The leave-one-host-out χ² (64.9 for 77 rows under C) does not by itself show excess scatter, so
  the two diagnostics point in different directions; the χ² is approximate (it ignores the
  cross-covariance of a host's SN rows with the kept rows) and is reported only.
- **How firm the null is (referee, post hoc).** The verdict sits near a knife edge in τ: z is −2.21
  at τ = 0 and −1.53 at τ̂, and crosses −2 at about τ ≈ 0.03 mag, below the 68% interval (0.048) but
  only about 1.5σ from τ̂ (the 0.03 is the referee's interpolation; only z at 0, τ̂ and the interval end
  are saved); the evidence for τ > 0 itself is modest (Δ(−2ℓ_R) = 3.50 at τ = 0,
  boundary likelihood-ratio p ≈ 0.03). τ is identified mostly by non-CCHP hosts (the largest
  leave-one-out terms are N5584, N2525, N1015), and R4 under V reuses the data τ was fitted on, so
  its spread of 1.005 is not an independent check. The rule was fixed knowing z = −2.21 and the
  direction of the effect (disclosed in section 2), so R2-RE is the pre-registered model-based
  answer, not an independent confirmation. **Read: in R22's data the CCHP host selection lowers H0
  by about 2 km/s/Mpc, at 1.5σ to 2.2σ depending on how much host-level scatter is allowed; it is not
  significant once a host-level random effect is modelled.** Whether τ̂ survives leaving out single
  hosts (N5584 first) and how unusual τ̂ and the 1.33 spread are under the null are registered as T-032.

### R2-RE-ROB (addendum 2026-11-17, T-032)

Run of 2026-11-18 (`python -m astrolab run 003`, 12,825 s; all earlier results reproduce exactly, only
timing fields changed). Numbers: `results/r2_re_rob.json`.

| Part | Result | Label (pre-registered rule) |
|---|---|---|
| A, leave one host out (τ route) | τ̂_j from 0.031 to 0.080 mag; z' from −2.04 to −1.50; the row changes only without N5584 (τ̂ = 0.031, z' = −2.04: "host selection significantly lowers H0, by the size the paper reports") | **verdict sensitive to single hosts' influence on τ̂ (N5584)** |
| A, data route (reported) | without host j, at τ = 0: z from −2.61 to −1.38; under V(τ̂_j): −1.89 to −0.95. Without N5584: −1.63 (C), −1.50 (V) | – |
| B, τ̂ under C (400 simulations, none failed) | 28 of 400 with τ̂_s ≥ 0.077; p = 0.072, 95% interval 0.047–0.100 (230 of 400 at τ̂ = 0) | **undetermined (Monte Carlo)** |
| B, R4 spread under C (2,000 simulations, 1,000 subsets) | spread_obs 1.307 (simulated median 0.976, 95th percentile 1.232); 42 of 2,000 ≥ 1.307; p = 0.021, interval 0.015–0.028 | **the R4 excess spread is unusual under C** |

- **Reading (pre-registered).** "Verdict sensitive": the null result of R2-RE depends on N5584's
  effect on τ̂. Without N5584, REML puts the host-level scatter at 0.031 mag, and the full-data host
  step under that τ gives z' = −2.04, which the pre-registered table reads as supporting the paper.
  The τ part is undetermined, as section 2 expected (p near the 0.03 boundary estimate). The spread
  part says R4's 1.33 is itself unusual under C: there is more scatter among calibrator SN rows than C
  allows, without identifying the cause.
- **What the two routes say together (descriptive).** N5584 matters in two opposite ways. Dropping
  it lowers τ̂ (so the τ route moves towards "supports"), but dropping its rows from the data also
  removes part of the shift: on the reduced data the host step gives z = −1.63 even at τ = 0. So the
  verdict does not flip to "supports" once N5584 is really left out; it flips only when N5584's rows
  stay in the shift while its influence on τ̂ is removed. Across all 37 removals the data route at
  τ = 0 ranges from −2.61 to −1.38, and under V(τ̂_j) from −1.89 to −0.95.
- **Status of R2.** The R2-RE headline row stands as pre-registered ("no host-selection effect
  detected"), now reported with the label "sensitive to single hosts (N5584)", and with the finding
  that excess calibrator scatter under C is present (spread) but τ̂ alone is not clearly unusual.
  The host-selection question remains between 1.5σ and 2.2σ, as before.
- **Post hoc (referee, 2026-11-18; section 6): one host carries every signal.** Over the R4
  subsets that exclude N5584 the spread is 1.027 (p = 0.33 under the same null; we reproduced the
  referee's cache-only check, which is approximate because N5584 stays in the 37-host reference fit), while excluding any other single host leaves 1.21–1.34 (p ≤ 0.056). So
  the "unusual spread" label, the size of τ̂ and the A flip are all the effect of one outlying host,
  N5584 (one SN, 2007af); whether its SN or its Cepheid distance is off is not identified. Without
  N5584's rows the host step gives z = −1.63 under C and −1.50 under V, i.e. "no host-selection effect
  detected" under either covariance. An explicit, pre-registered treatment of N5584 (removal and a
  heavy-tailed host effect) is registered as T-039.
- A smoke run before the formal run showed part of A (the N5584 removal: τ̂ ≈ 0.031, z ≈ −2.04);
  disclosed in `log.md` on 2026-11-17, rules unchanged.

## 6. Referee notes

Independent referee, 2026-11-14 (a subagent that saw the pre-registration, code and results, not
sections 5-8). Triage:

| # | Point | Triage |
|---|---|---|
| 1 | The host step's significance rests on C-propagated errors; R4 shows the spread of Δ/σ over random subsets is 1.33, so with σ inflated by that factor z ≈ −1.66 and the verdict table would give "no host-selection effect detected"; the two parts of the study disagree while the summary led with "supports the paper". | **Accepted.** The qualified verdict (`r2.json` `verdict`, `summary.json` `R2_host`) now states the inflated-σ outcome; section 5 and the claim say so. The pre-registered rule (C-propagated σ) is unchanged and its outcome is reported as `criterion_outcome`; the inflation is post-hoc and descriptive. A pre-registered test with a host-level random effect is registered as T-023. |
| 2 | The verdict string quoted the post-hoc Δ/σ percentile 4.7, not the pre-registered Δ percentile 5.68 (they fall on opposite sides of 5%). | **Fixed**: both are quoted and labelled. |
| 3 | Three unexpected constraint rows (Z_W prior −0.215 ± 0.12, column 44 fixed at 0 ± 3 × 10⁻⁵, b_W prior 0 ± 10) were not flagged by a check; the Z_W prior weighs more in anchor-reduced fits. | **Accepted limitation**, documented in section 5 (row classes). They are R22's own priors and are kept in every subsystem, as in R22's variants. |
| 4 | The N4038/N4639 tie-break uses fitted distances. | **Accepted, no change**: the single-row SN magnitude (12.454 = N4639) gives the same labelling; R2 and R4 are unaffected (both are CCHP hosts); R3's per-host rows for the two carry the caveat. |
| 5 | R3's "Cepheid" distances come from the host-step fit and include each host's own SN rows, so the per-host Δμ is not Cepheid-only (likely part of why χ² = 5.1 for 10). | **Accepted limitation**; noted here and in section 7. d (the H0 difference) is unaffected in meaning: both sides use the same SN rows. |
| 6 | Data vintage: R22 matrices against the paper's 2024 data; our shift is 1.8 times the paper's and agrees only within a wide (±0.086 mag) band that discriminates little. | **Accepted**; already stated in section 5. |
| 7 | R3's match to 69.29 is not like-for-like (full GLS on 77 rows against CCHP's rescaling of R22 fit 10). | **Accepted**; the pre-registered 0.02 mag tolerance was set for this; stated in section 4. |
| 8 | The reading that CCHP Table 2's σ_T excludes the zero-point terms is not stated by CCHP. | **Accepted**; the sensitivity without those terms moves σ_d from 0.048 to 0.052 and leaves d unchanged. |
| 9 | Lean: the `ResidSmall` gloss omitted that the paper's σ excludes the SN term. | **Fixed** in `argument/Argument.lean` (doc comment). All six `[stated]` premises were checked against the paper and are not stronger than their quotes; the GAP label is honest. |
| 10 | Literature: the 2024 paper's own random-subset test for the 8-SN JAGB sample gives about 5% (Fig. 6), a direct analogue of R4; the paper also says SNe dominate subsample scatter (consistent with the 1.33). | Noted (verified by the referee); Efstathiou arXiv:2007.10716 on calibrator scatter was cited unverified and is not used. |

### Referee, R2-RE (independent subagent, 2026-11-16)

The referee saw README sections 1-4 (with the R2-RE addendum), the code and the results, not sections
5-8; it ran a synthetic check only. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The Cepheid-row "sensitivity" is mathematically identical to the main model (indicators add to the host column; REML and the H0 estimate are invariant); it says nothing about whether the cause is on the SN or the Cepheid side | yes: saved τ̂ and z' agree to 10⁻¹¹; the referee's synthetic check agrees to 10⁻¹⁴ and breaks only if an anchor row touches a host column | **Accepted**; section 5 calls it an identity. The pre-registration text ("a different covariance direction") was wrong on this point; left as frozen, corrected here. |
| 2 | The leave-one-host-out χ² under C (64.9 / 77) shows no excess while REML prefers τ > 0; τ̂ may rest on N5584 (χ² 12.5 on 4 rows of 1 SN) and a few other non-CCHP hosts; the LOO statistic ignores the cross-covariance with the kept rows | yes (per-host terms in `r2_re.json`); the cross-covariance caveat was already in the results note | **Accepted**; section 5; leave-one-host-out τ̂ registered as T-032. |
| 3 | Knife edge: z' crosses −2 at τ ≈ 0.03; the plug-in ignores τ's uncertainty; evidence for τ > 0 is p ≈ 0.03 | yes (grid and z at 0, τ̂, interval end) | **Accepted**; section 5 states the range 1.5σ–2.2σ. |
| 4 | τ applies to calibrator SNe only; if the cause is SN intrinsic scatter it should apply to Hubble-flow SNe too; whether C already holds a within-SN block | partly (not inspected by us) | **Accepted limitation**; noted in section 7; Wojtak & Hjorth 2022 (arXiv:2206.08160, verified by the referee) give a calibrator-specific candidate. |
| 5 | Per-host versus per-SN offset for multi-SN hosts (N5643 is a CCHP host) | yes (pre-registration) | **Accepted limitation**; likely small. |
| 6 | Circularity: R4 under V reuses the data τ was fitted on; the 1.33 spread under C was never calibrated against the null | yes | **Accepted**; section 5; null simulations registered as T-032. |
| 7 | Code checks pass (REML, nested identity, interval, headline logic); `summary.json`'s `R2_host_shift`/`sigma`/`z` are the C values next to the R2-RE headline | yes | Noted here: those three fields are the C-error values; the R2-RE values are in `r2_re.json` (`host_step`) and `summary.json` `R2_RE.z`. Not changed (would need a rerun). |
| 8 | Literature: Wojtak & Hjorth 2022/2024/2025 (arXiv:2206.08160, 2403.10388, 2506.22150), Perivolaropoulos & Skara 2022 (arXiv:2208.11169), Gall et al. (arXiv:2411.05642), as found by the referee; Efstathiou 2020 and Mörtsell et al. 2022 unverified | partly | Listed as context; not used in any verdict. |

### Referee, R2-RE-ROB (independent subagent, 2026-11-18)

The referee saw README sections 1–4, the code and the results, not sections 5–8 or the log; it ran
offline checks from the cache. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | One host, N5584 (a single SN, 2007af), carries all three robustness outcomes: it alone flips the A row; it pulls τ̂ from 0.066–0.080 down to 0.031 when removed; and the R4 spread excess is entirely its effect: over the R4 subsets that exclude N5584 the spread is 1.027 (p = 0.33 against the same null), while excluding any other single host leaves 1.21–1.34 (p ≤ 0.056) | yes: we reran the referee's cache-only script (`spread_check.py`, 2.6 min): spread_obs 1.3071 and p = 0.0215 reproduced; without N5584 1.027, p = 0.330; next N1365 1.207, p = 0.056 (approximate: N5584 stays in the 37-host reference fit) | **Accepted** (post hoc, 2026-11-18). Section 5 reading extended below; the pre-registered labels stand. Follow-up registered as T-039. |
| 2 | The A flip comes from the hybrid τ route (N5584's rows kept in the shift, its scatter removed from τ̂) and sits on a knife edge (z' = −2.04, at the "supports the paper" row); the data route is "no effect" under V for all 37 removals, and under C 33 of 37 removals still read "supports" | yes (results) | Accepted; stated in section 5. |
| 3 | The R2 significance under C (z = −2.21) itself rests largely on N5584: without its rows z = −1.63 | yes (results) | Accepted; stated in section 5. |
| 4 | The addendum's "more scatter among calibrator SN rows than C allows" is too specific: a host's offset is its SN-versus-Cepheid distance residual, so the Cepheid side could equally be the cause | yes | Accepted; wording in section 5 says "one outlying host", the gloss is kept only as the pre-registered text. |
| 5 | The boundary-χ² estimate p ≈ 0.031 was optimistic (observed p_τ 0.072; 57.5% of null τ̂ exactly zero); τ̂ as the test statistic is not monotone in the likelihood ratio and costs some power | yes | Accepted limitation; noted. |
| 6 | The spread simulations reuse the τ simulations' seeds 10000–10399 | yes | Not a bug (correlates the two parts' simulations only); noted. |
| 7 | Literature (unverified, the referee's search): JWST/HST Cepheids in N5584 agree (arXiv:2307.15806); HST TRGB 31.76 ± 0.04 ± 0.12 (arXiv:1506.03089); JWST TRGB tip ambiguity (arXiv:2401.04776); TRGB–Cepheid comparison (arXiv:2408.00065); SN 2007af reddening (arXiv:2503.09702) | no | Context for T-039 (host extinction of SN 2007af is a hypothesis, not established); to be raised to [V] before use. |
| 8 | No code or statistics bug: leave-one-out row removal, τ and data routes, the null construction (REML and Δ/σ independent of q̂ under C), Clopper–Pearson intervals and labels checked | – | None. |

## 7. Open questions

- Why the public `lstsq_results.txt` differs from the printed baseline (a later or variant fit).
- How the 2024 data (SMC anchor, more Cepheids) change the host shift; not public as matrices.
- Does C understate host-to-host scatter? Answered by R2-RE (2026-11-16): a host-level random
  effect of 0.077 mag (0.048–0.105) brings the random-subset spread of Δ/σ from 1.33 to 1.005; its
  physical origin is open: it measures the host-level scatter of SN-based minus Cepheid-based
  distances beyond C and cannot say which side causes it; calibrator-specific SN colour behaviour
  (Wojtak & Hjorth 2022) is one candidate; whether C's calibrator block already holds a within-SN
  term is unchecked. Robustness of τ̂ to single hosts and its null distribution: T-032.
- A Cepheid-only per-host comparison for R3 (μ from fits without each host's SN rows).
- R4 suggests the CCHP selection is a low but ordinary draw: is there a property of those hosts
  (for example the TRGB-friendly, low-extinction halos) that correlates with their SN magnitudes?

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `cchp_hosts` | the host set for the host step and R3 (names as in R22 Table 6) | any subset of the 37 hosts (R3 needs CCHP Table 2 hosts) | cache only |
| `r4_draws`, `r4_seed` | random-subset draws and seed | 1000–10,000 (about 0.08 s per draw) | cache only |
| `sn_match_tol` | host-identification tolerance (mag) | 0.1–0.3 | cache only |
| `trgb_tip_sys` | NGC 4258 TRGB tip uncertainty in the R3 covariance (mag) | 0–0.05 | cache only |
| `re_check`, `re_tau_max`, `re_grid_step` | run R2-RE; τ search range and grid step (mag) | true/false; 0.3–1.0; 0.005–0.02 | cache only |

- Rerun with an override: `python -m astrolab explore 003-m02-hubble-tension-distance-ladder --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about 28 min with the default R4 and R2-RE;
  `--set r4_draws=1000` takes a few minutes; `--set re_check=false` skips R2-RE).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 003-m02-hubble-tension-distance-ladder --tag <topic> --script explore/<name>.py`.
  Existing: `explore/diag_hosts.py` (which checks link each L column to which host).
- Results files and keys: `summary.json` (verdicts), `r1.json` (`params` with `column_label`, `worst_param_label`,
  `fivelogh0`, `chi2`),
  `r2.json` (`anchor_step`, `host_step.shift`, `.shift_sigma` (C errors), `.verdict` (the headline, R2-RE
  when evaluated), `.criterion_outcome`, `.descriptive_inflated_sigma`, `.headline_source`,
  `.preregistered_verdict`), `r2_re.json` (`tau_hat`, `interval_68`, `reml`, `host_step`, `verdict`,
  `sensitivity_cepheid_rows`, `r4_under_v`, `loo_chi2`),
  `r3.json` (`cchp_side_h0`, `d`, `sigma_d`, `per_host`), `r4.json` (`percentile`, `quantiles`,
  histogram, `z_quantiles`, `z_std`, `z_percentile`, `cchp_z`), `host_identification.json` (`column_labels`, `relabelled`, `per_column_under_labels`),
  `cross_paper.json`.
- Example questions: "Which single CCHP host drives the shift?" → `--set cchp_hosts=[...]` leaving
  one out at a time; "Does the shift survive with a looser identification tolerance?" →
  `--set sn_match_tol=0.25`; "Is the CCHP set unusual among subsets with the same number of SNe?" →
  a script over `r4` draws.
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.
