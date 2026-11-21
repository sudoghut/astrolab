# M9 NANOGrav 15-yr GWB: power-law amplitude and spectral index from the KDE free spectrum

> 中文：[README.zh.md](README.zh.md) · Web page online: [https://sudoghut.github.io/astrolab/studies/005-m09-nanograv-gwb-power-law/web/](https://sudoghut.github.io/astrolab/studies/005-m09-nanograv-gwb-power-law/web/)

> Sections 1-4 were written on 2026-11-14 BEFORE run.py and before any data were fetched
> (pre-registration; derived from part 3 of the wiki article
> [Study-005](https://github.com/sudoghut/astrolab/blob/main/docs/wiki/Study-005-nanograv-gwb-power-law.md)
> and design plan 014). Later edits to them must carry a dated note.

## 1. Question

Agazie et al. 2023 (NANOGrav, ApJL 951, L8, arXiv:2306.16213; "L8") report the amplitude of the
gravitational-wave background (GWB) at γ = 13/3, A = 2.4 (+0.7/−0.6) × 10⁻¹⁵ (median, 90%
credible interval), and with γ free A = 6.4 (+4.2/−2.7) × 10⁻¹⁵, γ = 3.2 ± 0.6 (median, 5–95%),
with γ = 13/3 "included in the 99% credible region". They state the amplitudes "are compatible
with astrophysical expectations" of a GWB from supermassive black-hole binaries (SMBHBs),
pointing to the companion paper L37 (arXiv:2306.16220). Using the public KDE free-spectrum
representation (Lamb, Taylor & van Haasteren 2023, arXiv:2303.15442) and numpy only:

1. **R1.** Is our log10 A posterior at γ = 13/3 consistent with L8's interval?
2. **R2 (comparison under an approximate likelihood, not a reproduction).** With γ free, at what
   credible level q does the smallest 2-D HPD region touch γ = 13/3?
3. **R2b (overlap summary, not a compatibility test).** How many L37 Table A1 literature
   predictions overlap our 90% credible interval for A (this is the Lean `NUM` premise
   `num_overlap`), and how many contain our median?
4. **R3 (descriptive).** How much do R1 and R2 change between the 2026 data product v2.0.0
   (sampler bug fixed) and the 2023 v1.1.0?
5. **R4 (descriptive).** Bayes factor of a power law with a low-frequency turnover against the
   γ = 13/3 power law.

The Lean argument (`argument/`) is about L8's amplitude sentence. This study tests its `NUM`
premise (route 1) and the amplitude input (`stat_amp`) via R1; it does not test the two gaps
(`gap_overlap`, `gap_repr`) or route 2 (the holodeck populations).

## 2. Hypotheses and decision criteria

Tolerances are fixed here and are not changed after results are seen. Each criterion reports a
verdict, the numbers, and our explanation of any failure.

**Validity (before any criterion).** The structural checks of section 4 step 1 (files present,
array shapes consistent, the first frequency equal to 1/T within 1% for T = 16.03 yr, the grid
uniform) must pass for a data product, and every posterior must be finite and normalisable. The
edge rule applies to log10 A in R1, to log10 A and γ in R2, the same in R3, and to log10 A only in R4: less than 1% of
the posterior mass may lie in the outermost 1% of the prior range of each of these parameters
(otherwise the grid or prior edge is driving the result). In R4, mass at the prior edges of κ
and f_b is expected (κ → 0 and f_b below f₁ make the turnover inert) and is reported, not a
reason for "not evaluable". If a check fails, every criterion that depends on it
is reported as **not evaluable**, with the reason.

Amplitudes: Ã, A₅ and A₉₅ are 10^x of the median and 5/95% quantiles of x = log10 A.

**R1 (amplitude, γ = 13/3; v2.0.0, 14 frequencies).** Reference distribution q(x) for
x = log10 A: the median-pinned two-piece half-normal with m = log10(2.4e-15),
σ_lo = (m − log10(1.8e-15))/1.645, σ_hi = (log10(3.1e-15) − m)/1.645, density
φ((x − m)/σ_lo)/σ_lo for x < m and φ((x − m)/σ_hi)/σ_hi for x ≥ m (each side holds probability
0.5, so its 5/50/95% quantiles are L8's by construction). Hellinger distance
H = sqrt(1 − ∫ sqrt(p q) dx) between our posterior p and q on the R1 grid (both normalised on
the grid). **Consistent with L8's interval** if H < 0.15; otherwise **differs**. The threshold is
a pre-data choice (plan 014: Lamb+2023 found H = 0.13 for the free-spectrum refit on NG12.5,
0.06 for the 1-D log10 A marginal, and a median 2-D H of 0.26 over 100 simulations). Our median
and 5/95% quantiles against 2.4/1.8/3.1 × 10⁻¹⁵ are descriptive.

**R2 (spectral index; v2.0.0, 14 frequencies).** q = posterior mass of the region where the 2-D
density exceeds its maximum along the line γ = 13/3 (section 4, step 4). The result is q itself.
Descriptive category (project convention, always labelled as such): q in [0.95, 0.997] "same
order as L8's stated tension"; q < 0.95 "weaker"; q > 0.997 "stronger". Descriptive: medians and
5–95% quantiles of the A and γ marginals against L8's 6.4 (+4.2/−2.7) × 10⁻¹⁵ and 3.2 ± 0.6, and
the 1-D HPD level of γ = 13/3, and q computed with "≥" instead of ">" (cells tied with p*; the
likelihood is a histogram lookup, so exact ties can occur).

**R2b (Table A1 overlap summary; descriptive except the Lean binding).** With our R1 median Ã
and 90% interval [A₅, A₉₅]: for each Table A1 row with 16th/84th percentiles [P16, P84]
(closed intervals), overlap if A₅ ≤ P84 and P16 ≤ A₉₅; contains the median if P16 ≤ Ã ≤ P84.
Rows are counted as listed (24 rows; the identical rows Rasskazov & Merritt and Dvorkin &
Barausse count separately), and the counts after merging identical rows are reported alongside.
Bound by the Lean `NUM` premise: `n_models_overlap_ci90 >= 1`. If it fails, the Lean `NUM`
binding fails and is reported; route 1 of the argument then does not hold on our data.

**R3 (data versions; descriptive).** R1 and R2 repeated on v1.1.0; report the change in median,
quantiles and q, and the Hellinger distance between the two R1 posteriors.

**R4 (spectral shape; descriptive).** ln Bayes factor of the turnover model (section 4, step 6)
against the γ = 13/3 power law, both by grid integration over their priors. Prior-dependent
(L11 warns); no verdict.

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| NANOGrav 15-yr KDE free spectra v2.0.0 (primary) | Zenodo record 21844115, `ceffyl_data.zip` via `ctx.http` | the HD-correlated 30-frequency free spectrum (`30f_fs{hd}_ceffyl`: `freqs.npy`, `log10rhogrid.npy`, `density.npy`) | 3.0 MB zip; arrays ~30 × (grid ≲ 10³) floats |
| NANOGrav 15-yr KDE free spectra v1.1.0 (R3 only) | Zenodo record 10344086, `NANOGrav15yr_KDE-FreeSpectra_v1.1.0.zip` via `ctx.http` | same directory | 5.3 MB zip |
| L37 Table A1 (16th/84th percentiles of A_yr) | arXiv:2306.16220, App. A, transcribed by hand into `table_a1.py` (below) | all 24 rows | ~1 KB |

Total under 9 MB, cached; read in memory with `zipfile` and `numpy.load(..., allow_pickle=False)`
(the archives are treated as untrusted data); nothing is extracted into the project folder.
No ENTERPRISE, ceffyl or PTArcade install.

**L37 Table A1** (transcribed 2026-11-14 from the arXiv v2 HTML and ar5iv, read twice; units of
A_yr). The 2026 erratum (ApJL 1006, L67) fixes a galaxy-mass-function error, a sampler error and
a typo in L37's own population analysis; its full text could not be read, so whether it touches
Table A1 (literature values) was not checked; the transcription source is arXiv v2.

| # | Model (reference years from L37's list) | A_yr 16th | A_yr 84th |
|---|---|---|---|
| 1 | Rajagopal & Romani 1995 | 9.32e-17 | 2.41e-16 |
| 2 | Jaffe & Backer 2003 | 8.10e-17 | 1.50e-16 |
| 3 | Wyithe & Loeb 2003 | 4.77e-16 | 8.84e-16 |
| 4 | Enoki et al. 2004 | 4.70e-16 | 1.25e-15 |
| 5 | Sesana et al. 2008 | 1.15e-16 | 2.88e-15 |
| 6 | Sesana et al. 2009a | 2.79e-16 | 8.21e-16 |
| 7 | Sesana 2013b | 3.50e-16 | 1.50e-15 |
| 8 | McWilliams et al. 2014 | 1.07e-15 | 1.51e-14 |
| 9 | Ravi et al. 2014 | 6.51e-16 | 2.10e-15 |
| 10 | Kulier et al. 2015 | 1.58e-15 | 2.51e-15 |
| 11 | Ravi et al. 2015 | 5.10e-16 | 2.40e-15 |
| 12 | Rosado et al. 2015 | 1.91e-16 | 2.01e-15 |
| 13 | Roebber et al. 2016 | 4.00e-16 | 7.23e-16 |
| 14 | Sesana et al. 2016 | 2.15e-16 | 7.08e-16 |
| 15 | Rasskazov & Merritt 2017 | 8.74e-17 | 6.57e-16 |
| 16 | Dvorkin & Barausse 2017 | 8.74e-17 | 6.57e-16 |
| 17 | Kelley et al. 2017b | 1.00e-16 | 6.00e-16 |
| 18 | Ryu et al. 2018 | 5.30e-16 | 7.00e-16 |
| 19 | Bonetti et al. 2018b | 5.83e-16 | 1.01e-15 |
| 20 | Zhu et al. 2019 | 6.10e-17 | 2.40e-15 |
| 21 | Chen et al. 2019 | 1.04e-16 | 1.05e-15 |
| 22 | Chen et al. 2020 | 6.10e-17 | 5.40e-16 |
| 23 | Siwek et al. 2020 | 2.50e-16 | 1.00e-15 |
| 24 | Simon 2023 | 1.46e-15 | 2.26e-15 |

Rows 15 and 16 are identical in all four printed columns (also the A_10yr columns), probably a copy error in L37; they are counted as listed and the merged count is reported alongside (section 2). Table A1 also lists A_10yr percentiles, which this study does not use. The same numbers go into `table_a1.py`; a test checks that file against this table.

## 4. Method

1. **Load and check** (per data product). Open the zip from the cache, locate the directory
   whose name contains `30f_fs{hd}` (exactly one; otherwise not evaluable). Read `freqs.npy`
   (30 values), `log10rhogrid.npy` (G values, uniform spacing db, checked to 10⁻⁶ relative) and
   `density.npy` (log-density, shape (1, 30, G) or (30, G), with the frequency axis of length 30
   before the grid axis; any other shape makes that data product not evaluable). NaN densities
   are set to −36 as in ceffyl. Checks of section 2 "Validity". The zip is untrusted: each
   member is read with a bounded read of 50 MB + 1 byte and rejected if longer (the declared
   `file_size` is not trusted); only the three needed members are read (at most 150 MB in
   total), and an archive listing more than 10,000 members is rejected; and member names containing
   ".." or starting with "/" are rejected.
2. **Likelihood** (Lamb+2023 eq. 8–11; ceffyl `ln_likelihood`). For a model PSD S(f), ρ_k² =
   S(f_k)/T with T = 1/f₁ from the file (seconds), log10 ρ_k = ½ log10 ρ_k². Bin index
   idx_k = searchsorted(binedges, log10 ρ_k, side="left") − 1 with binedges = grid − db/2 plus a
   top edge equal to grid[G−1] (as in ceffyl, so the top cell is half-width and anything above
   grid[G−1] gives −∞); idx < 0 is set to 0 (below the grid: the bottom cell's density);
   idx ≥ G gives ln L = −∞.
   ln L = Σ_{k < K} density[k, idx_k] (the constant K·ln db is dropped). K = 14.
   Power law: S(f) = A²/(12π²) f_yr⁻³ (f/f_yr)^(−γ), f_yr = 1/(365.25 × 86400 s).
3. **R1.** Grid x = log10 A on [−18, −14], 4001 points (step 0.001); uniform prior; posterior
   p ∝ exp(ln L − max); normalised by the trapezoid rule. Median and 5/95% from the cumulative
   trapezoid integral with linear interpolation. Reference q as in section 2, evaluated on the
   same grid and renormalised there; H by the trapezoid rule.
4. **R2.** Grid log10 A on [−18, −11] (1401 points, step 0.005) × γ on [0, 7] (1401 points,
   step 0.005); uniform priors (L8 Appendix B). Posterior on the grid, node masses w_ij =
   p_ij t_i t_j ΔxΔγ normalised to 1, with trapezoid weights t = ½ on the first and last node
   of each axis and 1 elsewhere (the same weights for normalisation, q and the marginals). Line density: p along γ = 13/3 evaluated directly at the
   log10 A grid points, with the same normalising constant as p_ij; p* = its maximum.
   q = Σ w_ij over cells with p_ij > p* (strict, as intended; "≥" is reported descriptively).
   Evaluated in chunks over the γ axis (memory). Marginals by
   summing; medians/quantiles as in step 3; 1-D HPD level of 13/3: mass of the γ marginal where
   it exceeds its value at 13/3 (linear interpolation).
5. **R2b.** Section 2 rules with A₅, Ã, A₉₅ from R1.
6. **R4.** Turnover model (Sampson, Cornish & McWilliams 2015, arXiv:1503.02662):
   S(f) = S_PL(f; A, 13/3) / (1 + (f_b/f)^κ). Priors: log10 A ~ U(−18, −11), log10 f_b ~
   U(−9.0, −7.5) [Hz], κ ~ U(0, 7); grid 701 × 61 × 71 (steps 0.01, 0.025, 0.1), prior
   densities 1/7, 1/1.5, 1/7. Evidence Z = ∫ L π by the trapezoid rule, evaluated with
   log-sum-exp, in chunks over κ, with the same constant (K ln db) dropped in both models;
   ln BF = ln Z_turn − ln Z_PL, where Z_PL integrates the γ = 13/3 power law over log10 A ~
   U(−18, −11) (prior density 1/7) on a grid of step 0.01, matching the turnover A axis.
7. **R3.** Steps 1–4 on v1.1.0.

Sensitivity (explorable, section 8; not part of any criterion): ln L = −∞ also below the grid;
K = 30 frequencies; R1/R2 grid steps halved (knobs); R4 grid steps (knob `r4_steps`); R4 priors
(an explore script).

Systematics to keep in view: the factorised likelihood ignores cross-frequency covariance and
was validated on NG12.5 only; the reference distribution q is built from three quantiles, not
L8's posterior; the KDE was built with L8's noise model and pulsar set, which we cannot vary.

## 5. Results

Run of 2026-11-15 (`python -m astrolab run 005`: 12 s on the first run with download, 4.9 s cached; inputs 3.0 MB + 5.3 MB from Zenodo, cached;
page: [`web/index.html`](web/index.html)). v2.0.0 product: directory `ceffyl_data/30f_fs{hd}_ceffyl`,
log10 ρ grid −9.00 … −4.00 (10,000 points), T = 16.03 yr from the file.

| Criterion | Result (v2.0.0, 14 frequencies) | L8 | Verdict |
|---|---|---|---|
| R1 amplitude, γ = 13/3 | A = 2.31 [1.82, 2.92] × 10⁻¹⁵ (median, 5–95%); H = 0.099 | 2.4 [1.8, 3.1] × 10⁻¹⁵ | **consistent with L8's interval** (H < 0.15) |
| R2 HPD level of γ = 13/3 | q = 0.979 (same with "≥") | "included in the 99% credible region" | same order as L8's stated tension (descriptive category) |
| R2 free fit (descriptive) | A = 6.33 [3.46, 10.79] × 10⁻¹⁵; γ = 3.25 [2.65, 3.89]; 1-D HPD level of 13/3 = 0.993 | A = 6.4 [3.7, 10.6] × 10⁻¹⁵; γ = 3.2 [2.6, 3.8] | – |
| R2b Table A1 (Lean `NUM`) | 8 of 24 rows overlap our 90% interval (8 of 23 after merging the identical rows); 5 contain our median | "within the range of some of these model predictions" | binding `n_models_overlap_ci90 >= 1` **holds** |
| R3 v1.1.0 vs v2.0.0 | **not evaluable** under the pre-registered rule: the v1.1.0 archive has two directories containing `30f_fs{hd}` (`30f_fs{hd}_ceffyl` and `30f_fs{hd}_100fDMGP_ceffyl`) | – | – |
| R4 turnover vs γ = 13/3 power law | ln BF = 2.37 (ln Z_turn = −4.93, ln Z_PL = −7.30); edge mass f_b 0.008, κ 0.004 | – | descriptive (prior-dependent) |

Every edge mass is negligible (log10 A and γ below 10⁻¹⁰). The overlapping Table A1 rows: Sesana
et al. 2008, McWilliams et al. 2014, Ravi et al. 2014, Kulier et al. 2015, Ravi et al. 2015, Rosado et
al. 2015, Zhu et al. 2019, Simon 2023 (median inside: Sesana 2008, McWilliams, Kulier, Ravi 2015,
Zhu).

**Post-hoc exploration (not a pre-registered result; 2026-11-15).** With the exact directory name
(`--set dir_key=30f_fs{hd}_ceffyl`, tag `v1-exact-dir`), v1.1.0 gives R1 A = 2.52 [1.91, 3.11] × 10⁻¹⁵,
H = 0.143 against L8's reference (just under 0.15), and R2 q = 0.992, γ = 3.08 [2.52, 3.71],
A = 7.61 × 10⁻¹⁵. The Hellinger distance between the v1.1.0 and v2.0.0 R1 posteriors is 0.195: the
2026 sampler fix lowers the γ = 13/3 amplitude by about 8% and raises γ by about 0.17, moving
the refit slightly further from L8's published median but leaving all statements qualitatively
unchanged. Note that the v1.1.0 grid spans −15.1 … −0.9, the v2.0.0 grid −9.0 … −4.0.

Reading: on this compressed product, with L8's fiducial DMX noise model (see section 6), the refit
lands on L8's numbers (amplitude within the pre-registered fidelity, free-γ medians within 0.05 in γ
and about 1% in A), the spectral-index tension
is of the same order (q ≈ 0.98 here against "within 99%"), and route 1 of the Lean argument holds
on our data. The three gaps (`gap_overlap`, `gap_holo`, `gap_repr`; `gap_holo` relabelled after the
referee) are untouched by these numbers, and route 2 is not tested.

**Explorations after the referee (post hoc; outputs in `explore/`, not committed; 2026-11-15).**
DMGP noise model (v1.1.0 `30f_fs{hd}_100fDMGP_ceffyl`, tag `dmgp`): R1 A = 2.19 [1.69, 2.60] × 10⁻¹⁵,
H = 0.312 (would be "differs"); R2 q = 0.621, γ = 3.75 [3.13, 4.43]; R4 ln BF = 0.99.
K = 30 (tag `k30`): H = 0.093, q = 0.993, γ = 3.04, ln BF 2.63. K = 5 (tag `k5`): H = 0.243, q = 0.917.
`explore/r4_gamma_free.py`: ln BF free-γ power law vs γ = 13/3 = 1.76; turnover vs free-γ = 0.61.

## 6. Referee notes

Independent referee (2026-11-15; a subagent given the code, pre-registration and results, not our
reading). It found no code bugs and reproduced every number from the cached inputs. Triage:

1. **Noise model dominates R1 and R2 (accepted limitation).** On the DMGP free spectrum the R1
   verdict flips to "differs" (H = 0.312) and q falls to 0.62 (γ = 3.75); L8 §V.1 notes the same
   shift of γ towards 13/3. Our product choice (`30f_fs{hd}`, DMX) matches L8's fiducial model, so
   the pre-registered results stand, but they are conditional on that noise model. Recorded here,
   in the wiki and in the claim.
2. **Like-for-like version (accepted).** L8's numbers come from the 2023 chains; v1.1.0 is the
   contemporaneous product and gives H = 0.143 (post hoc). The approximation error against L8 is
   better read from that than from v2.0.0's 0.099.
3. **R3 not evaluable (as handled).** The directory rule failed on v1.1.0 because of the DMGP
   directory; the v1.1.0 numbers stay post hoc and are not written into `r3.json`. The v2.0.0
   directory name carries a trailing space (`30f_fs{hd}_ceffyl `), which a future exact-name rule
   must allow for.
4. **R4 is mostly a γ preference (accepted, verified).** Free-γ vs 13/3: ln BF 1.76; turnover vs
   free-γ: 0.61 (`explore/r4_gamma_free.py`). L8 App. E: turnover BF 1.46 under CURN, "inconclusive".
   The f_b edge mass (0.008) is close to 0.01 (not a criterion).
5. **Grid range and off-grid rule (no effect).** Truncating v1.1.0 to v2.0.0's grid range or using
   −∞ below the grid changes R1, R2, R4 only in the 3rd–4th decimal; R2 step 0.0025 gives q = 0.9787.
6. **Number of frequencies (reported above).** K = 14 follows L8.
7. **Code (fixed).** `provenance.json` listed v1.1.0 twice (a second `ctx.http` on the
   not-evaluable path; fixed, rerun gives identical results); a stale "< 0.1" in plan 014 corrected.
   The 1-D HPD level is a node sum (negligible).
8. **Pre-registration followed (confirmed).** The 0.1 → 0.15 threshold change is in commit
   ed8a634 (2026-11-14 23:22 EST), before the first data fetch (2026-11-15 04:59 UTC per the cache).
9. **Lean (accepted).** `mod_holo` relabelled as GAP `gap_holo` (applying L37's comparison with its
   own spectra to L8's γ = 13/3 amplitude is our reading); `num_overlap` now notes that the quote is
   about L37's own inferred amplitudes (5-bin fits, about 2.1 × 10⁻¹⁵) while the binding uses our
   14-bin interval. The binding holds under every variant tried (DMX/DMGP, v1/v2, K = 5–30).

## 7. Open questions

- Which noise model should a "reproduction" of L8 use when the two available ones disagree this
  much on γ (DMX q = 0.98–0.99, DMGP q = 0.62)? A pre-registered comparison of both was planned
  (T-024), but it cannot be blind (2026-11-16): the v2.0.0 product has no DMGP free spectrum (its
  30-frequency directories are `30f_fs{cp}_ceffyl`, `30f_fs{hd+mp+dp+cp}_ceffyl_hd-only` and
  `30f_fs{hd}_ceffyl`, names trimmed), and the only DMGP product, v1.1.0 `30f_fs{hd}_100fDMGP_ceffyl`, was already
  analysed after the referee (section 5). The comparison stays the post-hoc one in section 5; a blind
  test needs a new DMGP free spectrum (e.g. a future NANOGrav release).
- NG15 running-spectral-index analysis (Agazie et al. 2024, arXiv:2408.10166, unverified): does it
  change the reading of R4?

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `n_freq` | number of lowest frequencies K in the likelihood | 5–30 | cache only |
| `below_grid` | `"clip"` (bottom-cell density, ceffyl) or `"neg_inf"` | either | cache only |
| `r1_step`, `r2_step` | grid steps for R1 (log10 A) and R2 (both axes) | 0.0005–0.01 | cache only (smaller steps are slower) |
| `gamma_fixed` | γ for R1 | 2–6 | cache only |
| `r4_steps` | R4 grid steps (log10 A, log10 f_b, κ) | (0.005–0.02, 0.0125–0.05, 0.05–0.2) | cache only (smallest steps: minutes) |
| `versions` | data products to analyse | `["v2.0.0"]`, `["v2.0.0", "v1.1.0"]` | cache after first run (5.3 MB for v1.1.0) |

- Rerun with an override: `python -m astrolab explore 005-m09-nanograv-gwb-power-law --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; seconds from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 005-m09-nanograv-gwb-power-law --tag <topic> --script explore/<name>.py`.
- Results files and keys (planned): `results/r1.json` (`median_A`, `q05_A`, `q95_A`, `hellinger`,
  `verdict`); `results/r2.json` (`q_hpd_13_3`, `q_hpd_13_3_ge`, `category`, `gamma_median`,
  `gamma_q05`, `gamma_q95`, `gamma_hpd1d_13_3`, `A_median`, `A_q05`, `A_q95`);
  `results/r2b.json` (`n_models_overlap_ci90`, `n_models_contain_median`,
  `n_models_overlap_ci90_merged`, `n_models_contain_median_merged`, per-row table);
  `results/r3.json` (`delta_median_A`, `delta_q`, `hellinger_v1_v2`, and the v1.1.0 R1/R2
  numbers); `results/r4.json` (`ln_Z_pl`, `ln_Z_turn`, `ln_bf_turnover_vs_pl`, edge masses).
- Example questions: "what if we use all 30 frequencies?" → `--set n_freq=30`; "does the
  off-grid rule matter?" → `--set below_grid=neg_inf`; "how does A change at γ = 4?" →
  `--set gamma_fixed=4`.
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.
