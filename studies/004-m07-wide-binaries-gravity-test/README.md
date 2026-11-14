# Wide binaries: Newton or MOND at low acceleration?

> Sections 1-4 are the pre-registration (derived from part 3 of the wiki article
> [Study-004](https://github.com/sudoghut/astrolab/blob/main/docs/wiki/Study-004-wide-binaries-newton-or-mond.md)
> and design plan 013). Because the Gaia archive is offline 2026-11-25 to 12-02, data are fetched in
> two steps (section 3): step A (no velocity columns) may run once section 3 is committed; step B
> (proper motions and radial velocities) runs only after sections 1-4 are committed with a date.
> No ṽ, v_sky or median is computed before that commit. Later edits need a dated note.

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
  model has its own free Newtonian-regime normalisation A, fitted by generalised least squares with
  the bin covariance. (C26's Figure 8 draws both curves at 0.489 only for display.) x_j is the median x of the pairs in bin j (C26 Figure 8 uses the geometric mean;
  both are reported, the median is used in the fit).
- Bins (written before any velocity is computed): edges in x at the geometric midpoints of C26's
  Table 2 bin medians: 0.1057, 0.2307, 0.5088, 1.0275, 2.0902; the lowest bin has no lower edge
  (r_sky ≥ 1 kAU) and the highest no upper edge (r_sky ≤ 30 kAU).
- Δχ² = χ²_MOND − χ²_Newton, each at its best A; relative likelihood L = exp(Δχ²/2). The two models
  are not nested; L is a relative likelihood, not a Wilks test or posterior odds.

**Fit validity.** Each bin must hold at least 15 pairs; otherwise the highest bin is merged inward
with its neighbour until it holds at least 15 (its x_j is then the merged median, and the degrees of
freedom become n_bins − 1, also for the Newtonian p-value). No other merging or edge change is
allowed once counts are seen. The 15-pair minimum applies to every bootstrap replicate too: a
replicate with fewer than 15 pairs in any (merged) bin is redrawn; if more than 5% of draws are
redrawn, the fit is reported as invalid. The bootstrap covariance must be finite; if its condition
number exceeds 10⁸, its diagonal is used instead, flagged; if any diagonal entry is not strictly
positive, the fit is invalid and no verdict is given.

**R1 (reproduction; main sample = C26's "ṽ ≤ 2.5" row).**
- N within ±20% of 1421 (main) and of 1216 (ṽ ≤ 1.5 and ipd_frac_multi_peak = 0) →
  **reproduced sample size**; otherwise **different sample** (R2 is still computed but labelled
  "different sample; not a reproduction", and a diagnostic chain switching cuts on one at a time is
  reported).
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
Newtonian χ² and its p-value (5 degrees of freedom).

**R3 (descriptive).** Each variant changes one choice from the main sample: no perspective
correction; no HR cut; HR constant c ± 0.2 mag; d < 150 pc; d < 200 pc (needs its own A/B queries beyond the 150 pc parent cut; run only if their counts fit, otherwise reported as not run); parallax S/N > 100
(catalogue C10); ipd = 0 at 130 pc and at 150 pc; no degrouping; degrouping with relaxed neighbours
(any star with parallax_over_error > 5 and phot_g_mean_flux_over_error > 5, C24's download filter;
a required variant: its A2-relaxed count query is run first, and it is fetched if it fits the budget,
otherwise reported as not run with its count); perspective correction
from the inverse-variance-weighted mean RV of both stars instead of the primary's; ṽ ≤ 1.5 and ≤ 2. All are reported together in one table with
L (primary errors), compared with C26's quantitative statements (150 pc: MOND 12×; 150 pc with
ipd = 0: Newton 88×; no projection correction raises the outer-bin median by about 0.15). No
variant is a headline result and no variant-wise significance is claimed.

**R4 (descriptive, optional).** Only if the server-side count for B24's selection gives inputs
within the study budget; otherwise reported as not run.

## 3. Data (with size estimate)

All from the Gaia archive (gea.esac.esa.int, `gaiadr3.gaia_source`, plus
`gaiadr3.astrophysical_parameters` for FLAME masses), through `ctx.tap` (async), never El-Badry's
catalogue. Parent star: parallax > 6.6667 mas and parallax_over_error > 40 (C25; 824,463 stars,
counted 2026-11-14; C24's own download stopped at 7 mas, 143 pc, but 150 pc is needed for the R3
variants). Neighbours for degrouping follow C24's reading (§2.2.2: C25 "allows more potential faint
companion stars through the selection process for the purposes of deselecting potential triple
systems"; §2.3: "Where any star appeared in more than one pair, all such matching pairs were
rejected"): a neighbour is any star of the C25 set (parallax_over_error > 40, any photometry, no
RUWE or RV requirement) with parallax + 3·parallax_error > 6.6667 mas, under the same projected rule (≤ 0.5 pc at the
two stars' weighted parallax) and the same pairwise 3σ parallax rule, applied between the parent
star and each candidate neighbour.

| Query | Content | Selection (server side) | Est. rows / size |
|---|---|---|---|
| A1 candidate pairs (no velocities) | per pair: both stars' source_id, ra, dec, parallax, parallax_error, phot_g_mean_mag, bp_rp, ruwe, ipd_frac_multi_peak, a flag whether radial_velocity is not null, FLAME mass | both parent stars; projected separation ≤ 0.5 pc (103.1 kAU) at the inverse-variance-weighted parallax; parallaxes consistent within 3σ combined (|ϖ1 − ϖ2| < 3√(σ1² + σ2²), for the pair); proper-motion difference × distance < 10 km/s (computed in WHERE, not returned; ṽ ≤ 2.5 implies v_sky ≲ 4 km/s even at 1 kAU and 3 M☉, so this cap cannot touch the main sample; A1 is not rerun with other caps and no counts against the cap are looked at before the commit) | trial: 2,209 in one 15° strip with \|δ\| < 60° at a 5 km/s cap; the 10 km/s cap may give a few times more chance pairs: ≤ 200,000 rows in total, each strip query with max_rows = 50,000 (the default cap; a strip that overflows is split), ~300–400 B per row, ≤ 80 MB in total, ≤ 10 MB per query |
| A2 neighbour counts | per parent star: source_id, number of relaxed neighbours, and the smallest neighbour source_id | neighbours as defined above (no velocity condition); only stars with n ≥ 1 returned | ≤ 50,000 rows per strip (max_rows = 50,000, split if it overflows); at most one row per parent star, so ≤ 824,463 rows and ≤ 33 MB in total at 40 B per row (likely ≤ 200,000 rows, ≤ 8 MB) |
| B1 velocities (after the pre-registration commit) | the A1 pairs with pmra, pmdec, their errors, parallax_pmra_corr, parallax_pmdec_corr, pmra_pmdec_corr, radial_velocity and its error | A1's WHERE plus velocity-free cuts: r_sky ≤ 30 kAU at the weighted parallax and radial_velocity not null for both stars | ≤ 50,000 rows in total, ≤ 20 MB |

Total at most about 135 MB (A1 ≤ 80, A2 ≤ 33, B1 ≤ 20; more likely 25–45 MB), plus the relaxed-neighbour
A2 variant counted first, under the 200 MB study budget; no single query near 50 MB (each is split
into strips). Strips (half-open in α and δ, so that every parent star with parallax < 34 mas belongs to exactly one region and gets its A2 count from exactly one query; checked by an offline test): star a in 24 right-ascension strips of 15° for |δ| ≤ 60°, 8 strips of 45° for
60° < |δ| ≤ 80° (each hemisphere), and one query per polar cap (|δ| > 80°); star b restricted to the
same strip plus a margin of 1.2° in declination at every boundary and, in right ascension, 2.2°
(|δ| ≤ 60°), 7° (60–80°) and all right ascensions (caps). The search radius is 0.5 pc = 103.1 kAU,
1.031° at ϖ = 36 mas; the exact half-width in right ascension is asin(sin θ / cos δ) (2.06° at
δ = 61.2°, 5.95° at 80°), so the margins cover star a with parallax < 34 mas. Stars with parallax
≥ 34 mas (d < 29 pc) are queried separately with star b restricted to parallax + 3σ > 28 mas
(counted first, since an unrestricted star b failed on the server).
Each pair is kept once (canonical source_id_a < source_id_b; duplicates from the margins dropped);
this logic has an offline test. **Count first.** Before each A1, A2 and B1 query (every strip, the near-star query and every R3
or R4 variant that needs its own query), `run.py` runs the same FROM/WHERE as a server-side
`COUNT(*)` (through `ctx.count`), converts it to bytes at 400 B per A1/B1 row and 40 B per A2 row,
and fetches only if the query fits under 50,000 rows and 50 MiB and the cumulative estimate stays
under the 200 MB study budget; a strip over 50,000 rows is split in two in right ascension and
counted again. If the cumulative estimate would exceed the budget, the run stops and the user is
asked. The cache (`%LOCALAPPDATA%`, ~30 MB) must not be cleared until the study is closed.
Fallback mirror: VizieR I/355 (checked only if the Gaia archive fails before 11-24).

## 4. Method

1. **Pairs and degrouping (C24 §2.3, C26 §3.2.1).** A pair is kept only if each member's neighbour
   count (A2) is 1 and that neighbour is the partner; pairs sharing a star are thereby removed. The
   fraction of A1 pairs surviving degrouping is reported (velocity-free); it does not change the
   rule.
2. **Common distance and separation.** ϖ̄ = (σ²_ϖ2 ϖ1 + σ²_ϖ1 ϖ2)/(σ²_ϖ1 + σ²_ϖ2) (C24 Eq. A2);
   d = 1/ϖ̄; r_sky = d·θ (θ the angular separation, exact great-circle formula).
3. **Masses (C26 §4.1.2).** FLAME mass when available, else M⋆ = 10^{0.0725(M_G,⊙ − M_G)} with
   M_G,⊙ = 4.67 (Gaia G, Vega; Willmer 2018, ApJS 236, 47, Table 3 — verified against the table
   before any mass is computed, recorded in `PARAMS`) and M_G = G + 5 log10(ϖ̄/100) (ϖ̄, the pair's
   weighted parallax in mas, for both stars; C26 uses d_h); add 0.05 M☉ when M⋆ < 0.7 M☉.
   M = M⋆,1 + M⋆,2.
4. **Velocity (C24 Eqs. 2–8, C26 §4.1.6).** The primary's (brighter star's) space velocity is
   built from its pmra, pmdec, the common parallax ϖ̄ and its radial velocity; its components along
   the secondary's local east and north unit vectors are the expected proper-motion terms, and
   v_sky = |(κ/ϖ̄)·(μ_α*,2, μ_δ,2) − (expected terms)| with κ = 4.740470464 (C24 Eqs. 2–6; C26
   speaks of the "systemic RV"; the mean-RV version is an R3 variant). σ(v_sky), and σ(ṽ) =
   σ(v_sky)/v_c, by the Jacobian of C24 Appendix A over each star's (ϖ, μ_α*, μ_δ) with Gaia's
   parallax_error, pmra_error, pmdec_error, parallax_pmra_corr, parallax_pmdec_corr and
   pmra_pmdec_corr; positions are treated as exact (their errors are sub-mas and enter only through
   the small perspective term), the two stars are independent, and the radial-velocity error and
   the mass error are neglected, as in C24 and C26.
