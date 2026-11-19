# Wide binaries: Newton or MOND at low acceleration?

> 中文：[README.zh.md](README.zh.md)

> Sections 1-4 are the pre-registration (derived from part 3 of the wiki article
> [Study-004](https://github.com/sudoghut/astrolab/blob/main/docs/wiki/Study-004-wide-binaries-newton-or-mond.md)
> and design plan 013). Because the Gaia archive is offline 2026-11-25 to 12-02, data are fetched in
> two steps (section 3): step A (no velocity columns) may run once section 3 is committed; step B
> (proper motions and radial velocities) runs only after sections 1-4 are committed with a date.
> No velocity-derived quantity (ṽ, v_sky, any velocity-based selection or median of velocities) is
> computed before that commit; velocity-free quantities such as the HR constant c are allowed. Later edits need a dated note.

## 1. Question

Cookson, Banik, El-Badry et al. 2026 (C26, arXiv:2602.24035) build a clean Gaia DR3 wide-binary
sample within 130 pc and find the median scaled relative velocity ṽ = v_sky/√(GM/r_sky) flat with
r_sky/r_M, concluding that "Newtonian gravity is up to 1500× more likely than MOND". We ask:

1. **R1.** Rebuilt from Gaia DR3 with server-side queries and the same cuts, do we get a sample of
   comparable size and a median-ṽ profile like C26's Figure 8?
2. **R2 (the test).** With per-bin errors that are calibrated (a bootstrap over pairs), does the
   comparison still favour Newton over the MOND step by a relative likelihood of at least 100?
   This is the `gap_err` premise of the Lean argument.
3. **R3 (descriptive).** How do C26's choices (projection correction, HR cut, distance, parallax
   S/N, ipd_frac_multi_peak, degrouping, ṽ cap) move the result?
4. **R4 (descriptive, optional).** The median profile with Banik et al. 2024's selection
   (250 pc, G < 17), only if its server-side count fits the budget.

## 2. Hypotheses and decision criteria

