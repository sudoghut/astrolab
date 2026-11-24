# Hubble tension: SH0ES distance ladder and host selection

> 中文：[README.zh.md](README.zh.md) · Web page online: [https://sudoghut.github.io/astrolab/studies/003-m02-hubble-tension-distance-ladder/web/](https://sudoghut.github.io/astrolab/studies/003-m02-hubble-tension-distance-ladder/web/)

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

### Addendum 2026-11-18: R2-RE-N5584, explicit treatment of the outlying host N5584 (T-039), pre-registered before any of these fits

*Why.* The R2-RE-ROB referee (section 6) found that one host, N5584 (one SN, 2007af; 4 calibrator SN
rows and about 165 Cepheid rows), carries all three robustness signals. This addendum fixes two
treatments in advance: (a) remove N5584 completely; (b) give all 37 hosts a heavy-tailed host effect,
so that an outlier is down-weighted by the model rather than excluded. Literature (arXiv abstract
pages read 2026-11-18): the JWST and HST Cepheid period–luminosity intercepts agree in N5584 (Riess
et al. 2023, arXiv:2307.15806); Jang & Lee 2015 (arXiv:1506.03089) give a TRGB (tip of the red giant
branch) modulus of 31.76 ± 0.04 ± 0.12 without a Cepheid comparison in the abstract; Anand et al.
2024 (arXiv:2401.04776) report a mean TRGB–Cepheid difference over N1559 and N5584 together, and Li
et al. 2024 (arXiv:2408.00065) a sample-mean agreement with N5584 among the hosts; Murakami et al.
2025 (arXiv:2503.09702) measure an MW-like dust law in N5584 from background galaxies (SN 2007af is
not mentioned). This is compatible with the SN side (2007af) being the source of the offset, but does
not establish it; the referee's descriptions of 2401.04776 ("tip ambiguity") and 2503.09702 ("SN
2007af reddening") are not supported by the abstracts.

*Seen before this addendum.* Everything in sections 5–6, in particular: R2 z = −2.21 under C;
R2-RE τ̂ = 0.077 (0.048–0.105), z' = −1.53; R2-RE-ROB part A without N5584: τ̂ = 0.0314, τ route
z' = −2.04 ("supports"), data route z = −1.63 under C and −1.50 under V(0.031) (both "no effect
detected"); part B p_τ = 0.072, p_spread = 0.021; the referee's approximate spread over subsets
excluding N5584 1.027 (p = 0.33; excluding any other single host 1.21–1.34); N5584 has the largest
leave-one-out χ² term (12.5 on 4 rows); the 37-host null τ̂ values of part B (`r2_re_rob.json`:
230 of 400 at zero, 137 of 400 ≥ 0.0314). The reduced-system shifts are known: −0.0532 ± 0.0327
under C and −0.0512 ± 0.0341 under V(0.031). So in (a) the reduced-system τ̂ and both host steps are
already known (the removal is exactly part A's data route for N5584; the formal run only confirms
them), and in (b) the direction is predictable: N5584 will get the smallest weight, and ν was chosen
knowing that; the heavy-tailed model itself was chosen after the outlier was seen, with ν = 4, the
conventional default of Lange, Little & Taylor (1989, JASA 84, 881). From the 37-host null τ̂ values and
the referee's spread check, the expected (a) reading is "attributable to N5584". Not yet run: any heavy-tailed fit, R4 on 36 hosts, the τ interval without N5584, and
null simulations on the reduced system.

*Question.* (a) Without N5584, is the scatter of the calibrator SN rows consistent with C (τ and
spread), and where does the CCHP selection fall among random subsets? (b) Under a heavy-tailed host
effect, which row of R2's table does the host step give?

*(a) Removal (R2-RE-N5584-DROP).*
- System: the NGC 4258-only system (`rows_a`) without every row that has a non-zero entry in
  N5584's host column (its Cepheid and calibrator SN rows; counts reported); anchor, constraint and
  Hubble-flow rows kept; 36 hosts. `rows_s` is unchanged (N5584 is not a CCHP host), so Δ_h moves only
  through the reference fit. R1 and R3 are unchanged by construction and not rerun.
- Reference fit and host step under C, as in R2 (shift, σ, z, verdict row).
- R2-RE on the reduced system: R2-RE's REML (restricted maximum likelihood) procedure with 36 groups,
  including the 68% interval; the host step under V(τ̂_N) and its row; R2-RE's bound and fit-failure
  rules.
- R4-N: the ranked quantity is the CCHP shift of the 36-host system under C (Δ_h,N, relative to the
  36-host reference fit); 10,000 draws from `default_rng(0)` (R4's index stream, mapped to different hosts) with `rng.choice(36, 10, replace=False)` indexing the 36
  remaining host columns in column order (fresh draws, not a reuse of the R4 subsets that happen to
  exclude N5584); R4's runtime guard; reported: the percentile of Δ_h with R4's 5/95 rule, the z
  percentile and the spread of Δ/σ; the same draws refitted under V(τ̂_N).
- B-N: R2-RE-ROB part B on the reduced system: ŷ from the 36-host fit under C, K the Cholesky factor
  of C on the reduced rows, ε_s from `default_rng(10_000 + s)` (shorter vectors, so not ROB's draws);
  τ part s = 0…399 against τ̂_N; spread part s = 0…1,999 over the first 1,000 R4-N subsets; same p,
  two-sided 95% Clopper–Pearson interval, three-way labels and limit of 20 failed fits.
- Part A (leave one host out) is not repeated on 36 hosts.

*(b) Heavy-tailed host effect (R2-RE-T).*
- Model, on the full NGC 4258-only system (37 hosts, N5584 included): y = Xβ + Σ_j u_j h_j + e,
  e ~ N(0, C); u_j | w_j ~ N(0, τ²/w_j), w_j ~ Gamma(ν/2, rate ν/2) independent, so u_j is
  Student-t_ν(0, τ). **ν = 4 fixed** (variance 2τ²); ν = 2 and 10 reported only. β flat, as in REML.
- Fit: variational EM (expectation–maximisation; mean-field q(β, u)·q(w)), whose Gaussian step is the
  R2-RE model with per-host variance τ²/ω_j. Precompute with one Cholesky factor of C on `rows_a`:
  A = XᵀC⁻¹X, B = XᵀC⁻¹Z, D = ZᵀC⁻¹Z, b = (XᵀC⁻¹y; ZᵀC⁻¹y), Z (n × 37) holding the h_j, X with
  `infer.gls`'s kept columns. Iterate: P = [[A, B], [Bᵀ, D + diag(ω)/τ²]], m = P⁻¹b, S = P⁻¹;
  s_j = m_{u,j}² + S_{uu,jj}; ω_j ← (ν + 1)/(ν + s_j/τ²); τ² ← Σ_j ω_j s_j / 37. Two starts
  (τ = 0.077, ω = 1) and (τ = 0.20, ω = 1); stop when the largest relative change in τ² and in every
  ω_j is below 10⁻⁸; at most 10,000 iterations. Each τ² update uses the ω just updated in the same
  iteration (coordinate ascent on the evidence lower bound, ELBO); the fixed point maximises this
  variational bound, not the Student-t restricted likelihood, and ω̂_j = E_q[w_j].
- Plug-in (a definition: τ̂²/E_q[w_j], not E_q[τ²/w_j]): V_T = C + Σ_j (τ̂²/ω̂_j) h_j h_jᵀ; the host step under V_T (`host_step_under`) gives Δ_T,
  σ_T, z_T and R2's table gives the row.
- Validity, each failure giving "not evaluable" with the reason: (1) with ω held at 1 and started at
  τ = 0.20 the iteration is EM for REML and must reproduce R2-RE's τ̂ within 10⁻⁴ and z' within 0.005;
  (2) both starts converge within 10,000 iterations, otherwise "not evaluable (not converged)" with
  the iteration count; (3) both converged starts agree on τ̂ within 10⁻⁴, otherwise both fixed points
  are reported ("not evaluable (multiple fixed points)"); (4) τ̂_T < 10⁻³ counts as zero (V_T = C, R2's row); τ̂_T > 0.5 − 10⁻³ is
  "not evaluable (bound)"; (5) the Cholesky factor of V_T and both GLS fits succeed. The same checks
  apply to ν = 2 and 10, which are marked "reported, not evaluable" where they fail.

*Decision rules and labels, fixed now.* R2-RE's row ("no host-selection effect detected") stays the
headline; the R2 (2026-11-14), R2-RE and R2-RE-ROB verdicts and labels stay as recorded.
- (a) The reduced system's R2 and R2-RE rows are reported, marked "known before this addendum". R4-N
  gets R4's label; B-N gets ROB's three-way labels. Reading, rules checked in this order: any B-N part "not evaluable" → "not evaluable"; spread "consistent with C" and τ "consistent
  with C" or "undetermined (Monte Carlo)" (i.e. not "unusual") → "the excess calibrator scatter of R2-RE-ROB is attributable to N5584"; spread
  "unusual" → "excess scatter remains without N5584"; spread "consistent with C" and τ "unusual" →
  "τ excess remains without N5584"; otherwise "undetermined".
- (b) z_T's row equals R2-RE's row → **"R2-RE verdict robust to a heavy-tailed host effect"**;
  otherwise **"R2-RE verdict depends on the host-effect distribution (heavy-tailed: <row>)"**.
- Joint reading: if (b) is robust, "the null result holds under both removal and down-weighting of
  N5584; only the hybrid τ route of R2-RE-ROB A flips"; if (b) is not robust, "the verdict depends on
  how one host is modelled", quoting R2's z under C, R2-RE's z' under V(τ̂ = 0.077) and z_T under V_T, all on the
  full 37-host system (reported as observed values, not a decision rule); if (b) is not evaluable, there is no joint reading and (a)'s
  labels stand alone.

*Reported.* (a): rows removed, τ̂_N with its interval, z under C and V, the R4-N percentiles and
spread, R4-N under V, B-N's p values, intervals and quantiles. (b): τ̂_T, every ω̂_j ranked with its
effective scatter τ̂/√ω̂_j, iteration counts, the implementation check, and z_T with its row for
ν = 2, 4, 10 (only ν = 4 decides).

*Runtime.* From measured times (R4 0.117 s per draw; R2-RE-ROB 10,034 s): REML with interval about
1 min; R4-N and R4-N under V about 20 min each; B-N about 2.5 h (τ part, 400 REML fits) plus about
3 min (spread); (b) seconds. Added about 3.3 h; a full run about 7 h; no data downloaded. Switch:
`PARAMS["n5584_check"]`, with `"n5584_host": "N5584"`, `"t_nu": 4`, `"t_nu_sens": [2, 10]`, `"t_maxiter": 10000`, `"t_tol": 1e-8`,
`"t_starts": [0.077, 0.20]`. `n5584_check` runs after, and in addition to, the R2-RE-ROB
block (`rob_check`) and under the same condition (R2-RE run and the host step evaluable); R4-N and
B-N call R4 and `rob.null_sims`-style code with the reduced rows, groups and subsets passed in.

*Clarification 2026-11-18 (before the formal run; from the code review).* Near τ = 0 the EM's relative
change per step is O(τ²), so a true τ_T near zero would stop at the iteration cap and be labelled "not
evaluable (not converged)" rather than "zero, R2's row" (rule (4)); "not converged" takes precedence as
written, and the rules are not changed. A code check on the real data (run while implementing; only the
convergence flags and iteration counts were looked at, no τ̂_T, z_T, rows or labels) converged from both
starts for ν = 2, 4 and 10 (95–159 iterations), so this case does not arise here.

### Addendum 2026-11-19: R2-RE-SEL, a selection-aware null for the removal of N5584 (T-042), pre-registered before any of these simulations

*Why.* The R2-RE-N5584 referee (section 6, point 3) found that B-N simulates an unselected 36-host
system, while N5584 was removed because it was the most extreme of 37 hosts. Dropping the most
extreme host in each simulation would shrink the null τ̂ and the R4 spread, so B-N's p values (0.339
and 0.359) are biased upward, towards "attributable to N5584"; section 5 therefore reads that label,
post hoc, as "consistent with one outlying host". This addendum fixes a null that includes the
selection: simulate the full 37-host system under C, drop the most extreme host by a fixed criterion,
and only then compute τ̂ and the spread on the remaining 36 hosts.

*How N5584 was singled out, and the criteria.* N5584 was removed because it carried all three
robustness signals, found in sequence: (i) the largest leave-one-host-out χ² term under C (R2-RE
referee, section 6, R2-RE point 2: N5584, N2525, N1015); (ii) R2-RE-ROB part A: the smallest τ̂_j and the
only host whose removal flips the τ-route row; (iii) the R2-RE-ROB referee's spread-exclusion check: the
smallest spread over the R4 subsets that exclude the host. No single statistic reproduces that history.
Values on the real data, each picking N5584:

| Criterion | N5584 | Next | Source |
|---|---|---|---|
| Raw leave-one-out χ² term under C (largest) | 12.478 (4 rows) | N2525 5.837 (3 rows), N1015 5.394 | `r2_re.json` `loo_chi2.C.per_host` |
| Its χ² tail probability (smallest) | P(χ²₄ > 12.478) = 0.014 | N3982 P(χ²₁ > 4.246) = 0.039 | computed while drafting this addendum |
| Same term under V(τ̂) (largest) | 7.652 | N2525 5.774 | `r2_re.json` `loo_chi2.V.per_host` |
| Part A: smallest τ̂_j | 0.0314 | N1365 0.0659, N3982 0.0700 | `r2_re_rob.json` `A.hosts` |
| Part A: the τ-route row flips | only N5584 | – | `r2_re_rob.json` `A.sensitive_hosts` |
| Spread over the first 1,000 R4 subsets that exclude the host (smallest) | 1.027 (p = 0.330) | N1365 1.207 (p = 0.056); others up to 1.34 | section 6, R2-RE-ROB referee point 1 (our rerun of the referee's cache-only script; per-host values not saved in `results/`) |

Two criteria are registered, because they are cheap per simulation; part A's criteria would need 37
REML fits per simulation (about 11–12 min for the 37 fits of one simulation) and are not feasible.
- **Criterion X (raw leave-one-out χ² under C), used for the τ part and the first spread label.** It is
  the statistic that named N5584 first. It is computed by `loo_chi2` in `run.py` (R2-RE addendum,
  "reported, not decisive"): for host j with calibrator SN rows g_j (`calib_groups[j]`: rows with a
  non-zero in column 42 and in exactly one host column, that of j), refit the NGC 4258-only system
  (`rows_a`) under C without the rows g_j (host j's Cepheid rows kept, so μ₀,j is still fitted) with
  `infer.gls`; r_j = y[g_j] − L[g_j, kept] q̂; S_j = C[g_j, g_j] + L[g_j, kept] Cov(q̂) L[g_j, kept]ᵀ;
  χ²_j = r_jᵀ S_j⁻¹ r_j (`numpy.linalg.solve`). The raw term (not divided by its 1–4 rows, not a tail
  probability), argmax over the 37 hosts, ties to the lowest column. r_j is linear in y through a fixed
  map and S_j is fixed under C, so χ²_j is a fixed quadratic form in y (cheap per simulation). The
  statistic is approximate as a χ² (it ignores the cross-covariance with the kept rows; R2-RE note),
  which does not matter here: it is only a selection rule, used identically on data and simulations.
- **Criterion S (spread excluding the host), used for the second spread label.** It is the criterion that
  attributed the spread signal to N5584. Take R2-RE-ROB part B's subsets (the first 1,000 of R4's
  10-of-37 draws, in order) with their shift rows a_k and σ_k on the 37-host system under C (Δ_k = a_kᵀ y,
  σ_k² = σ²_subset − σ²_37, as in `rob.null_sims`; rebuilt in this block, about 2 min, since ROB does not
  save them). That the referee's check used these subsets is our reading of an unsaved script, confirmed
  only by its reproduction (spread_obs 1.3071, N5584 1.027). The reference fit is the 37-host fit with
  N5584 included, as in the referee's check; this replicates the historical selection, so the
  approximation noted in section 6 (N5584 stays in the reference fit) is irrelevant for a selection rule.
  For host j, spread_excl_j = `numpy.std` (ddof = 0) of Δ_k/σ_k over the subsets that do not
  contain j; the criterion is argmin_j spread_excl_j (ties to the lowest column). Linear in y up to the
  standard deviation, so cheap per simulation. On the real data it must reproduce N5584 at 1.027 (within
  0.001) and select N5584.

*Direction of the criterion bias (stated now).* Criterion X is less aligned with τ̂ and with the spread
than "smallest τ̂_j" or criterion S: in a simulation the host it drops is not necessarily the one that
inflates τ̂ or the spread most, so the selected null shrinks less than under the aligned criteria and p
is expected to come out higher (an expected direction, not a proven ordering: the host X drops
need not be the one driving either statistic):
"unusual" under X is strong evidence of remaining excess scatter, "not unusual" / "consistent" under X is
weak evidence for "one outlying host". Criterion S is aligned with the spread statistic, so the second
spread label is the stronger test of "consistent". The τ part has no aligned feasible criterion; its
label carries this caveat.

*Seen before this addendum.* Everything in sections 5–6, in particular: R2-RE τ̂ = 0.077 (0.048–0.105);
R2-RE-ROB part A: all 37 τ̂_j (N5584 0.0314, N1365 0.0659, N3982 0.0700, the other 34 from 0.0757 to
0.0800); part B on 37 hosts: p_τ = 0.072, p_spread = 0.021 (spread_obs 1.307), the 400 null τ̂ values
(`r2_re_rob.json`: 230 at zero, 137 ≥ 0.0314, i.e. 0.34); the referee's spread-exclusion values above
(N5584 1.027, p = 0.330; N1365 1.207, p = 0.056; the others up to 1.34; the full per-host list was seen
when we reran the script, not saved); R2-RE-N5584 (a): 169 rows removed, τ̂_N = 0.03137 (68% interval
0–0.070), host step z = −1.63 (C) and −1.50 (V); R4-N spread 1.044 (all 10,000 draws), CCHP at the 8.5th
percentile; B-N: τ part 135 of 400 ≥ τ̂_N (220 at zero; null quantiles 5/50/95% 0, 0, 0.0796), p =
0.339, interval 0.291–0.386; spread part spread_obs 1.0325 over the first 1,000 R4-N subsets, 717 of
2,000 ≥ it, p = 0.359, interval 0.337–0.380 (null quantiles 0.771, 0.977, 1.222); the pre-registered
reading "attributable to N5584" and its post-hoc gloss; R2-RE-T (ν = 4) ω̂ ranking: N5584 0.392, N1365
0.804, N3982 0.879, all others 0.97–1.06; every per-host leave-one-out χ² term (C and V). While drafting
this addendum, by arithmetic on those recorded terms only: treating the 37 terms under C as independent
χ²_n (n = 1 for 11 hosts, 2 for 15, 3 for 8, 4 for 3), the probability that the largest reaches 12.478
is about 0.12, so N5584's term is not exceptional once the choice among 37 hosts is allowed for
(approximate: the terms are neither exactly χ² nor independent). Not yet run: any simulation of the
selected null, in code or by hand; no code for this addendum exists.

*Expected outcome (stated now).* The expected direction: dropping the most extreme host of each simulated
system should lower the null τ̂ and spread relative to B-N, so the p values are expected below 0.339 and
0.359, and lower under criterion S than under X. This is not guaranteed: the selected null runs on a
different 36-host system in each simulation (N5584's simulated rows stay in whenever d_s ≠ N5584, and
criterion X favours hosts with 3–4 calibrator rows), so its null distribution can differ from B-N's for
reasons other than the selection. A rough argument (not a calculation of this test): under the null the
dropped host's term exceeds its expected value by about 5–7 in a summed χ² whose null spread is about
√(2 · 77) ≈ 12, a downward shift of roughly half a standard deviation, which would move p from about
0.34 to roughly 0.1–0.3 under X; under S the shift for the spread is expected to be larger, by an amount
we cannot estimate from recorded numbers. "Not unusual" / "consistent" under X is the more likely
outcome; under S "undetermined" or "unusual" is more plausible than under X (the R2-RE-ROB anticipation
of p ≈ 0.03 was off: observed 0.072).

*Question.* When the null includes the choice of the most extreme of 37 hosts by a criterion that singles
out N5584 on the real data, is the calibrator scatter of the remaining 36 hosts (τ̂_N and the R4-N spread)
consistent with C?

*Method (R2-RE-SEL).*
- Null data: as R2-RE-ROB part B. Under C, fit the NGC 4258-only system (`rows_a`, 3,489 rows, 37
  hosts) and take ŷ = L q̂ on those rows (the same ŷ as ROB). Simulation s draws y_s = ŷ + K ε_s on
  `rows_a`, K the lower Cholesky factor of C restricted to `rows_a`, ε_s =
  `numpy.random.default_rng(20_000 + s).standard_normal(len(rows_a))`. New seed base 20,000: ROB used
  10,000 + s (s up to 1,999) on vectors of the same length, so base 10,000 would reproduce ROB's
  simulations exactly; B-N used the same base on shorter vectors; R4 and R4-N use seed 0. Seeds
  20,000–21,999 collide with none of them. Under C both selection statistics, REML and each Δ_k/σ_k
  use only residual contrasts, so their joint null distribution does not depend on q̂.
- Selection: in simulation s, d_s = criterion X's host and d'_s = criterion S's host, computed on y_s
  exactly as defined above. The implementation may precompute, per host, the fixed map y[rows_a] → r_j
  and S_j⁻¹ (37 GLS fits with `return_estimator=True`), provided it reproduces `loo_chi2` on the real y
  to a relative 10⁻⁸ for every host (a mismatch is a bug and stops the run). On the real y both criteria
  must select the host named by `PARAMS["n5584_host"]` (N5584, column 26); the recorded values say they do.
- Reduced system for a dropped host d (d_s or d'_s): `rows_a` without every row with a non-zero in
  column d (that host's Cepheid and calibrator SN rows), with the 36 other calibrator groups; anchor,
  constraint and Hubble-flow rows kept. As in `n5584.drop_host`: rows_n = those rows; base_n = the rows of
  rows_n with no non-zero in any host column; host_rows_n[j] = host_rows[j] ∩ rows_n. Unlike `drop_host`,
  there is no guard against CCHP hosts (d can be one): the host step and `rows_s` are not used in this
  block. Applied to the real data (d = N5584) this is exactly R2-RE-N5584 (a), so the observed values
  are its τ̂_N and B-N's spread_obs.
- Observed values: τ̂_obs = τ̂_N of R2-RE-N5584 (a) and spread_obs = B-N's spread_obs, both from the same
  run; each must equal the recorded value: τ̂_N (0.03137144323410943) to a relative 10⁻⁶ (it comes from
  the bounded optimiser, xatol 10⁻⁵), spread_obs (1.0325254787240916) to a relative 10⁻⁹. On a mismatch the block stops with status "not evaluable (observed values differ from the recorded
  ones: code or data change)", which is reported and investigated before anything else.
- τ part (criterion X): s = 0, …, 399: τ̂_s by R2-RE's REML procedure on the reduced system for d_s (grid
  0, 0.01, …, 0.50 mag, then the bounded refinement; no interval; `reml_tau(..., interval=False)`), the
  raw τ̂_s compared as in ROB and B-N (a τ̂_s at the upper bound counts as a value). n_τ = simulations
  whose fit succeeded; k_τ = #{τ̂_s ≥ τ̂_obs}; p_τ = (1 + k_τ) / (1 + n_τ), with the two-sided
  equal-tailed 95% Clopper–Pearson interval for k_τ / n_τ (`rob._cp`). No τ part under criterion S (it
  would add 400 REML fits, about 2–2.8 h).
- Spread parts (criteria X and S): s = 0, …, 1,999 (the τ part's simulations are the first 400 of
  these, as in ROB). Subsets: the first 1,000 index draws of R4-N's stream, idx_k =
  `rng.choice(36, 10, replace=False)` in order from `default_rng(r4_seed = 0)`, the same for every
  simulation, mapped onto the 36 host columns other than d in column order (for d = N5584 these are
  exactly B-N's subsets; the first five must equal `r2_re_n5584.json` `drop.r4n.first_picks`). For each
  dropped host d that occurs under either criterion, as in `rob.null_sims`: the reference fit of the
  reduced system under C, the shift rows a_k (subset fit minus reference fit, `shift_vector`) and σ_k² =
  σ²_subset − σ²_36 (a non-positive value is a bug and stops the run), computed once per d and shared by
  both criteria; simulations are grouped by d so that one matrix is held at a time. spread_s(d) =
  `numpy.std` (ddof = 0) of (a_kᵀ y_s) / σ_k over the 1,000 subsets. The d = N5584 path on the real y must
  reproduce spread_obs to a relative 10⁻⁹ (else a bug). For criterion X: k_X = #{spread_s(d_s) ≥
  spread_obs}; for criterion S: k_S = #{spread_s(d'_s) ≥ spread_obs}; p = (1 + k) / 2,001 with the same
  Clopper–Pearson interval for k / 2,000.

*Decision rules and labels, fixed now (in this order).* R2-RE's row ("no host-selection effect
detected") stays the headline; the R2 (2026-11-14), R2-RE, R2-RE-ROB and R2-RE-N5584 verdicts, labels
and readings stay as recorded (in particular the (a) reading "attributable to N5584" under B-N's
unselected null).
- Not evaluable: the observed-value mismatch above → the whole block; R2-RE-N5584 (a) or its reduced-system
  R2-RE not evaluated → the τ part; B-N's spread part not evaluated (including when R4-N's runtime guard
  left no draws) → both spread parts; R4 has no draws (runtime guard) → the
  criterion-S spread part; a leave-one-out fit under C fails (these fits do not depend on simulated data)
  or criterion X does not select N5584 on the real data → the τ part and the criterion-X spread part;
  criterion S does not select N5584 on the real data → the criterion-S spread part; spread_excl for N5584
  on the real data differs from 1.027 by more than 0.001 → the criterion-S spread part (reproduction). τ part: more than 20
  failed REML fits (`sel_max_failed`) → not evaluable; with 20 or fewer, p_τ and its interval use the
  successful fits. Spread parts: a fit failure while building the rows for a dropped host → that part
  not evaluable (fit).
- τ label (criterion X): interval entirely below 0.05 → **"τ̂_N unusual under the selected null"**;
  entirely above 0.05 → **"τ̂_N not unusual under the selected null"**; containing 0.05 →
  **"undetermined (Monte Carlo)"**.
- Spread labels, one per criterion (X, S): entirely below 0.05 → **"the 36-host spread is unusual under
  the selected null (<X|S>)"**; entirely above → **"the 36-host spread is consistent with the selected
  null (<X|S>)"**; containing 0.05 → **"undetermined (Monte Carlo)"**.
- Reading, rules checked in this order: (1) any of the three parts not evaluable → "not evaluable"; (2)
  both spread labels "consistent" and τ "not unusual" or "undetermined (Monte Carlo)" (i.e. not
  "unusual") → **"the excess calibrator scatter of R2-RE-ROB is consistent with one outlying host,
  selection included"** (the τ label comes from criterion X only, so its "not unusual" supports this
  reading only to the extent the spread labels do); (3) either spread label "unusual" → **"excess scatter remains after removing
  the most extreme host, selection included (criterion <X, S or both>)"**; (4) both spread labels
  "consistent" and τ "unusual" → **"τ excess remains after removing the most extreme host, selection
  included"**; (5) otherwise → "undetermined". Rule (3) is the union of two spread tests; its
  false-alarm rate is not quantified (each label needs its whole Clopper–Pearson interval below 0.05,
  which is conservative; the two tests share the simulations and select the same host in many of them).
- What the reading changes in section 5 (the text, not any label): (2) → the post-hoc gloss "consistent
  with one outlying host" becomes the pre-registered reading of this test, quoted with the caveat that
  the τ part uses criterion X only (its p expected to be higher than under an aligned criterion); (3) or (4) → the gloss is withdrawn and
  section 5 states that the excess calibrator scatter is not accounted for by removing the single most
  extreme host once that choice is simulated ("attributable to N5584" stays recorded as the outcome under
  the unselected null); (5) or "not evaluable" → the gloss stays, marked post hoc, with this outcome next
  to it. Separately, and descriptive only (it does not override rules (3) and (4)): for any part whose selected-null p is not below B-N's (p_τ ≥ 0.339, a spread p ≥
  0.359), section 5 says that the selection did not lower that p value in this setup; the gloss then simply
  stands for that part. In no case do the R2-RE headline row, `summary.json` `R2_host` or the claim's
  verdict change.

*Reported (not decisive).* n_τ, k_τ, p_τ, interval, quantiles (5/50/95%) and number at zero of τ̂_s;
for each criterion k, p, interval and quantiles of the spread; next to them B-N's recorded unselected
values; the frequency of each dropped host under X (over all 2,000 simulations and over the first 400)
and under S, how often each is N5584 and how often d_s = d'_s; the null distributions of the largest
leave-one-out term and of the smallest spread_excl, with the share of simulations reaching N5584's real
values (max χ² ≥ 12.478; min spread_excl ≤ the real-data value), each as (1 + k) / 2,001 with its
Clopper–Pearson interval (descriptive: how extreme N5584 is as the most extreme of 37 under C; no
label); the real-data values of both criteria for all 37 hosts; the reproduction checks (leave-one-out
maps, the criterion-S value 1.027, observed values, first subsets); the number of distinct dropped hosts,
the time to build their rows, and the seconds per part.

*Runtime (from measured times).* Recorded: R4 0.113 s per draw (`r4.json`), R4-N 0.101 s per draw;
R2-RE-ROB block 9,037 s in the latest run (`r2_re_rob.json`; the R2-RE-N5584 addendum quoted 10,034 s);
the R2-RE-N5584 (a) block 9,307 s (`r2_re_n5584.json` `drop.seconds`). Derived, not timed per
simulation: from the (a) block, minus R4-N (10,000 × 0.101 s ≈ 1,010 s), R4-N under V (assumed about the
same), REML with interval (about 1 min) and the B-N spread part (a few minutes), about 7,000 s remain for
400 REML fits, about 18 s each; approximately 20 s on 37 hosts for ROB, from 9,037 s minus part A (37
REML fits ≈ 11 min plus about 222 host-step fits, a few minutes; not timed) and the spread part (about
2 min), i.e. about 8,000 s for 400. The 25 s of the TODO note is the conservative figure. Estimates:
criterion-X maps about 1 min and criterion-S rows about 2 min once, then milliseconds to a few tens of
milliseconds per simulation; τ part 400 × 18–25 s ≈ 2.0–2.8 h; spread parts about 2–2.5 min per distinct
dropped host (one reference fit and 1,000 subset fits with estimators), shared by both criteria and
bounded by 37 hosts ≈ 0.7–1.5 h, plus about a minute for the 2,000 simulated vectors. Added about
2.8–4.4 h, against 2.5 h for R2-RE-ROB. The block needs the R2-RE-N5584 block (`n5584_check`), which
itself runs independently of `rob_check`; `rob_check` stays on in the formal run only so that
`r2_re_rob.json` is not overwritten with "not run" (cost about 2.5 h). A full run is therefore about
8.5–10 h; no data downloaded. The formal run waits until no other study run uses the machine (TODO
T-042). 400 and 2,000 are kept from ROB and B-N so that the Monte Carlo precision is the same as that of
the p values being corrected. More simulations after the run would need a new pre-registration.

*Code checks before the formal run.* Synthetic data only (the 2026-11-17 smoke-run lesson, log.md). On
the real data, before the formal run, only the reproduction checks may be run (leave-one-out maps against
`loo_chi2`, both criteria selecting N5584 and the value 1.027, the observed values, the first subsets for
d = N5584), all of which reproduce numbers seen before this addendum; no simulation on the real ŷ, no
τ̂_s, spread_s, p value or label.

*Switch and code.* `PARAMS["sel_check"]` (true), with `"sel_seed_base": 20_000`, `"sel_n_tau": 400`,
`"sel_n_spread": 2000`, `"sel_n_subsets": 1000`, `"sel_max_failed": 20`. The block runs after the
R2-RE-N5584 block and only when that block runs (the same condition: R2-RE run and the host step
evaluable). Results in `results/r2_re_sel.json`, a short summary in `summary.json` (`R2_RE_SEL`). None of
this exists yet: no module (planned `sel.py`, which, like `rob.py` and `n5584.py`, receives `run.py`'s
functions and does not import `run`), no `sel_*` keys in `PARAMS`, no results file, summary key, test or
web section.

### Addendum 2026-11-21: R2-RE-D, one outlying host or diffuse host scatter (T-048), pre-registered before any of these simulations

*Why.* R2-RE-SEL (2026-11-20, T-042) read the 36-host calibrator scatter as "consistent with one outlying
host, selection included", but its null is C with no outlier, so the reading only says that the 36
remaining hosts do not reject C. The R2-RE-SEL referee (section 6, point 1) showed that the test has
little power against a host-level random effect spread over all 37 hosts (diffuse scatter, V(τ) of
R2-RE), and proposed, after seeing the data, the drop of the spread when the criterion-S host is removed
as a statistic that separates the two pictures. This addendum fixes in advance a comparison of three
data models for the excess calibrator scatter: C (no excess), diffuse host scatter V(τ), and one host
offset by δ with everything else under C. The statistics are the drop D, computed exactly (36-host
reference refits, not the referee's proxy), and a joint statistic J on the pair (37-host spread, 36-host
spread), calibrated by simulation so that it is a valid p value for a statistic whose form was chosen
after seeing the data. The labels attach to R2-RE-SEL's reading; they do not change any earlier label or the headline.

*Seen before this addendum.* Everything in sections 5–6, in particular: R2-RE τ̂ = 0.0767 (68% interval
0.0477–0.1050); R2-RE-ROB part B spread_obs (37 hosts, first 1,000 R4 subsets) = 1.3071, p = 0.021, 42 of
2,000 null simulations ≥ it; R2-RE-N5584 (a): τ̂_N = 0.0314 (0–0.070), B-N spread_obs (36 hosts, N5584
removed, 36-host reference fit, first 1,000 R4-N subsets) = 1.0325; R2-RE-T: N5584 ω̂ = 0.392, effective
scatter 0.120 mag; R2-RE-SEL: all numbers in section 5 (criterion S selects N5584 on the real data with
spread_excl = 1.0267; p = 0.244, 0.241, 0.137; dropped-host frequencies; P(max χ² ≥ 12.478) = 0.114;
P(min spread_excl ≤ 1.027) = 0.882; build times of the 37 reduced systems, 100–115 s each, 4,067 s in
all). The referee's exploratory, post-hoc numbers (cache-only script, reproduced by us, not saved in
`results/`), all with the **proxy** drop D_proxy = spread_37 − min_j spread_excl_j (37-host reference fit,
the about 740 of the 1,000 37-host subsets that exclude the host): D_proxy real = 0.280 (1.3071 − 1.0267);
P(D_proxy ≥ 0.280) = 0.006 under C (2,000 simulations, seeds 20,000–21,999, the R2-RE-SEL seeds; 99th
percentile 0.251), 0.019 under V(0.05) and 0.036 under V(0.077) (1,000 simulations each, seeds
50,000–50,999 for both τ); the joint event "spread_37 ≥ 1.307 and min spread_excl ≤ 1.027" 0.002 under
both V; the criterion-S spread test rejects V at 5% in 21% (τ = 0.05) and 45% (τ = 0.077) of simulations;
the real post-selection value is reached or undercut in 66% and 39%; P(spread_37 ≥ 1.307) = 25/2,000 under
C; conditional on a high simulated spread_37 the post-selection spread is ≥ 1.033 in 82–89%. While
drafting this addendum (cache only, no simulation): (i) by arithmetic on recorded values, the exact
D_obs = 1.3070929 − 1.0325255 = 0.2746 (0.0058 below the proxy: the proxy keeps N5584 in the reference fit
and uses about 740 subsets, the exact value refits on 36 hosts and uses 1,000 subsets); (ii) N5584's
calibrator rows are rows 3178–3181 (one SN, 2007af, four light-curve rows, non-zero in columns 26 and 42,
√C_ii 0.086–0.148 mag); (iii) one GLS fit under C of `rows_a` with an extra column, the indicator of
those four rows, gives δ̂ = +0.3363 mag with standard error σ_δ = 0.0925 mag (3.6σ); (iv) timings: the
Cholesky factor of C on `rows_a` 0.23 s, one K ε plus one 1,000 × 3,489 matrix–vector product 5.7 ms. Not
yet run: any simulation of the exact D or of J under any model, any simulation of a single-host offset
model, in code or by hand; no code for this addendum exists. N5584 was identified post hoc (R2-RE-SEL,
"How N5584 was singled out"), and δ̂ is estimated on the same data that the test uses. Found at the
first review of this addendum (gate 1, 2026-11-21), by a toy calculation and not from these data: the raw
probability of the quadrant anchored at the observed point (the form of the referee's joint event, and of
J in the first draft of this addendum) is not a valid p value. Under the true model the data sit at the
corner of their own quadrant, so the quadrant probability is stochastically far below uniform: for a
bivariate normal, reading "excluded" when it is below 0.05 happens in 20% of draws at correlation 0, 41% at
0.8 and 53% at 0.9 (for independent uniform coordinates P(quadrant probability ≤ t) = t(1 − ln t), 0.014
at t = 0.002). spread_37 and spread_36 are strongly correlated, so the referee's 0.002 overstates the
evidence against V; J is therefore calibrated below.