5. **Cuts (main sample, C26).** d < 130 pc; 1 ≤ r_sky ≤ 30 kAU; RUWE < 1.25 (both); both on the HR
   band: 0.5 < BP−RP < 3.5, 4 < M_G < 14, and 3.3(BP−RP) + c < M_G < 3.3(BP−RP) + c + 0.8 (slope
   3.3, height 0.8 mag; C26 §3.2.4). The band's position cannot be read from C26, so c is set by a
   velocity-free rule from the A1 stars: take the deduplicated set of A1 stars (each source_id once,
   using its own parallax for M_G) with non-null BP−RP, RUWE < 1.25, own parallax > 7.6923 mas
   (130 pc) and |BP−RP − 1.8| < 0.05; c = median(M_G − 3.3·(BP−RP)) − 0.4, so the band is centred on
   the K-star locus. If fewer than 30 stars qualify, the window widens once to |BP−RP − 1.8| < 0.15;
   if still fewer than 30, the main sample is not evaluable and R1–R2 are reported as not run. The numeric c is committed (dated) after A1 and before B1; the R3 variant uses
   c ± 0.2. Both stars with radial velocities and |ΔRV| < 10 km/s; σ(ṽ) < 0.1; ṽ ≤ 2.5.
6. **Statistics.** Section 2 definitions; bootstrap covariance; GLS fits for A.
7. **Parameters (`PARAMS` in run.py, saved with the results):** a0, bins, bootstrap count and seed,
   the cut values above, variant switches for R3. Changing a committed value amends this
   pre-registration and needs a dated note.

**Blinding fallback.** If the pre-registration commit misses 2026-11-24, B1 is still fetched before
the archive goes offline, and the study is labelled "unblinded" throughout.

**Systematics and limits.** Our pair finding (projected 0.5 pc with parallax consistency) is our
reading of C24's "within 0.5 pc of one another", which does not say whether the distance is 2D or
3D; the HR band's exact position and C26's bin edges are not published; FLAME masses exist for
only part of the sample; the sample-size discrepancy inside C26 (1421 vs 900) means R1's size
target is itself uncertain.

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

- Rerun with an override: `python -m astrolab explore 004-m07-wide-binaries-gravity-test --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about N s from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 004-m07-wide-binaries-gravity-test --tag <topic> --script explore/<name>.py`.
- Results files and keys: TODO (`results/<file>.json`: key - meaning).
- Example questions: TODO (question -> knob or script an agent would use).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