**Definitions (fixed here).**
- a0 = 1.2 × 10⁻¹⁰ m/s²; G = 6.674 × 10⁻¹¹ (SI); 1 AU = 1.495978707 × 10¹¹ m.
- r_M = √(GM/a0) with M the pair's total mass; x = r_sky/r_M.
- ṽ = v_sky/√(GM/r_sky) (C26 Eq. 9).
- MOND prediction (C26 Eqs. 2, 4–8, 10): ν(g_N) = 1/(1 − exp(−√(g_N/a0))) (MLS form);
  g_N,e = 1.184 a0. C26's x is r/r_M with the 3D r ≈ r_sky√(3/2) (Eq. 10), so with our
  x = r_sky/r_M the internal field is g_N,i = a0/((3/2)x²) (Eq. 5). g_N,t = √(g_N,i² + g_N,e²);
  K = ∂ln ν/∂ln g_N (Eq. 8) at g_N,t, in closed form K = −(y/2)e^{−y}/(1 − e^{−y}) with
  y = √(g_N,t/a0) (between −½ and 0); boost b(x) = √(ν(g_N,t)·(1 + (K/3)·tanh(0.825 g_N,e/g_N,i)^3.7)).
  An offline unit test checks b → 1 as x → 0 and b → √(ν_e(1 + K_e/3)) at large x.
  b → 1 as x → 0 (ν → 1, K → 0), so the MOND model for bin j is A·b(x_j) and the Newtonian model
  is the constant A. As in C26 (Table 3: the χ² values "are optimized with respect to the
  normalization in the Newtonian regime", for each gravity model; 5 degrees of freedom each), each
  model has its own free Newtonian-regime normalisation A — this study's fixed convention, the most
  natural reading of C26; the tied-normalisation calculation is reported as a sensitivity check —
  fitted by generalised least squares with the bin covariance. (C26's Figure 8 draws both curves at 0.489 only for display.) x_j is the median x of the pairs in bin j (C26 Figure 8 uses the geometric mean;
  both are reported, the median is used in the fit).
- Bins (written before any velocity is computed; a value equal to an edge goes to the upper bin): edges in x at the geometric midpoints of C26's
  Table 2 bin medians: 0.1057, 0.2307, 0.5088, 1.0275, 2.0902; the lowest bin has no lower edge
  (r_sky ≥ 1 kAU) and the highest no upper edge (r_sky ≤ 30 kAU).
- Δχ² = χ²_MOND − χ²_Newton, each at its best A; relative likelihood L = exp(Δχ²/2). The two models
  are not nested; L is a relative likelihood, not a Wilks test or posterior odds.

**Fit validity.** Each bin must hold at least 15 pairs. If the outermost bins fall short, the
highest bin is merged inward and the lowest bin is merged upward with their neighbours until each
end holds at least 15 (the merged x_j is the merged median). (Dated amendment, 2026-11-14, before
any data: the lower end was added after the gate-1 review of the step-B code noted that x < 0.1057
needs r_sky ≈ 1 kAU and M ≳ 1.8 M☉, so the lowest bin may be sparse; C26's own lowest-bin median,
x = 0.073 with 368 pairs, implies separations below the stated 1 kAU for typical masses, an
inconsistency recorded under systematics.) If any interior bin is still under 15, the fit is not
evaluable. Evaluable means: every final bin holds at least 15 pairs and at least two bins
remain; otherwise no verdict is given. All degrees of freedom are n_bins − 1 with the final n_bins,
including the Newtonian p-value. No other merging or edge change is allowed once counts are seen. The 15-pair minimum applies to every bootstrap replicate too: a
replicate with fewer than 15 pairs in any (merged) bin is redrawn; if more than 5% of draws are
redrawn, the fit is reported as invalid. The resulting covariance is therefore conditional on the
fixed final bins and this occupancy rule, not an unconditional bootstrap estimate. The bootstrap covariance must be finite; if its condition
number exceeds 10⁸, its diagonal is used instead, flagged; if any diagonal entry is not strictly
positive, the fit is invalid and no verdict is given.

**R1 (reproduction; main sample = C26's "ṽ ≤ 2.5" row).**
- Main sample: N within ±20% of 1421 → **reproduced sample size**; otherwise **different sample**
  (R2 is still computed but labelled "different sample; not a reproduction", and a diagnostic chain
  switching cuts on one at a time is reported).
- The cleanest variant (ṽ ≤ 1.5 and ipd_frac_multi_peak = 0) is compared with C26's 1216 as a
  diagnostic only (no pass/fail).
- Diagnostics only (no pass/fail): per-bin medians against C26 Figure 8 (read from the image),
  per-bin counts against 368, 228, 144, 99, 33, 28 (and N against their sum, 900, given C26's own
  1421-versus-900 inconsistency); the fitted Newtonian normalisation against
  0.489; which error formula (MAD/√N or 1.4826 MAD/√N) reproduces Figure 8's error bars.

**R2 (the test of C26's conclusion and of `gap_err`).** Primary errors: bootstrap over pairs —
2000 resamples of the whole sample with replacement (seed 0), each re-binned with the same final
(possibly merged) bins; the covariance of the n_bins bin medians is used in both fits, and every
degree-of-freedom count uses n_bins − 1. Verdicts on the main sample (ṽ ≤ 2.5), fixed here:

| Condition on L (primary errors) | Verdict |
|---|---|
| L ≥ 100 | Newton has the higher relative likelihood (agrees with C26's conclusion) |
| 1/100 < L < 100 | cannot distinguish (does not support the strength of C26's conclusion) |
| L ≤ 1/100 | MOND has the higher relative likelihood (contradicts C26) |

Also reported, without verdicts: χ²_MOND with A tied to the Newtonian best fit (an alternative
reading of C26's convention), L with C26's MAD/√N and with 1.4826 MAD/√N (the reproduction
column), L for the three other Table 3 rows, the bootstrap/MAD error ratio per bin, and the
Newtonian χ² and its p-value (n_bins − 1 degrees of freedom; 5 if no bins are merged).

**R3 (descriptive).** Each variant changes one choice from the main sample: no perspective
correction; no HR cut; HR constant c ± 0.2 mag; d < 150 pc; d < 200 pc (needs its own A/B queries beyond the 150 pc parent cut; dated note 2026-11-14, before any data: not attempted in this study because the authenticated fetch of the 150 pc sky takes about a day before the 11-25 archive outage; reported as not attempted); parallax S/N > 100
(catalogue C10); ipd = 0 at 130 pc and at 150 pc; no degrouping; degrouping with C25 neighbours only (diagnostic; needs a second set of A2 queries, counted first;
run only if time before 2026-11-24 allows, otherwise reported as not run); perspective correction
from the inverse-variance-weighted mean RV of both stars instead of the primary's; ṽ ≤ 1.5 and ≤ 2. All are reported together in one table with
L (primary errors), compared with C26's quantitative statements (150 pc: MOND 12×; 150 pc with
ipd = 0: Newton 88×; no projection correction raises the outer-bin median by about 0.15). No
variant is a headline result and no variant-wise significance is claimed.

**R4 (descriptive, optional).** Only if the server-side count for B24's selection gives inputs
within the study budget; otherwise reported as not run.

### 2.1 R5: power-gated re-test on an enlarged sample (d < 250 pc) (addendum 2026-11-18, T-034), pre-registered before any R5 query

*Why.* The 2026-11-16 R2 result ("cannot distinguish", L = 0.49) came from a test that had almost no
power (section 6, points 1–2). With our bins, noise-free Newtonian data give only L = 6.2. Restoring
C26's x coverage (r_sky ≥ 300 AU) does not fix this: the 130 pc sample is then expected to reach only
L ≈ 13 under Newton and L ≈ 0.11 under MOND. R5 therefore enlarges the volume to d < 250 pc and keeps
every other C26 selection rule. Its power is computed in advance on simulated data. A verdict at
C26's strength (L = 100) is allowed only if both gates pass: the design gate G1 (fixed here) and the
data gate G2 (computed after the run). R5 does not replace R2. The 2026-11-16 R2 verdict stays
recorded.

*Seen before this addendum (R5 is partly blind).*
- Sections 5–6 and every number in `results/`: summary, variants, and step A (c and the occupancy
  counts).
- The referee's numbers:
  - noise-free L = 6.2 (Newton) and 0.16 (MOND);
  - L ≈ 7 with C26's design, or ≈ 2000 with halved errors;
  - L = 0.17 with the pooled error model;
  - relaxed degrouping keeps 38% of 1–30 kAU pairs;
  - bootstrap errors scatter by 18–29%.
- The post-hoc exploration at r_sky ≥ 300 AU (section 5), which analysed pairs at d < 130 pc and,
  in its d < 150 pc variant, at d < 150 pc:
  - N = 1250; per-bin counts 543, 286, 232, 109, 56, 24; lowest-bin median x = 0.063;
  - L values: main 1.9; MAD/√N 1.9 × 10⁻⁴; d < 150 pc 0.67; no HR cut 196; no degrouping
    4.5 × 10⁻⁴;
  - the rest of that run was produced and is treated as seen.
- The R3 variants d < 150 pc and d < 150 pc with ipd = 0 (section 5), which also used velocities of
  pairs out to 150 pc.
- The velocity-free design counts of 2026-11-17/18 (T-034):
  - server proxy counts per x bin at 130, 200 and 250 pc (`explore/t034_design_counts.py`);
  - cached counts per bin at 130 and 150 pc with no, relaxed and approximate C25 degrouping
    (`explore/t034_degroup_counts.py`);
  - the server counts of parent stars, RV stars, FLAME masses and candidate pairs (section 3);
  - the cached fraction of candidate pairs that pass the N4 cuts (section 3).
- The simulated power numbers below (`explore/t034_power_mock.py`).
- No velocity-derived quantity of any pair beyond 150 pc has been computed.

Pairs within 150 pc have therefore been analysed with velocities. Only the 150–250 pc shell's velocity-derived
quantities are unseen (its velocity-free design counts were inspected). The shares can only be estimated, from two different count predictions: about 32% of the
predicted R5 sample lies at d < 130 pc (1250 of 3852) and about 38% at d < 150 pc (1467, the
cache-based prediction at 150 pc). The unseen shell therefore holds about 62%, about 2385 pairs.
Variant V14 tests that shell alone.

*R5 sample (exact).* Sections 2–4 apply unchanged except for the following.
- **Parent stars.** parallax > 3.4783 mas (287.5 pc) and parallax_over_error > 40. The margin is
  the same 1.15 that 150 pc gives for 130 pc.
- **Pairs.**
  - Both stars are parent stars, and both have radial_velocity not null.
  - Their parallaxes agree within 3σ combined, with the strict operator of the study code
    (`queries.pair_conditions`): |ϖ1 − ϖ2| < 3√(σ1² + σ2²).
  - r_sky ≤ 30 kAU at ϖ̄ (`<=`, as in `queries.b1_extra`). This is the server-side search radius, and it replaces the 0.5 pc A1
    search: the sample stops at 30 kAU, and degrouping has its own query.
  - Each pair is kept once, with source_id_a < source_id_b.
- **Distance.** ϖ̄ > 4.0 mas (d < 250 pc).
- **r_sky window.** 300 AU ≤ r_sky ≤ 30,000 AU at ϖ̄.
  - C26's lowest bin has median x = 0.073 and upper edge 0.1057. If pairs are spread uniformly in
    log x within that bin, its lower end is x_floor = 0.073²/0.1057 = 0.0504.
  - x_floor · r_M ≥ 300 AU only for M ≥ 0.72 M☉, so the floor preserves C26's implied coverage only
    for those pairs.
  - The value coincides with the floor of the post-hoc exploration. It is kept to avoid a new fork,
    not because it was derived independently of that run.
  - At d > 130 pc, 300 AU is less than 2.31″. Variant V3 adds the angular floor θ ≥ 2.31″.
- **Degrouping.** C26's relaxed rule, scaled to the new volume.
  - A neighbour is any star with parallax_over_error > 5, phot_g_mean_flux_over_error > 5 and
    parallax + 3·parallax_error > 3.4783.
  - It must satisfy the operators of the original degrouping (`queries.pair_conditions` with
    `DEGROUP_PC` = 100000/206264.806 pc). The projected separation at the two stars' weighted
    parallax must be ≤ 100 kAU (`<=`), and |ϖ_star − ϖ_neighbour| < 3√(σ_star² + σ_neighbour²) (`<`).
  - A pair is kept only if each member has exactly one neighbour and that neighbour is its partner.
- **Masses, v_sky, σ(ṽ) and x.** As in section 4, including the primary-star RV convention.
- **Cuts unchanged.**
  - RUWE < 1.25 for both stars.
  - The HR band with c = 1.590861779261529 for both stars, with M_G at ϖ̄ and no extinction
    correction.
  - Both RVs present, and |ΔRV| < 10 km/s.
  - σ(ṽ) < 0.1 and ṽ ≤ 2.5.
- **Bins and merge rule unchanged.** Edges 0.1057, 0.2307, 0.5088, 1.0275, 2.0902; at least 15 pairs
  per bin; x_j is the bin median.

*Error model (R5 primary): stratified bootstrap, diagonal covariance.*
1. Sort the pairs by (source_id_a, source_id_b).
2. Create one generator, `numpy.random.default_rng(0)`.
3. For each final bin j, in increasing x, draw `rng.integers(0, N_j, size=(10000, N_j))`. Each row
   indexes the bin's pairs in the sorted order.
4. Take the median of each row. σ_j is the standard deviation (ddof = 1) of these replicate medians.
5. The covariance is diag(σ_j²). The bins hold disjoint pairs, so with N_j fixed their medians are
   independent.
6. No replicate can fall below 15 pairs, so the redraw rule of this section does not apply.
7. Every σ_j must be finite and > 0.

Fits and L follow this section. A_N is the GLS fit of the constant model A to the bin medians m_j
with diag(σ_j²). A_M is the GLS fit of A·b(x_j) with the same covariance (`wb.compare_models`:
`A_newton`, `A_mond`). Then Δχ² = χ²_MOND − χ²_Newton and L = exp(Δχ²/2). The Newtonian p-value has
n_bins − 1 degrees of freedom.

*Power, pre-computed on simulated data (fixed here).* Every number in this subsection is regenerated
by `python -m astrolab explore 004 --tag t034-power --script explore/t034_power_mock.py` with its
default settings (about 1 h). f_cal is fixed at 1.227 throughout, and each computation uses a fresh
generator with a fixed seed.

**Mock population.**
- Keplerian orbits with GM = a = 1, f(e) = 2e, uniform mean anomaly and isotropic orientation.
- ṽ = |v_sky + noise| · √r_sky, with Gaussian noise of 0.03 per sky component.
- A pool of 2 × 10⁶ pairs from `default_rng(20261117)`.
- The scatter about the pool median is multiplied by the fixed f_cal = 1.227. It was derived once as
  the geometric-mean ratio of the 2026-11-16 bootstrap errors to the mock's errors at the same
  counts; the script recomputes this only as a check. With it, the old design
  gives L = 5.0, against the referee's 6.2.
- The mock assumes that the ṽ distribution at 130–250 pc has the same shape and relative width as at
  130 pc. Larger σ(ṽ) and more contamination at larger distance would widen it and lower the power.
  That is part of what the 25% margin and the gates G1b and G2 protect against.

**Design.**
- Predicted final counts per bin: 1408, 988, 789, 375, 220, 72.
- These are the server proxy counts at 250 pc (3067, 2409, 1771, 1047, 745, 439), multiplied by
  transfer factors T_j = 0.459, 0.410, 0.445, 0.359, 0.295, 0.163.
- T_j is the 130 pc ratio of the seen final counts to the proxy counts. The proxy omits degrouping,
  the |ΔRV| cut, the ṽ cap and FLAME masses, and uses an error-only stand-in for σ(ṽ).
- The T_j may over-predict at 250 pc. The 3σ parallax window in distance widens roughly ∝ d², so
  more chance neighbours fall within 100 kAU and degrouping removes more pairs. The −25% margin is
  arbitrary, but G1b uses the actual degrouped counts, so a shortfall is caught before N4.
- x_j = 0.063, 0.155, 0.328, 0.707, 1.31, 2.7.
- Under the MOND truth the medians are A·b(x_j), with errors scaled by b(x_j).

**How the values are computed.**
- Noise-free values: the per-bin errors come from 20,000 mock medians.
- Monte Carlo: 1000 mocks per truth, each with the stratified bootstrap at B = 1000.

| Quantity (R5 design, calibrated mock) | Value |
|---|---|
| Noise-free L, Newtonian truth: L_N* | **4.7 × 10³** |
| Noise-free L, MOND truth: L_M* | **7.2 × 10⁻⁴** |
| The same with every count reduced by 25% (margin check) | 568; 4.4 × 10⁻³ |
| Monte Carlo, Newtonian truth: median L; P(L ≥ 100); P(L ≥ 10); P(L ≤ 1/10); P(L ≤ 1/100) | 4.9 × 10³; 80.4%; 92.7%; 0.7%; 0.3% |
| Monte Carlo, MOND truth: median L; P(L ≤ 1/100); P(L ≤ 1/10); P(L ≥ 10); P(L ≥ 100) | 6 × 10⁻⁴; 75.3%; 89.0%; 0.5%; 0.0% |
| G2 (symmetric rule below) and verdict, Newtonian truth: P(G2 passes); P(G2 passes and L ≥ 100); P(G2 passes and L ≤ 1/100) | 99.4%; 80.8%; 0.1% |
| The same, MOND truth: P(G2 passes); P(G2 passes and L ≤ 1/100); P(G2 passes and L ≥ 100) | 99.4%; 73.7%; 0.1% |
| The same with every count reduced by 25%, Newtonian truth; MOND truth | 84.4%, 58.1%, 0.3%; 84.4%, 53.0%, 0.1% |
| Shell 150–250 pc alone (V14; predicted 771, 651, 517, 248, 154, 44): noise-free L_N*; L_M* | 242; 8.7 × 10⁻³ |

The G2 rows come from 1000 mocks per truth, with B = 1000 and `default_rng(20261121)`.

*Why 250 pc.* The distance was chosen by a rule: the smallest counted design that keeps C26's relaxed
degrouping and passes G1 with every predicted count reduced by 25%. The 25% is a margin for the
transfer factors. Calibrated noise-free L (Newton, MOND) of the counted designs:

| Design | L (Newton, MOND) |
|---|---|
| 130 pc, relaxed | 13, 0.11 |
| 150 pc, relaxed | 20, 0.080 |
| 200 pc, relaxed | 417, 0.0059; fails at −25% (94, 0.021) |
| 250 pc, relaxed | passes, including at −25% |

C25 degrouping at 150 pc (374, 0.0066) changes C26's rule and also fails at −25%.

*Decision rule (labels fixed here).*
- **G1 (design, fixed now): passes in simulation**, conditional on the mock's assumptions (velocity
  distribution and fixed calibration transferred to 130–250 pc; G1b and G2 are the guards). L_N* = 4.7 × 10³ ≥ 100 and L_M* = 7.2 × 10⁻⁴ ≤ 1/100. It also
  passes with counts reduced by 25%.
- **G1b (velocity-free go/no-go; always applied before the velocity query N4).**
  1. Apply these cuts, in order, to the N1–N3 rows:
     - canonical pairs;
     - relaxed degrouping (N2);
     - ϖ̄ > 4.0 mas;
     - 300 AU ≤ r_sky ≤ 30,000 AU;
     - RUWE < 1.25 for both stars;
     - the HR band for both stars;
     - masses (FLAME, else M_G) and x;
     - the error-only proxy σ̃ < 0.1, where σ̃ = 4.740470464/ϖ̄ · √((σ²_μα*,1 + σ²_μδ,1 + σ²_μα*,2 +
       σ²_μδ,2)/2) / v_c. It uses the N1 error columns pmra_error and pmdec_error only.
  2. Count the pairs per bin, multiply by the fixed factors 0.969, 0.937, 0.953, 0.899, 0.809,
     0.521, and round each product to the nearest integer (halves up).
     - The factors are T_j × (no-degrouping / relaxed-degrouping velocity-free counts at 130 pc).
       They are applied to the counts only, never to the pairs or their x.
     - They stand for the steps that cannot be applied before velocities: the |ΔRV| cut, the ṽ cap,
       and the residual between the σ̃ proxy and the true σ(ṽ) cut.
     - They are not split by step, because the 130 pc results record that attrition per step only
       as totals, not per bin.
     - This is an approximation. It assumes that the σ̃ attrition and the FLAME/M_G mass difference
       do not depend on degrouping.
  3. Apply the 15-pair merge rule of this section to the scaled-and-rounded counts, exactly as
     `wb.merge_outer(counts, 15)`: the highest bin is merged inward and the lowest upward until each
     end holds 15; no other merge. If any final bin still holds fewer than 15 or fewer than two bins
     remain, G1b fails ("R5: not run (insufficient predicted power)").
     - x_j is the median x of the pairs in each final bin, taken over exactly the pairs that pass
       step 1. That means every cut N1–N3 allow before velocities, including degrouping from N2,
       masses from N3 and the σ̃ proxy; it is the same set whose counts are scaled in step 2.
     - Approximation: the remaining velocity steps are assumed independent of x within a bin. G2 is
       the post-hoc guard.
  4. Compute L_N* and L_M* with `g1b()` in `explore/t034_power_mock.py`:
     - the pool from `default_rng(20261117)` with f_cal fixed at 1.227;
     - one fresh `default_rng(20261118)`;
     - for each bin in increasing x, 20,000 replicate medians, each drawing N_j indices.
  5. G1b passes if L_N* ≥ 100 and L_M* ≤ 1/100, with no margin.
  6. If G1b fails, N4 is not fetched, and R5 is reported as "R5: not run (insufficient predicted
     power)", with the counts.
  7. Step 1 is implemented in `run.py` in stage 2 exactly as written. Steps 2–5 are
     `g1b_pipeline()` in `explore/t034_power_mock.py`, which takes the x values of the pairs that
     survive step 1 and calls `g1b_counts()` and `g1b()`. run.py calls these same functions.
- **G2 (data-conditional, after the run; symmetric).**
  - Let r_j = σ_j/m_j be the relative errors of the data.
  - Newtonian truth: medians A_N, errors A_N·r_j.
  - MOND truth: medians A_M·b(x_j), errors A_M·b(x_j)·r_j.
  - Fit each with `wb.compare_models` to get L_N^data and L_M^data.
  - G2 passes if L_N^data ≥ 100 and L_M^data ≤ 1/100.
- **Unblinded rule.** If any N4 row with velocity data is read (downloaded or from the cache; an
  attempt that returns no rows does not count) before section 2.1 is merged to main (section 3), R5 is
  permanently unblinded. Every R5 label is then prefixed "R5 (unblinded, descriptive):", and no
  confirmatory verdict is given, even after the merge.
- **R5 verdict.** A value equal to a threshold takes the outer label.

| Condition | Label |
|---|---|
| Fit invalid or not evaluable (rules of this section; σ_j not finite or not > 0) | "R5: invalid fit (no label)" |
| G1b fails | "R5: not run (insufficient predicted power)" |
| A required query (N1–N4) cannot be completed before 2026-11-24 | "R5: not run (data not obtained)" |
| G2 fails, L ≥ 10 | "R5: no verdict at C26's strength (insufficient power, data-conditional); Newton weakly preferred (descriptive)" |
| G2 fails, 1/10 < L < 10 | "R5: no verdict at C26's strength (insufficient power, data-conditional); no preference (descriptive)" |
| G2 fails, L ≤ 1/10 | "R5: no verdict at C26's strength (insufficient power, data-conditional); MOND weakly preferred (descriptive)" |
| G2 passes, L ≥ 100 | "R5: Newton has the higher relative likelihood (agrees with C26's conclusion)" |
| G2 passes, 1/100 < L < 100 | "R5: cannot distinguish" |
| G2 passes, L ≤ 1/100 | "R5: MOND has the higher relative likelihood (contradicts C26)" |

- **Not a reproduction.** R5 is labelled "enlarged sample; not a reproduction". C26 used d < 130 pc.
  R5 makes the same model comparison on a C26-quality sample out to 250 pc.
- **Population changes with distance.** At larger d the RV and parallax-S/N limits select brighter,
  more massive stars, which can change the mass and x mix within each bin. As a descriptive check,
  the per-bin medians of ṽ and x are reported separately for d < 150 pc and 150–250 pc.
- **Distance-dependent bias towards MOND.** At 130–250 pc there are more loose co-moving groups
  (e.g. Sco-Cen, Taurus, the Pleiades, α Per, IC 2602/2391) and more chance pairs at large r_sky.
  Contamination that adds a roughly fixed km/s raises the outer-bin ṽ and mimics MOND, and
  measurement noise inflates the median more at large x. Variants V1, V2, V8, V9 and V13, and the
  per-shell bin medians, are the checks.
- **Allowed afterwards.** Documented, dated bug fixes only. Not allowed: changes of D, the floor, the
  edges, the merge rule, degrouping, the error model, B, the seeds, the mock settings, the factors or
  the thresholds.

*Sensitivity variants (fixed here; descriptive, no verdicts).* Each variant changes one choice from
R5 and keeps the R5 error model. Each reports N, the counts, L, the descriptive grade (L ≥ 10, or
1/10 < L < 10, or L ≤ 1/10) and its own G2 numbers. A variant that is invalid by the rules of this
section is listed without L.

| Id | Change from R5 | Note |
|---|---|---|
| V1 | d < 130 pc (the C26 volume) | approximately the explored sample [seen: L ≈ 1.9 under the original error model] |
| V2 | d < 200 pc | |
| V3 | additionally θ ≥ 2.31″ (angular floor) | |
| V4 | r_sky ≥ 1000 AU | |
| V5 | additionally x ≥ 0.0504 | |
| V6 | no HR cut | [at 130 pc: seen 196] |
| V7a, V7b | c + 0.2, c − 0.2 | also probes reddening at 130–250 pc |
| V8 | no degrouping | [at 130 pc: seen 4.5 × 10⁻⁴] |
| V9 | C25-neighbour degrouping (neighbours with parallax_over_error > 40, same rules) | needs the N2-C25 query, counted first; not run if it cannot be completed before 2026-11-24 or only unrestricted |
| V10, V11 | ṽ ≤ 2, ṽ ≤ 1.5 | |
| V12 | ipd_frac_multi_peak = 0 for both stars | |
| V13 | parallax_over_error > 100 (catalogue C10) | |
| V14 | 150 pc ≤ d < 250 pc (ϖ̄ ≤ 6.6667 mas; the unseen shell only) | the only fully unseen sample |
| E1 | whole-sample bootstrap, 2000 resamples, seed 0, full covariance, 5% redraw rule (the R2 primary) | |
| E2 | pooled scale: σ_j = m_j·k/√N_j with k² = Σ_j N_j·(N_j σ_j²/m_j²) / Σ_j N_j (σ_j from the stratified bootstrap) | |
| E3, E4 | MAD/√N; 1.4826 MAD/√N | |
| E5 | MOND with A tied to the Newtonian fit | |

## 3. Data (with size estimate)

All from the Gaia archive (gea.esac.esa.int, `gaiadr3.gaia_source`, plus
`gaiadr3.astrophysical_parameters` for FLAME masses), through `ctx.tap` (async), never El-Badry's
catalogue. Parent star: parallax > 6.6667 mas and parallax_over_error > 40 (C25; 824,463 stars,
counted 2026-11-14; C24's own download stopped at 7 mas, 143 pc, but 150 pc is needed for the R3
variants). Neighbours for degrouping (dated change, 2026-11-14, before any data): C26 §3.2.2 asks that the
initial selection be relaxed before degrouping so that faint stars, stars without RVs and stars with
missing BP/RP can still flag contaminated systems ("It is important to include such stars at the
degrouping stage"). So the main sample uses relaxed neighbours: any star with
parallax_over_error > 5 and phot_g_mean_flux_over_error > 5 (C24's download filter, §2.2.1;
BP/RP unrestricted; no RUWE or RV requirement) and parallax + 3·parallax_error > 6.6667 mas, under the
projected radius C26 uses for degrouping (§3.2.1: no third star "within 100 kAU"; 100 kAU at the two
stars' weighted parallax) and the same pairwise 3σ parallax rule, applied between the parent star and
each candidate neighbour. (Candidate pairs in A1 are searched to 0.5 pc = 103.1 kAU, a superset of
the 30 kAU sample.) Degrouping with C25 neighbours
only (parallax_over_error > 40, C24 §2.2.2) is a diagnostic variant.

| Query | Content | Selection (server side) | Est. rows / size |
|---|---|---|---|
| A1 candidate pairs (no velocities) | per pair: both stars' source_id, ra, dec, parallax, parallax_error, phot_g_mean_mag, bp_rp, ruwe, ipd_frac_multi_peak, rv_method_used (non-null when a radial velocity exists) | both parent stars; projected separation ≤ 0.5 pc (103.1 kAU) at the inverse-variance-weighted parallax; parallaxes consistent within 3σ combined (|ϖ1 − ϖ2| < 3√(σ1² + σ2²), for the pair); no velocity condition (as in C24, which has no velocity cut at pair finding; C26's velocity-related cuts ΔRV < 10 km/s, σ(ṽ) < 0.1 and ṽ ≤ 2.5 are applied after B1, section 4) | each region counted first; the total is known only from those counts (expected tens of thousands of rows; ≤ 50,000 per query, max_rows = 50,000, a region that overflows is split), ~600 B per row by conservative estimate |
| A2 neighbour counts | per parent star: source_id, number of relaxed neighbours, and the smallest neighbour source_id | neighbours as defined above (no velocity condition); only stars with n ≥ 1 returned | ≤ 50,000 rows per strip (max_rows = 50,000, split if it overflows); at most one row per parent star, so ≤ 824,463 rows and ≤ 33 MB in total at 40 B per row (likely ≤ 200,000 rows, ≤ 8 MB) |
| A3 FLAME masses (velocity-free) | per parent star in the region with a FLAME mass: source_id, mass_flame | parent stars of the region (same half-open rule as star a) joined on the server to `gaiadr3.astrophysical_parameters` with mass_flame not null | counted first; at most one row per parent star (≤ 824,463 in total, ~19% expected per C26 §4.1.2), 24 B per row, ≤ 20 MB |
| B1 velocities (after the pre-registration commit) | the A1 pairs with pmra, pmdec, their errors, parallax_pmra_corr, parallax_pmdec_corr, pmra_pmdec_corr, radial_velocity and its error | A1's WHERE plus velocity-free cuts: r_sky ≤ 30 kAU at the weighted parallax and radial_velocity not null for both stars | counted per region with this exact WHERE before each fetch (no total is assumed); ~600 B per row by conservative estimate (20 fields) |

Totals are known only from the per-region counts (A1, A2, A3 before step B; B1 in step B); the
cumulative estimate is checked before every fetch (expected 25–60 MB), including the relaxed-neighbour
A2 variant, counted first, under the 200 MB study budget; no single query near 50 MB (each is split
into strips). Strips (half-open in α and δ, so that every parent star with parallax < 100 mas belongs to exactly one region and gets its A2 count from exactly one query; checked by an offline test): star a in regions of 5° in α × 30° in δ for |δ| ≤ 60° (four declination bands with edges −60°, −30°, 0°, 30°, 60°; 288 regions; smaller than first planned because the archive kills longer joins under load, dated 2026-11-14, before any data), 15° in α for 60° < |δ| ≤ 80° (24 per hemisphere), and one query per polar cap (|δ| > 80°), 338 regions in all; star b restricted to the
same strip plus a margin of 3.3° in declination at every boundary and, in right ascension, 7.2°
(|δ| ≤ 60°), 30° (60–80°) and all right ascensions (caps). The search radius is 0.5 pc = 103.1 kAU,
θ = 3.15° at a weighted parallax of 110 mas (star a < 100 mas); the exact half-width in right
ascension is asin(sin θ / cos δ) (7.0° at δ = 63.3°, 27.7° at 83.3°), so the margins cover star a with
parallax < 100 mas (checked by an offline test at 110 mas). Stars with parallax ≥ 100 mas (d < 10 pc,
a few hundred stars; the 50,000-row cap is verified by the query's own count, since pairs can outnumber stars, and the run stops if it is exceeded) are
queried once with star b restricted to parallax + 3σ > 80 mas, counted first.
Each pair is kept once (canonical source_id_a < source_id_b; duplicates from the margins dropped);
this logic has an offline test. **Units.** Parallaxes are in mas, distances in pc (d = 1000/ϖ), r_sky in AU from d and the angle.

**Count first.** Before each A1, A2, A3 and B1 query (every strip, the near-star query and every R3
or R4 variant that needs its own query), `run.py` runs the same FROM/WHERE as a server-side
`COUNT(*)` (through `ctx.count`), converts it to bytes at 600 B per A1 row (20 columns, VOTable), 600 B per B1 row (20 fields), 40 B
per A2 row and 24 B per A3 row (conservative schema-based estimates; the
actual guarded downloads are still subject to the hard per-download and study limits in `astrolab`),
and fetches only if the query fits under 50,000 rows and under `config.HTTP_MAX_BYTES` (the exact
single-download limit used by `astrolab.fetch`) and the cumulative estimate stays
under the 200 MB study budget; a strip over 50,000 rows is split in two in right ascension and
counted again. The budget counts unique fetched inputs (a cached result is not counted again; a
failed attempt that returns nothing counts nothing). If the cumulative estimate would exceed the budget, the run stops and the user is
asked. The cache (`%LOCALAPPDATA%`, ~30 MB) must not be cleared until the study is closed: step A's
rows (A1, A2, A3) live only there, and step B re-issues the same queries, which are then cache hits.
Fallback mirror: VizieR I/355 (checked only if the Gaia archive fails before 11-24).

**R5 data (addendum 2026-11-18, T-034; section 2.1).**

*Run mode.* R5 runs in its own mode (`PARAMS["mode"] = "r5"`) with its own per-run budget,
charged by the study framework as for any run: every input the run reads, cached or downloaded, at its
full size, N2-C25 included when it runs; a download that would take the run past 200 MB stops the
run (`TooLarge`) and the user is asked (AGENTS.md 1.6).
- It loads only the R5 inputs (N1–N4, N2-C25), plus the committed HR constant from `PARAMS`.
- It does not rerun R2 or read the 130 pc step A and B queries.
- The 130 pc cache must not be cleared, because R2's inputs live there.

*Regions.* All new queries use the 338 star-a regions of this section plus the near-star query
(339 queries in all), with the same star-b margins (3.3° in δ; 7.2°, 30° or all of α). These are a
superset of what the 30 kAU search needs: θ ≤ 0.93° at ϖ < 100 mas, i.e. an α half-width of
asin(sin θ / cos δ). Every region is counted first and split if it reaches 50,000 rows.

*Server counts.* These ran on 2026-11-18 and were COUNT queries only; the ADQL is in
`explore/t034_design_counts.py`. At 250 pc:
- 3,312,626 parent stars (parallax > 3.4783 and parallax_over_error > 40);
- 1,565,112 of them with an RV;
- 788,730 of those with a FLAME mass.

| Query | Content | Selection (server side) | Est. rows / size |
|---|---|---|---|
| N1 R5 pairs, velocity-free (step A') | per pair: both stars' A1 columns (source_id, ra, dec, parallax, parallax_error, phot_g_mean_mag, bp_rp, ruwe, ipd_frac_multi_peak, rv_method_used) plus pmra_error and pmdec_error (errors only, for the G1b proxy) | both stars parent at 250 pc, both radial_velocity not null, 3σ parallax rule, r_sky ≤ 30 kAU at ϖ̄ | 60,259 rows (counted; at most 7,289 per 15° declination band); 43.4 MB at 720 B per row (24 fields) |
| N2 relaxed-neighbour counts for N1 stars (step A') | per N1 star: source_id, number of neighbours, smallest neighbour source_id | neighbours as in section 2.1; star a restricted on the server to members of an N1 pair (the same pair subquery) | ≤ 120,518 rows, ≤ 4.8 MB; fallback if the archive refuses the restricted join: star a = all parent RV stars, ≤ 1,565,112 rows, ≤ 62.6 MB |
| N3 FLAME masses for N1 stars (step A') | source_id, mass_flame | the same restriction, joined to `gaiadr3.astrophysical_parameters` | ≤ 120,518 rows, ≤ 2.9 MB; fallback 788,730 rows, 18.9 MB |
| N4 R5 velocities (step B', only after G1b passes) | B1 columns for the surviving pairs | N1's WHERE plus the velocity-free cuts on the server: ϖ̄ > 4.0 mas, 300 AU ≤ r_sky, RUWE < 1.25 for both stars (no HR cut, so that V6 stays possible) | est. about 18,900 rows, 11.3 MB at 600 B (the cached 130 pc analogue keeps 31.3% of N1-like pairs: 6,867 of 21,949); bound 60,259 rows, 36.2 MB |
| N2-C25 (variant V9 only) | as N2, with C25 neighbours | as N2 | ≤ 120,518 rows, ≤ 4.8 MB (unrestricted ≤ 62.6 MB) |

*Budget (R5 run mode, 200 MB).*
- Restricted queries: N1 43.4 + N2 4.8 + N3 2.9 + N4 11.3 + N2-C25 4.8 ≈ 67 MB. With N4 at its
  bound, ≤ 92 MB.
- Unrestricted N2 and N3 fallback, without V9: 43.4 + 62.6 + 18.9 + 11.3 ≈ 136 MB, ≤ 161 MB with N4
  at its bound.
- An unrestricted N2-C25 would exceed the budget, so V9 then runs only in restricted form or is
  reported as not run.
- Each download is at most 50,000 rows × 720 B = 36 MB, under the 50 MB cap.

*Restricted-join risk.* The archive may refuse or time out the restricted N2/N3 joins. In that case:
- N2 and N3 fall back to the unrestricted queries, counted first. Like all R5 queries they are
  partitioned into the regions above, so each download stays ≤ 50,000 rows and ≤ 50 MB
  (≤ 2 MB per region at 40 B per row).
- If neither form completes before 2026-11-24, R5 is reported as "R5: not run (data not obtained)".

*Schedule.* The Gaia archive is offline from 2026-11-25 to 12-02.
1. Merge section 2.1 and this block to main, after the dual-gate review, before 2026-11-21.
2. Fetch N1–N3 (velocity-free), counting first.
3. Apply G1b. It is always applied before N4.
4. Fetch N4.

If N4 rows are accessed (downloaded or read from the cache) before that merge, R5 is permanently unblinded (section 2.1): every label is prefixed
"R5 (unblinded, descriptive):", and no confirmatory verdict is given. Everything must be fetched by
2026-11-24. If N4 cannot be completed, R5 is reported as "R5: not run (data not obtained)".

## 4. Method

1. **Pairs and degrouping (C24 §2.3, C26 §3.2.1).** A pair is kept only if each member's neighbour
   count (A2) is 1 and that neighbour is the partner; pairs sharing a star are thereby removed. The
   fraction of A1 pairs surviving degrouping is reported (velocity-free); it does not change the
   rule.
2. **Common distance and separation.** ϖ̄ = (σ²_ϖ2 ϖ1 + σ²_ϖ1 ϖ2)/(σ²_ϖ1 + σ²_ϖ2) (C24 Eq. A2), where σ_ϖ1 and σ_ϖ2 are
   the two stars' parallax_error;
   d = 1/ϖ̄; r_sky = d·θ (θ the angular separation, exact great-circle formula).
3. **Masses (C26 §4.1.2).** FLAME mass when available (A3), else, for every star without one, M⋆ = 10^{0.0725(M_G,⊙ − M_G)} with
   M_G,⊙ = 4.67 (Gaia G, Vega; Willmer 2018, ApJS 236, 47, Table 3 — verified against the table
   before any mass is computed, recorded in `PARAMS`) and M_G = G + 5 log10(ϖ̄/100) (ϖ̄, the pair's
   weighted parallax in mas, for both stars; C26 uses d_h); add 0.05 M☉ when M⋆ < 0.7 M☉.
   M = M⋆,1 + M⋆,2.
4. **Velocity (C24 Eqs. 2–8, C26 §4.1.6).** The primary's (brighter star's) space velocity is
   built from its pmra, pmdec, the common parallax ϖ̄ and its radial velocity; its components along
   the secondary's local east and north unit vectors are the expected proper-motion terms, and
   v_sky = |(κ/ϖ̄)·(μ_α*,2, μ_δ,2) − (expected terms)| with κ = 4.740470464 (C24 Eqs. 2–6). Using the
   primary's RV is this study's convention (C26 §4.1.6 says one star's RV suffices and speaks of the
   "systemic RV"; the mean-RV version is an R3 variant); both stars need an RV anyway because of
   C26's ΔRV < 10 km/s cut. σ(v_sky), and σ(ṽ) =
   σ(v_sky)/v_c, by the Jacobian of the full perspective-corrected v_sky (common parallax and
   perspective term included) with respect to each star's (ϖ, μ_α*, μ_δ), taken by central finite
   differences, with each star's 3 × 3 covariance from parallax_error, pmra_error, pmdec_error,
   parallax_pmra_corr, parallax_pmdec_corr and pmra_pmdec_corr (C24 Appendix A extended to the
   corrected expression); positions and the radial velocity are treated as exact, the two stars are
   independent, and the mass error is neglected, as in C24 and C26.
5. **Cuts (main sample, C26).** d < 130 pc; 1 ≤ r_sky ≤ 30 kAU; RUWE < 1.25 (both); both on the HR
   band: 0.5 < BP−RP < 3.5, 4 < M_G < 14, and 3.3(BP−RP) + c < M_G < 3.3(BP−RP) + c + 0.8 (slope
   3.3, height 0.8 mag; C26 §3.2.4). The band's position cannot be read from C26, so c is set by a
   velocity-free rule from the A1 stars: take the deduplicated set of A1 stars (each source_id once,
   using its own parallax for M_G) with non-null BP−RP, RUWE < 1.25, own parallax > 7.6923 mas
   (130 pc) and |BP−RP − 1.8| < 0.05; c = median(M_G − 3.3·(BP−RP)) − 0.4, so the band is centred on
   the K-star locus. If fewer than 30 stars qualify, the window widens once to |BP−RP − 1.8| < 0.15;
   if still fewer than 30, the main sample is not evaluable and R1–R2 are reported as not run. The numeric c is committed (dated) after A1 and before B1; the R3 variant uses
   c ± 0.2. *Dated note 2026-11-16 (after step A, before any velocity column was fetched):* c =
   1.5909 (2081 stars in the 0.05 window; `results/step_a.json`), committed as `PARAMS["hr_c"]`.
   Velocity-free occupancy check (exploration script `explore/occupancy_step_a.py`, same cuts up to
   the HR band, masses and x without velocities): per x bin 3, 371, 407, 204, 162, 223 pairs, each an
   upper bound for step B (A1 ⊇ the merged step-B pairs; the RV, σ(ṽ) and ṽ cuts only remove pairs);
   the final merge is decided from the step-B counts by the same rule (here it would join the lowest
   bin to the next). These counts lie at larger x than C26's Fig. 8, a velocity-free sign of the x
   convention issue listed under systematics; no edge, x definition or merge rule is changed in
   response (section 2 forbids it). Before step A, only server-side pair counts under the earlier
   velocity-cap guard were run (plan 013); no velocity value has been fetched (A1's `rv_method_used` is
   the availability flag listed in the section 3 table, not a velocity, and is not used). *(End of note.)*
   Both stars with radial velocities and |ΔRV| < 10 km/s; σ(ṽ) < 0.1; ṽ ≤ 2.5.
6. **Statistics.** Section 2 definitions; bootstrap covariance; GLS fits for A.
7. **Parameters (`PARAMS` in run.py, saved with the results):** a0, bins, bootstrap count and seed,
   the cut values above, variant switches for R3. Changing a committed value amends this
   pre-registration and needs a dated note.

**Blinding fallback.** If the pre-registration commit misses 2026-11-24, B1 is still fetched before
the archive goes offline, and the study is labelled "unblinded" throughout.

**Systematics and limits.** C26's x convention is ambiguous: its Table 2 lowest-bin median
x = 0.073 sits below what r_sky ≥ 1 kAU allows for typical masses with r_M = √(GM/a0); our x is
r_sky/r_M as written in C26, and the per-bin counts against Figure 8 are reported. Our pair finding (projected 0.5 pc with parallax consistency) is our
reading of C24's "within 0.5 pc of one another", which does not say whether the distance is 2D or
3D; the HR band's exact position and C26's bin edges are not published; FLAME masses exist for
only part of the sample; the sample-size discrepancy inside C26 (1421 vs 900) means R1's size
target is itself uncertain.

## 5. Results (2026-11-16)

Step A (velocity-free, 339 sky regions plus a near-star query) and step B (velocities, after the
pre-registration commit) ran on 2026-11-14 to 11-16 through the authenticated Gaia archive; the
cumulative byte estimate was 155.4 MB (budget 200 MB). Page: [`web/index.html`](web/index.html)
(`python -m astrolab serve`); numbers in `results/summary.json` and `results/variants.json`.

| Criterion | Ours | C26 | Verdict |
|---|---|---|---|
| R1 main sample (ṽ ≤ 2.5) | N = 639 | 1421 (±20%) | **different sample** |
| R1 cleanest (ṽ ≤ 1.5, ipd = 0), diagnostic | N = 497 | 1216 | — |
| R1 Newtonian normalisation, diagnostic | A = 0.499 | 0.489 | — |
| R2 Newton vs MOND (bootstrap covariance) | L = 0.49 (Δχ² = −1.44; Newton p = 0.34, 4 dof) | Newton favoured by a large factor | **cannot distinguish** (does not support the strength of C26's conclusion) — labelled "different sample; not a reproduction" |

- **R1.** The diagnostic chain (`summary.json` `R1.diagnostic_chain`): 21,949 candidate pairs with both
  radial velocities → degrouping 8,425 → d < 130 pc 7,376 → 1 ≤ r_sky ≤ 30 kAU 2,825 → RUWE 1,635 →
  HR band 712 → |ΔRV| < 10 km/s 662 → σ(ṽ) < 0.1 650 → ṽ ≤ 2.5 639. Per x bin (before merging)
  3, 215, 232, 109, 56, 24 against C26 Fig. 8's 368, 228, 144, 99, 33, 28: our pairs sit at larger
  x, the x-convention issue listed under systematics (C26's lowest-bin median x = 0.073 implies
  separations below its own 1 kAU floor). The lowest bin was merged into the next by the
  pre-registered rule (five bins). The Newtonian normalisation (0.499) agrees with C26's 0.489.
- **R2.** With the pre-registered bootstrap covariance, L = 0.49: neither model is preferred. The
  bootstrap errors are 1.4–3.1 times MAD/√N, the formula C26 states (per bin 2.3, 2.2, 3.1, 1.4, 2.4).
  With MAD/√N errors the same medians give L = 1.7 × 10⁻⁵ (MOND favoured), and with 1.4826 MAD/√N
  L = 6.7 × 10⁻³ (reproduction column, no verdict): on our sample the error convention, not the
  data, decides the outcome. This is numerical evidence for the Lean gap `gap_err` (the error
  model of the chain). Because the sample differs (R1), R2 is not a reproduction of C26's number.
- **Power of the test (referee, post hoc; verified by us).** With our five bins and bootstrap errors,
  noise-free Newtonian data (flat at A = 0.499) give L = 6.2 and noise-free MOND data L = 0.16:
  neither reaches the pre-registered 100 or 1/100. "Cannot distinguish" was therefore almost
  certain for this sample whatever the truth; it says the sample cannot decide, not that the data
  disfavour C26's conclusion. The referee's design calculation with C26's own bins and counts gives
  L ≈ 7 for flat data with correctly sized errors and L ≈ 2000 with errors halved (the size of
  MAD/√N), i.e. the order of C26's "up to 1500×" (an estimate that assumes C26's per-pair scatter
  equals ours).
- **R3 (descriptive).** ṽ ≤ 2: L = 0.40; ṽ ≤ 1.5: 0.92; no perspective correction: 0.13; d < 150 pc:
  1.16; parallax S/N > 100: 0.49; mean RV: 0.44 — all "cannot distinguish". No degrouping (N = 1465):
  L = 0.034. Invalid fits (more than 5% of bootstrap replicates redrawn because a bin fell below 15 pairs:
  the outermost bin, or for no HR cut the lowest bin with 17 pairs): ṽ ≤ 1.5 with ipd = 0, ipd = 0, d < 150 pc with ipd = 0, no HR cut, c ± 0.2. Not
  attempted or not run: d < 200 pc, degrouping with C25 neighbours only (dated notes in sections 3–4).
  None of C26's quantitative variant statements (150 pc: MOND 12×; 150 pc with ipd = 0: Newton 88×)
  is reproduced: our 150 pc variant gives L = 1.16 and the ipd = 0 variant is invalid.
- **R4.** Not run (optional; the B24 server-side count was not attempted before the archive outage).
- **Exploration after the referee (post hoc, 2026-11-16; output deleted, no verdict).** The same
  cached data with the r_sky floor lowered to 300 AU (`--set rsky_min_au=300 --set n_boot=500`):
  main sample N = 1250, per x bin 543, 286, 232, 109, 56, 24 (C26: 368, 228, 144, 99, 33, 28), lowest
  median x = 0.063 (C26: 0.073). So C26's sample very probably includes pairs below its stated 1 kAU
  floor. On that sample: main L = 1.9 ("cannot distinguish"), with MAD/√N errors L = 1.9 × 10⁻⁴;
  d < 150 pc L = 0.67; no HR cut L = 196 (Newton); no degrouping L = 4.5 × 10⁻⁴ (MOND). The outcome
  swings by orders of magnitude with the sample definition. A pre-registered re-test is T-034.

### R5 (addendum 2026-11-18, T-034): power gate G1b

Run of 2026-11-18 (`python -m astrolab run 004` in R5 mode with `r5_stop_after_g1b` true; numbers in
`results/r5.json`, provenance in `results/provenance_r5.json`). Three earlier attempts the same day
stopped on archive errors (a malformed XML response, an aborted asynchronous job, read timeouts and a
transient "Unknown table gaiadr3.gaia_source"); each raised the pre-registered retry before the
2026-11-24 deadline, and the final attempt resumed from the cache (25,969 s; no fallback regions;
estimated input 54.0 MB of the 200 MB budget). Rows: N1 60,259, N2 116,401, N3 53,860, N2-C25
116,348. **N4 (velocities) was not fetched**, so no R5 velocity data have been read.

| Step | Result |
|---|---|
| G1b step 1, pairs after each cut | canonical 60,259 → relaxed degrouping 11,445 → ϖ̄ > 4.0 mas 11,078 → 300 AU ≤ r_sky ≤ 30 kAU 8,296 → RUWE 4,929 → HR band 2,239 → masses and x 2,239 → σ̃ < 0.1 2,194 |
| Counts per x bin (step 1) | 865, 521, 416, 205, 118, 69 |
| Scaled and rounded (step 2) | 838, 488, 396, 184, 95, 36 (2,037); no merge needed (step 3) |
| Bin median x | 0.067, 0.150, 0.328, 0.707, 1.37, 2.71 |
| Design prediction (section 2.1) | 1408, 988, 789, 375, 220, 72 (3,852); x_j 0.063, 0.155, 0.328, 0.707, 1.31, 2.7 |
| L_N*, L_M* (step 4) | 68.4 (needs ≥ 100), 0.028 (needs ≤ 0.01) |
| **Label** | **"R5: not run (insufficient predicted power)"** |

- **Reading (pre-registered).** G1b fails on both conditions, so N4 is not fetched and R5 gives no
  verdict. The R2 result of 2026-11-16 ("cannot distinguish", with the referee's finding that the
  test had no power) stands as the study's only test of C26's conclusion.
- **Why (descriptive).** The x medians match the design, but the counts are 53% of the prediction
  (43–60% per bin), well beyond the 25% margin (with which L_N* would have been 568). Most of the
  difference comes before velocities, at degrouping: it keeps 19% of N1's candidate pairs (11,445 of
  60,259), against 38% in the 2026-11-16 sample (150 pc parent, degrouped before its d < 130 pc cut; 8,425
  of 21,949). Section 2.1 named this risk (the 3σ parallax
  window widens with distance, so more chance neighbours fall within 100 kAU), and G1b caught it
  before any velocity was read, as designed.
- We recomputed `g1b_counts` and `g1b` from the saved counts and medians and got the same numbers
  (L_N* 68.41653, L_M* 0.0278849).
- **Post hoc (referee, 2026-11-18; section 6).** The loss is degrouping, and it was predictable.
  Velocity-free, with the same cuts, relaxed degrouping keeps 44% of pairs at 130 pc, 39% at 150 pc and
  23% at 250 pc (1,347 of 3,042; 1,581 of 4,094; 2,194 of 9,478). The design's transfer factors were
  measured at 130 pc and so carried that survival out to 250 pc. Even pairs at 300–1,000 AU, which
  are expected to be mostly bound (El-Badry et al. 2021, arXiv:2101.05282), survive only 11% of the time in the 150–250 pc shell (46% within 130 pc), and
  survival depends strongly on Galactic latitude (|b| > 40°: 60% within 130 pc, 20% at 150–250 pc;
  |b| < 10°: 17% and 2%). This points to chance neighbours inside a parallax window that deepens
  ∝ d², rather than real triples (an inference from the latitude dependence, the loss even at
  300–1,000 AU and the mean neighbour count rising from 4.1 to 6.1 per star; the direct test is T-043):
  at 250 pc the relaxed rule thins the sample by sky density and biases it towards high latitudes.
  Without degrouping and with M_G-only masses the same pipeline gives exactly the server proxy counts (3,067, 2,409, 1,771, 1,047, 745, 439), so tiling, de-duplication and the other cuts
  are consistent. The G1b failure therefore most likely reads as "the relaxed degrouping rule does
  not scale beyond about 130–150 pc", not as a shortage of wide binaries. With the C25 neighbour table the same
  counts would give L_N* = 8 × 10⁵ (reported only; switching designs after seeing the counts is not
  allowed, and that design would need its own purity validation).

## 6. Referee notes

Independent referee, 2026-11-16 (a subagent that saw README sections 1-4, the code, the results, the
Lean argument and its quote / kind / body table, not sections 5-8; it ran offline synthetic checks:
perspective correction, σ(ṽ) Jacobian, MOND boost, bootstrap against MAD/√N). No bug found.

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | The test had almost no power: noise-free Newtonian data give L = 6.2 and MOND data 0.16, so neither threshold can be reached; with C26's design and halved errors flat data give L ≈ 2000, C26's order | yes: L = 6.17 and 0.161 recomputed by us with `wb.compare_models` | **Accepted**; section 5 states it next to the verdict. |
| 2 | The shortfall is almost entirely C26's lowest x bin (outside it we have 636 pairs against C26's 532); C26's lowest-bin median x = 0.073 is inconsistent with its 1 kAU floor, so C26 probably includes pairs below 1 kAU or uses a different x scale | partly: per-bin counts from `summary.json`; the exploration below | **Accepted as the likely cause**; post-hoc exploration with r_sky ≥ 300 AU (below); follow-up T-034. |
| 3 | Degrouping with relaxed neighbours (parallax S/N > 5, 3σ parallax consistency) keeps only 38% of 1–30 kAU pairs, much stricter than C26 appears to be | yes (cut traces) | **Accepted limitation**; the C25-neighbour diagnostic was not run (section 3); follow-up T-034. |
| 4 | The bootstrap errors are noisy (18–29% scatter at these N); a pooled error model σ_j = k/√N_j moves L from 0.49 to 0.17 | partly (referee's computation) | **Accepted**; reported as a sensitivity here; no verdict change (both "cannot distinguish"). |
| 5 | Contamination that adds a fixed km/s grows in ṽ with x and mimics MOND (no_degroup: L = 0.034); any MOND-ward reading of the MAD/√N result may be contamination | partly | **Accepted** as context; no verdict uses it. |
| 6 | The ">5% redrawn" rule invalidated 6 of 14 variants (a bin of 15–20 pairs); invalid variants' L values must not be quoted | yes | **Accepted**; section 5 lists them as invalid; recorded as a design lesson (section 7). |
| 7 | No projection correction raises our outer median by 0.038, against C26's ≈ 0.15 (about 1σ given 24 pairs) | yes | Noted; the code was verified on synthetic pairs. |
| 8 | The saved R1 chain is cumulative, not one cut at a time as section 2 says | yes | Accepted (only the HR and degrouping one-at-a-time variants exist). |
| 9 | Lean: `[stated]` premises are no stronger than their quotes; the conclusion should carry "for our cleanest sample"; a missing gap is "x computed on the model's scale" | yes | Docstring of the conclusion qualified; the x-scale gap is recorded in section 7 and the wiki (not added to the Lean argument in this PR). |
| 10 | Literature: Banik et al. 2024 (arXiv:2311.03436) and Chae 2023 (arXiv:2305.04613) on close-binary contamination; El-Badry, Rix & Heintz 2021 (arXiv:2101.05282) and Pittordis & Sutherland 2023 (arXiv:2205.02846) unverified | partly (the first two are study papers) | Context only. |

### Referee, R5 (independent subagent, 2026-11-18)

The referee saw README sections 1–4, the code and the results, not sections 5–8 or the log. It
rebuilt N1–N3 and N2-C25 from the cache only (2,712 cache hits, no network, velocity queries
refused) and reran G1b. We reran its scripts and reproduced every number below. Triage:

| # | Point | Verified | Action |
|---|---|---|---|
| 1 | G1b and the label were evaluated as written: step-1 trace, raw and scaled counts (838.19 → 838 … 35.95 → 36), no merge, x medians, L_N* 68.42 and L_M* 0.0279 reproduce; factors, seeds, f_cal and thresholds equal the README; N4 never fetched | yes | None. |
| 2 | The shortfall is degrouping: velocity-free kept fraction 0.443 (130 pc), 0.386 (150 pc), 0.231 (250 pc); among N1 pairs by distance 0.535, 0.298, 0.203, 0.125, 0.067 (< 100, 100–130, 130–150, 150–200, 200–250 pc); the design's T_j carried the 130 pc survival to 250 pc | yes (our rerun) | **Accepted** (post hoc, section 5). The trend was visible in the cached 130 and 150 pc degrouping counts seen before the pre-registration (`explore/t034_degroup_counts.py`, section 2.1) and was covered only by the arbitrary 25% margin. |
| 3 | The loss points to chance neighbours, not triples: pairs at 300–1,000 AU survive 10.8% in the 150–250 pc shell against 45.7% within 130 pc; survival by latitude 0.17 → 0.020 (\|b\| < 10°) and 0.60 → 0.20 (\|b\| > 40°); mean neighbours per star 4.1 → 6.1 | yes | **Accepted** as an inference (the direct chance-neighbour measurement is T-043); at 250 pc the relaxed rule is a density-dependent thinning that biases the sample to high latitudes (a selection effect for any design that keeps it). |
| 4 | No artefact: without degrouping and with M_G masses the pipeline gives exactly the server proxy counts at 250 pc from a different tiling; N1 equals the lean server count; no fallback regions | yes | None. |
| 5 | 25 of 116,426 N1 members have no N2 row, so their pairs always fail degrouping; the README does not cover this case (probably the relaxed neighbour filter, phot_g_mean_flux_over_error ≤ 5 or null; unchecked, needs a query) | partly (116,401 N2 rows) | Accepted limitation: at most 25 pairs before cuts; no effect on G1b. |
| 6 | `se_rel` uses ddof = 0 | yes | Immaterial at 20,000 replicates. |
| 7 | With the N2-C25 table the G1b-style counts would be 2,152, 1,572, 1,147, 615, 371, 121 (L_N* 8 × 10⁵, L_M* 8 × 10⁻⁶) | yes | Reported only; not a verdict and not an allowed switch of design. |
| 8 | Literature: Banik et al. 2024 (arXiv:2311.03436) use 8,611 wide binaries within 250 pc and model line-of-sight contamination; Chae 2023 (arXiv:2305.04613) 26,615 within 200 pc; El-Badry, Rix & Heintz 2021 (arXiv:2101.05282) estimate chance-alignment probabilities empirically (1.3 million binaries with > 90% bound probability within about 1 kpc); no published per-distance degrouping losses found | yes: the three abstract pages (2026-11-18); Pittordis & Sutherland (arXiv:2205.02846) not verified, not used | Context: larger samples at these distances model or estimate contamination instead of a hard neighbour veto. |
| 9 | Most important next test: the chance-neighbour rate from randomly shifted positions (velocity-free, counted first), as a function of distance and latitude | – | Registered as T-043. |

## 7. Open questions

- Why our sample is less than half of C26's (639 against 1421) with the same cuts: degrouping
  (21,949 → 8,425) and the r_sky window (→ 2,825) remove most pairs; whether C26's x or r_sky
  convention differs (their lowest bin implies r_sky < 1 kAU) could be tested with the per-bin
  medians of Fig. 8 and a relaxed r_sky floor (an exploration, no verdict).
- Which error model is right for the bin medians: the bootstrap errors are 1.4–3.1 times MAD/√N,
  enough to turn "MOND favoured" into "cannot distinguish". A mock with known Newtonian velocities
  and C26's selection would calibrate both.
- The outermost bin (x ≈ 2.7) holds only 24 pairs, which made the ipd = 0 and HR-constant variants
  invalid; without the HR cut the lowest bin (17 pairs) made that variant invalid.
- d < 200 pc and the C25-neighbour degrouping diagnostic were not run (sections 3–4).
- R5 (2026-11-18) was not run: G1b failed because degrouping at 250 pc keeps half the 130 pc
  fraction. Whether a larger volume can reach C26's power at all depends on a degrouping rule that
  does not lose pairs to spurious neighbours (most likely chance neighbours, T-043) as the parallax window widens (section 6: the relaxed rule
  keeps 44% at 130 pc and 23% at 250 pc); any such design needs a new pre-registration (its
  velocity-free counts are now seen). A shifted-field measurement of the chance-neighbour rate is T-043.
- The Lean argument lacks a premise that x is computed on the MOND model's scale (referee point 9);
  C26's lowest bin is inconsistent with its stated 1 kAU floor.
- Design lesson: a hard 15-pair floor with a 5% redraw limit invalidates variants whose sparsest bin
  holds 15–20 pairs.

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `vt_max` | ṽ cap of the main sample | 1.5–3 | cache only |
| `d_max_pc` | distance limit (pc) | 100–150 (the parent query stops at 150) | cache only |
| `rsky_min_au`, `rsky_max_au` | projected separation window | 500–2000; 10,000–30,000 | cache only |
| `ruwe_max`, `drv_max`, `sig_vt_max` | quality cuts | 1.1–1.4; 5–20 km/s; 0.05–0.2 | cache only |
| `hr_c` | HR band constant (committed from step A) | ± 0.3 | cache only |
| `edges`, `min_per_bin` | x-bin interior edges and the minimum count | C26's edges; 10–30 | cache only |
| `n_boot`, `boot_seed` | bootstrap replicates and seed | 500–5000 | cache only |
| `a0`, `gne_over_a0` | MOND constant and external field | 1.0–1.3 × 10⁻¹⁰; 0–2 | cache only |
| `step` | "A" (velocity-free) or "B" | B for explorations | cache only (both steps are cached) |

- Rerun with an override: `python -m astrolab explore 004-m07-wide-binaries-gravity-test --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about 35 min from the cache: every query is a
  cache hit, the bootstrap of 14 variants dominates; `--set n_boot=200` is much faster).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 004-m07-wide-binaries-gravity-test --tag <topic> --script explore/<name>.py`.
- Results files and keys: `summary.json` (`R1`: N, the diagnostic chain, counts against Fig. 8; `R2`,
  `R2_L`; `not_run`), `variants.json` (per variant: `N`, `counts_raw`, `counts`, `medians`, `x_median`,
  `reproduction` (MAD/√N fits), `primary` (bootstrap fit: `L`, `dchi2`, `p_newton`, `boot_errors`,
  `boot_over_mad`, `redraw_fraction`, `verdict`), `cut_trace`), `step_a.json` (step-A counts, HR c),
  `provenance.json` (every query; templated format, read it with `astrolab.provenance.expand`).
- Example questions: "Does a 500 AU r_sky floor bring the counts closer to C26?" → `--set rsky_min_au=500`.
  "How does the verdict depend on the bootstrap?" → `--set n_boot=5000 --set boot_seed=1`.
  "What if a0 = 1.0e-10?" → `--set a0=1.0e-10`. The velocity-free occupancy check:
  `--script explore/occupancy_step_a.py`.
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