*Expected outcome (stated now).* The proxy 0.002 under V(0.05) and V(0.077) is the raw quadrant
probability over 1,000 draws (with the proxy spread_36), not a calibrated p. The calibrated p_J is
expected to be larger, at least several times so (about seven times for independent coordinates; more
for correlated ones), by an amount we cannot estimate from recorded numbers: it may stay below 0.05 for
V(0.05) and V(0.077), and may lie above 0.05 for V(0.105). V(0.105) is untested; a larger τ raises the
36-host spread (against V) but also the 37-host spread (towards the data), so the direction is not clear.
D should exclude V(0.05) (proxy 0.019); for V(0.077) the proxy 0.036 rests on 1,000 simulations and the
exact D_obs is 0.006 smaller, so "undetermined (Monte Carlo)" or "not excluded" is as likely as
"excluded"; D is expected not to exclude V(0.105), because a larger τ also makes larger drops. O(δ̂)
should not be excluded by either statistic, largely by construction (δ̂ is fitted to these data). Rule
(2) with the qualifier "joint statistic only" and rule (3) ("diffuse host scatter not excluded", most
likely through τ = 0.105) are both plausible; we do not rank them.

*Question.* Is the excess calibrator scatter of the 37-host system better described by one host offset
(N5584 shifted by δ, all else under C) than by a host-level random effect on all 37 hosts (V(τ), τ =
0.05, 0.077, 0.105 mag), judged by how often each model produces data as "one-outlier-like" as observed
(a 37-host spread as high together with a post-selection 36-host spread as low, calibrated: J), and a
drop as large as observed (D)?

*Statistics (the same on data and simulations).* For a data vector y on `rows_a`:
- spread_37 = `numpy.std` (ddof 0) of Δ_k/σ_k over the first 1,000 R4 subsets on 37 hosts, with the shift
  rows a_k and σ_k of R2-RE-ROB part B (`rob.shift_rows` with the 37-host reference fit under C). On the
  real y this is ROB's spread_obs.
- d' = criterion S of R2-RE-SEL: argmin_j spread_excl_j on the same rows (ties to the lowest column).
- spread_36 = the R2-RE-SEL spread for dropped host d': `sel.reduced_system` for d', its reference fit
  under C, the first 1,000 index draws of R4-N's stream (`sel.index_stream(1000, r4_seed, 36, 10)`) mapped
  onto the 36 other host columns, shift rows and σ_k from `rob.shift_rows`. On the real y (d' = N5584) this
  is B-N's spread_obs.
- **D = spread_37 − spread_36** (exact; d' is still chosen by the proxy criterion S, which is only a
  selection rule, used identically on data and simulations). D_obs = 0.27457 from the recorded values;
  the run uses the full-precision value it computes (all printed thresholds here are rounded).
- **J (calibrated quadrant statistic).** For a point x = (spread_37, spread_36) and a model M, the
  quadrant probability Q_M(x) is the probability that spread_37 ≥ x's spread_37 and spread_36 ≤ x's
  spread_36: high with all hosts, ordinary without the selected one. A small Q_M(x) means x is
  "one-outlier-like" for M. Q_M at the observed point is not itself a p value (see "Seen before"), so it is
  calibrated: split the 10,000 simulations of M into half A (s even) and half B (s odd, n_B = 5,000);
  T_M(x) = the share of half-A simulations in x's quadrant (Q_M estimated on A); t_obs = T_M(observed
  point) and t_i = T_M(x_i) for each simulation i of half B; **p_J = (1 + k_J)/(1 + n_B), k_J = #{i in B:
  t_i ≤ t_obs}** (ties counted, which errs towards larger p). Because A and B are independent and x_i is a
  draw from M, p_J is a valid Monte Carlo p value for "the data are as one-outlier-like as M produces". The
  observed point (1.30709, 1.03253, full precision in the run) was chosen after seeing the data, as the
  referee's joint event was; the calibration removes the corner effect, not that choice. The raw
  quadrant probability Q_M(observed) over all 10,000 simulations is reported, descriptive only.
- The σ_k and a_k always come from fits under C: the statistic is fixed, only the data model changes.
  Adding L q to y changes no Δ_k, so ŷ = L q̂ does not affect D or J.

*Models.* All simulate y_M,s = ŷ + K_M ε_s (+ offset) on `rows_a` (3,489 rows, 37 hosts), ŷ = L q̂ from
the fit under C (as in ROB and SEL), K_M the lower Cholesky factor of the model covariance on `rows_a`.
- C: K_C from C.
- V(τ), τ = 0.05, 0.077, 0.105 mag (decisive): K from `with_re(C, calib_groups, τ)` (τ² added on each
  host's calibrator SN block). 0.077 is R2-RE's τ̂, 0.05 and 0.105 the ends of its 68% interval (0.048 and
  0.105, rounded). T-048 named 0.05 and 0.077; 0.105 is added because D grows with τ, so a diffuse model
  can only be called excluded if the upper end is excluded too.
- O(δ̂) (decisive): y_C,s + δ̂ h, h the indicator of N5584's calibrator rows (`calib_groups[26]`, the four
  rows above), δ̂ the GLS coefficient of h fitted with L under C on `rows_a` (recorded 0.33634; the run
  refits and must reproduce it to an absolute 5 × 10⁻⁶, the precision at which it was recorded (amendment
  2026-11-21, before any simulation on the data: first written as a relative 10⁻⁶, which a 5-digit value cannot
  meet; the full value 0.33633686472064284 seen since came from the code's own cache-only reproduction run, so
  it is not used as the reference); a mismatch is rule (1), the whole block). The offset is on the calibrator SN rows only, where R2-RE puts the random effect and R2-RE-T
  the heavy tail; whether it belongs to the SN or the Cepheid distance the data cannot tell (section 7).
- Reported, not decisive: O(δ̂ − σ_δ) (δ = 0.2438, one standard error towards zero, the analogue of
  τ = 0.05); O(δ̂) + V(τ̂_N) (N5584 offset and τ̂_N = 0.0314 on all 37 hosts, the "one outlier plus a
  small diffuse term" reading of R2-RE-N5584; τ̂_N from the same run); O_any(δ̂): the offset on a host
  drawn uniformly from the 37 in each simulation (`numpy.random.default_rng(200_000 + s).integers(0,
  37)`), the single-outlier model without N5584's identity.
- Seeds: ε_s = `numpy.random.default_rng(100_000 + s).standard_normal(3489)`, s = 0, …, 9,999, the same
  ε_s for every model (common random numbers: O(δ̂) is exactly C plus the offset, and model differences
  are not Monte Carlo noise between independent streams). 100,000–109,999 and 200,000–209,999 collide
  with none of R4/R4-N (0), ROB and B-N (10,000–11,999), SEL (20,000–21,999) or the referee's exploratory
  V runs (50,000–50,999). n = 10,000 per model (8 models, 80,000 simulations).

*Why δ̂ is (partly) circular, and what the design does about it.* δ̂ is fitted on the same y and
N5584 was singled out by these data, so O(δ̂) reproduces the observation largely by construction: "not
excluded" for O(δ̂) is a consistency check, not evidence. The information in the reading is in whether
the diffuse models are excluded; their τ values come from the same data too (τ̂ = 0.077 is fitted with
N5584 included, which inflates it towards larger diffuse scatter), so both alternatives carry one fitted
parameter. The reported O(δ̂ − σ_δ) and O_any variants show how much "not excluded" depends on the
plug-in value and on the identity of the host. No composite test (δ refitted in each simulation) is made.

*Comparison.* For each model M: D: k_D = #{D_s ≥ D_obs} over all n = 10,000 simulations, p_D = (1 +
k_D)/(1 + n), with the two-sided equal-tailed 95% Clopper–Pearson interval for k_D/n (`rob._cp`); J: p_J
as above, with the Clopper–Pearson interval for k_J/n_B (n_B = 5,000). Per model and
statistic the label is: interval entirely below 0.05 → **"excluded (<D|J>)"**; entirely above 0.05 →
**"not excluded (<D|J>)"**; containing 0.05 → **"undetermined (Monte Carlo)"** (`rob.three_way`).
Reported, not decisive: the density ratio of O(δ̂) to each V(τ) and to C at the observed point, from
`scipy.stats.gaussian_kde` (Scott bandwidth) in two dimensions (spread_37, spread_36) and in one (D), with
a 68% interval from 200 bootstrap resamples of the simulations (`default_rng(300_000 + b)`) and the same
ratio with the bandwidth halved (tail densities depend on the bandwidth, so no label uses them).

*Decision rules and labels, fixed now (in this order).* R2-RE's row ("no host-selection effect
detected") stays the headline; the R2 (2026-11-14), R2-RE, R2-RE-ROB, R2-RE-N5584 and R2-RE-SEL verdicts,
labels and readings stay as recorded.
- (1) Not evaluable: the observed values differ from the recorded ones (spread_37,obs = 1.3070929081086322
  and spread_36,obs = 1.0325254787240916 to a relative 10⁻⁹, criterion S selecting N5584 with spread_excl
  within 0.001 of 1.027, δ̂ = 0.33634 to an absolute 5 × 10⁻⁶) → the whole block (code or data change,
  investigated first); a fit failure while building the 37-host shift rows or the rows of the reduced
  system without N5584 → the whole block; an empty index stream (R4's or R4-N's) → the whole block; a fit
  failure while building the rows for another dropped host d → every model with at least one simulation
  whose d' = d is not evaluable (as `sel.spread_part` does); a failed Cholesky factor of a model → that
  model not evaluable; any decisive model not evaluable → reading "not evaluable".
- (2) Every V(τ) (0.05, 0.077, 0.105) "excluded (J)", and O(δ̂) "not excluded (J)" and "not excluded
  (D)" → **"the three tested diffuse models V(0.05), V(0.077), V(0.105) excluded by J; one offset host not excluded"**
  (this does not establish that the one-offset-host model is preferred: O(δ̂) is fitted to the same data,
  so its non-exclusion is a consistency check), with the qualifier
  "(both statistics)" if every V(τ) is also "excluded (D)", else "(joint statistic only; D does not exclude
  τ = <list>)".
- (3) Any V(τ) "not excluded (J)" → **"tested diffuse model(s) not excluded (τ = <list>)"**.
- (4) Every V(τ) "excluded (J)" and O(δ̂) "excluded (J)" or "excluded (D)" → **"neither one offset host
  nor diffuse scatter reproduces the observed spreads"**.
- (5) Otherwise → **"undetermined"**.
- C's labels are reported next to them (expected "excluded" by D; ROB found P(spread_37 ≥ 1.307) =
  0.021 under C, but the calibrated p_J need not be as small); they enter no rule.
- "Diffuse" means V at these three fixed τ values only, not a test over a range of τ: the values were
  chosen after seeing the data (R2-RE's τ̂ and its 68% interval on these data), the calibration treats
  each as fixed and does not account for that choice or for the uncertainty of τ, so no range-level claim
  is made; the conjunction in (2) needs three
  intervals below 0.05; the union in (3) is not corrected for three looks; the labels share ε_s and are
  correlated.

*What changes in section 5 (the text, not any earlier label).* A new subsection "R2-RE-D". Reading (2) →
the R2-RE-SEL post-hoc bullet ("points towards one outlying host but does not show it") is replaced by this
pre-registered reading, quoted with the caveats: δ̂ fitted on the same data, N5584 identified post hoc, J's
quadrant anchored at a point chosen after seeing the data (calibrated, but chosen post hoc), C taken as correct (R2-RE-SEL referee point 5), and, if so labelled, "joint
statistic only". Reading (3) → section 5 states that the data do not distinguish one outlying host from
host-level scatter of R2-RE's size; R2-RE-SEL's reading stays, glossed "consistent with C after removing one
host, and not distinguished from diffuse scatter". Reading (4) → section 5 states that neither model
reproduces both spreads, and the "one outlying host" gloss is marked unsupported. Reading (5) or "not
evaluable" → the post-hoc bullet stays as it is, with this outcome next to it. Section 7's open question
"is the excess one outlying host or scatter spread over all hosts?" is answered accordingly. In no case do
the R2-RE headline row, `summary.json` `R2_host` or the claim's verdict change.

*Reported (not decisive).* Per model: k, n, p, interval and label for D and J (with t_obs); the raw
quadrant probability Q_M(observed) over all 10,000 simulations, with its Clopper–Pearson interval
(descriptive only: not a p value); quantiles (5/50/95%) of spread_37, spread_36 and D; P(spread_37 ≥ obs)
and P(spread_36 ≤ obs) separately; the frequency of each d' and how often d' = N5584 (and, for O_any, how
often d' is the offset host); the proxy D_proxy with P(D_proxy ≥ D_proxy,obs), D_proxy,obs = 0.2804099…
(full precision in the run), for comparison with the referee's exploratory numbers (other seeds, so
agreement within Monte Carlo error is expected, not required); the KDE ratios above. Checks and seconds
per part. Per-simulation values are saved so that every label can be re-derived: one file per model,
`results/r2_re_d_sims_<model>.json` (model keys `C`, `V050`, `V077`, `V105`, `O`, `Olo`, `OVN`, `Oany`),
holding the 10,000 (spread_37, spread_36) pairs rounded to 4 decimals, d' per simulation, and for each
half-B simulation the integer count of half-A simulations in its quadrant, plus that count at the observed
point (about 400–450 KB each as pretty-printed JSON, about 3.3 MB in all, every file below 1 MB; amended
2026-11-21 from "about 180 KB", which did not count the JSON layout). The test recomputes k_J exactly from the saved integer
counts, checks those counts against the pairs only away from rounding ties (pairs within 5 × 10⁻⁵ of each
other in either coordinate are skipped), and recomputes k_D from the pairs except within 1.5 × 10⁻⁴ of D_obs
(the largest rounding error of a difference of two rounded values is 10⁻⁴).

*Runtime (from measured times).* Recorded in `r2_re_sel.json`: criterion S's 37-host rows 109 s
(`criterion_s_rows`); the 37 reduced systems' rows 100–115 s each, 4,067 s in all
(`dropped_hosts_built.seconds_build`); the selection pass 14.4 s for 2,000 simulations under both
criteria. The shift rows do not depend on y or on the data model (the statistic is fixed under C), so they
are built once and shared by all eight models: at most 37 reduced systems, about 68 min, not 70 min per
model as the T-048 note assumed. Per simulation, pass 1 (K ε, spread_37, criterion S) is about 7 ms
(selection pass) and pass 2 (regenerate y, one reduced-system product, grouped by d' so one matrix is held
at a time) about the same: 80,000 × about 15 ms ≈ 20 min. Five Cholesky factors (C, the three V(τ) and
V(τ̂_N)), 5 × 0.23 s, each 3,489 × 3,489 in float64 (97 MB), about 0.5 GB held at once (plus one
1,000 × 3,489 shift-row matrix, 28 MB, at a time); the calibration of J (5,000 quadrant counts over 5,000
points per model) and the KDE bootstrap a minute or two. Block ≈ 1.5 h (1.2–1.8 h; an estimate until the implementation is timed); the reported variant O(δ̂) + V(τ̂_N) needs one REML fit for
τ̂_N (about a minute). Run in a standalone mode (`PARAMS["d_only"] = true`): it recomputes only what the
block needs (the fit under C on `rows_a`, the R4 and R4-N index streams, the reduced system for N5584 and
its REML τ̂_N, the checks above; host identification and R1 are computed internally but not saved with
`ctx.save`), writes `results/r2_re_d.json` and the per-model `r2_re_d_sims_<model>.json` files, updates
only the `R2_RE_D` key of `summary.json` and keeps every other key byte-identical, records its run with
`ctx.record_suffix = "_d"` (`provenance_d.json`, `run_info_d.json`), and leaves every other results file
untouched; it does not rerun the ~9.3 h of earlier blocks. No data downloaded (cache only); it waits until
no other study run uses the machine. 10,000 per model gives a Clopper–Pearson half-width of about 0.0045
near p = 0.05 for D; J's calibration uses n_B = 5,000, a half-width of about 0.006 near 0.05. More
simulations after the run would need a new
pre-registration. The τ analogue (τ̂_37 − τ̂_36 under V, about 4 h of REML fits) is not part of this
addendum.

*Code checks before the formal run.* Synthetic data only (the 2026-11-17 smoke-run lesson, log.md): the
statistic on a small synthetic system, the offset added only to the chosen host's calibrator rows, the
common ε_s across models, D and J from known inputs, the rule order (1)–(5) and the qualifier. On the
real data before the formal run only the reproduction checks (spread_37,obs, spread_36,obs and D_obs =
0.27457, criterion S selecting N5584 at 1.0267, D_proxy = 0.2804, δ̂ and σ_δ), all reproducing numbers
recorded here; no simulation on the real ŷ, no p value or label.

*Switch and code.* `PARAMS["d_check"]` (true), with `"d_seed_base": 100_000`, `"d_n_sims": 10_000`,
`"d_taus": [0.05, 0.077, 0.105]`, `"d_host_seed_base": 200_000`, `"d_kde_boot": 200`, `"d_only": false`
(the default; set to true only for the formal R2-RE-D run and back to false after it, with a dated note in
log.md); the offset host is `PARAMS["n5584_host"]`; the recorded δ̂, spreads and tolerances are module
constants, as in `sel.py`. In the standalone mode the block computes τ̂_N itself (R2-RE's REML on the
reduced system without N5584, which must reproduce the recorded 0.03137144… (`sel.RECORDED_TAU_N`, the full value of the R2-RE-N5584 run) to a relative 10⁻⁶, else that
reported variant is "not run"); in a full run it runs after the R2-RE-SEL block under the same condition
as the R2-RE-N5584 block. Planned module `onehost.py` (receives `run.py`'s functions, reuses `rob.shift_rows`, `rob._cp`,
`rob.three_way`, `sel.reduced_system`, `sel.index_stream`, `sel.crit_s_values`, `sel.pick_min`; does not
import `run`), results in `results/r2_re_d.json`, a short summary in `summary.json` (`R2_RE_D`), a test
`test_onehost.py` (synthetic checks, including the calibration of J on two bivariate-normal toy models
(correlation 0 and 0.8, fixed seed, 2,000 toy replicates of 2,000 simulations each): the share of replicates
with p_J ≤ 0.05 must not exceed the upper end of the 99% Clopper–Pearson interval of 0.05 for the calibrated
statistic (amendment 2026-11-21, before any simulation on the data: one-sided, since a valid test may be
conservative and counting ties towards larger p makes it so at the toy size; the two-sided version failed
at correlation 0.8, share 0.0365; with a lower guard so that a J that always returns large p fails: the share
of p_J ≤ 0.05 at least 0.02 and the share of p_J ≤ 0.5 within [0.45, 0.55] at both correlations), and
outside it for the raw quadrant probability at correlation 0.8; labels re-derived from saved k and n and from the per-simulation files), conclusion assertions in
`test_conclusions.py`, a web section, section 8 knobs. None of this exists yet.

### Addendum 2026-11-21: R2-RE-G, a composite shape test of one offset host against diffuse host scatter (T-055), pre-registered before any of these simulations

*Why.* R2-RE-D (T-048) read "tested diffuse model(s) not excluded (τ = 0.077, 0.105)", and its referee (section 6,
R2-RE-D points 2–4) found three weaknesses: the comparison has only about 50% power against its own one-host
alternative; both alternatives use plug-in values fitted to the same data (δ̂ is the offset of the host already
selected as most extreme, τ̂ = 0.077 is fitted with N5584 included); and the statistics are not specific to one
outlier (part of J's exclusion is "too much total scatter"). The referee's point 10 proposed the test registered
here: a shape statistic G, the share of the summed squared host-offset z-scores carried by the largest one,
calibrated under diffuse host scatter with τ refitted in each simulation (a composite null, not a plug-in at fixed
τ), with its power against a single offset host on a random host, σ-matched to the observed outlier, fixed and
reported before the data value of G is computed. The maximum over the 37 hosts puts the choice of the outlier
inside the statistic, so N5584's identity is not used. This block attaches a label to R2-RE-D's reading; it changes
no earlier label or the headline.

*Seen before this addendum.* Everything in sections 5–7 and log.md, in particular: R2-RE τ̂ = 0.07669875579792439
(68% interval 0.0477–0.1050; Δ(−2ℓ_R) = 3.50 at τ = 0) and its saved REML grid (`r2_re.json` `reml.grid_m2l`, 51
values, used below as a reproduction check); R2-RE-ROB part B (null τ̂ zero in 230 of 400 simulations); R2-RE-N5584
(τ̂_N = 0.0314 without N5584; ν = 4 weights, N5584 ω̂ = 0.392, next N1365 0.804, N3982 0.879); R2-RE-SEL (all of
section 5); R2-RE-D: N5584's one-column offset δ̂ = 0.3363369 mag, σ_δ = 0.0925160, **z = δ̂/σ_δ = 3.6354** (so the
numerator of the observed G, z² = 13.22, is known if N5584 is the largest), every model's p_D and p_J (C 0.0057 and
0.017; V(0.05) 0.016 and 0.039; V(0.077) 0.034 and 0.080; V(0.105) 0.076 and 0.068; O(δ̂) 0.52 and 0.68; O_any 0.13
and 0.30), the reading (rule (3)), criterion S finding the offset host in 4,358 of 10,000 O_any simulations; the
R2-RE-D referee's post-hoc figures (halves swapped: p_J 0.061, 0.077, 0.070, 0.016 for V(0.05), V(0.077), V(0.105),
C; power of J against V(0.077) and V(0.105) 54% and 57% if O(δ̂) is true, 20–30% if O_any is true; D 57%, 45% and
10–15%; under C, P(spread_37 ≥ obs) = 0.013 against p_J = 0.017). The per-host leave-one-out χ² terms under C
(`r2_re.json` `loo_chi2.C`: 64.9 in all on 77 rows; N5584 12.48 on 4 rows, N2525 5.84 and N1015 5.39 on 3 rows each, N3982 4.25 on 1 row)
are related to the z_j² of this addendum (for a one-row host they measure the same residual, up to the
cross-covariance the leave-one-out statistic ignores; for a multi-row host z_j² is the one-degree-of-freedom part
along the host indicator), so the denominator of the observed G can be guessed; we have not computed it. While
drafting (no data, no simulation): the algebra below (the reduced REML form, z = W y, Cov(u) = M + τ²M²) was checked
on a random synthetic system (60 rows, agreement to 10⁻¹³), and the per-simulation costs were timed on random
synthetic matrices of the real sizes (single thread). Not yet computed: z_j for any host other than N5584, Σ_j z_j²,
G on the data or in any simulation, the matrix M, any τ̂ refitted in a simulation, any power or size; no code for
this addendum exists.

*Expected outcome (stated now).* A rough guess from the recorded numbers (not a calculation of this test): the
observed G is about 0.2–0.35 (13.2 over a sum of about 40–55). Under C the largest of 37 one-degree-of-freedom z²
exceeds about 10 in 5% of draws (independent terms), more under V(τ) because the z_j of precisely measured hosts
are inflated most; under O_any σ-matched to z = 3.64 the outlier's z² is about 13 on average, while its own τ̂_s is
pulled up by the outlier, which widens the null it is tested against. So the power against O_any at z_obs (on C, and on V(τ̂_N)) is
expected to be modest, roughly 0.2–0.6, and **"undetermined (underpowered)" is the most likely reading**; the
reported power curve then says how large a single offset these 37 hosts could separate from diffuse scatter. If the
power reaches 0.8, we do not rank "preferred" against "not excluded". The size of the plug-in bootstrap test under
V(τ) at the three checked values τ = 0.05, τ̂_obs ≈ 0.077 and 0.105 is expected near or below 0.05 (G's null distribution changes slowly with τ, and the label requires the whole
Clopper–Pearson interval below 0.05).

*Question.* With τ refitted in every simulation and the outlying host chosen inside the statistic, are the
calibrator host offsets more concentrated in one host than host-level scatter spread over all 37 hosts (V(τ))
produces, by a test whose power against one σ-matched offset host is fixed before the data value is read?

*Statistic (the same on data and simulations).* On the NGC 4258-only system (`rows_a`, 3,489 rows, 37 hosts, the
amended host labelling): X = the columns of L fitted on `rows_a` (`infer.gls`'s `kept`, as in R2-RE's REML); C_a = C
on `rows_a`; P = C_a⁻¹ − C_a⁻¹X(XᵀC_a⁻¹X)⁻¹XᵀC_a⁻¹ (the GLS residual projector under C); Z = (h_1, …, h_37), h_j the
indicator of host j's calibrator SN rows (`calib_groups[j]`, as in R2-RE and R2-RE-D); M = ZᵀPZ (37 × 37); u = ZᵀPy.
- **Host-offset z-scores, one host at a time:** z_j = u_j / √M_jj. This is δ̂_j/σ_δ,j, where δ̂_j is the GLS
  coefficient of the single extra column h_j added to L and fitted under C on `rows_a`, and σ_δ,j = M_jj^(−1/2) its
  standard error (the Frisch–Waugh–Lovell identity for GLS); for N5584 it is R2-RE-D's `fit_delta`, z = 3.6354.
- **G = max_j z_j² / Σ_j z_j²** over the 37 hosts (between 1/37 and 1; scale-free); ĵ = the argmax (ties to the lowest
  column), reported.
- **One matrix–vector product per simulation:** z = W y with W = diag(M_jj^(−1/2)) ZᵀP (37 × 3,489, computed once
  from one Cholesky factor of C_a). WX = 0, so ŷ = L q̂ and any L q drop out, as in R2-RE-D.
- *Why one host at a time, not a joint fit.* The joint fit with all 37 offsets is expected to be rank-deficient: their
  sum is the calibrator part of the M⁰_B column, and the calibrators are what separates M⁰_B from 5 log H0 (the code
  attempts the joint fit once and reports its rank; it is not used either way). The one-at-a-time z_j is the standard
  mean-shift outlier statistic, is exactly the matrix–vector product the referee asked for, and reproduces the recorded
  N5584 value.

*The diffuse null, with τ refitted in each simulation.* V(τ) = C + τ²ZZᵀ, R2-RE's model. Exact facts used (standard
identities for V = C + ZGZᵀ; PC_aP = P): under V(τ), u ~ N(0, M + τ²M²); an offset δ on host k's calibrator rows
adds δ M e_k to the mean of u. R2-RE's restricted likelihood, −2ℓ_R(τ) = log det V + log det XᵀV⁻¹X + rᵀV⁻¹r,
equals, up to a constant that does not depend on τ, **f(τ; u) = Σ_i [log(1 + τ²λ_i) − τ² v_i² / (1 + τ²λ_i)]**,
with M = Q diag(λ) Qᵀ and v = Qᵀu. So τ̂ depends on the data only through u, and one evaluation costs O(37).
Numerical rank: eigenvalues with |λ_i| < 10⁻¹⁰ · max λ are set to 0 (in f and in the inner draws below), so a
rank-deficient or near-singular M gives finite values; every M_jj must be positive (rule (1)), so every z_j is defined.
- **Estimator:** R2-RE's procedure applied to f, `reml_tau(f, 0.5, 0.01, interval=False)`: grid τ = 0, 0.01, …, 0.50
  mag, then `minimize_scalar` (bounded, xatol 10⁻⁵) on the grid interval around the grid's global minimum, the
  better of the refined and the grid minimum (the grid minimum if the refinement fails); τ̂ < 10⁻³ counts as zero
  (V = C); τ̂ > 0.5 − 10⁻³ is "at the upper bound": in a simulation it is kept as its value (counted and reported,
  as in ROB), on the real data it is rule (1).
- **Refit in every simulation, not on a grid:** the reduced form makes a refit cost about 0.1–1 ms (synthetic timing),
  so τ̂_s is refitted exactly in each of the 130,000 outer simulations; a fixed τ grid is not needed.
- **Reproduction on the real data (rule (1)):** f(τ_i; u_obs) − f(0; u_obs) equals R2-RE's saved grid_m2l_i − grid_m2l_0
  at all 51 grid points within 10⁻⁵ (absolute), and τ̂_obs reproduces 0.07669875579792439 within 2 × 10⁻⁵ (absolute;
  twice the optimiser's xatol, since its path can differ in the last digits). τ̂_obs (full precision from the run)
  defines the null V(τ̂_obs).
- **G is not pivotal in τ.** Under V(τ) the z_j of precisely measured hosts are inflated more than the others, so G's
  null distribution depends on τ. This is handled by drawing the null exactly at the refitted τ̂ (no pivotality is
  assumed), by measuring the size of the whole procedure with τ refitted, decisively under VHAT, V050 and V105
  (rule (1)) and reported under C, and by the double-bootstrap p_dbl (reported). The composite-null claim is therefore
  calibrated at the three checked values τ = 0.05, τ̂_obs ≈ 0.077 and 0.105 only (the ends of R2-RE's 68% interval and
  τ̂_obs); interior values are not checked and no monotonicity of the size in τ is assumed.

*The test applied to one data vector (real or simulated).* For a data vector with statistic G and refitted τ̂:
k = #{i: G_i^in(τ̂) ≥ G} over N_in = 20,000 inner draws, **p_boot = (1 + k)/(1 + N_in)**, and the label
`rob.three_way(k, N_in, "excluded", "not excluded")` (signature `three_way(k, n, unusual, usual)`): the two-sided 95%
Clopper–Pearson interval of k/N_in entirely below 0.05 → "excluded",
entirely above → "not excluded", containing 0.05 → "undetermined (Monte Carlo)"; the label uses k/N_in, while p_boot = (1 + k)/(1 + N_in). The inner draws are exact draws of u
from N(0, M + τ̂²M²): z_i = diag(M_jj^(−1/2)) Q diag(√(λ(1 + τ̂²λ))) e_i (λ clipped as above), with e_i the rows of one fixed matrix
E_in = `numpy.random.default_rng(600_000).standard_normal((20_000, 37))`, the same for every evaluation (common random
numbers). On the real data: **p_G = p_boot(G_obs, τ̂_obs)** with its interval and label.

*Models (outer simulations).* Each outer simulation is a full data vector y_s = ŷ + K ε_s (+ offset) on `rows_a`, as in
R2-RE-D, with ε_s = `numpy.random.default_rng(400_000 + s).standard_normal(3489)`, s = 0, …, 9,999, the same ε_s for
every model (common random numbers), and K the lower Cholesky factor of the model covariance on `rows_a`. It is
computed as z_s = B ε_s (+ the offset's term) with B = W K (37 × 3,489, once per covariance), which equals W y_s
exactly. In each simulation: z_s, G_s, ĵ_s, u_s → τ̂_s (refitted), then p_boot,s, k_s and the label at τ̂_s.
- **VHAT (decisive null):** V(τ̂_obs). Its rejection rate is the size at τ̂_obs.
- **V050 and V105 (decisive for the size):** V(0.05) and V(0.105), the ends of R2-RE's 68% interval (0.048 and 0.105,
  rounded as in R2-RE-D), the null in each simulation still V(τ̂_s) refitted. Their rejection rates are the size at these
  two checked values (Codex review, before any run, 2026-11-21: first registered with VHAT's size only; round 2: claim restricted to the checked values).
- **OANY (decisive alternative):** C plus an offset on one host k_s drawn uniformly from the 37
  (`numpy.random.default_rng(500_000 + s).integers(0, 37)`), **σ-matched**: δ_k = z_obs · σ_δ,k on host k's calibrator
  SN rows, with z_obs = δ̂/σ_δ of N5584 from the run (recorded 3.6354437025541553), so the offset host's expected z is
  z_obs whatever its σ_δ (R2-RE-D referee point 7). Its rejection rate is R_OANY. Its τ̂_s is refitted with the
  outlier inside, as τ̂_obs is fitted with N5584 inside, so the power includes the widening of the null that an outlier
  causes.
- **OANYVN (decisive alternative):** OANY on V(τ̂_N) instead of C, τ̂_N = `sel.RECORDED_TAU_N` = 0.0314 ("one outlier
  plus a small diffuse term", R2-RE-N5584's reading), with the same host draws and σ-matching. The **power** is
  min(R_OANY, R_OANYVN): the test must be powered against one offset host both on C and on a small diffuse background.
- Reported, not decisive: **C** (size when there is no excess); **OANYLO** (OANY with z_obs − 1 = 2.635: a one-standard-error
  sensitivity of the σ-matched magnitude, not a correction for the winner's curse of z_obs being the largest of 37);
  **O** (R2-RE-D's O(δ̂): δ̂ on N5584 itself,
  on C); and a **power curve**, OANY with z_alt = 2.5, 3.0, 4.0, 4.5 and 5.0 (counts only).
- Seeds 400,000–409,999, 500,000–509,999 and 600,000 collide with none of R4/R4-N (0), ROB and B-N (10,000–11,999), SEL
  (20,000–21,999), the referee's V runs (50,000–50,999), R2-RE-D (100,000–109,999, 200,000–209,999) or its KDE bootstrap
  (300,000–300,199). All OANY variants share the host draws.
- **Counts:** n = 10,000 outer simulations per model and per curve point (13 sets, 130,000 simulations); N_in = 20,000
  inner draws (fixed: it is part of the test). **Runtime guard:** the first 1,000 VHAT simulations are timed; if the
  projection for all sets exceeds `g_max_minutes` = 120 min, n drops to the largest multiple of 1,000 that fits, with a
  floor of 5,000 (recorded in the results); if even 5,000 does not fit, the block is "not evaluated (runtime)".
  The guard runs in the power stage only: the full stage takes n and the guard decision from `r2_re_g_power.json` and
  does not re-time. N_in never changes.

*Power, size and their order (fixed before the data value is read).* For a model m, R_m = #{s: label_s =
"excluded"}/n, with its Clopper–Pearson interval. **Power = min(R_OANY, R_OANYVN)** (point estimates) and the **size** = max(R_VHAT, R_V050, R_V105), at the three checked values τ = 0.05, τ̂_obs and 0.105 only. Neither
depends on G_obs: power uses only the design (L, C, the host groups), z_obs and the recorded τ̂_N; size also uses τ̂_obs. The block runs
in two stages. **Power stage** (`g_stage = "power"`): the reproduction checks that use no data value beyond those
recorded here (τ̂_obs, the REML grid, δ̂, σ_δ and z_obs of N5584), then all outer simulations; it writes
`results/r2_re_g_power.json` (counts, power, size, curve, τ̂_s summaries, checks); it computes u_obs in memory only for the REML
reproduction and never forms, saves or logs the z_j of hosts other than N5584, Σz² or G_obs. Its power, size and curve are written into log.md and committed on the
branch **before** the full stage is started. **Full stage** (`g_stage = "full"`): recomputes the power stage with the n recorded there (its
counts must equal those of `r2_re_g_power.json` exactly), then computes G_obs, p_G and the reading. In a full study
run both stages run in this order in one process, the power record saved and logged before G_obs is computed.

*Decision rules and labels, fixed now (in this order; exactly one applies).* R2-RE's row ("no host-selection effect
detected") stays the headline; the R2 (2026-11-14), R2-RE, R2-RE-ROB, R2-RE-N5584, R2-RE-SEL and R2-RE-D verdicts,
labels and readings stay as recorded.
- (1) **Not evaluable** (with the reason), when any of these holds: a reproduction check fails (the REML grid
  differences, τ̂_obs, δ̂ = 0.33634 within 5 × 10⁻⁶ absolute, σ_δ = 0.09251604267299487 and z_obs =
  3.6354437025541553 within a relative 10⁻⁶; in the full stage also W y on the real data against the 37 one-column GLS
  fits, |Δz_j| ≤ 10⁻⁸ for every host); a pointwise check fails (for the first three simulations of VHAT and of OANY,
  y_s built in full, the 37 one-column GLS z against B ε_s within 10⁻⁸, and τ̂_s from the reduced form against
  `reml_tau` on `reml_m2l` within 2 × 10⁻⁵); τ̂_obs at the upper bound; some M_jj ≤ 0; the Cholesky factor of C, V(τ̂_obs), V(0.05), V(0.105) or V(τ̂_N) fails;
  the full stage does not reproduce the power stage's counts; the runtime guard's floor is not met ("not evaluated
  (runtime)"); or the test is anti-conservative: the 95% Clopper–Pearson interval of the rejection rate lies entirely above 0.05
  under any of VHAT, V050 or V105 → "not evaluable (anti-conservative at τ = <list>)" (Codex review, before any run, 2026-11-21: first registered with VHAT's size only; round 2: claim restricted to the checked values). A reported model whose factor fails is "not evaluable" alone and enters no rule.
- (2) Power < 0.8 → **"undetermined (underpowered)"**, whatever p_G is (p_G and its label are still reported).
  This is a conservative choice (a rejection by a size-checked test would remain valid at low power): with power below
  0.8 no outcome of G is read as deciding between the two pictures. When p_G's label is "excluded", the sub-label
  **"diffuse excluded; test underpowered against the σ-matched alternative"** is reported with the reading (a sub-label,
  not a separate reading).
- (3) Power ≥ 0.8 and p_G's interval entirely below 0.05 → **"one offset host preferred over diffuse scatter"**.
- (4) Power ≥ 0.8 and p_G's interval entirely above 0.05 → **"diffuse scatter not excluded"**.
- (5) Power ≥ 0.8 and p_G's interval containing 0.05 → **"undetermined (Monte Carlo)"**.
- Notes. 0.8 is compared with the smaller of the two point estimates (n = 10,000, standard error about 0.004; exactly 0.8 counts as
  powered). Rules (3)–(5) use the same three-way Clopper–Pearson label as each simulation, so R_OANY and R_OANYVN are the
  probabilities, under each alternative, that the whole procedure (τ refitted, bootstrap, label) reads "excluded". "Preferred" in (3)
  means that diffuse scatter of the fitted size is excluded (the size checked at τ = 0.05, τ̂_obs ≈ 0.077 and 0.105 only) by a concentration statistic that was powered against one
  offset host; it does not say that the offset is a data defect, nor whether it sits on the SN or the Cepheid side.

*What changes in section 5 (the text, not any earlier label).* A new subsection "R2-RE-G". Reading (3) → section 5
states that, with τ refitted in every simulation and the host chosen inside the statistic, the concentration of the
calibrator offsets in one host is unusual under diffuse host scatter of the fitted size; R2-RE-D's reading stays
recorded, glossed "a powered composite shape test prefers one offset host (R2-RE-G)", with the caveats that G's form
was proposed after the data were seen and that C is taken as correct. Reading (4) → section 5 states that G does not
exclude diffuse scatter with τ = 0.05, 0.077 or 0.105, with a test that would have found a σ-matched single outlier in at least 80% of cases, both on C and on V(τ̂_N); R2-RE-D's
gloss "not distinguished" becomes "diffuse scatter not excluded by a powered shape test", with the reverse check next to
it. Reading (2), (5) or "not evaluable" → section 5 states that no powered shape test separates the two pictures on
these data, quoting the power, the size and the smallest curve z with power ≥ 0.8 (if any); R2-RE-D's reading and gloss
stay. Section 7's open question is answered accordingly. In no case do the R2-RE headline row, `summary.json`
`R2_host` or the claim's verdict change.

*Reported (not decisive).* G_obs, ĵ_obs and its z, Σ_j z_j², all 37 z_j, δ̂_j and σ_δ,j on the real data (full stage);
p_G with k, N_in, interval and label; p_G of the data under fixed V(0.05), V(0.105) and C (inner draws at those τ, same
E_in); the double-bootstrap (prepivoted) p, p_dbl = (1 + #{s in VHAT: p_boot,s ≤ p_G})/(1 + n), which calibrates the
plug-in p_G with τ refitted; the reverse check for OANY and O, p_rev = (1 + #{s: G_s ≤ G_obs})/(1 + n) (at full precision in the run) with its
interval (a small value says the observed offsets are less concentrated than one such offset host typically makes them);
per model: the rejection rate with its interval, quantiles (5/50/95%) of G_s and τ̂_s, the number of τ̂_s at zero and
at the bound, and for OANY-type models how often ĵ_s is the offset host; the power curve and the smallest z_alt with
power ≥ 0.8; the joint-fit rank; checks and seconds per part. Per-simulation values, so that every count can be
re-derived: `results/r2_re_g_sims_<model>.json` for `VHAT`, `V050`, `V105`, `C`, `OANY`, `OANYLO`, `OANYVN`, `O`, holding
G_s (5 decimals), τ̂_s (6 decimals), k_s, ĵ_s and, for the OANY models, the offset host (about 400–550 KB each as
pretty-printed JSON, every file below 1 MB, about 4 MB in all); `results/r2_re_g.json` (full stage) and
`results/r2_re_g_power.json` (power stage), each well below 1 MB. The tests re-derive power, size and every rejection
rate from the saved k_s and the label from the saved k, and recompute p_rev from the 5-decimal G_s, skipping simulations
with |G_s − G_obs| ≤ 10⁻⁵ (rounding ties, like `TIE_D` in R2-RE-D).

*Runtime (from measured times and the synthetic timing).* Recorded: one-column GLS fit 1.17 s (`r2_re_d.json`
`seconds.delta_fit`); five Cholesky factors of 3,489 × 3,489 covariances 1.9 s; one REML fit with `reml_m2l` about
20 s (R2-RE-SEL). Synthetic, single thread, on matrices of the real sizes: one inner p_boot at N_in = 10,000 3.2 ms
(so about 6.5 ms at 20,000); one τ refit with the reduced form 0.14 ms vectorised (about 0.5–1 ms through `reml_tau`'s
scalar calls, estimated); one outer draw (3,489 normals and a 37 × 3,489 product) 0.06 ms. Per outer simulation about
7–8 ms, so 130,000 simulations about 16–18 min. Setup (C's factor, P and W, four more factors and the B products) under
a minute; checks: the 37 one-column fits on the real data about 45 s (full stage only), the pointwise checks 6 × 37 fits
and 6 REML fits about 7 min. Power stage about 25 min, full stage about 30 min, both about 1 h; up to about twice that if
another run shares the CPU. Memory: one 97 MB factor at a time, E_in 6 MB. Standalone mode (`PARAMS["g_only"] = true`,
like `d_only`): it recomputes only what the block needs (the fit under C on `rows_a`, the host groups, the checks); the
power stage writes only `r2_re_g_power.json` (records `provenance_gp.json`, `run_info_gp.json`); the full stage writes
`r2_re_g.json`, the eight `r2_re_g_sims_<model>.json` and only the `R2_RE_G` key of `summary.json` (every other key
byte-identical, `onehost.summary_with_key`) with `ctx.record_suffix = "_g"`; no other results file is touched. No data
downloaded (cache only); the formal stages wait until no other study run uses the machine. More simulations after the
run would need a new pre-registration.

*Code checks before the formal run.* Synthetic data only (the 2026-11-17 smoke-run lesson, log.md): the reduced REML
form against `reml_m2l` differences and `reml_tau`; z = W y against one-column GLS fits; Cov(u) = M + τ²M²; G and ĵ;
the offset only on the chosen host's calibrator rows and its σ-matching; common ε_s and E_in; the size of the bootstrap
test on a synthetic system at a known τ (rejection rate not above the upper end of the 99% Clopper–Pearson interval of
0.05); the rule order (1)–(5) and the sub-label of rule (2); a rank-deficient synthetic system (singular M), asserting that no
G, τ̂ or p_boot is NaN; a test that searches the power stage's outputs (`r2_re_g_power.json`, `provenance_gp.json`,
`run_info_gp.json`) and its log for G_obs, Σz² and the z_j of hosts other than N5584 (their keys) and fails if any
appears. On the real data before the formal run only the
reproduction checks that use recorded values (the REML grid differences, τ̂_obs, δ̂, σ_δ, z_obs); no simulation on the
real design, no z_j of another host, no G, power, p value or label.

*Switch and code.* `PARAMS["g_check"]` (true), with `"g_seed_base": 400_000`, `"g_host_seed_base": 500_000`,
`"g_inner_seed": 600_000`, `"g_n_sims": 10_000`, `"g_n_inner": 20_000`, `"g_power_min": 0.8`, `"g_z_curve": [2.5,
3.0, 4.0, 4.5, 5.0]`, `"g_taus_rep": [0.05, 0.105]`, `"g_max_minutes": 120`, `"g_min_sims": 5_000`, `"g_only": false`
and `"g_stage": "full"` (set to true and to "power", then "full", only for the formal runs, back afterwards, with dated
notes in log.md); the recorded τ̂_obs, REML grid source, δ̂, σ_δ, z_obs and tolerances are module constants, as in
`onehost.py`. In a full study run the block runs after the R2-RE-D block under the same condition (R2-RE run and the
host step evaluable). Planned module `shape.py` (receives `run.py`'s functions, among them `reml_tau`, `reml_m2l`,
`fit` and `with_re`; reuses `rob._cp`, `rob.three_way`, `onehost.fit_delta` and `onehost.summary_with_key`; does not
import `run`), results as above, a short summary in `summary.json` (`R2_RE_G`), a test `test_shape.py` (the synthetic
checks above; labels, power and size re-derived from the saved files; every file below 1 MB), conclusion assertions in
`test_conclusions.py`, a web section, section 8 knobs. None of this exists yet.

*Amendments before any R2-RE-G simulation (2026-11-21).* Implementation choices made while writing the code (`shape.py`,
`test_shape.py`, `run.py`'s `g_*` knobs), before any simulation on the real design and before any z_j other than
N5584's, Σz², G, power or size was computed on the real data (the code was run on synthetic systems only); the text above
is unchanged.
1. `g_check` defaults to false in `run.py` until the formal stages (the "(true)" above is its value in the formal runs):
   a full study run before the power record is in log.md would compute G_obs in the same process. For the formal stages
   it is set to true with `g_only = true`, first with `g_stage = "power"`, then `"full"`; whether it stays true
   afterwards is recorded in log.md.
2. The conclusion check is one function, `test_conclusions.check_r2_re_g`, used by `test_r2_re_g_labels` on the saved
   files and by `test_shape.py` on synthetic output.
3. REML grid source: in the standalone mode the committed `results/r2_re.json` (`reml.grid_m2l`, read next to
   `run.py`, also in an exploration); in a full study run R2-RE's grid of the same run (the values that run saves). The
   source is recorded in `settings.reml_grid_source`.
4. The full stage recomputes everything the power stage computes, including the pointwise checks, also in a full study
   run (the power stage's arrays are not reused), so a full run does the simulations twice.
5. Rule (1): several reasons are joined as "not evaluable (<reason>; <reason>)", and the guard's floor gives "not
   evaluated (runtime)"; τ values in "anti-conservative at τ = <list>" are printed to 4 significant digits. A rule-(1)
   condition found before the simulations (a reproduction check, τ̂_obs at the bound, some M_jj ≤ 0, a Cholesky
   factor, a pointwise check) stops the stage there; a count mismatch stops the full stage before G_obs is formed; when
   only the anti-conservative condition holds, the full stage still computes and reports G_obs, p_G and the other
   reported numbers, and the reading is rule (1)'s.
6. A negative eigenvalue of M below −10⁻¹⁰ · max λ (impossible for the positive semi-definite M up to rounding) stops
   the run with an error (a bug), not a rule-(1) outcome.
7. Runtime guard: the projection is the mean time of the first 1,000 VHAT simulations (drawing ε_s, B ε_s, the refit
   and the inner draws) times n times the number of sets that run (13); setup and checks are not included. When n is
   reduced, the first 1,000 VHAT simulations are kept.
8. The smallest z_alt with power ≥ 0.8 is taken over the five curve points only; OANYLO and OANY are listed next to the
   curve (`curve_with_oany`) but do not enter it. For O, "how often ĵ_s is the offset host" counts ĵ_s = N5584.
9. Reported in addition (not decisive): the SHA-256 of each set's k_s in both stages (`k_sha256`; the full stage
   reports whether they match, the counts decide), σ_δ,j = M_jj^(−1/2) for every host, max |W X| and the joint rank
   p + rank(M) (design only, both stages), and Clopper–Pearson intervals of p_dbl's and p_rev's counts over n.
10. No G on the data before the formal two-stage run (gate-1 review, 2026-11-21, two rounds). Until the formal full
    stage's `results/r2_re_g.json` is committed next to `run.py` (status "evaluated", or a record with `observed`), a
    run with `g_check = true` must be `g_only = true`: a full study run or a full-study exploration with
    `g_check = true` is refused before any data is loaded, and so is a `g_only` full stage in an exploration, so an
    exploration may only run `g_stage = "power"`. The formal `g_only` full stage reads `results/r2_re_g_power.json`
    before loading any data and refuses (an error) when it is missing, a stub, has other settings (item 13), or when
    its power line (`shape.power_log_line` of that record) is not present in the study's `log.md` (the code checks
    presence; committing it is the operator's step). `shape.run_stage` itself refuses a full stage unless the formal
    `r2_re_g.json` exists or the power record's line is present in `log.md`, so a script calling it directly cannot
    bypass the gate. Exploration scripts
    (`explore/*.py`) must not compute G, Σz² or the z_j of other hosts on the data before the formal run either. The
    sentence above "In a full study run both stages run in this order in one process" therefore applies only after the
    formal two-stage run: then a full study run, or an exploration's full stage (whose folder starts empty), runs both
    stages in one process, the power record saved first. When the power record stopped before its simulations (rule
    (1), or "not evaluated (runtime)"), the full stage records the same reasons without recomputing (there are no
    counts to reproduce). The first formal outcome stands (round 3): any rerun after a rule-(1) outcome is recorded in
    log.md with its reason before it starts, and the code refuses a `g_only` full stage when `results/r2_re_g.json`
    already holds a full-stage outcome (any status) unless `PARAMS["g_rerun_reason"]` is a non-empty text that is also
    present in log.md.
11. Splitting a model's simulations into blocks changes B ε_s in the last bits (BLAS blocking), so the stages split them
    identically (VHAT: the first 1,000, then blocks of 500; every other set: blocks of 500 from s = 0); the count
    comparison is exact.
12. Measured (synthetic system of the real size: 3,489 rows, 37 hosts, 47 columns, dense C; single thread while another
    study run used the machine): one outer simulation 4.0 ms (inner draws 3.3 ms, τ refit through `reml_tau` 0.4 ms,
    ε_s 0.04 ms), the design 1.1 s, four more Cholesky factors and the five B products 1.6 s, one one-column GLS fit
    0.6 s, one REML fit with `reml_m2l` 30 s. Projected per stage: simulations 130,000 × 4 ms ≈ 9 min, pointwise checks
    6 × (37 fits + 1 REML fit) ≈ 5 min, setup, data loading and host identification about 2–3 min; power stage about
    17 min, full stage about 18 min (with the 37 fits on the real data and the joint fit), about 35 min in all, up to
    twice that with a shared CPU. The runtime guard (120 min) does not bind at this speed.
13. The power record must match the full stage (gate-1 review, 2026-11-21): the full stage stops with an error (not a
    rule-(1) outcome) when the power record is a "not run" stub or not a power-stage record, or when any of `g_seed_base`,
    `g_host_seed_base`, `g_inner_seed`, `g_n_sims`, `g_n_inner`, `g_power_min`, `g_z_curve`, `g_taus_rep`,
    `g_max_minutes`, `g_min_sims`, `n5584_host` or the thread settings differ from the power record's (round 2: the
    environment is compared strictly, the thread pools only for a library present in both records).
14. Thread settings (gate-1 review): both records store `settings.threads` (the `OMP_NUM_THREADS`, `MKL_NUM_THREADS`
    and `OPENBLAS_NUM_THREADS` environment and the BLAS thread pools seen by `threadpoolctl`), and both stages must run
    with the same settings (item 13), since the count comparison is exact.
15. A full study run whose R2-RE-G block does not run (`g_check = false`, or with `g_check = true` R2-RE or the host
    step not evaluable; gate-1 review, two rounds) writes its records only where no R2-RE-G file exists, so it never
    overwrites a formal result, and takes `summary.json`'s `R2_RE_G` from an existing `r2_re_g.json`.

### Addendum 2026-11-21: R2-RE-GT, the shape test G against heavy-tailed diffuse host scatter (T-057), pre-registered before any of these simulations

*Why.* R2-RE-G (T-055) read "undetermined (underpowered)" (power 0.49) with the sub-label "diffuse excluded":
G_obs = 0.305 is unusual under Gaussian diffuse host scatter of the fitted size (p_G = 0.016). Its referee
(section 6, R2-RE-G points 2 and 8) noted that the null family is Gaussian: host effects drawn from a heavy-tailed
distribution with no single defective host also concentrate G, so the sub-label may only say "Gaussianity excluded".
This addendum calibrates the same statistic G under diffuse host scatter with Student-t host effects (ν = 4, the value
R2-RE-N5584 used), its scale tied to the refitted τ in each simulation, with the power against the same σ-matched
single offset host fixed and logged before the data's p value under this null is computed. It attaches a label to
R2-RE-G's sub-label; it changes no earlier label, reading or the headline.

*Seen before this addendum.* Everything in sections 5–7 and log.md, in particular all of R2-RE-G's results: G_obs =
0.30486 (ĵ = N5584, z = 3.6354; next |z| N1365 2.33, N3982 2.03; Σ_j z_j² = 43.35), τ̂_obs = 0.0766988, p_G =
0.016 under V(τ̂_obs) (0.013 at τ = 0.05, 0.023 at 0.105, 0.011 under C), the power 0.49 (R_OANY 0.535, R_OANYVN 0.491),
the size (≤ 0.048) and the power curve (0.8 reached at z_alt ≈ 5). So the data value of G is known; what is not known
is its distribution under the null of this addendum. Not yet computed: any simulation with Student-t host effects, any
p value, power or size under that null; no code for this addendum exists.

*Expected outcome (stated now).* A heavier-tailed null puts more probability on one large host effect, so G's null
distribution moves up: the power against the σ-matched offset host is expected below R2-RE-G's 0.49 (roughly 0.2–0.45),
and **"undetermined (underpowered)" is the most likely reading**. The informative part is then the sub-label, whether
G_obs is still unusual under t₄ diffuse scatter: our rough guess is a p value of about 0.03–0.15, so any of the three
sub-labels is plausible.

*Question.* Is the concentration of the calibrator host offsets in one host (G_obs = 0.305) unusual under diffuse host
scatter whose host effects are Student-t with ν = 4 and variance matched to the refitted τ̂, and how much power does
this test have against one σ-matched offset host?

*Statistic.* G, z_j, M, W, u, Q, λ and the numerical-rank rule exactly as in R2-RE-G (the same design: NGC 4258-only
system `rows_a`, 37 hosts, the amended host labelling, C on `rows_a`).

*The heavy-tailed null T(τ).* y = ŷ + K_C ε + Z b, where K_C is the lower Cholesky factor of C on `rows_a`, ε is
standard normal, and the host effects b_j = s·t_j are independent with t_j Student-t with ν = 4 degrees of freedom
and s = τ/√2, so that Var(b_j) = s²ν/(ν − 2) = τ² (variance matched to R2-RE's random effect of the same τ). Then
u = ZᵀP y = ZᵀP K_C ε + M b, with Cov(ZᵀP K_C ε) = M (as in R2-RE-G), so z = diag(M_jj^(−1/2)) (ZᵀP K_C ε + M b).
- **τ in each data vector:** the Gaussian REML τ̂ of R2-RE-G (the reduced form f(τ; u), `reml_tau(f, 0.5, 0.01,
  interval=False)`, the same zero and bound rules). It is used as a variance estimate of the host effects, not as a
  model claim; the size of the whole procedure under T(τ) is checked by simulation (below), so no property of REML
  under t₄ effects is assumed. *Why the scale is tied to τ̂ and not fitted by a t likelihood (R2-RE-G referee point 8
  asked for a fitted scale):* REML's estimating equations use only second moments, so τ̂² estimates Var(b) whatever the
  effect distribution, and variance matching is the matching consistent with τ̂; at ν = 4 the fourth moment is
  infinite, so τ̂ is noisy, which is why the size is checked by simulation. Reported as a sensitivity on the real data
  only: p_T,obs with the scale fitted by R2-RE-N5584's ν = 4 variational EM, s = 0.07521926289752753
  (`r2_re_n5584.json` `heavy_tail.nu_main.tau_hat`; in that model u_j | w_j ~ N(0, s²/w_j) with w_j ~ Gamma(2, rate 2),
  so it is the t scale and Var(b) = 2s², about 1.9 times τ̂_obs²), descriptive like the ν sensitivities below.
- **Inner draws (the test applied to one data vector with refitted τ̂):** u_i = Q diag(√λ) e_i + M b_i, b_i =
  (τ̂/√2)·t_i, with e_i the rows of R2-RE-G's fixed E_in (`numpy.random.default_rng(600_000).standard_normal((20_000,
  37))`) and t_i the rows of one fixed matrix T_in = `numpy.random.default_rng(610_000).standard_t(4, (20_000, 37))`
  (common random numbers); z_i = diag(M_jj^(−1/2)) u_i; k = #{i: G_i ≥ G}, **p_T = (1 + k)/(1 + N_in)**, N_in =
  20,000, and the label `rob.three_way(k, N_in, "excluded", "not excluded")` as in R2-RE-G (the 95% Clopper–Pearson
  interval of k/N_in below, above or containing 0.05). On the real data: **p_T,obs = p_T(G_obs, τ̂_obs)**.

*Models (outer simulations).* Each outer simulation s = 0, …, 9,999 uses R2-RE-G's ε_s
(`numpy.random.default_rng(400_000 + s).standard_normal(3489)`) and, for the T models, host draws t_s =
`numpy.random.default_rng(410_000 + s).standard_t(4, 37)`, common to every T model. In each simulation: z_s, G_s,
u_s → τ̂_s (refitted), then p_T,s, k_s and the label at τ̂_s.
- **THAT, T050, T105 (decisive for the size):** T(τ̂_obs), T(0.05), T(0.105) (τ̂_obs from the run; the same three
  checked values as R2-RE-G). Their rejection rates are the size at these values.
- **OANY and OANYVN (decisive alternatives):** exactly R2-RE-G's (one host drawn by `numpy.random.default_rng(500_000 +
  s).integers(0, 37)`, σ-matched offset z_obs·σ_δ,k on C, and on V(τ̂_N) with τ̂_N = 0.0314), now tested with the T null.
  **Power = min(R_OANY, R_OANYVN)**.
- Reported, not decisive: **TC** (C, no excess, tested with the T null); **VHAT** (R2-RE-G's Gaussian V(τ̂_obs), tested
  with the T null: how conservative the T test is when the truth is Gaussian); and, on the real data only, p_T,obs with
  ν = 3 and ν = 10 inner draws (T_in drawn with `default_rng(611_000)` and `default_rng(612_000)`, scale s =
  τ̂·√((ν − 2)/ν), i.e. τ̂/√3 and τ̂·√0.8, so the variance stays τ̂²) and at fixed τ = 0.05, 0.105 (ν = 4). These
  sensitivities have no size check (only ν = 4 is checked, and only at the three τ), so they are descriptive, not
  calibrated p values.
- Seeds 410,000–419,999 and the three inner seeds 610,000, 611,000 and 612,000 collide with none used before (R2-RE-G's list plus 400,000–409,999,
  500,000–509,999, 600,000). Counts: n = 10,000 outer simulations per model (7 sets, 70,000 simulations); N_in =
  20,000 (fixed). Runtime guard as in R2-RE-G (`gt_max_minutes` = 120, floor 5,000, the power stage only).

*Power, size and their order.* R_m = #{s: label_s = "excluded"}/n with its Clopper–Pearson interval; power = min(R_OANY,
R_OANYVN); size = max(R_THAT, R_T050, R_T105). Two stages as in R2-RE-G: the **power stage** computes the reproduction
checks and all outer simulations and writes `results/r2_re_gt_power.json`; it never computes p_T,obs, and one line with its power and
size is written into log.md and committed **before** the full stage starts. The **full stage**
recomputes the power stage (counts must match exactly), then computes p_T,obs and the reading. (G_obs itself is already
known from R2-RE-G; the two stages fix the power and the size before the data's p value under this null is seen.)

*Decision rules and labels, fixed now (in this order; exactly one applies).* All earlier verdicts, labels, readings and
sub-labels (R2 through R2-RE-G) stay as recorded; R2-RE's row stays the headline.
- (1) **Not evaluable** (with the reason) when: a reproduction check fails (R2-RE-G's checks on τ̂_obs, the REML grid,
  δ̂, σ_δ, z_obs; in the full stage also G_obs = 0.30485762235426483 within a relative 10⁻⁸ and |Δz_j| ≤ 10⁻⁸ against
  the 37 one-column fits); a pointwise check fails (the first three simulations of THAT: y_s built in full with K_C ε_s +
  Z b_s, the 37 one-column GLS z against the reduced computation within 10⁻⁸); some M_jj ≤ 0; a Cholesky factor fails;
  the full stage does not reproduce the power stage's counts; the reproduction of R2-RE-G's outer simulations fails
  (OANY, OANYVN and VHAT use R2-RE-G's ε_s and host draws, so their G_s and τ̂_s must equal the saved
  `r2_re_g_sims_<model>.json` values to the saved precision, 5 and 6 decimals; in the full stage the Gaussian inner
  draws at τ̂_obs must give R2-RE-G's k = 326 for G_obs); the reduced-form τ̂_s of the first three THAT simulations
  differs from `reml_tau` on `reml_m2l` by more than 2 × 10⁻⁵; an eigenvalue of M below −10⁻¹⁰·max λ (R2-RE-G
  amendment 6); the runtime floor is not met; or the test is anti-conservative: the Clopper–Pearson interval of
  R_THAT, R_T050 or R_T105 lies entirely above 0.05. Several reasons are joined. When the only reason is
  anti-conservativeness, p_T,obs and its label are still computed and reported (as R2-RE-G amendment 5), with no
  sub-label. A reported model (TC, VHAT) whose factor fails is "not evaluable" alone and enters no rule.
- (2) Power < 0.8 → **"undetermined (underpowered)"**, with a sub-label from p_T,obs's label: **"t₄ diffuse
  excluded"**, **"t₄ diffuse not excluded"** or **"t₄ diffuse undetermined (Monte Carlo)"** (sub-labels, not readings;
  the sub-label is reported in every case because the question of this addendum, R2-RE-G's referee point 2, is about
  p_T,obs).
- (3) Power ≥ 0.8 and p_T,obs's interval entirely below 0.05 → **"one offset host preferred over t₄ diffuse scatter"**.
- (4) Power ≥ 0.8 and the interval entirely above 0.05 → **"t₄ diffuse scatter not excluded"**.
- (5) Power ≥ 0.8 and the interval containing 0.05 → **"undetermined (Monte Carlo)"**.
- Notes. "t₄ diffuse excluded" means: with host effects of R2-RE's size drawn from a Student-t with ν = 4, a
  concentration as large as G_obs is rare, so R2-RE-G's sub-label does not rest on Gaussian tails alone (at ν = 4 and
  the three checked τ only). "t₄ diffuse not excluded" means: R2-RE-G's sub-label says only that Gaussian diffuse
  scatter is excluded. Neither says whether an offset is a data defect or on which side of the ladder it sits.

*What changes in section 5 (the text, not any earlier label).* A new subsection "R2-RE-GT" with the numbers and the
reading; R2-RE-G's sub-label is glossed with this addendum's sub-label or reading: "not only Gaussian tails" for t₄
excluded (or reading (3)); "not shown to hold beyond Gaussian tails" for t₄ not excluded (or reading (4)); "t₄
comparison undetermined (Monte Carlo)" for that sub-label (or reading (5)); and for rule (1) "t₄ comparison not
evaluable (<reason>)". The open question of section 7 is answered accordingly. The
headline, `summary.json` `R2_host` and the claim's verdict do not change.

*Reported (not decisive).* p_T,obs with k, interval and label; p_T,obs at ν = 3 and 10 and at fixed τ = 0.05, 0.105;
per model the rejection rate with its interval and the quantiles (5/50/95%) of G_s and τ̂_s; TC's and VHAT's rejection
rates; the per-simulation k_s, G_s and τ̂_s in `results/r2_re_gt_sims_<model>.json` (each below 1 MB);
`results/r2_re_gt.json` and `results/r2_re_gt_power.json`; a key `R2_RE_GT` in `summary.json` (every other key
byte-identical). Checks and seconds per part.

*Runtime.* R2-RE-G's power stage took 764 s for 13 sets; the inner draws here add one 37 × 37 product per draw (M b_i),
about doubling the inner cost. Estimate: 7 sets, power stage about 15 min, full stage about 15 min, both about 30 min
single-threaded. Cache only, no download.

*Code checks before the formal run (synthetic data only).* The heavy-tailed draw (sample variance of b at s = τ/√2
equals τ² within Monte Carlo error); u = ZᵀP K_C ε + M b against full y_s; the inner draw's covariance equals M +
τ²M² (the variance matching); the size of the T test on a synthetic system at a known τ under T(τ) (not above the
upper end of the 99% Clopper–Pearson interval of 0.05); the rule order and the sub-labels of rule (2); the power
record contains no p_T,obs. On the real data before the formal run only R2-RE-G's reproduction checks.

*Switch and code.* `PARAMS["gt_check"]` (false by default; true with `gt_only` = true and `gt_stage` "power", then
"full", only for the formal runs, back afterwards with dated notes in log.md; defaults `gt_only` false, `gt_stage`
"full"), `"gt_seed_base": 410_000`, `"gt_inner_seed": 610_000`, `"gt_inner_seeds_rep": [611_000, 612_000]`, `"gt_nu":
4`, `"gt_nu_rep": [3, 10]`, `"gt_n_sims": 10_000`, `"gt_n_inner": 20_000`, `"gt_power_min": 0.8`,
`"gt_max_minutes": 120`, `"gt_min_sims": 5_000`, `"gt_rerun_reason": ""`; reused from R2-RE-G: `g_seed_base`
(400,000, ε_s), `g_host_seed_base` (500,000, the OANY host draws), `g_inner_seed` (600,000, E_in) and `g_taus_rep`
([0.05, 0.105]). Standalone records: `provenance_gtp.json`, `run_info_gtp.json` (power stage) and
`provenance_gt.json`, `run_info_gt.json` (full stage). **R2-RE-G's procedural safeguards apply unchanged to the
`gt_*` stages** (its amendments 10, 13 and 15): the full stage is refused unless the power line is in log.md; until
the formal `r2_re_gt.json` is committed, no exploration may run the full stage or compute p_T,obs (an exploration may
only run the power stage); the first formal outcome stands and a rerun needs a reason also present in log.md; the power
record's settings, including the thread environment and all `gt_*` and reused `g_*` values, must equal the full stage's;
a run that skips the block writes no formal `r2_re_gt*` file. Since p_T,obs is a fast deterministic function of known
data, these procedural gates are the protection. Module `shape.py` gains the T null (no
change to R2-RE-G's functions or results), tests in `test_shape.py`, conclusion checks, a web section, section 8 knobs.
None of this exists yet.

*Amendments before any R2-RE-GT simulation (2026-11-21).* Implementation choices made while writing the code (the
R2-RE-GT block appended to `shape.py`, `run.py`'s `gt_*` knobs, `test_shape.py`, `test_conclusions.py`, the web
section), before any simulation with Student-t host effects on the real design and before any p value, power or size
under the T null was computed (the code was run on synthetic systems only); no rule above is changed.
1. `gt_check` defaults to false in `run.py`; for the formal stages it is set to true with `gt_only = true`, first with
   `gt_stage = "power"`, then `"full"`, and set back afterwards with dated notes in log.md. Until the formal
   `r2_re_gt.json` is committed, `gt_check = true` outside `gt_only` is refused before any data is loaded (as R2-RE-G
   amendment 10); afterwards a full study run runs the block after R2-RE-G's under the same condition (R2-RE run and
   the host step evaluable), both stages in one process. `gt_only` cannot be combined with `d_only` or `g_only`.
2. Model keys and order: THAT, T050, T105, OANY, OANYVN, TC, VHAT (THAT first; the runtime guard times its first
   1,000 simulations and projects over the 7 sets). All sets use R2-RE-G's blocks of 500 simulations (its amendment
   11), so OANY, OANYVN, VHAT and TC compute z_s with exactly R2-RE-G's arithmetic.
3. The host effects enter as WH b_s with WH = W Z = diag(M_jj^(−1/2)) M as computed (not eigen-clipped; the clipped
   direction contributes below 10⁻¹⁰ relative), the same matrix in the outer draws and in the inner draws (T0 = T_in
   WHᵀ); A0 = E_in (diag(M_jj^(−1/2)) Q diag(√λ))ᵀ is R2-RE-G's inner matrix at τ = 0. A refitted τ̂ < 10⁻³ gives
   scale 0 (as R2-RE-G's zero rule).
4. "To the saved precision" (rule (1), the reproduction of R2-RE-G's simulations) means |G_s − saved| ≤ 0.5 × 10⁻⁵
   and |τ̂_s − saved| ≤ 0.5 × 10⁻⁶ (each plus 10⁻¹²) for every one of the first min(n, 10,000) simulations of VHAT,
   OANY and OANYVN, checked after the simulations in both stages (the models are still recorded). The reference is
   R2-RE-G's committed `results/r2_re_g_sims_<model>.json` (also in an exploration) or, in a full study run whose
   R2-RE-G block ran, that run's records. A missing file, a record that is not "evaluated", or seeds other than
   `g_seed_base`, `g_inner_seed` and (OANY models) `g_host_seed_base` stop the run with an error before any data is
   loaded (not a rule-(1) outcome). A VHAT whose factor fails is "not compared".
5. A formal `gt_only` stage (not an exploration) refuses to start (an error) when its thread settings differ from those
   recorded in `r2_re_g.json` (R2-RE-G's formal run: one thread): last-bit differences in B ε_s could move a τ̂_s by
   the optimiser's tolerance and fail the reproduction spuriously.
6. The full stage's real-data checks run after the count comparison, in this order: the 37 one-column fits against
   W y (|Δz_j| ≤ 10⁻⁸), G_obs against the recorded value (relative 10⁻⁸), and R2-RE-G's Gaussian inner draws at
   τ̂_obs (`shape.inner_k` with E_in) giving k = 326 exactly. A failure adds "reproduction check failed: …" to rule (1)
   and p_T,obs is not computed. The recorded G_obs and k are module constants and are not written into the power
   record.
7. An eigenvalue of M below −10⁻¹⁰ · max λ: `shape.design` raises (R2-RE-G amendment 6, unchanged); R2-RE-GT catches
   that error and records it as a rule-(1) reason, as the addendum lists it under rule (1).
8. Cholesky factors: C (the design) and V(τ̂_N) (OANYVN, decisive) failing is rule (1) and stops the stage; V(τ̂_obs)
   is used by VHAT only (reported), so its failure makes VHAT alone "not evaluable".
9. The pointwise checks (the first three THAT simulations) report the z check (10⁻⁸) and the τ̂ check (2 × 10⁻⁵) as
   separate rule-(1) reasons; either stops the stage before the outer simulations.
10. The section-5 gloss is stored as `gloss` in `r2_re_gt.json` and in `summary.json`'s `R2_RE_GT`; for rule (1) it is
    "t₄ comparison not evaluable (<reasons joined by '; '>)" (the runtime floor gives "(runtime)"). Labels name
    t_ν for `gt_nu` (t₄ in the registered run).
11. Sensitivities (`sensitivities` in `r2_re_gt.json`): `gt_nu_rep` and `gt_inner_seeds_rep` are paired in order
    (ν = 3 with 611,000, ν = 10 with 612,000), each with its own T_in and the same E_in, at τ̂_obs; the fixed τ use the
    ν = 4 T_in; the EM scale s is used directly as the t scale with the ν = 4 T_in.
12. Per-simulation files for all seven models (`r2_re_gt_sims_<model>.json`): G_s (5 decimals), τ̂_s (6), k_s, ĵ_s;
    the T models also `tau_t` and `t_seed_base`, the OANY models `offset_host`. The power record must not contain
    `p_T_obs`, `observed`, `sensitivities`, `reading`, `sub_label`, `gloss`, `section5`, `G_obs`, `k_gauss_obs` or
    `real_data` (`shape.GT_FORBIDDEN_POWER_KEYS`, checked by the tests).
13. A full study run whose R2-RE-GT block does not run writes its "not run" records only where no R2-RE-GT file exists
    and takes `summary.json`'s `R2_RE_GT` from an existing `r2_re_gt.json` (as R2-RE-G amendment 15).
14. The conclusion checks are `test_conclusions.check_r2_re_gt` and `check_r2_re_gt_power`, used on the saved files
    and by `test_shape.py` on synthetic output; on the saved files they also compare VHAT's, OANY's and OANYVN's G_s
    and τ̂_s with R2-RE-G's saved files.
15. R2-RE-G's code is pinned: `test_shape.py` checks the SHA-256 of `shape.py`'s R2-RE-G text (everything before the
    R2-RE-GT block) and of `run.py`'s R2-RE-G functions as reviewed in T-055.
16. Runtime (single thread, synthetic timing): one T inner evaluation (20,000 × 37) about 2 ms against 4 ms for
    R2-RE-G's Gaussian one (the 37 × 37 products are done once), so an outer simulation costs about 3 ms; 70,000
    simulations about 4 min, the pointwise checks (3 × 37 fits and 3 REML fits) about 2.5 min, data loading and host
    identification about 2–3 min: power stage about 10 min, full stage about 10 min (with the 37 fits on the real data
    and the sensitivities), up to twice that with a shared CPU. The runtime guard does not bind.
17. (Gate-1 review of the code.) A full study run with `gt_check` true (allowed only after the formal stages) obeys
    the same rule as a `gt_only` full stage: if `results/r2_re_gt.json` holds a formal outcome it is refused, before
    any data is loaded, unless `gt_rerun_reason` is non-empty and present in log.md; its reproduction reference is
    always R2-RE-G's committed `r2_re_g_sims_<model>.json`, read before any data is loaded. If the formal full stage
    ends under rule (1) without p_T,obs, the exploration gate stays closed (no exploration full stage, no full run
    with `gt_check`) until a rerun with a logged reason. Sensitivity keys are written as `f"{ν:g}"` ("3", "10").

### Addendum 2026-11-22: R2-RE-GTP, a profile of R2-RE-GT over the tail weight and the scale (T-060), pre-registered before any of these simulations

*Why.* R2-RE-GT (T-057) read "undetermined (underpowered)" with the sub-label "t₄ diffuse undetermined (Monte
Carlo)": p_T,obs = 0.052 at ν = 4 and τ̂_obs, its interval containing 0.05. Its referee (section 6, R2-RE-GT points 1,
2, 7 and 10) noted that the Monte Carlo error (about ±0.003) is small against the model choices: the descriptive
sensitivities moved p from 0.021 (ν = 10) to 0.092 (EM scale), and the size was checked only at ν = 4. This addendum
computes, on one grid of tail weights ν and scales τ, the fixed-τ p values on the data, and for the τ-refitted
plug-in test its size and a calibrated p value. **It is a reported, non-decisive profile: it changes no verdict,
label, reading, sub-label or gloss, and R2-RE's row stays the headline.**

*Seen before this addendum.* Everything in sections 5–7 and log.md, in particular all of R2-RE-GT's results: p_T,obs =
0.0524 (k = 1,047) at ν = 4 and τ̂_obs = 0.0766988; at ν = 4 and fixed τ 0.05 and 0.105, p = 0.025 (k = 501) and
0.090 (k = 1,806); at τ̂_obs, ν = 3 0.074 (k = 1,476) and ν = 10 0.021 (k = 422); with the EM scale 0.092; the rates
R_THAT 0.0461, R_T050 0.0410, R_T105 0.0442; and all of R2-RE-G's results, in particular its Gaussian p values (p_G =
0.016 at τ̂_obs, k = 326; `p_G_fixed` 0.013 at 0.05, k = 254, and 0.023 at 0.105, k = 453), its double-bootstrap
check p_dbl = 0.016 and the rates R_VHAT 0.0477, R_V050 0.0447, R_V105 0.0483. From the referee of R2-RE-GT: the THAT
rejection rates by τ̂_s bins, the calibrated fractions P(k_s ≤ k_obs) = 0.050 (THAT), 0.046 (T050), 0.051 (T105) and
P(G_s ≥ G_obs) = 0.056, 0.027, 0.093. **The summary statement below is therefore already determined**: the
recorded points include "excluded" (ν = ∞ at all three τ; ν = 4 at 0.05; ν = 10 at τ̂_obs) and "not excluded" (ν = 3
at τ̂_obs; ν = 4 at 0.105), so it can only read "model-limited", with its lower end 0.0127 (ν = ∞, τ = 0.05) already
known. What is new is the upper end of the fixed-τ p values, the size of the refitted test at ν = 3, 6, 10, 30, and
its calibrated p value there. Not yet computed: any simulation or inner draw at ν = 6 or 30, any outer simulation at
ν = 3 or 10, any fixed-τ p at ν = 3 or 10 other than at τ̂_obs, and p_cal at ν = ∞ under V050 and V105
(derivable from R2-RE-G's committed k_s but never computed; only VHAT's p_dbl was); no code for this addendum exists.

*Grid.* ν ∈ {3, 4, 6, 10, 30, ∞} (∞: Gaussian host effects) × τ ∈ {0.05, τ̂_obs, 0.105} mag, the three values that
R2-RE-G and R2-RE-GT checked (close to R2-RE's 68% interval 0.048–0.105). The statistic G, z_j, M, W, the design, the
inner draws, the REML refit and `rob.three_way` are exactly R2-RE-GT's (R2-RE-G's for ν = ∞).

*Two kinds of number (kept apart).*
- **Fixed-τ p values p_fix(ν, τ)** (18; Monte Carlo estimates of simple-null p values, no size check needed):
  k = #{i: G_i ≥ G_obs} over the 20,000 fixed inner draws at τ, p = (1 + k)/(1 + 20,000), labelled by `rob.three_way`
  as in R2-RE-GT. For finite ν the inner draws are z_i = A0_i + s T0_i with s = τ√((ν − 2)/ν) and T_in drawn with ν;
  for ν = ∞ they are R2-RE-G's Gaussian inner draws at τ (`shape.inner_k`, `inner_matrix(τ)`). The value at τ̂_obs,
  p_plug(ν) = p_fix(ν, τ̂_obs), is also the data value of the τ-refitted plug-in test.
- **The τ-refitted plug-in test at each ν** (calibrated across the three true τ): outer simulations from T_ν(τ) with
  host effects b_j = s·t_j, t_j ~ t_ν (as R2-RE-GT's THAT, T050, T105; for ν = ∞ R2-RE-G's VHAT, V050, V105), n =
  10,000 per (ν, τ), τ refitted in each, k_s from the ν inner draws at τ̂_s. Reported per (ν, τ): **size(ν, τ)**, the
  rate of "excluded", with its Clopper–Pearson interval (flagged "anti-conservative" if the interval lies entirely
  above 0.05); and **p_cal(ν, τ) = (1 + #{s: k_s ≤ k_obs(ν)})/(1 + n)**, with k_obs(ν) the data's k at τ̂_obs, R2-RE-G's
  double-bootstrap calibration p_dbl generalised to ν (labelled by `rob.three_way` on the count). size and p_cal
  calibrate only p_plug(ν); the fixed-τ values at 0.05 and 0.105 need no calibration.
- Streams. Inner T_in: ν = 4 `default_rng(610_000)`, ν = 3 `611_000`, ν = 10 `612_000` (R2-RE-GT's), ν = 6
  `613_000`, ν = 30 `614_000`, all `.standard_t(ν, (20_000, 37))`; E_in R2-RE-G's (`600_000`). Outer ε_s R2-RE-G's
  (`400_000 + s`); outer t_s: ν = 4 `410_000 + s` (R2-RE-GT's), ν = 3 `430_000 + s`, ν = 6 `440_000 + s`, ν = 10
  `450_000 + s`, ν = 30 `460_000 + s`. Seeds 430,000–469,999, 613,000 and 614,000 collide with none used before.
- Reuse. ν = 4 takes size and the k_s from R2-RE-GT's committed simulations (THAT, T050, T105) and its fixed-τ p from
  R2-RE-GT's records; ν = ∞ takes them from R2-RE-G's (VHAT, V050, V105; `p_G`, `p_G_fixed`). Only k_s counts enter
  p_cal (integers, no rounding ties). New: 12 outer sets (ν = 3, 6, 10, 30 × three τ) and the fixed-τ p at the 10 new
  (ν, τ) pairs.

*Checks (a failure makes R2-RE-GTP "not evaluable (<reason>)", reported instead of the summary).* R2-RE-G's and
R2-RE-GT's reproduction checks on the data (τ̂_obs, the REML grid, z_obs, G_obs within a relative 10⁻⁸); the recomputed
k at the eight recorded (ν, τ) pairs equal the records exactly (ν = 4 at τ̂_obs, 0.05, 0.105: 1,047, 501, 1,806;
ν = 3 and 10 at τ̂_obs: 1,476, 422; ν = ∞ at τ̂_obs, 0.05, 0.105: 326, 254, 453); for each new outer set the first
three simulations pass R2-RE-GT's pointwise checks (y_s built in full: the 37 one-column GLS z within 10⁻⁸, τ̂ within
2 × 10⁻⁵).

*Summary statement (reported; fixed now; already determined, see above).* From the 18 p_fix labels: all "excluded" →
"t-tail comparison: excluded across the profile"; all "not excluded" → "t-tail comparison: not excluded across the
profile"; any other mix (including "excluded" or "not excluded" together with "undetermined (Monte Carlo)" points) →
**"t-tail comparison: model-limited (p_fix from <min> to <max>)"**, min and max over all 18 points. Reported with it:
the 18 p_fix with labels; per ν, p_plug, the three sizes and the three p_cal; the ν values at which the refitted test
is flagged anti-conservative at any τ (their p_plug, sizes and p_cal are still listed, marked, and left out of the
p_cal extremes); per ν, max over τ of p_cal(ν, τ), labelled "at the three checked τ only"; and the largest and
smallest p_cal over the unflagged ν. The largest p_fix is "the
largest of 18 model-specific p values", not a p value for a composite null (the grid is coarse and ν, τ are
not integrated over). The statement is attached in section 5 to R2-RE-GT's sub-label as its profile; it is not a
reading and does not replace the sub-label.

*Expected outcome (stated now).* p_fix grows with heavier tails and larger τ: the largest at ν = 3, τ = 0.105, likely
about 0.10–0.13. The size of the refitted test should stay near or below 0.05 at ν ≥ 4; at ν = 3 it may exceed 0.05
(heavier tails make one large draw inflate G and τ̂ together), and then ν = 3 is flagged. p_cal should be close to
p_plug where the size is near 0.05 (already seen at ν = 4: 0.046–0.051 against p_plug 0.052), and larger where the
test is conservative.

*Runtime.* R2-RE-GT's outer sets took about 18 s each for 10,000 simulations (single thread); 12 new sets about 4 min,
the inner p and checks under 1 min, data loading and host identification 2–3 min: about 10 min single-threaded.
Cache only, no download.

*Code checks before the formal run (synthetic data only).* The variance matching at ν = 3, 6, 10, 30 (sample variance
of b equals τ²); ν = ∞ uses R2-RE-G's functions unchanged; the summary rule (including mixes with Monte Carlo-
undetermined points) and the anti-conservative flag; p_cal from k_s counts; the record contains every grid point. On
the real data before the formal run only the reproduction checks above.

*Switch and code.* `PARAMS["gtp_check"]` (false by default; true with `gtp_only` = true only for the formal run, back
afterwards with a dated note in log.md), `"gtp_nus": [3, 4, 6, 10, 30, "inf"]`, `"gtp_t_seeds": {3: 430_000, 6:
440_000, 10: 450_000, 30: 460_000}`, `"gtp_inner_seeds": {6: 613_000, 30: 614_000}`, `"gtp_n_sims": 10_000`. Results
`results/r2_re_gtp.json` and `results/r2_re_gtp_sims_<ν>_<τ>.json` for the 12 new sets (G_s, τ̂_s, k_s; each below
1 MB), a key `R2_RE_GTP` in `summary.json` (other keys byte-identical); `shape.py` gains the profile after R2-RE-GT's
block (no change to R2-RE-G's or R2-RE-GT's functions or results), tests, conclusion checks, a web section and section 8
knobs. As for R2-RE-GT, the first formal outcome stands, and a rerun needs a reason also present in log.md. None of
this exists yet.

*Amendments before any R2-RE-GTP simulation (2026-11-22).* Implementation choices made while writing the code (the
R2-RE-GTP block appended to `shape.py`, `run.py`'s `gtp_*` knobs, tests, the conclusion check, the web section), before
any simulation or inner draw of this addendum on the real data (the code was run on synthetic systems only); no rule
above is changed.
1. The block runs only standalone (`gtp_check` and `gtp_only` both true; `gtp_check` alone is refused, and it cannot
   be combined with `d_only`, `g_only` or `gt_only`). A full study run never runs it and copies `R2_RE_GTP` from an
   existing `r2_re_gtp.json` (else "not run (standalone only)"). Records: `provenance_gtpp.json`, `run_info_gtpp.json`.
2. Before any data is loaded it reads R2-RE-GT's `r2_re_gt.json` (which must be formal) and R2-RE-G's `r2_re_g.json`,
   and the six reused simulation files (`r2_re_gt_sims_{THAT,T050,T105}.json`, `r2_re_g_sims_{VHAT,V050,V105}.json`),
   each evaluated with `gtp_n_sims` simulations; a formal run refuses to start when its thread settings differ from
   R2-RE-GT's recorded ones (the recorded k would not be reproduced bit for bit), when `summary.json` is missing or does
   not re-serialise to itself, or when `r2_re_gtp.json` already holds a formal outcome and `gtp_rerun_reason` is not a
   non-empty text present in log.md. An exploration may run the block only after the formal `r2_re_gtp.json` is
   committed.
3. "Checks" also include: G_obs against R2-RE-G's recorded value (relative 10⁻⁸), and the reused counts: the number of
   "excluded" among the reused k_s must equal R2-RE-GT's and R2-RE-G's recorded `n_excluded` for each of the six sets.
   The order is: reproduction on the data, G_obs, the 18 p_fix with the eight recorded k, the 36 pointwise checks (12
   new sets × 3), the 12 new outer sets, the reused counts; the first failure stops the block as "not evaluable
   (<reason>)" and no simulation file is written.
4. τ̂_obs < 10⁻³ would count as zero for the p_fix at τ̂_obs (R2-RE-G's zero rule); the outer simulations use R2-RE-GT's
   `gt_simulate` unchanged (blocks of 500, the same ε_s), with the t_s seed base of the ν.
5. "Undetermined (Monte Carlo)" labels of p_cal are reported as they come; the extremes of p_cal are over the ν not
   flagged anti-conservative (all three τ of a flagged ν are left out).
6. (Gate-1 review of the code.) Runtime corrected: R2-RE-GT's pointwise checks took about 41 s each (123 s for 3), so
   the 36 checks take about 25 min; with the 12 outer sets (about 4 min) and data loading the run takes about 30–35 min
   single-threaded, not 10 min. There is no runtime guard; the estimate changes no rule.
7. A formal run refuses to start unless `gtp_nus`, `gtp_t_seeds`, `gtp_inner_seeds`, `gtp_n_sims` and the reused
   `gt_*`/`g_*` streams equal the pre-registered values (`shape.GTP_PREREGISTERED`) and R2-RE-G's `r2_re_g.json` is
   evaluated with p_G. The statement's p values are written with four decimals. A "not evaluable" outcome (including
   "host step not evaluable") is the first formal outcome and carries `settings`; the conclusion check also verifies
   the new simulation files' streams.

### Addendum 2026-11-24: R2-RE-NU, an outside constraint on the tail weight ν from the Hubble-flow supernovae (T-062), pre-registered before any of these fits

Revised the same day after two rounds of gate-1 review (SN grouping, misspecification injections, a defensive importance
proposal, the p_int bounds, a scale-agreement condition, a whole-mock rejection for the truncated mocks), still before any Hubble-flow residual was computed.

*Why.* R2-RE-GTP (T-060) found that whether G excludes diffuse host scatter depends on the tail weight ν of the host
effects: the calibrated p_cal is at most 0.031 for ν ≥ 6, 0.051 at ν = 4 and 0.078 at ν = 3. Its referee (section 6,
R2-RE-GTP point 8) asked for a constraint on ν from data not used in G, and for p_cal integrated over that ν. This
addendum fixes such a constraint in advance. **It is reported and non-decisive: it changes no verdict, label, reading,
sub-label, gloss or statement of R2 through R2-RE-GTP, and R2-RE's row stays the headline.**

*Which outside data (scoping review of 2026-11-24, before this addendum; post hoc with respect to R2-RE-GTP).*
- *Cepheid−TRGB/JAGB distance differences of shared hosts* (Freedman et al. 2024/25, arXiv:2408.06153; Li et al. 2024,
  arXiv:2408.00065 and 2401.04777; Anand et al. 2024, arXiv:2401.04776; Riess et al. 2024, arXiv:2408.11770; host lists as
  read in the scoping review, not re-verified for this addendum and not used in any rule): about 15 hosts, all among
  the 37 that define G, so not outside G. They also probe only the Cepheid side, where this study's R3 found no excess
  (per-host χ² 5.1 for 10 hosts, section 5). A synthetic power calculation in the scoping review (Kullback–Leibler
  divergence between t₃ and t₁₀ effects at τ = 0.077 with Gaussian errors; no data) needs about 120–145 hosts at
  σ = 0.05 mag to separate the two, so this route has essentially no power. Not used.
- *Leave-N5584-out residuals* of the other 36 hosts are the denominator of G (Σ_j z_j²): not independent of G. Not used.
- **Used: the Hubble-flow SN rows already in the cache** (277 rows; `row_classes`' `hflow`: a non-zero in columns 42
  and 46 and in no host column). They are not in G, their residuals are on the SN side only, and no download is needed.
  **The transfer assumption, stated now:** the per-SN excess scatter of Hubble-flow SNe beyond C has the same tail shape
  ν as the calibrator host effects. This is an assumption, not a result: the calibrator effects are host-level
  SN-minus-Cepheid offsets (either side can contribute; section 6), whereas Hubble-flow residuals include peculiar
  velocities and the Hubble-flow selection (including an outlier cut, item 6 below), and calibrator SNe may differ
  systematically from Hubble-flow SNe (Wojtak & Hjorth 2022, arXiv:2206.08160, as verified by the R2-RE referee,
  section 6: a calibrator-specific candidate). Every label below is conditional on this assumption and says so.
- **Not independent of the calibrators (M1).** The Hubble-flow rows are coupled to the calibrator SN rows through C
  (Pantheon+ systematics) and through the shared M⁰_B. Computed from C and L only (277 ungrouped rows, NGC 4258-only
  system): the canonical correlations between the Hubble-flow and the calibrator-row contrasts (blocks of P, below)
  are 0.78, 0.69, 0.63, 0.46 (on C's raw blocks 0.81, 0.74, 0.65, 0.48). Calibrator host effects at τ̂_obs = 0.0767
  would add to Cov(u) (u below) a matrix of trace 9.0 and top eigenvalue 3.75, against 612 and 15.1 for Hubble-flow
  effects at the gate value τ_HF = 0.02 (τ²·tr(M²) and τ²·λ_max²). The leakage is small but not zero; Stages 1 and 2
  are therefore repeated with the calibrator host effect at τ̂_obs in the base covariance (reported only).

*Seen before this addendum.* Everything in sections 5–7 and log.md, in particular all of R2-RE-GTP's results. On the
Hubble-flow rows specifically, everything already recorded or seen:
1. R1's baseline fit on all 3,492 rows (the 277 Hubble-flow rows included): χ²/dof = 3552.8/3445 = 1.031 (section 5;
   `r1.json` `chi2`, `chi2_dof`), matching R22's printed 1.03. This is a whole-fit number, not split by row class; it
   shows no gross excess over C in the system as a whole.
2. R22's statements as recorded in this README: 277 Hubble-flow SNe (section 4; R22's count) and the baseline χ²/dof of
   1.03 (R1's secondary target). The observed number of rows is 277 (`summary.json` `validity.row_counts.hflow`), but
   the rows are **not** one per SN: like the calibrator rows (77 rows for 42 SNe), they include duplicate light curves
   of the same SN (items 3 and 4).
3. The structure of L and C on these rows (inspected for this addendum from the cache, without y): each Hubble-flow row
   has exactly two non-zeros in L, +1 in column 42 (M⁰_B) and −1 in column 46 (5 log H0); C's Hubble-flow block is dense
   (99.6% of off-diagonal entries non-zero), with diagonal σ from 0.085 to 0.367 mag (median 0.133; 5–95%: 0.103–0.211)
   and off-diagonal correlations mostly small (1–99%: −0.083 to 0.092); 41 pairs have a correlation above 0.3, 19 above
   0.45 and 13 above 0.5 (largest 0.751); the connected components of the graph "correlation > 0.3" number 242 (largest
   3 rows), of "> 0.45" 261. The Hubble-flow rows are correlated in C with all 77 calibrator SN rows and with no other
   row. M has one eigenvalue at zero (−7.6 × 10⁻¹⁴, next 7.46, largest 194.4). The coupling numbers of M1 above. Timings
   of the code paths below on synthetic inputs only. *Validation of the grouping on the calibrator rows* (C, L and the
   host labelling only): the 77 calibrator SN rows belong to 42 SNe; at "> 0.3" they form 41 components, with 2
   cross-host pairs above 0.3 (largest 0.327), i.e. false merges; at "> 0.45" they form 49 components and no component
   spans two hosts (the grouping errs by splitting); N5584's four light curves of SN 2007af correlate at 0.34–0.69. The
   two errors act in opposite directions: a false merge forces one b on two SNe (fewer, larger effects), a false split
   gives the duplicates of one SN independent b's, so their common offset is read as several effects and the fit drifts
   towards heavy tails; the 0.45 sensitivity brackets the split side.
4. From the cached `Pantheon+SH0ES.dat` (0.58 MB, fetched on 2026-11-14 for another purpose), only the columns CID,
   IDSURVEY, zHD and USED_IN_SH0ES_HF were read: 277 rows have USED_IN_SH0ES_HF = 1, with 238 distinct CID (zHD 0.0234 to
   0.1490, sorted). Matching these rows to the Hubble-flow rows of y, L and C in file order fails: none of the 41 pairs
   with correlation > 0.3 shares a CID, and the 48 same-CID pairs have correlations between −0.04 and 0.3. No other
   allowed key exists (L is identical on all Hubble-flow rows; the remaining columns are magnitudes, errors or residuals),
   so the SN identity of each row cannot be read without a magnitude or error column, and the grouping below uses C.
5. The R2-RE referee's point 4 (section 6): if τ came from SN intrinsic scatter it should also appear in the Hubble
   flow; whether C holds a within-SN term was not inspected (section 7).
6. **Pantheon+'s outlier cut and scatter model.** "The sample includes a 3.5σ Hubble residual outlier cut to remove 5
   potential contaminants" (Brout et al. 2022, arXiv:2202.04077, section III.1.1). Its distance uncertainties include a
   scatter term from the BS21 dust-based intrinsic-scatter model, whose parameters "have been fit to the observed scatter
   in the dataset" (section III.3.3), and a gray floor determined to bring the Hubble diagram's reduced χ² to unity
   (section II.1), found to be zero for BS21 (section IV.1). [V] 2026-11-24, read in the arXiv HTML version through a
   summary (the first quotation verbatim). Hubble-residual figures published by R22 and Pantheon+ have been seen
   (general familiarity, not studied for this addendum).
7. From the recorded p_cal (`r2_re_gtp.json`), **the possible range of p_int below is already known**: it lies between
   the smallest and largest p_cal(ν, τ̂_obs), 0.0165 (ν = ∞) and 0.0768 (ν = 3). With weights equal to the prior (the
   Hubble flow says nothing about ν) p_int = 0.0352 (flat) and 0.0364 (uniform in 1/ν); with the maximum over τ, 0.0359
   and 0.0372. **The light-tail label implies p_int < 0.0324** (at most 0.05 of the weight at ν = 3, the rest at ν = 6);
   **under the heavy-tail label p_int ≥ 0.0487** (at least 0.95 at ν = 4, the rest at ν = ∞) **and is above 0.05 unless
   almost all the weight is on ν = 4**. Under "weakly constrained" either side of 0.05 is possible: a weight of 0.556 on
   ν = 3 with the rest on ν = ∞ already gives 0.05, while weight spread like the prior inside {3, 4} and inside {6, 10,
   30, ∞} needs P(ν ≤ 4) of about 0.7.
No statistic of the Hubble-flow residuals has been computed or recorded: no τ_HF, no Hubble-flow χ² or residual
scatter, no excess over C, no tail statistic, from the cached data or from any results file, and no magnitude, error or
residual column of `Pantheon+SH0ES.dat` was read. The Hubble-flow rows enter every fit of this study (R2 through
R2-RE-GTP keep them in every subsystem), but no saved quantity isolates them (the leave-one-out χ² of R2-RE covers the
77 calibrator rows only). No code for this addendum exists.

*Expected outcome (stated now).* Pantheon+'s scatter model was fitted to the observed Hubble-diagram scatter (item 6),
and C's SN block comes from Pantheon+, so little excess beyond C is expected: **"ν not evaluable (no excess scatter in
the Hubble flow)" is the most likely outcome**, and if Stage 1 passes, **"ν weakly constrained"** is next: at a per-SN
scale of a few hundredths of a magnitude against σ ≈ 0.13 mag, about 240 SNe carry little information on the tail
shape, and the 3.5σ cut removes the far tail. A constrained label would be a surprise.

*Design.* The NGC 4258-only system of R2-RE (`rows_a`, 3,489 rows; all 277 Hubble-flow rows are in it), with the fitted
columns X of L on those rows (`infer.gls`'s `kept`), so every global parameter (including M⁰_B and 5 log H0) is free and
treated exactly as R2-RE's REML treats it.
- **SN groups (S1).** The Hubble-flow rows are grouped into SNe as the connected components of the graph whose edges
  join two Hubble-flow rows with a correlation in C above **0.3** (main; above 0.45 as a sensitivity, Stage 1 and the
  Stage-2 weights reported only). Every row of a group gets the same effect b_g. *Count check:* the number of groups
  n_g is compared with the number of distinct CID among the USED_IN_SH0ES_HF = 1 rows of the cached `Pantheon+SH0ES.dat`
  (read through `ctx.http`, columns CID and USED_IN_SH0ES_HF only); the check passes if |n_g − n_CID| ≤ 0.05·n_CID
  (rounded down). It applies to the main 0.3 grouping only; the 0.45 grouping is reported without a check. The main
  check is already known to pass (242 against 238, item 3 and 4), so it is a regression guard, not a test. (Matching
  rows to CID, the preferred route, is impossible without a magnitude or error column, item 4.)
- Z is the 3,489 × n_g group design (Z_{r,g} = 1 if Hubble-flow row r is in group g). V = C + Z D Zᵀ with D =
  diag(d_g). No calibrator host effect is included in the main fit (C as is on every other row).

*Stage 1 (excess scatter in the Hubble flow).*
- **Model.** d_g = τ_HF² for all groups (a Gaussian per-SN effect, shared by the light curves of one SN).
- **Estimate and interval.** τ̂_HF by R2-RE's REML procedure, unchanged: `reml_m2l` on `rows_a` with the n_g Hubble-flow
  groups, `reml_tau(f, 0.5, 0.01)` (grid 0, 0.01, …, 0.50 mag, bounded refinement, xatol 10⁻⁵), with R2-RE's 68%
  interval (the crossing of min + 1 by `brentq`; lower end 0 when −2ℓ_R(0) is within 1 of the minimum), zero rule
  (τ̂ < 10⁻³) and bound rule.
- **Gate, fixed now.** If the interval's lower end is 0, or τ̂_HF < **0.02 mag**, the outcome is **"ν not evaluable (no
  excess scatter in the Hubble flow)"** and Stage 2, the known-answer check and p_int are not computed. *Why 0.02 mag:*
  the median Hubble-flow σ in C is 0.133 mag (the median of √C_ii over the 277 Hubble-flow rows of `rows_a`, per row,
  not per group), so at τ_HF = 0.02 the effects add 2.3% to a typical SN's variance and
  their scale is 0.15 of the noise; the tail shape of effects that small cannot be read from about 240 SNe. It is also
  about a quarter of the calibrators' τ̂ = 0.077 (one sixteenth of the variance). The threshold was chosen after seeing
  C's Hubble-flow σ (item 3), before any residual. If the lower end is "not determined" (the `brentq` search fails),
  the outcome is label 1 (below).
- **Reported with it:** τ̂_HF with its interval; the ratio τ̂_HF/τ̂_obs (τ̂_obs = 0.0766988, R2-RE) and whether 0.0767
  lies inside τ̂_HF's 68% interval (used by label 4/5's scale condition, below); Δ(−2ℓ_R) at τ = 0; τ̂_HF under the 0.45
  grouping; and τ̂_HF with the calibrator host effect at τ̂_obs added to C (V(τ̂_obs) of R2-RE as the base covariance),
  reported only.

*Reduced form (used by Stage 2 and the mocks).* With P = C⁻¹ − C⁻¹X(XᵀC⁻¹X)⁻¹XᵀC⁻¹ on `rows_a`, u = ZᵀP y (n_g) and
M = ZᵀP Z (n_g × n_g), the REML criterion relative to D = 0 is exactly
g(D) = log det(I + D^½ M D^½) − uᵀ D^½ (I + D^½ M D^½)⁻¹ D^½ u, i.e. −2ℓ_R(V) = −2ℓ_R(C) + g(D) (the determinant
lemma and the Woodbury identity; the same reduction as R2-RE-G's f(τ; u), which g equals for D = τ²I). g is computed
from the Cholesky factor of I + D^½ M D^½ (log det from its diagonal). M has rank n_g − 1 (5 log H0 enters only the
Hubble-flow rows, with −1 in each, so the common shift of all Hubble-flow rows is absorbed). Eigenvalues are treated as
in R2-RE-G (`shape.EIG_RTOL` = 10⁻¹⁰): an eigenvalue below −`EIG_RTOL`·λ_max raises an error (a bug, as R2-RE-G
amendment 6 and `shape.design`); the eigenvalues with |λ| < `EIG_RTOL`·λ_max are set to zero, and exactly one is
expected (more than one is label 1, "design"). Given b, u ~ N(M b, M), so the Gaussian posterior of b under d_g = τ² has
Σ = (τ⁻² I + M)⁻¹ and mean μ = Σ u.

*Stage 2 (shape, run only if Stage 1 passes the gate).*
- **Family.** b_g = s·t_g with t_g ~ t_ν independent, s = τ√((ν − 2)/ν) (variance τ², as in R2-RE-GT/GTP), ν ∈ {3, 4,
  6, 10, 30, ∞} (the GTP grid; ∞ Gaussian). As a scale mixture, b_g | w_g ~ N(0, s²/w_g), w_g ~ Gamma(ν/2, rate ν/2).
- **Likelihood of ν.** Λ(ν, τ) = E_w[exp(−½ g(diag(s²/w_g)))] (the restricted likelihood relative to C, with the global
  parameters handled exactly as in Stage 1, the correlated C included through M). **Primary: L(ν) = Λ(ν, τ̂_HF)**, the
  scale tied to the Gaussian REML τ̂_HF by variance matching, as R2-RE-GT/GTP tie the t scale to the REML τ̂. **L(ν) is
  a variance-matched plug-in: neither a profile likelihood over the scale nor a likelihood marginal over it; the
  procedure as a whole is calibrated only by the known-answer check below (M4).** ν = ∞: Λ = exp(−½ g(τ̂_HF² I)), exact.
- **Method for finite ν: importance sampling over w (S3).** Per group, a defensive mixture proposal q_g(w) = 0.1·Gamma(w;
  ν/2, rate ν/2) + 0.9·Gamma(w; (ν + 1)/2, rate (ν + m_g/s²)/2), with m_g = μ_g² + Σ_gg from the Gaussian posterior **at the
  τ being evaluated** (τ̂_HF for the primary, m·τ̂_HF in the profile, τ̂_s in a mock; one deterministic step, no tuning
  on the result). Each coordinate is drawn from the prior component with probability 0.1 (a Bernoulli draw, then the
  component's Gamma draw), from one `numpy.random.default_rng(seed)` per stream in a fixed order (the component
  indicators for all N × n_g coordinates, then the prior-component Gammas, then the posterior-component Gammas, each
  in row-major order). Log weights log ω = Σ_g [log Gamma(w_g; ν/2, ν/2) − log q_g(w_g)] − ½ g(diag(s²/w)), all in log
  space; log Λ̂ = logsumexp(log ω) − log N (the plain importance estimate); ESS = (Σω)²/Σω²; and the Pareto shape k̂ of
  the largest weights (Pareto-smoothed importance sampling diagnostic, Vehtari et al., arXiv:1507.02646: a generalized
  Pareto fit to the largest min(0.2N, 3√N) weights by the Zhang–Stephens estimator; used as a diagnostic only, the
  estimate is not smoothed). **N = 4,000 per stream, two streams** per ν: seeds 730,000 + 10j + r (j = 0, …, 4 for ν =
  3, 4, 6, 10, 30; r = 0, 1). **Accuracy check:** for every finite ν, |log Λ̂_r=0 − log Λ̂_r=1| ≤ 0.1, ESS ≥ 200 and
  k̂ < 0.7 in each stream; the result is the pooled estimate (N = 8,000). If the check fails for any ν, all five ν are
  redone once with N = 32,000 per stream (seeds 740,000 + 10j + r) and the same check; if it fails again the outcome is
  **"ν not determinable by this method (Monte Carlo)"**.
- **Weights.** w(ν) ∝ π(ν)·L(ν) over the six grid points. Primary: π flat on the grid. Sensitivity (reported): π uniform
  in 1/ν, i.e. each grid point weighted by the length of its cell in 1/ν ∈ [0, 1/3] (cell edges at the midpoints between
  grid values): π = 0.125 (ν = 3), 0.25 (4), 0.225 (6), 0.20 (10), 0.15 (30), 0.05 (∞). The summary quantity is
  **P(ν ≤ 4) = w(3) + w(4)** (prior value 1/3 flat, 0.375 in 1/ν). ν ≤ 4 is where GTP's crossover lies (between 4 and 6),
  chosen after R2-RE-GTP (post hoc).
- **Sensitivities (reported only, with the check outcome; no escalation).** (i) Profile: Λ(ν, m·τ̂_HF) for m ∈ {0.5, 0.75, 1, 1.5, 2} (same N and check; seeds
  770,000 + 100k + 10j + r for the k-th m other than 1), L_prof(ν) = max_m, and P(ν ≤ 4) from it. (ii) The V(τ̂_obs) base
  (M1): u and M recomputed with the calibrator host effect at τ̂_obs in the base covariance, τ̂_HF refitted on it, and
  P(ν ≤ 4) with the same N and check (seeds 820,000 + 10j + r). (iii) The 0.45 grouping: P(ν ≤ 4) with seeds 830,000 +
  10j + r.

*Known-answer check (before L(ν) is computed on the data; only if Stage 1 passes).* All mocks are at the data's τ̂_HF
with u_s = B ε_s + M b_s, B = ZᵀP K_C (K_C the lower Cholesky factor of C on `rows_a`), ε_s =
`default_rng(700_000 + s).standard_normal(3489)` (common to all four injections), **s = 0, …, 199 per injection**:
- **t₃** and **t₁₀**: b_s = s_ν·t_s, s_ν = τ̂_HF√((ν − 2)/ν), t_s = `default_rng(710_000 + s).standard_t(3, n_g)` and
  `default_rng(720_000 + s).standard_t(10, n_g)`.
- **(i) Heteroscedastic Gaussian (S2):** b_g ~ N(0, d_g) with d_g ∝ c_g, c_g the mean of C_ii over group g's rows, scaled
  so that the mean of d_g over the groups is τ̂_HF² (variance-matched); draws `default_rng(780_000 + s).standard_normal(n_g)`
  times √d_g.
- **(ii) t₃ truncated at 3.5σ (S2), by whole-mock rejection (exact conditioning):** the residual is the GLS residual of
  the mock under C with all global parameters refitted, r = C_a P (K_C ε + Z b) on `rows_a` (the same projection as the
  data fit), and σ_i = √C_ii, on the Hubble-flow rows; a mock passes the cut if no group has a row with |r_i| > 3.5σ_i.
  Attempt 0 is the plain t₃ mock's (ε_s, t_s); attempts k = 1, …, 99 draw ε (3,489 values) and then t (n_g values,
  `standard_t(3)`) together from one `default_rng(1_000_000 + 1_000·s + k)`. The first attempt that passes is the mock
  (the noise alone can exceed the cut: a design-only estimate gives a probability of about 0.12 per attempt). A mock with
  no passing attempt among these 100 is "truncation failed" and left out (more than 10 such mocks: "ν not determinable
  (selection)"). Mocks accepted at k ≥ 1 lose the common random numbers with the plain t₃ mocks, which is harmless for
  the comparison of means. This keeps the design fixed and draws from the mock distribution conditioned on no SN beyond
  3.5σ; it uses the SH0ES-system residual and C's diagonal, not Pantheon+'s own fit and uncertainties, so it approximates
  the cut of item 6.
In each mock: τ̂_s refitted by the reduced form (`reml_tau(f, 0.5, 0.01, interval=False)`, the zero rule), then L_s(ν)
at τ̂_s for the six ν with one stream of N = 2,000 and the same estimator (seeds 750,000 + 10s + j for t₃, 760,000 + 10s
+ j for t₁₀, 800,000 + 10s + j for (i), 810,000 + 10s + j for (ii)), and P_s(ν ≤ 4) with flat weights (if τ̂_s < 10⁻³,
every L_s = 1 and P_s = 1/3). No accuracy check per mock; the fraction of mocks with ESS < 200 or k̂ ≥ 0.7 in any ν is
reported (M5).
**Pass rule, fixed now.** (a) The heavy-tail label (P_s > 0.95) in at most 10 of the 200 t₁₀ mocks, and the light-tail
label (P_s < 0.05) in at most 10 of the 200 t₃ mocks. (b) Δ_b = mean P_s(t₃) − mean P_s(t₁₀) ≥ 0.10. (c) The heavy-tail
label in at most 10 of the 200 heteroscedastic mocks (i). Then, only if (a)–(c) hold, the truncated mocks (ii), over
those not "truncation failed": (d) |mean P_s(t₃ truncated) − mean P_s(t₃)| ≤ Δ_b; (e) the light-tail label (P_s < 0.05)
in at most 10 of them. If (a), (b) or (c) fails, the outcome is **"ν not determinable by this method"** with the failing
part named ((a): mislabels; (b): no power at this τ_HF; (c): heteroscedasticity); otherwise, if (d) or (e) fails or more
than 10 truncated mocks failed, **"ν not determinable (selection)"**. In all these cases L(ν) on the data and p_int
are not computed. Reported: the four mean P_s, the label counts per injection, the fraction of t₃ mocks with
P_s > 0.95 (M5), the quantiles of P_s and τ̂_s, the fraction of mocks with τ̂_s ≥ 0.02 (a proxy for passing the Stage-1 gate, labelled "proxy" in the output: the
mock refits use `interval=False`, so the interval's lower end is not checked), the number of
rejected attempts and of "truncation failed" mocks, and the ESS and k̂ quantiles.

*Integrated p (computed only when label 4, 5 or 6 is reached).* p_int = Σ_ν w(ν)·p_cal(ν, τ) with the recorded
R2-RE-GTP values, never recomputed: **primary at τ̂_obs**, p_cal from `r2_re_gtp.json` `refit.<ν>.tau_obs.p_cal.p`
(0.0768, 0.0504, 0.0300, 0.0208, 0.0166, 0.0165 for ν = 3, 4, 6, 10, 30, ∞); **bound** with the maximum over the three
τ, `p_cal_max_over_tau.<ν>` (0.0783, 0.0510, 0.0303, 0.0216, 0.0178, 0.0165), labelled "at the three checked τ only".
Both are reported with the flat weights (primary) and the 1/ν weights, next to the prior-only values (item 7).
p_int is a weighted average of calibrated p values, not itself a calibrated p value for a composite null; it inherits
R2-RE-GTP's caveats (three τ, coarse grid that stops at ν = 3).

*Labels, fixed now (exactly one applies, in this order).*
1. **"ν not evaluable (<reason>)"**: a check fails (below; the reason names it), the τ̂_HF interval's lower end is "not
   determined", or Stage 1's τ̂_HF is at the upper bound (reason "bound").
2. **"ν not evaluable (no excess scatter in the Hubble flow)"**: Stage 1's gate.
3. **"ν not determinable by this method (<part>)"** or **"ν not determinable (selection)"**: the known-answer check
   fails, or the Monte Carlo accuracy check fails twice (part "Monte Carlo").
4. **"ν constrained to the light-tail side (P(ν ≤ 4) < 0.05)"**; 5. **"ν constrained to the heavy-tail side (P(ν ≤ 4) >
   0.95)"**; 6. **"ν weakly constrained"** otherwise. Each of 4–6 is written with "(if Hubble-flow and calibrator effects
   share ν)" and reports p_int. **Scale condition (S5):** under 4 or 5, if 0.0767 lies outside τ̂_HF's 68% interval, the
   label gets "(scale differs: transfer not supported)" appended.
- *Reading of p_int against 0.05, fixed now.* Under labels 4 and 5 without the scale suffix, p_int (primary) is stated as
  "below 0.05" or "at or above 0.05": below 0.05 reads "integrated over the Hubble-flow-informed ν, diffuse host scatter
  of R2-RE's size is excluded by G at the 5% level (reported, non-decisive)"; at or above reads "not excluded". Under 4
  or 5 with the scale suffix, and under label 6, p_int is reported but **not** read against 0.05 (under 6 next to the
  prior-only reference value 0.0352: the weights there reflect the grid prior as much as the data, item 7). The bound
  and the 1/ν version are reported in every case and are not read.
- The labels attach to R2-RE-GTP's statement as its outside constraint; R2-RE-GT's sub-label and gloss, R2-RE-GTP's
  statement, R2-RE's headline row, `summary.json` `R2_host` and the claim's verdict do not change.

*Checks (a failure gives label 1 with the reason).* Row classes: 277 Hubble-flow rows, all in `rows_a` (3,489 rows);
the grouping count check (above); R2-RE's reproduction on the data with R2-RE-G's tolerances by name (τ̂_obs within
`shape.TAU_OBS_ATOL`, the recorded REML grid differences within `shape.GRID_ATOL`); the reduced form against
`reml_m2l`: g(τ²I) equals reml_m2l(τ) − reml_m2l(0) within `shape.GRID_ATOL` at τ = 0.01, 0.05 and τ̂_HF; M's eigenvalue
rule above; the Cholesky factor of C; for the first three t₃ mocks, y_s built in full (ŷ + K_C ε_s + Z b_s on `rows_a`)
and τ̂_s from `reml_m2l` with the n_g groups within `shape.TAU_OBS_ATOL` of the reduced-form τ̂_s.

*Order and stages (as R2-RE-GT's power and full stages).* A **check stage** runs the checks, Stage 1 and, if the gate
passes, the known-answer check, and writes `results/r2_re_nu_check.json` (τ̂_HF, the gate, the mock summary and per-mock
τ̂_s, P_s, ESS, k̂); it never computes L(ν) on the data. One line with τ̂_HF, the gate and the known-answer outcome is
written into log.md and committed **before** the full stage starts. The **full stage** recomputes the checks, Stage 1
and the first 20 mocks of each injection (all must equal the check record exactly), then computes L(ν), the weights,
the label and p_int, and writes `results/r2_re_nu.json` (under 1 MB) with the key `R2_RE_NU` in `summary.json` (every
other key byte-identical). If Stage 1's gate gives label 2, or the known-answer check gives label 3, the check stage's
outcome is final and the full stage only writes `r2_re_nu.json` with that label (no L(ν)). The first formal outcome
stands; a rerun needs a reason also present in log.md.

*Data and runtime.* Cache only, no download (the three FITS files of section 3, and `Pantheon+SH0ES.dat` already in the
cache, 0.58 MB, read through `ctx.http`, which may download it again if the cache has evicted it; the code reads it
with `usecols` = CID and USED_IN_SH0ES_HF only, and a test asserts that no other column is read). Timed on synthetic inputs, single
thread: `reml_m2l` on `rows_a` with 277 single-row groups 0.47 s per evaluation (about the same with the grouped design),
so Stage 1 (about 70 evaluations with the refinement and the interval) about 35 s per covariance and grouping (three:
main, 0.45, V(τ̂_obs) base); one importance evaluation g(D) about 0.9 ms at 277 × 277, somewhat less at n_g ≈ 240.
Known-answer check: 800 mocks × 5 finite ν × 2,000 draws ≈ 8 × 10⁶ evaluations, about 1.5–2 h; data Stage 2 (5 × 8,000)
under 1 min, the sensitivities about 6 min, an escalation about 5 min; the three pointwise mocks about 2 min; data
loading and host identification 2–3 min. Check stage about 2 h, full stage about 20 min, up to twice that with a
shared CPU.

*Code checks before the formal run (synthetic data only).* g(D) against direct REML on a synthetic system with V = C +
Z D Zᵀ for random D and a grouped Z (10⁻⁸); the importance sampler, **with the same defensive estimator and diagnostics**,
on a synthetic factorised system (diagonal C on the Hubble-flow rows, single-row groups, no cross terms) against
per-SN one-dimensional quadrature of the Gaussian–t convolution (log Λ within three Monte Carlo standard errors, at ν = 3
and 10); ν = 10⁶ against the Gaussian closed form; the k̂ estimator against known generalized Pareto samples; the
variance matching (sample variance of b = τ²) and the heteroscedastic scaling (mean d_g = τ²); the grouping (connected
components) and its count check (main grouping only); the truncation (whole-mock rejection: attempt 0 is the plain
mock, then the seeds of attempts 1–99; no residual beyond 3.5σ in an accepted mock; the attempt limit and the
"truncation failed" count);
the `usecols` read of `Pantheon+SH0ES.dat` (no other column is read); the 1/ν
weights listed above; the gate, the label order, the scale condition, the pass rule and the p_int arithmetic from the
recorded keys; the check record contains no L(ν), weights, label or p_int computed on the data. On the real data before
the formal run, nothing beyond the checks above (no τ_HF).

*Switch and code.* `PARAMS["nu_check"]` (false by default; true with `nu_only` = true, first with `nu_stage` "check",
then "full", only for the formal runs, back afterwards with dated notes in log.md; the block never runs in a full study
run, which copies `R2_RE_NU` from an existing `r2_re_nu.json`), `"nu_grid": [3, 4, 6, 10, 30, "inf"]`, `"nu_tau_gate":
0.02`, `"nu_group_corr": 0.3`, `"nu_group_corr_sens": 0.45`, `"nu_q_prior_frac": 0.1`, `"nu_n_is": 4_000`,
`"nu_n_is_escalate": 32_000`, `"nu_is_seed": 730_000`, `"nu_is_seed_escalate": 740_000`, `"nu_n_mocks": 200`,
`"nu_n_is_mock": 2_000`, `"nu_cut_sigma": 3.5`, `"nu_cut_attempts": 100`, `"nu_mock_seeds":
{"eps": 700_000, "t3": 710_000, "t10": 720_000, "het": 780_000, "trunc_joint": 1_000_000, "is_t3":
750_000, "is_t10": 760_000, "is_het": 800_000, "is_trunc": 810_000}`, `"nu_profile_m": [0.5, 0.75, 1, 1.5, 2]`,
`"nu_profile_seed": 770_000`, `"nu_vbase_seed": 820_000`, `"nu_group_sens_seed": 830_000`, `"nu_rerun_reason": ""`.
Seeds 700,000–789,999, 800,000–839,999 and 1,000,000–1,199,099 collide with none used before (R2-RE-GTP's list plus 430,000–469,999,
613,000 and 614,000). A formal run uses one thread (`OMP_NUM_THREADS`,
`MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS` = 1) and refuses to start unless the `nu_*` values equal those above. Results
`results/r2_re_nu_check.json` and `results/r2_re_nu.json` (each below 1 MB); a new module or a block appended to
`shape.py` (no change to earlier functions or results), tests, a conclusion check, a web section and section 8 knobs.
None of this exists yet.

*What changes in section 5.* A new subsection "R2-RE-NU" with the numbers and the label; the R2-RE-GTP reading gains one
sentence with the label and p_int; the open question of section 7 on ν is answered accordingly. Post hoc throughout in
one respect: the route (Hubble flow), the gate threshold, the grouping thresholds and the summary P(ν ≤ 4) were chosen
after all of R2-RE-GTP's results and after seeing the structure of C on the Hubble-flow rows (items 3 and 4), though
before any Hubble-flow residual.

*Amendments before any R2-RE-NU computation on the data (2026-11-24).* Two points the addendum left open, fixed while
writing the code (`nu.py`) and before anything was computed from the Hubble-flow rows of y; no rule, threshold or label
above changes.
1. **Profile seeds.** In "770,000 + 100k + 10j + r for the k-th m other than 1", k is counted from 0, like j and r: k = 0,
   1, 2, 3 for m = 0.5, 0.75, 1.5, 2.
2. **Upper end of τ̂_HF's interval not determined.** If the root search for the upper end fails, the interval is taken as
   [lower end, ∞) for the scale condition (0.0767 counts as inside if it is at least the lower end), and this is reported
   as `upper_end: "not determined"`. A lower end that is not determined is label 1, as registered.

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
  The τ part is undetermined, the label section 2 expected (it estimated p ≈ 0.03; observed 0.072). The
  spread part says R4's excess spread (1.307 on the first 1,000 subsets; 1.33 on all 10,000) is itself unusual under C: there is more scatter among calibrator SN rows than C
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
  the "unusual spread" label, most of τ̂ (0.077 → 0.031 without it) and the A flip are the effect of one outlying host,
  N5584 (one SN, 2007af); whether its SN or its Cepheid distance is off is not identified. Without
  N5584's rows the host step gives z = −1.63 under C and −1.50 under V, i.e. "no host-selection effect
  detected" under either covariance. An explicit, pre-registered treatment of N5584 (removal and a
  heavy-tailed host effect) is registered as T-039.
- A smoke run before the formal run showed part of A (the N5584 removal: τ̂ ≈ 0.031, z ≈ −2.04);
  disclosed in `log.md` on 2026-11-17, rules unchanged.

### R2-RE-N5584 (addendum 2026-11-18, T-039)

Run of 2026-11-18 (`python -m astrolab run 003`, 20,775 s, of which this block 9,311 s; all earlier
results reproduce exactly, only timing fields changed). Numbers: `results/r2_re_n5584.json`.

| Part | Result | Label (pre-registered rule) |
|---|---|---|
| (a) rows removed | 169 (4 calibrator SN rows, 165 Cepheid rows, no other); 3,320 rows, 36 hosts | – |
| (a) host step under C (known before) | −0.0532 ± 0.0327 mag, z = −1.63 | no host-selection effect detected |
| (a) R2-RE on 36 hosts (known before) | τ̂_N = 0.031 mag (68% interval 0–0.070); under V(τ̂_N) −0.0512 ± 0.0341, z = −1.50 | no host-selection effect detected |
| (a) R4-N, 10,000 draws of 10 of 36 hosts | CCHP shift at the 8.5th percentile (z percentile 7.3); spread of Δ/σ 1.044; under V(τ̂_N): spread 0.993, percentiles 9.1 (shift) and 7.9 (z) | **consistent with random-subset fluctuations** |
| (a) B-N, τ̂ under C (400 simulations, none failed) | 135 of 400 with τ̂_s ≥ 0.031 (220 at zero); p = 0.339, 95% interval 0.291–0.386 | **τ̂ not unusual under C** |
| (a) B-N, R4-N spread under C (2,000 simulations, 1,000 subsets) | spread_obs 1.033; 717 of 2,000 ≥ it; p = 0.359, interval 0.337–0.380 | **the R4 spread is consistent with C** |
| (a) reading | – | **the excess calibrator scatter of R2-RE-ROB is attributable to N5584** |
| (b) implementation check (ω = 1, start τ = 0.20) | 147 iterations; τ within 6 × 10⁻⁷ and z' within 6 × 10⁻⁶ of R2-RE | passed |
| (b) ν = 4, 37 hosts | both starts converge (95 and 121 iterations) to τ̂_T = 0.0752; N5584 ω̂ = 0.392 (effective scatter τ̂/√ω̂ = 0.120 mag), next N1365 0.804 and N3982 0.879, all others 0.97–1.06; host step under V_T −0.0553 ± 0.0401, z_T = −1.38 | no host-selection effect detected; **R2-RE verdict robust to a heavy-tailed host effect** |
| (b) ν = 2 and 10 (reported only) | τ̂_T 0.068 and 0.078; N5584 ω̂ 0.175 and 0.724; z_T −1.32 and −1.46 | same row |
| Joint reading | – | **the null result holds under both removal and down-weighting of N5584; only the hybrid τ route of R2-RE-ROB A flips** |

- **Reading (pre-registered).** Without N5584 the calibrator scatter is what C allows: τ̂ = 0.031 is
  an ordinary value under the null (p = 0.34) and the spread over the first 1,000 subsets falls from
  1.307 (37 hosts) to 1.033 (36 hosts; p = 0.36; over all 10,000 R4-N draws 1.044), so the
  pre-registered rule gives "attributable to N5584". Because the null does not include the choice of
  N5584 as the most extreme of 37 hosts (post hoc, section 6), we read this as "consistent with one
  outlying host"; the selection-aware test R2-RE-SEL (T-042, below) gives this as its pre-registered reading. The CCHP selection is again an ordinary low draw (8.5th
  percentile; R4 on 37 hosts gave 5.7). Keeping N5584 but letting the model down-weight it (ν = 4)
  gives N5584 alone a clearly reduced weight and leaves the verdict where R2-RE put it (z_T = −1.38;
  R2-RE −1.53). Both treatments give the same row; the R2-RE-ROB A flip to "supports the paper"
  needs N5584's rows in the shift while its scatter is taken out of τ̂, which neither treatment does.
- **As expected.** Section 2 predicted (a)'s reading and the direction of (b) (N5584 gets the
  smallest weight); (a)'s τ̂ and host steps were known. What is new is that the B-N simulations
  calibrate the 36-host scatter (p_τ = 0.34, p_spread = 0.36, against 0.072 and 0.021 with N5584),
  that R4-N stays in the ordinary range, and that the heavy-tailed fit keeps the row for ν = 2, 4 and 10.
- **Descriptive.** Over the treatments that remove or model N5584 the host step is z = −1.38 to −1.63
  (C on 36 hosts −1.63, V on 36 hosts −1.50, V_T −1.38; R2-RE on 37 hosts −1.53); only C on all 37
  hosts, which treats N5584's offset as measured, reaches −2.21. τ̂_T (0.075) is close to R2-RE's 0.077: the
  heavy tail barely changes the typical host scatter; it widens N5584's own variance and so removes
  most of N5584's pull on the shift.
- **Status of R2.** The R2-RE headline row stands ("no host-selection effect detected"); R2-RE-ROB's
  label "verdict sensitive to single hosts' influence on τ̂ (N5584)" stays as recorded and now has its pre-registered
  explanation. Whether N5584's offset comes from its SN (2007af) or its Cepheid distance is still not
  identified by these data.
- **Post hoc (referee, 2026-11-18; section 6).** (1) The variational EM is not the Student-t
  estimate: the exact Student-t restricted likelihood (w integrated out by importance sampling) peaks
  at τ ≈ 0.055 for ν = 4 (0.035 for ν = 2, 0.070 for ν = 10), against the EM's 0.075, 0.068 and 0.078;
  the README said the fixed point maximises a bound, not the likelihood. Across fitting methods and
  plug-in definitions z ranges from −1.11 to −1.85 (ν = 4: −1.15 to −1.67; exact posterior mixture
  −1.47), so the row is the same in every variant, but z_T itself carries a method spread of about
  ±0.3. (2) The B-N null does not include the selection of N5584 as the most extreme of 37 hosts;
  a null that drops the worst host in each simulation would give smaller p values, so "attributable
  to N5584" is better read as "consistent with one outlying host" (selection-aware null registered as
  T-042). (3) Dropping only N5584's four SN rows gives z = −1.68 under C, and dropping only its
  Cepheid rows −1.62: either removal neutralises the host, so the data cannot say which side is off.
  Its SN rows sit +0.25 to +0.35 mag faint relative to the fit without them; the literature points to
  the SN side: an independent reanalysis of N5584's HST Cepheids agrees with SH0ES (μ = 31.810 ± 0.047
  against 31.786 ± 0.046, Javanmardi et al. 2021, arXiv:2102.12489) and JWST and HST Cepheid
  intercepts agree there (Riess et al. 2023, arXiv:2307.15806), whose full text (read in the HTML version through a summary,
  not quoted verbatim; the reddening description is theirs) also describes SN 2007af as a
  normal, low-reddening SN Ia and the host as an expected outlier of about 0.25 mag among the
  calibrators. That would make N5584 (literature-based, not tested here) a statistical fluctuation of the SN Ia population rather than a data
  defect, which is the random-effect picture.

### R2-RE-SEL (addendum 2026-11-19, T-042)

Run of 2026-11-20 (`python -m astrolab run 003`, 33,375 s, of which this block 12,258 s; all earlier
results reproduce exactly, only timing fields changed). Numbers: `results/r2_re_sel.json`.

| Part | Selected null (this block) | Unselected null B-N (recorded) | Label (pre-registered rule) |
|---|---|---|---|
| Reproduction checks | leave-one-out maps within 3.4 × 10⁻¹² of `loo_chi2`; both criteria select N5584 on the real data (X: χ² 12.478; S: spread_excl 1.0267, expected 1.027 ± 0.001); τ̂_N and spread_obs equal the recorded values; the first five subsets equal B-N's | – | passed |
| τ̂ under C, criterion X (400 simulations, none failed) | 97 of 400 with τ̂_s ≥ τ̂_N = 0.031 (257 at zero; quantiles 5/50/95% 0, 0, 0.062); p = 0.244, 95% interval 0.201–0.288 | 135 of 400 (220 at zero; 95% quantile 0.080); p = 0.339 | **τ̂_N not unusual under the selected null** |
| 36-host spread under C, criterion X (2,000 simulations, 1,000 subsets) | 481 of 2,000 ≥ spread_obs 1.033 (quantiles 0.746, 0.947, 1.153); p = 0.241, interval 0.222–0.260 | 717 of 2,000 (0.771, 0.977, 1.222); p = 0.359 | **the 36-host spread is consistent with the selected null (X)** |
| 36-host spread under C, criterion S | 273 of 2,000 ≥ 1.033 (quantiles 0.705, 0.898, 1.106); p = 0.137, interval 0.122–0.152 | as above | **the 36-host spread is consistent with the selected null (S)** |
| Reading | – | – | **the excess calibrator scatter of R2-RE-ROB is consistent with one outlying host, selection included** (rule 2) |

- **Reading (pre-registered, rule 2).** With the choice of the most extreme of 37 hosts simulated, the
  scatter of the 36 remaining hosts is still ordinary under C: all three Clopper–Pearson intervals lie
  above 0.05 (τ under X 0.201–0.288, spread under X 0.222–0.260, spread under S 0.122–0.152). So the post-hoc gloss of R2-RE-N5584, "consistent with one outlying host", is now the
  pre-registered reading of this test, with one caveat: the τ part uses criterion X only, which is less
  aligned with τ̂ than "smallest τ̂_j" (not feasible: 37 REML fits per simulation), so its p is
  expected to be higher than under an aligned criterion; the τ label supports the reading only as far
  as the spread labels do. The pre-registered label of R2-RE-N5584 (a), "attributable to N5584", stays
  recorded as the outcome under the unselected null. *Gloss since 2026-11-21 (R2-RE-D, rule (3), next
  subsection):* consistent with C after removing one host, and not distinguished from diffuse scatter.
- **As expected, in direction.** The selection lowered every p value relative to B-N (τ 0.339 → 0.244;
  spread 0.359 → 0.241 under X and → 0.137 under S), and criterion S, the one aligned with the spread,
  lowered it most; no part has p at or above B-N's (descriptive rule: none). The X values fall in the
  0.1–0.3 that section 2's rough argument gave. Section 2 thought "undetermined" or "unusual" more
  plausible under S than under X; the outcome under S is "consistent" (interval 0.122–0.152).
- **Which host the criteria drop (reported).** Under the null, criterion X drops one of the hosts with
  four calibrator rows most often (N5468 and N5584 190 times each, N5643 170 of 2,000; all 37 hosts
  occur), as expected from a raw χ² term; criterion S drops N5468 192, N5643 170 and N5584 161 times
  (36 hosts occur). The two criteria drop the same host in 457 of 2,000 simulations (89 of the first
  400). The selection is simulated, not N5584's identity: in about nine simulations out of ten the
  dropped host is another one.
- **How extreme N5584 is as the most extreme of 37 (descriptive, no label).** The largest
  leave-one-out χ² term reaches N5584's 12.478 in 228 of 2,000 null simulations (p = 0.114, interval
  0.100–0.129), close to the 0.12 that section 2 estimated by treating the 37 terms as independent χ²
  variables: N5584's term is large but not exceptional once the choice among 37 hosts is allowed for.
  The smallest spread_excl over the 37 hosts is at or below the real value 1.027 in 1,764 of 2,000
  simulations (p = 0.882): under C, leaving out the "best" host typically leaves a smaller spread (median
  0.886) than leaving out N5584 does on the real data, so by this statistic the subsets without N5584
  are on the high side, in line with p = 0.14 under criterion S; it uses the 37-host reference fit
  (N5584 inside), unlike the spread parts.
- **Post hoc (referee, 2026-11-20; section 6): what "consistent" can and cannot show.** The null is C
  with no outlier, so rule (2) says only that the 36 remaining hosts do not reject C; it does not test
  one outlying host against host-level scatter spread over all hosts. Against such diffuse scatter the
  criterion-S spread test has little power (with a proxy statistic, see section 6: it rejects at 5% in
  21% of simulations for τ = 0.05 mag and 45% for τ = 0.077), so the pre-registered reading, which
  stands as a label, should be read as "after the selection is simulated, the 36 remaining hosts are
  consistent with C". The drop of the spread when the S-selected host is removed (real data 1.307 −
  1.027 = 0.280) is unusual under C and less unusual under diffuse scatter: it is reached in 0.6% of
  simulations under C and in 1.9% and 3.6% under diffuse scatter with τ = 0.05 and 0.077 (37-host
  spread at least 1.307 and post-drop spread at most 1.027 together: 0.2% under either). This points
  towards one outlying host but does not show it: no single-outlier model was simulated, and the drop
  partly restates the already high 37-host spread (reached in 25 of 2,000 simulations under C). The
  statistic was chosen after seeing the data and uses a proxy; a pre-registered comparison, including a
  single-host offset model, is registered as T-048. Two further points: the three labels are not
  independent (τ̂_s and the criterion-X spread correlate at 0.81 over the first 400 simulations), and
  criterion X barely conditions the τ part (p = 0.26 in the 37 simulations where X drops N5584, 0.24 in
  the other 363), as the section 2 caveat said. *Outcome of T-048 (2026-11-21, R2-RE-D, next
  subsection):* reading (3), "tested diffuse model(s) not excluded (τ = 0.077, 0.105)"; this bullet stays
  as written (the addendum replaces it only under reading (2)). *Outcome of T-055 (2026-11-21,
  R2-RE-G):* "undetermined (underpowered)" (power 0.49): no powered shape test separates the two
  pictures; Gaussian diffuse scatter is excluded by G (p_G 0.016) but not independently of R2-RE-D.
- **Status of R2.** Unchanged, as fixed in section 2: the R2-RE headline row ("no host-selection
  effect detected"), the R2-RE-ROB and R2-RE-N5584 labels, `summary.json` `R2_host` and the claim's
  verdict stay as recorded.
- **Runtime.** The block took 12,258 s: τ part 8,015 s (about 20 s per REML fit), spread parts 3,975 s
  (rows for the other 36 dropped hosts, about 110 s each; N5584's were built before the τ part); the whole run 9.3 h, within the 8.5–10 h estimate. No
  data downloaded.

### R2-RE-D (addendum 2026-11-21, T-048)

Run of 2026-11-21 in the standalone mode (`PARAMS["d_only"]` set to true for the run and back to false
afterwards; `python -m astrolab run 003`, 3,962.6 s, of which this block 3,961.4 s; cache only, no data
downloaded). It wrote only `results/r2_re_d.json`, the eight `results/r2_re_d_sims_<model>.json`,
`provenance_d.json`, `run_info_d.json` and the `R2_RE_D` key of `summary.json`. Numbers:
`results/r2_re_d.json` (keys in brackets below are under `models.<key>`).

**Checks (rule (1)).** All passed (`observed.mismatches` empty): spread_37 = 1.3070929 and spread_36 =
1.0325255 reproduce the recorded values to a relative 1.9 × 10⁻¹⁴ and 7.2 × 10⁻¹⁴ (tolerance 10⁻⁹);
criterion S selects N5584 on the real data with spread_excl 1.02668 (within 0.00032 of 1.027, tolerance
0.001; next lowest N1365 1.2066); δ̂ = 0.3363369 mag, 3.1 × 10⁻⁶ from the recorded 0.33634 (tolerance
5 × 10⁻⁶), σ_δ = 0.09252 (δ̂/σ_δ = 3.64); τ̂_N = 0.0313714 reproduces the recorded value to a relative
7 × 10⁻¹⁰ (tolerance 10⁻⁶), so the reported variant O(δ̂) + V(τ̂_N) was run. The rows of all 37
reduced systems were built (89–114 s each), none failed; every model's Cholesky factor succeeded and all
eight models are "evaluated".

**Observed statistics** (`observed`): spread_37 = 1.30709, spread_36 = 1.03253 (N5584 removed), D =
spread_37 − spread_36 = 0.27457; the proxy D_proxy = 0.28041 (for comparison with the referee only).

| Model | D: k / 10,000, p_D, 95% interval | Label (D) | J: k_J / 5,000 (count at the observed point of 5,000 half-A), p_J, 95% interval | Label (J) | Q_raw (descriptive) |
|---|---|---|---|---|---|
| C (reported) | 56, 0.0057, 0.0042–0.0073 | excluded (D) | 86 (3; t_obs 0.0006), 0.0174, 0.0138–0.0212 | excluded (J) | 0.0006 |
| **V(0.05)** | 156, 0.0157, 0.0133–0.0182 | **excluded (D)** | 192 (10; 0.0020), 0.0386, 0.0332–0.0441 | **excluded (J)** | 0.0025 |
| **V(0.077)** | 338, 0.0339, 0.0303–0.0375 | **excluded (D)** | 399 (26; 0.0052), 0.0800, 0.0724–0.0877 | **not excluded (J)** | 0.0048 |
| **V(0.105)** | 763, 0.0764, 0.0712–0.0817 | **not excluded (D)** | 339 (23; 0.0046), 0.0680, 0.0610–0.0751 | **not excluded (J)** | 0.0044 |
| **O(δ̂)**, δ̂ = 0.3363 | 5,193, 0.519, 0.509–0.529 | **not excluded (D)** | 3,377 (979; 0.1958), 0.675, 0.662–0.688 | **not excluded (J)** | 0.193 |
| O(δ̂ − σ_δ), δ = 0.2438 (reported) | 1,873, 0.187, 0.180–0.195 | not excluded (D) | 1,484 (233; 0.0466), 0.297, 0.284–0.310 | not excluded (J) | 0.044 |
| O(δ̂) + V(τ̂_N), τ̂_N = 0.0314 (reported) | 4,957, 0.496, 0.486–0.506 | not excluded (D) | 3,271 (897; 0.1794), 0.654, 0.641–0.667 | not excluded (J) | 0.175 |
| O_any(δ̂) (reported) | 1,318, 0.132, 0.125–0.139 | not excluded (D) | 1,478 (227; 0.0454), 0.296, 0.283–0.308 | not excluded (J) | 0.044 |
| Reading | – | – | – | **tested diffuse model(s) not excluded (τ = 0.077, 0.105)** (rule 3) | – |

Bold rows are the decisive models. p_D = (1 + k)/(1 + 10,000) [`D.p`], p_J = (1 + k_J)/(1 + 5,000)
[`J.p`]; intervals are the Clopper–Pearson intervals of k/n [`ci95`]; Q_raw is the raw quadrant share
over all 10,000 simulations [`Q_raw.share`], not a p value.

- **Reading (pre-registered, rule 3).** Rule (1) does not apply (all checks passed, all models
  evaluated). Rule (2) needs every V(τ) "excluded (J)"; V(0.077) and V(0.105) are "not excluded (J)", so
  rule (2) fails, and rule (3) applies: **"tested diffuse model(s) not excluded (τ = 0.077, 0.105)"**
  (`reading`; `summary.json` `R2_RE_D.reading`). Rules (4) and (5) are not reached. The reading is formed
  by the rules fixed in section 2 before any simulation; nothing was chosen after the run.
- **What "not excluded" means.** A model is "not excluded" by a statistic when the whole 95% interval of
  its Monte Carlo p value lies above 0.05: the model produces data as extreme as observed (as
  "one-outlier-like" for J, as large a drop for D) often enough to be consistent with the data at the 5%
  level. It is not evidence for that model, and "not excluded" for the diffuse models is not evidence
  against a single outlying host: the one-host model O(δ̂) is not excluded either. Neither picture is
  rejected; the test does not decide between them. The referee (post hoc, below and section 6) found
  that the comparison has only about 50% power against its own one-host alternative, so this "not
  excluded" is an underpowered null result, not evidence for diffuse scatter.
- **Section-5 action (fixed by the addendum for reading (3)).** These data do not distinguish one
  outlying host from host-level scatter of R2-RE's size (τ = 0.077–0.105 mag). R2-RE-SEL's reading stays,
  glossed "consistent with C after removing one host, and not distinguished from diffuse scatter" (added
  to its reading bullet above); its post-hoc referee bullet stays as written. The R2-RE headline row
  ("no host-selection effect detected"), `summary.json` `R2_host` and the claim's verdict do not change;
  no earlier label changes.
- **The smallest diffuse model is excluded.** V(0.05) is excluded by both statistics (D 0.016, J 0.039):
  host scatter as small as the lower end of R2-RE's 68% interval, spread over all hosts, rarely produces
  the observed pattern. D also excludes V(0.077) (0.034), but D is not the deciding statistic for rule
  (3), which uses J. The J exclusion of V(0.05) is not firm: it depends on which half calibrates J
  (post hoc, below).
- **The one-host models.** O(δ̂) is not excluded (D 0.52, J 0.68), largely by construction (δ̂ is fitted
  to these data and N5584 was singled out by them): a consistency check, not evidence. The reported
  variants are not excluded either: with the offset reduced by one standard error (O(δ̂ − σ_δ): D 0.19,
  J 0.30), with a small diffuse term added (O(δ̂) + V(τ̂_N): 0.50, 0.65), and with the offset on a host
  drawn at random instead of N5584 (O_any: 0.13, 0.30; criterion S picks the offset host in 4,358 of
  10,000 simulations, `Oany.selected.n_offset_host`). Under O(δ̂) criterion S picks N5584 in 9,318 of
  10,000 simulations (7,213 under O(δ̂ − σ_δ), 9,077 under O(δ̂) + V(τ̂_N)); under C 696, under V(0.05),
  V(0.077), V(0.105) 738, 779, 823 [`selected.n_host`].
- **C (reported, enters no rule).** Excluded by both statistics (D 0.0057, J 0.017); the observed
  pattern is rare without any excess scatter, as ROB found (here P(spread_37 ≥ obs) = 132 of 10,000
  under C, against ROB's 42 of 2,000 on other seeds with ROB's p = 0.021).
- **Marginals (reported, `P_spread_37_ge_obs`, `P_spread_36_le_obs`).** The two coordinates pull in
  opposite directions as τ grows: P(spread_37 ≥ 1.307) is 0.013 (C), 0.077, 0.267, 0.576 (V(0.05),
  V(0.077), V(0.105)) and 0.431 (O(δ̂)); P(spread_36 ≤ 1.033) is 0.863, 0.661, 0.395, 0.150 and 0.657.
  A large τ makes the 37-host spread ordinary but the post-removal spread low; only the one-host models
  have both near the middle. Quantiles (5/50/95%) of D: C 0.018/0.079/0.182; V(0.05) 0.023/0.091/0.212;
  V(0.077) 0.028/0.106/0.253; V(0.105) 0.036/0.126/0.304; O(δ̂) 0.088/0.282/0.572 [`quantiles_5_50_95`].
- **KDE density ratios at the observed point (reported, not decisive; `kde`).** O(δ̂) over V(0.05):
  8.2 in two dimensions (68% bootstrap interval 7.0–10.0; 7.3 with half the bandwidth), 10.2 in D alone;
  over V(0.077): 4.8 (4.3–5.4; 4.8), 4.2; over V(0.105): 5.4 (5.0–5.9; 5.6), 2.4; over C: 21 (17–32;
  12.4), 15.5. The observed point is more probable under the one-host model by factors of about 2–10
  against the diffuse models, but O(δ̂) has its offset fitted to these data, which favours it in any such
  ratio, the tail densities depend on the bandwidth, and no rule uses these ratios.
- **Against the expectation stated in section 2.** As expected: the calibrated p_J is much larger than
  the raw quadrant probability (V(0.05): 0.039 against 0.0025; V(0.077): 0.080 against 0.0048), and it
  lies above 0.05 for V(0.105). Section 2 said p_J "may stay below 0.05 for V(0.05) and V(0.077)": it did
  for V(0.05) (0.039) but not for V(0.077), which came out above (0.080, interval 0.072–0.088), and this
  is what makes the reading rule (3) rather than rule (2); D excludes V(0.05) and not V(0.105); O(δ̂)
  is excluded by neither. Section 2 thought "undetermined" or "not excluded" as likely as "excluded" for
  D under V(0.077); the outcome is "excluded (D)" (interval 0.030–0.038). Section 2 thought rule (3) most
  likely through τ = 0.105; it holds through both 0.077 and 0.105. The direction of p_J in τ was left
  open: p_J is not monotone (0.039, 0.080, 0.068 for τ = 0.05, 0.077, 0.105).
- **Proxy comparison with the referee (reported).** P(D_proxy ≥ 0.2804) = 0.0056 under C, 0.0166 under
  V(0.05), 0.0363 under V(0.077) (`D_proxy.share`), against the referee's 0.006, 0.019 and 0.036 on other
  seeds: agreement within Monte Carlo error. The referee's joint-event 0.002 under both V corresponds to
  Q_raw 0.0025 and 0.0048 here; once calibrated (p_J), V(0.077) is not excluded.
- **Caveats (from the addendum).** δ̂ is fitted on the same data and N5584 was identified post hoc; J's
  quadrant is anchored at a point chosen after seeing the data (calibrated, but chosen post hoc); the
  three τ values were also chosen from these data (R2-RE's τ̂ and its 68% interval) and each is treated
  as fixed, so no statement is made about a range of τ; the union in rule (3) is not corrected for three
  looks (a correction would only make exclusion harder); the labels share ε_s and are correlated; every
  model takes the public C as correct (R2-RE-SEL referee, point 5).
- **Post hoc (referee, 2026-11-21; section 6, points 1, 2 and 4; recounts from the saved per-simulation
  files, no new simulation).** (i) *Halves swapped.* J's interval holds half A fixed; calibrating on the
  odd simulations and testing the even ones gives p_J = 0.061 for V(0.05) (recorded 0.039), 0.077 for
  V(0.077) (0.080), 0.070 for V(0.105) (0.068) and 0.016 for C (0.017). The reading turns on V(0.077)
  and V(0.105), which are stable under the swap; V(0.05)'s exclusion by J is not. (ii) *Power.* With
  each V's own calibration at α = 0.05, if O(δ̂) is true J excludes V(0.077) in 54% and V(0.105) in 57%
  of simulations (D: 57% and 45%); if O_any is true, in only 20–30% (J; D 10–15%). The comparison is therefore
  underpowered (about 50%) against its own one-host alternative: "not excluded" is a null result that
  carries little information, not evidence for diffuse scatter. (iii) *What J measures.* J is not
  specific to one outlier: under C, P(spread_37 ≥ obs) = 0.013 against p_J = 0.017, so part of J's
  exclusion of V(0.05) is "too much total scatter". D is the sharper shape statistic. Next to the
  reading, which is unchanged: V(0.05) is excluded by both statistics and V(0.077) by D. The labels and
  the reading stay as pre-registered; these points change only how they are read.
- **Runtime.** Block 3,961 s (66 min), below the 1.2–1.8 h estimate: 37-host rows 112 s, observed
  values and N5584's reduced system 103 s, τ̂_N 22 s, five Cholesky factors 1.9 s, pass 1 52 s, pass 2
  (with the other 36 reduced systems) 3,668 s, statistics and KDE 2 s (`seconds`).

### R2-RE-G (addendum 2026-11-21, T-055)

Run of 2026-11-21 in two stages, standalone mode (`g_check` and `g_only` true; `g_stage` "power", then
"full"; set back to false, false and "full" afterwards), single-threaded, cache only, no data downloaded.
Power stage 764 s, committed with its power line in `log.md` before the full stage; full stage 797 s.
Numbers: `results/r2_re_g.json` (`results/r2_re_g_power.json` for the power record).

**Checks (rule (1)).** All passed (`rule1` empty): τ̂_obs = 0.0766988, δ̂ = 0.33634, σ_δ = 0.09252,
z_obs = 3.6354 reproduced (REML grid to 1.0 × 10⁻¹¹; W·y against the 37 one-column GLS fits to
1.5 × 10⁻¹²); M has rank 36 of 37 (one eigenvalue clipped, as expected: a common shift of all
calibrator hosts is degenerate with H0); every pointwise check passed; no Cholesky factor failed; the
full stage reproduced every count and `k_sha256` of the power stage.

**Power and size (fixed before G was read).** Power = min(R_OANY 0.535, R_OANYVN 0.491) = **0.491**, below
0.8. Size at the three τ: R_VHAT 0.048 (95% interval 0.044–0.052), R_V050 0.045 (0.041–0.049), R_V105
0.048 (0.044–0.053); none anti-conservative. Power curve (O_any on C): z_alt 2.5 → 0.19, 3 → 0.32,
4 → 0.65, 4.5 → 0.797, 5 → 0.90; the smallest z with power ≥ 0.8 is 5.0. With z_obs − 1 (reported) the
power is 0.22.

**Observed.** G_obs = 0.305: N5584's z = 3.64 carries 30% of Σ_j z_j² = 43.4 (next |z|: N1365 −2.33,
N3982 −2.03). Under V(τ̂_obs), p_G = (1 + 326)/(1 + 20,000) = **0.016** (0.015–0.018), label "excluded"; at fixed τ:
0.013 (τ = 0.05), 0.023 (0.105), 0.011 (C), all "excluded". Double-bootstrap check p_dbl = 0.016. Reverse
p (how typical the data are of one σ-matched offset host): 0.62 under O_any, 0.62 under O(δ̂). The
joint fit with all 37 offsets is rank deficient, as expected (reported, not used).

**Reading (rule (2)): "undetermined (underpowered)"**, with the sub-label "diffuse excluded; test
underpowered against the σ-matched alternative". As fixed in the addendum (reading (2)): no powered shape
test separates one offset host from diffuse host scatter on these data (power 0.49, size ≤ 0.048, power
≥ 0.8 only from z ≈ 5). R2-RE-D's reading and gloss stay as recorded, and R2-RE's row stays the headline.
The sub-label says the concentration of the calibrator offsets in one host is unusual under Gaussian
diffuse scatter of the fitted size (and at τ = 0.05 and 0.105), and the data look typical of one offset
host; it is not a separate reading, and it is not independent of R2-RE-D (referee, section 6). Gloss from
R2-RE-GT (T-057, next subsection): "t₄ comparison undetermined (Monte Carlo)".

**As expected.** The addendum forecast G_obs ≈ 0.2–0.35, power ≈ 0.2–0.6 and "undetermined
(underpowered)" as the most likely reading; all three held.

### R2-RE-GT (addendum 2026-11-21, T-057)

Run of 2026-11-22 in two stages, standalone mode (`gt_check` and `gt_only` true; `gt_stage` "power", then
"full"; set back to false, false and "full" afterwards), single-threaded as R2-RE-G's formal run, cache only, no
data downloaded. Power stage 252 s, committed with its power line in `log.md` before the full stage; full stage
281 s. Numbers: `results/r2_re_gt.json` (`results/r2_re_gt_power.json` for the power record).

**Checks (rule (1)).** All passed (`rule1` empty): R2-RE-G's reproduction checks (τ̂_obs = 0.0766988, δ̂ = 0.33634,
σ_δ = 0.09252, z_obs = 3.6354; REML grid to 1.0 × 10⁻¹¹); the three pointwise checks of THAT (z to 2.9 × 10⁻¹²);
no Cholesky factor failed; VHAT, OANY and OANYVN reproduce R2-RE-G's saved G_s and τ̂_s in all 10,000 simulations
each (amendment 4); the full stage reproduced every count and `k_sha256` of the power stage; on the real data
W·y matches the 37 one-column fits to 1.5 × 10⁻¹², G_obs equals the recorded value exactly and R2-RE-G's Gaussian
inner draws give k = 326 again (amendment 6).

**Power and size (fixed before p_T,obs was computed).** Power = min(R_OANY 0.384, R_OANYVN 0.317) = **0.317**,
below 0.8. Size under t₄ host effects: R_THAT 0.046 (95% interval 0.042–0.050), R_T050 0.041 (0.037–0.045),
R_T105 0.044 (0.040–0.048); none anti-conservative. Reported: under C (no excess) the T test rejects 3.9% (TC), and
under R2-RE-G's Gaussian V(τ̂_obs) 2.1% (VHAT): conservative when the truth is Gaussian. Under THAT the 95th
percentile of G_s is 0.313 (median 0.163); under OANY the median G_s is 0.270, and ĵ_s is the offset host in
8,668 of 10,000 simulations.

**Observed.** G_obs = 0.305 (N5584, as in R2-RE-G). Under T(τ̂_obs), p_T,obs = (1 + 1,047)/(1 + 20,000) =
**0.052** (95% interval of k/N_in 0.049–0.056), which contains 0.05: label **"undetermined (Monte Carlo)"**.
Reported, not decisive (`sensitivities`; descriptive, only ν = 4 at the three checked τ has a size check):

| Inner null | p | Label |
|---|---|---|
| t₄ at τ̂_obs (decisive) | 0.052 (0.049–0.056) | undetermined (Monte Carlo) |
| t₃ at τ̂_obs | 0.074 (0.070–0.078) | not excluded |
| t₁₀ at τ̂_obs | 0.021 (0.019–0.023) | excluded |
| t₄ at τ = 0.05 | 0.025 (0.023–0.027) | excluded |
| t₄ at τ = 0.105 | 0.090 (0.086–0.094) | not excluded |
| t₄ with R2-RE-N5584's EM scale s = 0.0752 (variance 0.0113) | 0.092 (0.088–0.096) | not excluded |
| Gaussian at τ̂_obs (R2-RE-G, for comparison) | 0.016 | excluded |

**Reading (rule (2)): "undetermined (underpowered)"**, with the sub-label **"t₄ diffuse undetermined (Monte
Carlo)"**. R2-RE-G's sub-label "diffuse excluded" is glossed **"t₄ comparison undetermined (Monte Carlo)"**: the
data's concentration of the offsets in N5584 sits at the 5% point of what t₄ diffuse host scatter of the fitted size
produces, so whether R2-RE-G's sub-label rests on Gaussian tails alone is not decided by this test. The p value
moves across 0.05 with the tail weight (ν = 3 against ν = 10) and with the scale (τ = 0.05 against 0.105): the answer
depends on the tail weight and scale assumed for diffuse host scatter, which these data do not fix. The
"Monte Carlo" in the label is the registered wording; the Monte Carlo error of p_T,obs (about ±0.003) is small
against these model choices, so the result is limited by the null's tail and scale, not by the number of draws
(referee, section 6; a profile over ν and τ is T-060). All earlier verdicts, labels, readings and sub-labels stay
as recorded; R2-RE's row stays the headline, and `summary.json` `R2_host` and the claim's verdict are unchanged.

**As expected.** The addendum forecast a power of roughly 0.2–0.45 (0.317), "undetermined (underpowered)"
as the most likely reading (it is) and a p value of about 0.03–0.15 (0.052).

### R2-RE-GTP (addendum 2026-11-22, T-060)

Run of 2026-11-22, standalone (`gtp_check` and `gtp_only` true, set back to false afterwards), single-threaded as
R2-RE-GT, cache only: 1,736 s, of which 1,510 s for the 36 pointwise checks. A first attempt was refused before any
data was loaded by a bug in the preflight thread check (fixed; log.md). Numbers: `results/r2_re_gtp.json` and the 12
`results/r2_re_gtp_sims_<ν>_<τ>.json`. Reported, non-decisive: no verdict, label, reading, sub-label or gloss changes.

**Checks.** All passed: R2-RE-G's and R2-RE-GT's reproduction checks on the data; the eight recorded k (1,047, 501,
1,806, 1,476, 422, 326, 254, 453) recomputed exactly; the reused counts of R2-RE-GT's THAT/T050/T105 and R2-RE-G's
VHAT/V050/V105 equal their records; all 36 pointwise checks of the 12 new sets passed.

**Statement: "t-tail comparison: model-limited (p_fix from 0.0112 to 0.1211)"** (already determined by values seen
before the addendum, as disclosed there; the disclosed lower end 0.0127 was not the minimum: ν = 30 at τ = 0.05 gives
0.0112 on its own inner stream, within about 1.4σ of binomial noise of the Gaussian's 0.0127). The calibrated p values
span 0.015–0.078. No ν is flagged anti-conservative: the 18 sizes of the refitted test lie in
0.040–0.050, every Clopper–Pearson interval includes or lies below 0.05.

| ν | p_fix at τ = 0.05 / τ̂_obs / 0.105 | size of the refitted test (true τ = 0.05 / τ̂_obs / 0.105) | p_cal (same) |
|---|---|---|---|
| 3 | 0.037 / 0.074 / 0.121 | 0.040 / 0.044 / 0.042 | 0.071 / 0.077 / 0.078 |
| 4 | 0.025 / 0.052 / 0.090 | 0.041 / 0.046 / 0.044 | 0.046 / 0.050 / 0.051 |
| 6 | 0.017 / 0.032 / 0.055 | 0.042 / 0.045 / 0.048 | 0.028 / 0.030 / 0.030 |
| 10 | 0.013 / 0.021 / 0.036 | 0.045 / 0.047 / 0.050 | 0.020 / 0.021 / 0.022 |
| 30 | 0.011 / 0.016 / 0.025 | 0.047 / 0.046 / 0.046 | 0.018 / 0.017 / 0.015 |
| ∞ | 0.013 / 0.016 / 0.023 | 0.045 / 0.048 / 0.048 | 0.016 / 0.016 / 0.016 |

- p_fix labels: all "excluded" for ν ≥ 10 and ν = ∞; at ν = 6 "excluded" except τ = 0.105 ("not excluded", 0.055); at
  ν = 4 as recorded (0.025 excluded, 0.052 undetermined (Monte Carlo), 0.090 not excluded); at ν = 3 "excluded" only at
  τ = 0.05.
- **p_cal, the calibrated p value of the refitted plug-in test**, is at most 0.031 for every ν ≥ 6 (largest over the
  three true τ: 0.030, 0.022, 0.018, 0.016 for ν = 6, 10, 30, ∞), 0.051 at ν = 4 and 0.078 at ν = 3 (the largest of the
  18 values, not a composite-null p value; the grid is coarse and stops at ν = 3, so heavier tails would raise it
  further: the upper end is set by where the grid stops, not by the data). The cells share ε_s and, within a ν, the
  same t draws rescaled, so the flatness of p_cal across τ partly reflects these common random numbers.

**Reading (post hoc).** The answer to "does R2-RE-G's exclusion of diffuse scatter rest on Gaussian tails alone?"
depends on how heavy the tails are allowed to be: for host effects with ν ≥ 6 (including the Gaussian), the calibrated
test excludes diffuse scatter of R2-RE's size (p_cal ≤ 0.031) at every checked scale; at ν = 4 it is on the boundary
(0.05), and at ν = 3 it does not (0.08). These data (one value of G) cannot fix ν: under variance matching a t₃ draw puts most of the variance into a few
large host effects, close to the one-offset-host alternative. R2-RE-GT's sub-label "t₄ diffuse undetermined (Monte
Carlo)" stays as recorded; the profile adds that diffuse scatter is excluded unless the host effects are about as
heavy-tailed as t₄ or heavier (the crossover lies between ν = 4 and 6). The
refitted test is not anti-conservative anywhere on the grid (sizes 0.040–0.050). The headline (R2-RE) and every earlier
label stay as recorded. An outside constraint on ν (from host-level residuals not used in G) is registered as T-062.

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

### Referee, R2-RE-N5584 (independent subagent, 2026-11-18)

The referee saw README sections 1–4, the code and the results, not sections 5–8 or the log; it ran
offline checks from the cache. We reran its scripts (exact Student-t likelihood, z variants, partial
removals) and reproduced every number quoted below. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The variational EM's τ̂_T is biased high against the exact Student-t restricted likelihood (ν = 4: 0.075 against about 0.055; ν = 2: 0.068 against 0.035; ν = 10: 0.078 against 0.070); z depends on the plug-in definition: exact posterior mixture −1.47, E_post[τ²/w] −1.34, τ²/E_post[w] −1.67, EM with E_q[τ²/w] −1.15; ν = 2 variants −1.11 to −1.85; the pre-registered plug-in τ̂²/ω̂_j gives N5584 less variance than the model's own E_q[τ²/w] | yes (our rerun: same numbers; importance-sampling effective sample size ≥ 3,600, smallest 3,690 at ν = 2) | **Accepted limitation**, post hoc in section 5: the label "robust" holds in every variant (none reaches −2); z_T is reported with a method spread of about ±0.3. The pre-registered definition is kept. |
| 2 | Both pre-registered EM starts lie at or above the Gaussian τ̂, so they could not reveal a low-τ mode; from 0.01, 0.02, 0.031, 0.05 and 0.4 all starts converge to the same fixed point (τ 0.075219, N5584 ω 0.3925) | referee's check (not rerun) | Noted; no bug. |
| 3 | B-N simulates an unselected 36-host system, while N5584 was removed as the most extreme of 37; dropping the worst host in each simulation would shrink the null τ̂ and spread, so B-N's p values (0.34, 0.36) are biased upward, towards "attributable" | yes (argument; not computed) | **Accepted**; section 5 reads the label as "consistent with one outlying host"; a selection-aware null is registered as T-042. The pre-registered label stands. |
| 4 | The two treatments disagree about the other 36 hosts: removal gives τ̂_N = 0.031 (0–0.070), while the t model gives the others an effective scatter of about 0.074 | yes (`omega_ranked`) | Accepted; noted in section 5 (descriptive). |
| 5 | Dropping only N5584's SN rows (z = −1.68 under C; REML minimum near τ 0.03) is close to the full removal, so "the effect sits on the SN side"; its SN residuals are +0.25 to +0.35 mag | partly: the numbers reproduce, but dropping only its Cepheid rows gives z = −1.62 as well, since either removal leaves the host's offset unconstrained | **Inference rejected**; numbers recorded in section 5. The side is not identified by these data. |
| 6 | Literature: Riess et al. 2023 (arXiv:2307.15806) report N5584 about 0.25 mag from the sample mean, Cepheids bright for the SN's standardised magnitude, SN 2007af normal and low-reddening, a couple of such outliers expected; JWST–HST intercept difference 0.02 ± 0.03 mag; Javanmardi et al. 2021 (arXiv:2102.12489) μ = 31.810 ± 0.047 against SH0ES 31.786 ± 0.046; Anand et al. 2024 (arXiv:2401.04776) and Li et al. 2024 (arXiv:2408.00065) give only sample means | yes: 2102.12489 and the 2307.15806 JWST–HST numbers on the abstract pages (2026-11-18); the 2307.15806 full-text statements were read in the HTML version through a summary, not quoted | **Accepted** as context (section 5): the Cepheid side is supported by an independent reanalysis of the HST data and by the JWST–HST agreement, so SN 2007af being faint after standardisation is the likely reading; not used in any label. |
| 7 | No goalpost moved: every label and the joint reading re-derive from the saved numbers; EM updates, row removal (169 rows), R4-N mapping, B-N construction and the rule order are correct | yes (`test_conclusions.py`) | None. |

### Referee, R2-RE-SEL (independent subagent, 2026-11-20)

The referee saw README sections 1–4, the code and the results, not sections 5–8 or the log; it ran a
cache-only script (about 3 min) that rebuilt criterion S's subset rows and re-simulated seeds
20,000–21,999, reproducing the saved criterion-S choices and smallest spread_excl values exactly. We
reran that script and the τ split ourselves and reproduced every number quoted below. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | Rule (2) cannot tell one outlying host from diffuse host scatter: the null is C with no outlier; with the smallest spread_excl as a proxy (correlation 0.979 with the 36-host spread under S), a diffuse random effect V(τ) on all 37 hosts is rejected at 5% in only 21% (τ = 0.05) and 45% (τ = 0.077) of simulations, and the simulated post-selection value is at or below the real one in 66% and 39% (the real value is ordinary under V too). The drop D = spread_37 − min_j spread_excl_j (real 0.280) is rarer: P(D ≥ 0.280) = 0.006 under C (99th percentile 0.251), 0.019 under V(0.05), 0.036 under V(0.077); the joint event "spread_37 ≥ 1.307 and post-drop spread ≤ 1.027" has probability 0.002 under both diffuse models | yes (our rerun: same numbers; 2,000 simulations under C, 1,000 per V, seeds 50,000 +) | **Accepted** (post hoc): section 5 reads the label as "the 36 remaining hosts are consistent with C" and reports D as exploratory, pointing towards one outlying host without showing it (no single-outlier model was simulated; D partly restates the high 37-host spread); the pre-registered label stands. A pre-registered comparison of C, diffuse scatter and a single-host offset model is registered as T-048. |
| 2 | Criterion X hardly conditions the τ null: p is about the same whether X dropped N5584 (37 simulations) or another host (363); X mostly drops hosts with 3–4 calibrator rows (N5468, N5584, N5643 about 9% each; N3982, second by tail probability, 6 of 2,000), so the fall from 0.339 to 0.244 may come as much from the different 36-host systems as from selection | yes ((1 + k)/(1 + n): 0.263 and 0.245) | Accepted; this is the direction section 2 stated; noted in section 5. |
| 3 | The three labels are not independent: τ̂_s and spread_X correlate at 0.81 over the first 400 simulations; both spreads share the subset rows | yes (0.810) | Accepted; section 5 says so; rule (2)'s three labels are not three confirmations. |
| 4 | The history is not mimicked: N5584 was looked at because the 37-host spread was already high (ROB p = 0.021) and singled out by X, part A and S in sequence; but conditioning on a high simulated 37-host spread (top 10%, or ≥ 1.2) gives post-selection spread ≥ 1.033 in 82–89% of simulations, so conditioning would strengthen "consistent"; P(spread_37 ≥ 1.307) under C is 25 of 2,000; union selection was not simulated | yes (0.825 for the top 10%, 0.889 for ≥ 1.2) | Accepted limitation; does not change the reading. |
| 5 | Every test takes the public C as correct; a globally under-scaled calibrator SN block would shift all nulls together, and no block tests a global rescaling against a host term | argued | Accepted limitation; noted in section 7. |
| 6 | No code bug: leave-one-out maps (3.4 × 10⁻¹²), criterion S (1.0267; N5584 is outside 740 of the 1,000 subsets, 700–756 across hosts), observed values, subsets and seeds, sorted `rows_a` for the `searchsorted` calls, spread_X = spread_S where the criteria agree, REML on the reduced rows; the `sel_n_subsets` guard is an implementation guard (already stated in section 8) | yes | None. |
| 7 | No goalpost moved: every label and the reading re-derive from the saved counts; the outcome under S ("consistent", p = 0.137) is less extreme than section 2 thought plausible | yes | None; stated in section 5. |
| 8 | Literature: Feeney, Mortlock & Dalmasso 2018 (arXiv:1707.00007; abstract checked by the referee) model ladder outliers with non-Gaussian populations instead of cutting them (H0 72.72 → 73.15); Wojtak & Hjorth 2022 (arXiv:2206.08160, unverified by the referee) as a diffuse-scatter alternative; Efstathiou 2020 (arXiv:2007.10716) marginal | partly | Context only; not used in any label. |

### Referee, R2-RE-D (independent subagent, 2026-11-21)

The referee saw README section 2's R2-RE-D addendum and the earlier definitions it relies on, `onehost.py`,
the `d_*` paths of `run.py` and the results (`r2_re_d.json`, the per-model simulation files), not sections
5–7 or the log; it ran only short single-threaded checks on the saved files. It found no bug that
changes a statistic or a label. We recounted point 1 (halves
swapped) from the saved pairs and reproduced it (0.016, 0.061, 0.077, 0.070). Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | J's Clopper–Pearson interval holds half A fixed; swapping halves (calibrate on odd, test on even) gives p_J V(0.05) 0.061 (recorded 0.039), V(0.077) 0.077 (0.080), V(0.105) 0.070 (0.068), C 0.016 (0.017) | yes (post hoc recount from the saved simulations) | **Accepted**: V(0.05)'s J exclusion depends on the split and is not firm; the reading turns on V(0.077) and V(0.105), which are stable; reported in the results subsection (post hoc) |
| 2 | Low power both ways (post hoc, from the saved pairs, each V's own calibration, α = 0.05): if O(δ̂) is true, J excludes V(0.077) in 54% and V(0.105) in 57% of simulations (D: 57%, 45%); if O_any is true only 20–30% for J (D: 15% for V(0.077), 10% for V(0.105)); so "not excluded" carries little information | yes (post hoc recount) | **Accepted**: the results subsection and the headline places say the comparison is underpowered (about 50%) against its own alternative; it is a null result, not evidence for diffuse scatter |
| 3 | Plug-in parameters from the same data: δ̂ is the offset of the host already selected as most extreme (winner's curse), so O(δ̂) is nearly guaranteed not to be excluded; under O_any criterion S finds the offset host in 44% (4,358 of 10,000); τ̂ = 0.077 was fitted with N5584 included | yes | Accepted limitation (stated in the addendum's caveats); a composite test refitting δ or τ in each simulation is the clean fix |
| 4 | J is not specific to one outlier: under C, P(spread_37 ≥ obs) = 0.013 against p_J 0.017; part of J's exclusion of V(0.05) is "too much total scatter". D is the sharper shape statistic and excludes V(0.077) at 0.034 | yes | **Accepted**: next to the reading (unchanged), the results subsection reports that V(0.05) is excluded by both statistics and V(0.077) by D |
| 5 | Three fixed τ values are not a model family; the labels are correlated (shared ε_s) | – | Accepted; no statement about τ in general |
| 6 | C is taken as correct: an overall misscaling of the SN calibrator errors acts like V | – | Accepted limitation |
| 7 | O_any uses δ = 0.336 for hosts with different σ_δ: a weaker comparator than O, not matched in significance | yes | Noted |
| 8 | Monte Carlo precision adequate; tie handling immaterial (strict / mid-p: V(0.077) 0.0784 / 0.0792, V(0.105) 0.0652 / 0.0666) | yes | No action |
| 9 | Literature: Riess et al. 2023, JWST "Crowded No More" (arXiv:2307.15806: Cepheids in NGC 5584 agree with HST) bears on whether an N5584 offset is Cepheid crowding; Feeney, Mortlock & Dalmasso 2018 (arXiv:1707.00007, Student-t outlier likelihoods) is the natural intermediate model; others (Efstathiou 2020, Freedman et al. 2024, Uddin et al. 2023) | unverified (identifiers from the referee) | Noted |
| 10 | Most important additional test: a composite shape test with the statistic G = max_j z_j²/Σ_j z_j² (host-offset z-scores from the GLS under C), calibrated under V(τ) with τ refitted in each simulation and under O_any with σ-matched δ, with its power reported before the data are read | – | Registered as T-055 (new pre-registration) |

### Referee, R2-RE-G (independent subagent, 2026-11-21)

The referee saw the R2-RE-G addendum and the definitions it relies on, `shape.py`, the `g_*` paths of
`run.py`, `test_shape.py`, the conclusion checks and the results files, not sections 5–7 or the log; it
ran only short single-threaded checks on the saved files. It found no bug that could change G_obs, p_G,
the power, the size or the reading, and reproduced p_G (P(G_s ≥ G_obs) = 0.0162 under VHAT), the
near-uniform calibration of p_boot under VHAT (0.0101, 0.0505, 0.1028 at 0.01, 0.05, 0.1) and the GLS
algebra. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | Bookkeeping: at the time of review `run.py` PARAMS still read `g_check` true, `g_only` true; a plain full run would redo the power stage | yes | **Fixed**: set back to false, false, "full" with a log note; the values used are stored in `r2_re_g.json` `settings` |
| 2 | The null is a Gaussian random effect: "diffuse excluded" means Gaussian diffuse scatter is excluded; heavy-tailed diffuse scatter (e.g. Student-t, ν = 4, as R2-RE-N5584 used) also concentrates G and is not in the null family | yes (`shape.py` simulation of V(τ)) | **Accepted**: section 5 says "Gaussian"; a t₄ null for G is registered as T-057 |
| 3 | The statistic was proposed after R2-RE-D, -ROB, -N5584 and -SEL had all singled out N5584; the maximum over 37 hosts removes host choice, not statistic choice; p_G is correlated with R2-RE-D's p_D and p_J, so the sub-label is not a fresh detection; p_rev 0.62 says the data are typical of one offset host, but rule (2) declines to decide | yes | **Accepted**; stated in section 5 |
| 4 | σ-matching to z_obs, the maximum of 37, makes the power optimistic (z_obs − 1 gives 0.22) | yes | Accepted; reinforces "underpowered" |
| 5 | C: host-specific errors in C move G; N5584's four calibrator rows (duplicate light curves of SN 2007af) give σ_δ = 0.093, close to single-row hosts, so no sign that z is inflated by under-correlated duplicates. JWST Cepheids in N5584 agree with HST (0.02 ± 0.03 mag; Riess et al. 2023), so a real offset would point to the SN side or chance | partly (σ_δ values in `r2_re_g.json`); the JWST number was verified 2026-11-18 (R2-RE-N5584 referee notes, row 6) | Noted (interpretation, open question) |
| 6 | Size is checked at three τ only, as pre-registered; no τ̂ reached the REML grid's upper bound | yes (`n_tau_bound` 0 in every set) | No action |
| 7 | Literature: Riess et al. 2023 (arXiv:2307.15806), Riess et al. 2024 (arXiv:2401.04773), Feeney, Mortlock & Dalmasso 2018 (arXiv:1707.00007), Cardona, Kunz & Pettorino 2017 (arXiv:1611.06088), Follin & Knox 2018 (arXiv:1707.01175), Efstathiou 2020/2021, Wojtak & Hjorth 2022, Uddin et al. 2023, Murakami et al. 2023 | unverified except arXiv:2307.15806 (abstract checked 2026-11-18; R2-RE-N5584 referee notes, row 6) | Noted |
| 8 | Most important additional test: calibrate G under a heavy-tailed diffuse null (host effects t_ν, ν = 4, scale fitted) next to a matched one-offset alternative | – | Registered as T-057 |

### Referee, R2-RE-GT (independent subagent, 2026-11-22)

The referee saw the R2-RE-GT addendum with its amendments, the R2-RE-G addendum it builds on, `shape.py`
(the R2-RE-GT block and the R2-RE-G functions it calls), the `gt_*` paths of `run.py`, `test_shape.py`, the
conclusion checks, the results files and the power line in `log.md`, not sections 5–7; it ran only short checks on
the saved files. It found no code or statistics bug: the t scale gives Var(b) = τ² for every ν, inner and outer
draws have the same covariance, rules (1)–(5) run in the registered order, the power stage was committed before
the full stage, `shape.py` is unchanged since the code review, and the label follows from the numbers. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | "Monte Carlo" in the sub-label names the wrong source of uncertainty: the Monte Carlo error of p_T,obs is about ±0.003, while ν (0.021–0.074) and τ or the scale (0.025–0.092) move it far more; more inner draws would only settle the ν = 4 plug-in value | yes (`sensitivities`) | **Accepted**: the registered label stands; section 5 says the result sits on the 0.05 boundary and that the answer depends on the tail weight and scale, which the data do not fix |
| 2 | The registered variance matching gives s = 0.054; the t₄ likelihood fit of R2-RE-N5584 gives s = 0.075 (host variance 1.9 τ̂²) and p = 0.092, "not excluded". REML τ̂² is unbiased for Var(b) on average (mean τ̂_s² 0.00600 against 0.00588 in THAT), but a t₄ fit prefers a wider distribution | yes (`sensitivities.em_scale`; THAT sims) | **Accepted**; reported next to the sub-label in section 5 (table); the registered choice stands |
| 3 | The plug-in test is calibrated on average over τ̂ but not conditionally: in THAT the rejection rate is 6.1% at τ̂ = 0, 5.1% at 0.001–0.05, 3.4% at 0.05–0.08, 2.8% at 0.08–0.11 and 9.1% above 0.11 (label "excluded"; with p_s < 0.05 instead 6.2, 5.6, 3.6, 3.1 and 9.8%); the data (τ̂ = 0.077) sit in the conservative range, and one large t draw inflates τ̂ and G together | yes (THAT sims, by τ̂_s bins; our recomputation agrees) | **Accepted limitation**: the size (max 0.046) is honest as registered; conditional on τ̂ near the data's the test is conservative, which pushes p_T,obs up, not down |
| 4 | Calibrated checks from the committed sims agree with the plug-in: P(k_s ≤ k_obs) = 0.050 in THAT (T050 0.046, T105 0.051); P(G_s ≥ G_obs) = 0.056 (T050 0.027, T105 0.093) | yes (recomputed) | Noted: supports "on the boundary" at ν = 4 and τ ≈ τ̂_obs, and again a factor of about 3 across τ |
| 5 | With power 0.317 against an offset as large as observed, and τ̂ absorbing the offset under OANY (median 0.066 at a true diffuse τ = 0), "not excluded" or "undetermined" carries almost no weight against one offset host | yes (`models.OANY.quantiles_5_50_95.tau_hat`) | **Accepted**; this is reading (2), "undetermined (underpowered)", as forecast |
| 6 | Under Gaussian truth the t₄ test rejects 2.1% (VHAT) and under C 3.9% (TC): it gives up about half its level | yes | Noted; expected (section 5) |
| 7 | The size is checked only at ν = 4 and three τ; under a supremum-p convention over ν ≥ 3 and τ in [0.05, 0.105] p ≥ 0.09, "not excluded"; ν = 4 was taken from R2-RE-N5584 after G_obs was known (disclosed) | yes | **Accepted**; the sensitivities are reported as descriptive, as registered |
| 8 | Minor: all T models share t_s and all p values share one T_in (rates correlated, size conditional on T_in); sims files 0.34–0.41 MB | yes | No action |
| 9 | Literature on heavy-tailed or outlier treatment in the ladder (Efstathiou 2014, arXiv:1311.3461; Cardona, Kunz & Pettorino 2017, arXiv:1611.06088; Feeney, Mortlock & Dalmasso 2018, arXiv:1707.00007, Student-t tails with H0 fairly insensitive; Follin & Knox 2018, arXiv:1707.01175; Efstathiou 2020, arXiv:2007.10716; Mörtsell et al. 2022, arXiv:2105.11461; Wojtak & Hjorth 2022, arXiv:2206.08160; Freedman et al. 2024, arXiv:2408.06153); none singles out N5584 | no; the IDs were given by the referee from memory, unverified (Wojtak & Hjorth 2022 is cited in section 7) | Noted; not used |
| 10 | Most important additional test: profile p_T,obs and its size over ν (3, 4, 6, 10, 30, ∞) and τ across τ̂_obs's REML interval with the existing machinery, reporting the supremum p next to the plug-in value (about 10–20 min) | – | Registered as T-060 (backlog), a reported, non-decisive sensitivity |

### Referee, R2-RE-GTP (independent subagent, 2026-11-22)

The referee saw the R2-RE-G, R2-RE-GT and R2-RE-GTP addenda with their amendments, `shape.py`, the `gtp_*` path of
`run.py`, the tests and the results files, not sections 5–7. It re-derived all 18 p_cal counts from the saved k_s and
found them equal to the record, checked the streams, the variance matching and the ν = ∞ path, and found no bug that
changes a reported number. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | "Model-limited" is close to true by construction: under variance matching a small ν puts the variance into a few large host effects, close to the one-offset-host alternative, and one G value cannot measure ν. The grid stops at ν = 3, so the upper end (p_fix 0.121, p_cal 0.078) is set by where the grid stops, not a bound | yes | **Accepted**; section 5 says so and states the conditional reading (excluded for ν ≥ 6, not for ν ≤ 3–4) |
| 2 | The statement's range uses p_fix; the calibrated range (0.015–0.078) should stand next to it, since p_fix at ν = 3, τ = 0.105 is a simple-null p above the data's τ̂ | yes | **Accepted**; both ranges given in section 5 (the registered statement is unchanged) |
| 3 | The addendum's "already known" lower end (0.0127) was not the minimum: ν = 30, τ = 0.05 gives 0.0112 on its own inner stream (about 1.4σ of binomial noise); p_fix is not monotone in ν at that level | yes | **Accepted**; corrected in section 5 |
| 4 | The size is that of the label "excluded" (upper Clopper–Pearson bound below 0.05, effective level about 0.047), so the anti-conservative flag could miss a test rejecting slightly above 0.05 at nominal p < 0.05; the observed sizes (0.040–0.050) and p_cal ≈ p_plug show no miscalibration | yes | Noted (as registered for R2-RE-GT) |
| 5 | The cells share ε_s and, within a ν, the same t draws rescaled: the flatness of p_cal across τ is partly common random numbers, not replication | yes | **Accepted**; stated in section 5 |
| 6 | The thread check now compares only the libraries present in both snapshots (weaker than before); no effect here, as all eight recorded k reproduced exactly | yes | Noted (it is R2-RE-GT's own comparison) |
| 7 | Literature: Feeney, Mortlock & Dalmasso 2018 (arXiv:1707.00007; abstract checked by the referee), Riess et al. 2022 (arXiv:2112.04510), Efstathiou 2020 (arXiv:2007.10716), Wojtak & Hjorth 2022 (arXiv:2206.08160), Freedman et al. 2019 (arXiv:1907.05922), Anand et al. 2022 (arXiv:2108.00007); none estimates ν for host-level offsets | the first by the referee; the others unverified | Noted; not used |
| 8 | Most important additional test: constrain ν from outside the 37 G-defining hosts (for example Cepheid−TRGB distance differences of shared hosts, or leave-N5584-out residuals) and report p_cal integrated over that ν (and τ) | – | Registered as T-062 (backlog) |

## 7. Open questions

- Why the public `lstsq_results.txt` differs from the printed baseline (a later or variant fit).
- How the 2024 data (SMC anchor, more Cepheids) change the host shift; not public as matrices.
- Does C understate host-to-host scatter? Answered by R2-RE (2026-11-16): a host-level random
  effect of 0.077 mag (0.048–0.105) brings the random-subset spread of Δ/σ from 1.33 to 1.005; its
  physical origin is open: it measures the host-level scatter of SN-based minus Cepheid-based
  distances beyond C and cannot say which side causes it; calibrator-specific SN colour behaviour
  (Wojtak & Hjorth 2022) is one candidate; whether C's calibrator block already holds a within-SN
  term is unchecked. Robustness of τ̂ to single hosts and its null distribution: T-032 (answered:
  the excess is consistent with one outlying host, N5584; R2-RE-N5584, T-039; also with the selection
  of the most extreme host simulated, R2-RE-SEL, T-042, a test with little power against diffuse host
  scatter; T-048: these data do not distinguish one outlying host from diffuse host scatter of
  R2-RE's size, a comparison with about 50% power, R2-RE-D, 2026-11-21).
- Is N5584's offset (effective scatter 0.12 mag under the heavy-tailed model) from its single SN,
  2007af, or from its Cepheid distance? The data cannot tell (section 6); the literature favours the SN
  (an independent Cepheid reanalysis agrees with SH0ES). A published per-host TRGB or JAGB distance for
  N5584 would decide it.
- Does "attributable to N5584" survive a null that also selects the most extreme host? Answered by
  R2-RE-SEL (2026-11-20, T-042): with the selection simulated the 36-host scatter is still ordinary
  under C (p = 0.24 for τ̂ under criterion X; 0.24 and 0.14 for the spread under X and S), so the
  reading is "consistent with one outlying host, selection included"; the τ part has no aligned
  criterion. The test has little power against diffuse host scatter (referee, post hoc); is the excess
  one outlying host or scatter spread over all hosts? A post-hoc spread-drop statistic points towards
  one host but no single-outlier model was simulated; a pre-registered comparison is T-048.
  Answered by R2-RE-D (2026-11-21, T-048): **not distinguished**. Diffuse host scatter with τ = 0.077
  and 0.105 mag is not excluded by the calibrated joint statistic J (p_J = 0.080, 0.068), nor is one
  host (N5584) offset by δ̂ = 0.34 mag (p_J = 0.68, by construction); only the smallest diffuse model,
  τ = 0.05, is excluded (p_J = 0.039, not firm under a swap of J's halves; p_D = 0.016). Reading
  "tested diffuse model(s) not excluded (τ = 0.077, 0.105)", an underpowered null: the comparison
  has about 50% power against its own one-host alternative (referee, post hoc). Open: a composite shape
  test (G = max_j z_j²/Σ_j z_j², τ refitted in each simulation, σ-matched O_any, power fixed before the
  data are read; T-055; answered by R2-RE-G, 2026-11-21: "undetermined (underpowered)", power 0.49,
  with the sub-label that Gaussian diffuse scatter is excluded, p_G 0.016, not independently of
  R2-RE-D; next bullet); outside the spreads, an independent distance to N5584 (previous question) would
  show whether its offset is real.
- Is the calibrator SN block of C globally under-scaled? Every null in this study takes C as given
  (R2-RE-SEL referee, point 5).
- A Cepheid-only per-host comparison for R3 (μ from fits without each host's SN rows).
- R4 suggests the CCHP selection is a low but ordinary draw: is there a property of those hosts
  (for example the TRGB-friendly, low-extinction halos) that correlates with their SN magnitudes?
- Is the one-host picture distinguishable from heavy-tailed diffuse host scatter? R2-RE-G (T-055)
  excludes Gaussian diffuse scatter (p_G 0.016; a sub-label, not independent of R2-RE-D) but is
  underpowered (0.49) and its null is Gaussian; a
  Student-t (ν = 4) diffuse null for G is registered as T-057. Answered by R2-RE-GT (2026-11-22, T-057):
  **not decided**. Under t₄ diffuse scatter of the fitted size p_T,obs = 0.052, with a Monte Carlo interval
  (0.049–0.056) that contains 0.05, and the test is underpowered (0.317); the p value moves across 0.05 with the
  tail weight (ν = 3: 0.074; ν = 10: 0.021) and the scale (τ = 0.05: 0.025; 0.105: 0.090). So whether R2-RE-G's
  sub-label rests on Gaussian tails alone stays open; these data do not fix the tail of diffuse host scatter.
  Profiled by R2-RE-GTP (2026-11-22, T-060): "model-limited". Post hoc and conditional on ν: the calibrated p is at
  most 0.031 for host effects with ν ≥ 6 (Gaussian included), 0.051 at ν = 4 (Monte Carlo-undetermined) and 0.08 at ν = 3, so diffuse scatter is
  excluded unless the tails are about as heavy as t₄ or heavier (three checked τ only); the question stays open until ν
  is constrained from outside G (T-062). If
  an offset is real, JWST Cepheids in N5584 (Riess et al. 2023) point to the SN 2007af side or chance.

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
| `sel_check`, `sel_seed_base`, `sel_n_tau`, `sel_n_spread`, `sel_n_subsets`, `sel_max_failed` | run R2-RE-SEL (selection-aware null, addendum 2026-11-19; needs `n5584_check`); seed base of ε_s, simulations in the τ part and the spread parts, subsets per spread, failed REML fits allowed | true/false; 20,000 (pre-registered; seeds overlapping 10,000–11,999 would repeat ROB's simulations); 400 and 2,000 are the pre-registered counts (smaller values only for a quick look, about 20 s per τ simulation); 1,000 (must equal `rob_n_subsets`: otherwise the block stops before any simulation with a configuration status, an implementation guard, not one of the addendum's rules); 20 | cache only |
| `d_check`, `d_seed_base`, `d_n_sims`, `d_taus`, `d_host_seed_base`, `d_kde_boot`, `d_only` | run R2-RE-D (one outlying host or diffuse host scatter, addendum 2026-11-21; module `onehost.py`); seed base of ε_s (common to all eight models), simulations per model, the τ of the diffuse models V(τ) (mag), seed base of O_any's offset host, bootstrap resamples of the KDE ratios, standalone mode | true/false (default true: a full run, or a full exploration without `d_only`, adds about 1.5 h; `--set d_check=false` skips the block); 100,000 and 200,000 (pre-registered; must not overlap 0, 10,000–11,999, 20,000–21,999 or 50,000–50,999); 10,000 (pre-registered; J's halves A/B are the even/odd simulations, so use an even number; about 1.5 h for the block, of which about 68 min build the reduced systems, so a quick look with `--set d_n_sims=200` still takes most of an hour); [0.05, 0.077, 0.105] (pre-registered; the reading's wording names the three values); 200; `d_only=true` runs only this block (cache only, about 1.5 h): it writes `r2_re_d.json`, the eight `r2_re_d_sims_<model>.json`, `provenance_d.json`, `run_info_d.json` and the `R2_RE_D` key of `summary.json` (every other key kept byte-identical; it refuses to run without an existing `summary.json`, except in an exploration, where it writes a summary with that key only). The block needs `n5584_check` (with it false, a full run records the block as "not run") and uses `rob_n_subsets` subsets and `n5584_host`; an index stream shorter than `rob_n_subsets` makes the whole block "not evaluable" (an implementation guard, added 2026-11-21 before any run; it cannot fire in a full run, where R4 keeps at least 2,000 draws); the recorded values (spreads, criterion S, δ̂, τ̂_N) and tolerances are constants in `onehost.py` | cache only |
| `g_check`, `g_seed_base`, `g_host_seed_base`, `g_inner_seed`, `g_n_sims`, `g_n_inner`, `g_power_min`, `g_z_curve`, `g_taus_rep`, `g_max_minutes`, `g_min_sims`, `g_only`, `g_stage`, `g_rerun_reason` | run R2-RE-G (composite shape test G = max_j z_j²/Σ_j z_j², addendum 2026-11-21, T-055; module `shape.py`); seed bases of ε_s (common to all 13 sets), of O_any's offset host and of the fixed inner matrix; outer simulations per set (with the runtime guard's floor), inner draws per p_boot, the power threshold, the power curve's z_alt, the two checked τ besides τ̂_obs (mag), the guard's limit (min) and floor, standalone mode and its stage, the reason for rerunning a formal full stage | `g_check` false (default until the formal stages; before the formal two-stage run `g_check=true` is accepted only with `g_only=true`, afterwards it also runs the block in a full run, adding about 35 min); 400,000, 500,000 and 600,000 (pre-registered; must not overlap 0, 10,000–11,999, 20,000–21,999, 50,000–50,999, 100,000–109,999, 200,000–209,999 or 300,000–300,199); 10,000 (pre-registered; floor 5,000; about 4 ms per simulation and set, so an exploration with `--set g_check=true g_only=true g_stage=power g_n_sims=200` takes about 7 min, most of it the pointwise checks); 20,000 (part of the test: do not change); 0.8; [2.5, 3.0, 4.0, 4.5, 5.0]; [0.05, 0.105]; 120; 5,000; `g_only=true` with `g_stage="power"` writes only `r2_re_g_power.json` (with `provenance_gp.json`, `run_info_gp.json`), with `g_stage="full"` it needs that file, recomputes it and writes `r2_re_g.json`, the eight `r2_re_g_sims_<model>.json`, `provenance_g.json`, `run_info_g.json` and only the `R2_RE_G` key of `summary.json` (every other key byte-identical); `g_rerun_reason` "" (a `g_only` full stage over an existing full-stage outcome needs a non-empty reason also present in log.md); until the formal `r2_re_g.json` is committed, an exploration may only run the power stage (`g_only=true`, `g_stage="power"`; a full stage or a full-study exploration with `g_check=true` is refused) and exploration scripts must not compute G, Σz² or other hosts' z_j on the data; afterwards an exploration's full stage runs both stages. Both stages must run with the same thread settings (`OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS`) and the same `g_*` values, else the full stage stops with an error. The recorded τ̂_obs, δ̂, σ_δ, z_obs, τ̂_N and the tolerances are constants in `shape.py`; the REML grid comes from `results/r2_re.json` | cache only |
| `gt_check`, `gt_only`, `gt_stage`, `gt_seed_base`, `gt_inner_seed`, `gt_inner_seeds_rep`, `gt_nu`, `gt_nu_rep`, `gt_n_sims`, `gt_n_inner`, `gt_power_min`, `gt_max_minutes`, `gt_min_sims`, `gt_rerun_reason` | run R2-RE-GT (the shape test G against Student-t diffuse host scatter, addendum 2026-11-21, T-057; the R2-RE-GT block of `shape.py`; reuses `g_seed_base`, `g_host_seed_base`, `g_inner_seed` and `g_taus_rep`); standalone mode and its stage; seed base of the t host draws t_s (common to the T models), seed of the fixed inner matrix T_in and of the ν sensitivities' T_in; ν of the null and of the sensitivities; outer simulations per set (with the runtime guard's floor), inner draws per p_T, the power threshold, the guard's limit (min) and floor, the reason for rerunning a formal full stage | `gt_check` false (default until the formal stages; before the formal two-stage run `gt_check=true` is accepted only with `gt_only=true`, afterwards it also runs the block in a full run, adding about 20 min); `gt_only` false, `gt_stage` "full"; 410,000, 610,000 and [611,000, 612,000] (pre-registered; must not overlap R2-RE-G's list, 400,000–409,999, 500,000–509,999 or 600,000); 4 and [3, 10] (pre-registered; the labels name t_ν); 10,000 (pre-registered; floor 5,000; about 3 ms per simulation and set, so an exploration with `--set gt_check=true gt_only=true gt_stage=power gt_n_sims=200` takes about 6 min, most of it data loading and the pointwise checks); 20,000 (part of the test, and R2-RE-G's k = 326 check needs it: do not change); 0.8; 120; 5,000; `gt_only=true` with `gt_stage="power"` writes only `r2_re_gt_power.json` (with `provenance_gtp.json`, `run_info_gtp.json`), with `gt_stage="full"` it needs that file, recomputes it and writes `r2_re_gt.json`, the seven `r2_re_gt_sims_<model>.json`, `provenance_gt.json`, `run_info_gt.json` and only the `R2_RE_GT` key of `summary.json` (every other key byte-identical); `gt_rerun_reason` "" (a `gt_only` full stage over an existing full-stage outcome needs a non-empty reason also present in log.md); until the formal `r2_re_gt.json` is committed, an exploration may only run the power stage and exploration scripts must not compute p_T on the data; afterwards an exploration's full stage runs both stages. Both stages need R2-RE-G's committed `r2_re_g_sims_{VHAT,OANY,OANYVN}.json` (their G_s and τ̂_s must be reproduced), must run with the same thread settings and `gt_*` / reused `g_*` values, and a formal stage must run with R2-RE-G's recorded thread settings (one thread), else it stops with an error. The recorded G_obs, k = 326 and the EM scale are constants in `shape.py` | cache only |
| `gtp_check`, `gtp_only`, `gtp_nus`, `gtp_t_seeds`, `gtp_inner_seeds`, `gtp_n_sims`, `gtp_rerun_reason` | run R2-RE-GTP (the profile of R2-RE-GT over ν and τ, addendum 2026-11-22, T-060; the R2-RE-GTP block of `shape.py`; reuses `gt_nu`, `gt_inner_seed`, `gt_nu_rep`, `gt_inner_seeds_rep`, `gt_n_inner`, `g_seed_base` and `g_inner_seed`); standalone mode; the ν grid; the outer t_s seed bases of the new ν; the inner T_in seeds of ν = 6 and 30; outer simulations per (ν, τ); the reason for rerunning a formal outcome | `gtp_check` and `gtp_only` false (true together only for the formal run, or for an exploration after the formal `r2_re_gtp.json` is committed; `gtp_check` outside `gtp_only` is refused: the block never runs in a full study run, which copies `R2_RE_GTP` from `r2_re_gtp.json`); [3, 4, 6, 10, 30, "inf"], {3: 430,000, 6: 440,000, 10: 450,000, 30: 460,000}, {6: 613,000, 30: 614,000} and 10,000 (pre-registered; ν = 4 and ∞ reuse R2-RE-GT's and R2-RE-G's committed simulations of 10,000, so `gtp_n_sims` must equal that); `gtp_rerun_reason` "" (a formal rerun over an existing outcome needs a non-empty reason also present in log.md). Writes `r2_re_gtp.json`, the 12 `r2_re_gtp_sims_<ν>_<τ>.json` (ν = 3, 6, 10, 30), `provenance_gtpp.json`, `run_info_gtpp.json` and only the `R2_RE_GTP` key of `summary.json`. A formal run must use R2-RE-GT's thread settings (one thread) | cache only |
| `nu_check`, `nu_only`, `nu_stage`, `nu_grid`, `nu_tau_gate`, `nu_group_corr`, `nu_group_corr_sens`, `nu_q_prior_frac`, `nu_n_is`, `nu_n_is_escalate`, `nu_is_seed`, `nu_is_seed_escalate`, `nu_n_mocks`, `nu_n_is_mock`, `nu_cut_sigma`, `nu_cut_attempts`, `nu_mock_seeds`, `nu_profile_m`, `nu_profile_seed`, `nu_vbase_seed`, `nu_group_sens_seed`, `nu_rerun_reason` | run R2-RE-NU (an outside constraint on the tail weight ν from the Hubble-flow supernovae, addendum 2026-11-24, T-062; module `nu.py`); standalone mode and its stage; the ν grid; Stage 1's gate (mag); the SN grouping's correlation threshold and its sensitivity; the prior fraction of the defensive proposal; importance draws per stream and after an escalation, and their seed bases; mocks per injection and draws per mock; the truncation cut (σ) and attempts; the mock seeds; the profile's multiples of τ̂_HF and its seed base; the seed bases of the V(τ̂_obs)-base and the 0.45-grouping sensitivities; the reason for rerunning a formal outcome | `nu_check` and `nu_only` false, `nu_stage` "check" (true together only for the formal runs, first with `nu_stage` "check", then "full", or for an exploration after the formal `r2_re_nu.json` is committed: before it, nothing may be computed from the Hubble-flow rows of y, and an exploration is refused; `nu_check` outside `nu_only` is refused: the block never runs in a full study run, which copies `R2_RE_NU` from `r2_re_nu.json`); every other `nu_*` value as pre-registered ([3, 4, 6, 10, 30, "inf"], 0.02, 0.3, 0.45, 0.1, 4,000, 32,000, 730,000, 740,000, 200, 2,000, 3.5, 100, the seed dictionary of the addendum, [0.5, 0.75, 1, 1.5, 2], 770,000, 820,000, 830,000): a formal run refuses to start otherwise, and with any of `OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS` not 1; `nu_rerun_reason` "" (a formal rerun over an existing check record or outcome needs a non-empty reason also present in log.md). The check stage writes `r2_re_nu_check.json` (checks, Stage 1, the per-mock τ̂_s, P_s, ESS, k̂; never L(ν) on the data), `provenance_nuc.json`, `run_info_nuc.json`; the full stage writes `r2_re_nu.json`, `provenance_nu.json`, `run_info_nu.json` and only the `R2_RE_NU` key of `summary.json`. The count check reads `Pantheon+SH0ES.dat` (0.58 MB, cached; through `ctx.http`) with `usecols` CID and USED_IN_SH0ES_HF only. The profile's seed bases are 770,000 + 100k with k = 0, 1, 2, 3 for m = 0.5, 0.75, 1.5, 2 (k counted from 0) | cache only (Pantheon+SH0ES.dat may be fetched again, 0.58 MB, if evicted) |

- Rerun with an override: `python -m astrolab explore 003-m02-hubble-tension-distance-ladder --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about 28 min with the default R4 and R2-RE;
  `--set r4_draws=1000` takes a few minutes; `--set re_check=false` skips R2-RE).
- R2-RE-G's formal run, in two stages (README section 2, addendum 2026-11-21): (1) set `g_check` and `g_only` to true and `g_stage` to "power" and run `python -m astrolab run 003-m02-hubble-tension-distance-ladder` (cache only, about 17 min): it writes `r2_re_g_power.json` and logs one line with the power, the size and the curve (`shape.power_log_line`); nothing in it uses G on the data. (2) Paste that line unchanged, on one line, into log.md and commit it on the branch (the code checks only that the line is present in log.md; committing is the operator's step). (3) Set `g_stage` to "full" and run again (about 18 min), with the same thread environment and `g_*` values as stage (1); it refuses to start unless the power line from (1) is present in log.md. It recomputes the power stage (its counts must equal the power record's, else rule (1)), then computes G_obs, p_G and the reading. (4) Set `g_only` back to false and `g_stage` to "full", with dated notes in log.md.
- R2-RE-GT's formal run, in two stages (README section 2, addendum 2026-11-21, T-057), with the thread environment of R2-RE-G's formal run (`OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS` = 1): (1) set `gt_check` and `gt_only` to true and `gt_stage` to "power" and run `python -m astrolab run 003-m02-hubble-tension-distance-ladder` (cache only, about 10 min): it writes `r2_re_gt_power.json` and logs one line with the power, the size and the reported TC and VHAT rates (`shape.gt_power_log_line`); nothing in it uses p_T on the data. (2) Paste that line unchanged, on one line, into log.md and commit it on the branch. (3) Set `gt_stage` to "full" and run again (about 10 min), with the same thread environment and `gt_*` / `g_*` values; it refuses to start unless the power line is present in log.md. It recomputes the power stage (its counts must equal the power record's, else rule (1)), then checks G_obs and k = 326 and computes p_T,obs, its sensitivities, the reading, the sub-label and the gloss. (4) Set `gt_check` and `gt_only` back to false and `gt_stage` to "full", with dated notes in log.md.
- R2-RE-GTP's formal run (README section 2, addendum 2026-11-22, T-060), with one thread (`OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS` = 1, as R2-RE-GT): (1) set `gtp_check` and `gtp_only` to true and run `python -m astrolab run 003-m02-hubble-tension-distance-ladder` (cache only, about 30–35 min, most of it the 36 pointwise checks); it checks the eight recorded k values and R2-RE-GT's and R2-RE-G's reused counts before writing any simulation file, and a failure is written as a "not evaluable" outcome, which is the first formal outcome. (2) Set both back to false, with a dated note in log.md.
- R2-RE-NU's formal run, in two stages (README section 2, addendum 2026-11-24, T-062), with one thread (`OMP_NUM_THREADS`, `MKL_NUM_THREADS`, `OPENBLAS_NUM_THREADS` = 1): (1) set `nu_check` and `nu_only` to true and `nu_stage` to "check" and run `python -m astrolab run 003-m02-hubble-tension-distance-ladder` (cache only; timed on synthetic inputs at n_g = 240 about 35 min for the 800 mocks on an idle CPU, plus a few minutes for loading, Stage 1 and the pointwise checks; up to twice that on a shared CPU): it runs the checks, Stage 1 and, if the gate passes, the known-answer check, writes `r2_re_nu_check.json` and logs one line (`nu.check_log_line`); it never computes L(ν) on the data. (2) Paste that line unchanged, on one line, into log.md and commit it on the branch. (3) Set `nu_stage` to "full" and run again (about 10–15 min) with the same thread environment and `nu_*` values; it refuses to start unless the line is present in log.md, recomputes the checks, Stage 1 and the first 20 mocks of each injection (they must equal the check record exactly, else label 1), then computes L(ν), the weights, the label, p_int and the sensitivities. If the check stage gave label 1, 2 or 3, the full stage only writes that label. If the upper end of τ̂_HF's 68% interval is "not determined", the full stage stops with an error before L(ν) (a case the scale condition does not cover). (4) Set `nu_check` and `nu_only` back to false and `nu_stage` to "check", with dated notes in log.md.
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 003-m02-hubble-tension-distance-ladder --tag <topic> --script explore/<name>.py`.
  Existing: `explore/diag_hosts.py` (which checks link each L column to which host).
- Results files and keys: `summary.json` (verdicts), `r1.json` (`params` with `column_label`, `worst_param_label`,
  `fivelogh0`, `chi2`),
  `r2.json` (`anchor_step`, `host_step.shift`, `.shift_sigma` (C errors), `.verdict` (the headline, R2-RE
  when evaluated), `.criterion_outcome`, `.descriptive_inflated_sigma`, `.headline_source`,
  `.preregistered_verdict`), `r2_re.json` (`tau_hat`, `interval_68`, `reml`, `host_step`, `verdict`,
  `sensitivity_cepheid_rows`, `r4_under_v`, `loo_chi2`), `r2_re_sel.json` (`tau`, `spread_X`, `spread_S`,
  `reading`, `selection`, `extremeness`, `checks`; summary key `R2_RE_SEL`),
  `r2_re_d.json` (`observed` with `spread_37`, `spread_36`, `D`, `D_proxy`, `delta_hat`, `sigma_delta`,
  `mismatches`; `tau_hat_N`; `models.<key>` for `C`, `V050`, `V077`, `V105`, `O`, `Olo`, `OVN`, `Oany` with
  `status`, `decisive`, `D` (`k`, `n`, `p`, `ci95`, `label`), `J` (`k`, `n_B`, `count_obs`, `t_obs`, `p`, `ci95`,
  `label`), `Q_raw`, `quantiles_5_50_95`, `P_spread_37_ge_obs`, `P_spread_36_le_obs`, `D_proxy`, `selected`;
  `kde`; `reading`; `section5`; `checks`; `seconds`; summary key `R2_RE_D`), `r2_re_d_sims_<key>.json` (per
  simulation: `pairs` (spread_37, spread_36) rounded to 4 decimals, `dropped` (d'), `half_b_counts`,
  `count_obs`, and for `Oany` `offset_host`),
  `r2_re_g_power.json` (power stage: `status`, `rule1`, `n_sims`, `runtime_guard`, `design` (`rank_M`, `sigma_delta_j`, `joint_rank`), `checks` (`reproduction`, `pointwise`), `models.<key>` for `VHAT`, `V050`, `V105`, `C`, `OANY`, `OANYLO`, `OANYVN`, `O`, `Z250`–`Z500` with `n_excluded`, `rate`, `ci95`, `quantiles_5_50_95` of G_s and τ̂_s, `n_tau_zero`, `n_tau_bound`, `n_jhat_is_offset_host`, `k_sha256`; `power`, `size`, `curve`, `curve_with_oany`, `smallest_z_alt_power_08`, `seconds`), `r2_re_g.json` (the same recomputed, plus `checks.power_stage_counts_reproduced`, `observed` (`G_obs`, `j_hat_obs`, `host_j_hat`, `sum_z2`, `hosts_observed` with every z_j, δ̂_j, σ_δ,j), `p_G` (`k`, `n_inner`, `p`, `ci95`, `label`), `p_G_fixed`, `p_dbl`, `p_rev`, `joint_fit`, `reading`, `sub_label`, `section5`; summary key `R2_RE_G`), `r2_re_g_sims_<key>.json` (per simulation: `G` (5 decimals), `tau_hat` (6 decimals), `k`, `j_hat`, and for the OANY models `offset_host`),
  `r2_re_gt_power.json` (power stage: `status`, `rule1`, `n_sims`, `runtime_guard`, `design`, `checks` (`reproduction`, `pointwise`, `r2_re_g_simulations_reproduced`), `models.<key>` for `THAT`, `T050`, `T105`, `OANY`, `OANYVN`, `TC`, `VHAT` with `tau_t`, `n_excluded`, `rate`, `ci95`, `quantiles_5_50_95`, `k_sha256`; `power`, `size`, `reported`), `r2_re_gt.json` (the same recomputed, plus `checks.power_stage_counts_reproduced`, `checks.real_data` (G_obs, k = 326), `observed`, `p_T_obs` (`k`, `n_inner`, `p`, `ci95`, `label`), `sensitivities` (`nu`, `fixed_tau`, `em_scale`), `reading`, `sub_label`, `gloss`; summary key `R2_RE_GT`), `r2_re_gt_sims_<key>.json` (per simulation: `G`, `tau_hat`, `k`, `j_hat`; the T models `tau_t`, the OANY models `offset_host`),
  `r3.json` (`cchp_side_h0`, `d`, `sigma_d`, `per_host`), `r4.json` (`percentile`, `quantiles`,
  histogram, `z_quantiles`, `z_std`, `z_percentile`, `cchp_z`), `host_identification.json` (`column_labels`, `relabelled`, `per_column_under_labels`),
  `cross_paper.json`.
- Example questions: "Which single CCHP host drives the shift?" → `--set cchp_hosts=[...]` leaving
  one out at a time; "Does the shift survive with a looser identification tolerance?" →
  `--set sn_match_tol=0.25`; "Is the CCHP set unusual among subsets with the same number of SNe?" →
  a script over `r4` draws.
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.
