# M12 Poor old heart: Gaia XP metallicities of the oldest Milky Way stars

> 中文：[README.zh.md](README.zh.md) · Web page online: [https://sudoghut.github.io/astrolab/studies/012-m12-poor-old-heart/web/](https://sudoghut.github.io/astrolab/studies/012-m12-poor-old-heart/web/)

> Write sections 1–4 BEFORE writing run.py (pre-registration). Edit them later only
> with a dated note explaining the change.

## 1. Question

Rix et al. 2022 (ApJ 941, 45; arXiv:2209.02722; "R22") estimate [M/H] for about 2 million bright
giants within 30° of the Galactic Centre from Gaia DR3 XP spectra, with an XGBoost model trained on
APOGEE DR17. They report about 18,000 stars with −2.7 < [M/H] < −1.5, a spherical-Gaussian extent of
σ_RGC ≈ 2.7 kpc, at least about 5×10⁷ M☉ of stars, no net rotation below [M/H] = −2 and rotation-dominated
orbits near −1, and read the population as the most ancient proto-Galactic component of the Milky Way.

Using only R22's two public files (Zenodo record 7035810), we ask:

1. Do R22's counts reproduce from the public sample, and which of the paper's inconsistent numbers does
   it support? (T1)
2. Does the spatial extent reproduce, and does it survive a likelihood that includes the sample's own
   selection, a flattened or power-law shape, and the "most stars within 5 kpc" statement? (T2a, T2b)
3. Does the rotation–metallicity relation reproduce: no net rotation below −2, rotation dominated near
   −1, and how sharp is the transition? (T3)
4. How much do these results lean on the metallicity scale and errors? (T4)
5. How many of the metal-poor stars are GSE or halo stars passing through, and do most have apocentres
   below 5 kpc? (T5)
6. How does the mass depend on the conversion choices? (T6, no verdict)

The tests are derived from Part 3 of the wiki article
([Study-012](https://github.com/sudoghut/astrolab/wiki/Study-012-poor-old-heart)), which maps each to a
premise or gap of the Lean decomposition (`argument/Argument.lean`). The age ordering ("older than the
disc", `gap_onezone`) and the proto-Galactic reading (`gap_proto`) cannot be tested with these files;
they are explorations (section 4.9).

This section and sections 2–4 were written on 2026-11-21, before any data file was downloaded or opened.
Our only contact with the data was the Zenodo landing page: file names, sizes, MD5 checksums, licence and
the one-paragraph description ("1.5 million stars" with XGBoost T_eff, log g and [M/H]; "1.2 million
stars" with Galactocentric coordinates, actions and basic orbital parameters). The column layout is not
documented there; it is read at load time (section 3), and every test is defined on quantities R22
describe.

## 2. Hypothesis and decision criteria

The hypothesis under test is R22's description of the metal-poor population as numbers that the public
sample should reproduce (T1, T2a, T3), and as properties that should survive our checks (T2a version
(ii), T2b, T4, T5).

**Conventions.**
- Bootstrap intervals are central 95% percentile intervals over resamples of stars.
- Where a p-value is computed from N mocks with k at least as extreme as the data, p_boot = (1 + k)/(1 + N).
  The design below uses mock pass counts and bias medians, not p-values; pass counts are reported with
  their binomial standard error, √(n·p(1 − p)), which is about 4 at 80 of 100.
- Each test has its own label. A test that cannot be evaluated is labelled "undetermined" with the
  reason (for example "data not in the files", "method bias", "unmodelled selection", "fit at bound").
- Labels are checked in the order written; the first that applies is the label.

| Test | Quantity | Labels (decision rules) |
|---|---|---|
| **T1** recount | counts in the metallicity file: N([M/H] < −2), N(< −1.5), N(−2.7 < [M/H] < −1.5), N(< −1), total N. R22's statements and their samples: abstract (∼18,000 for −2.7 < [M/H] < −1.5; sample 2 million); Section III.2 (>4,000 below −2; ∼18,000 below −1.5; almost 100,000 below −1; no sample named); Fig. 4 caption (∼5,000; ∼20,000; nearly 100,000; sample ∼1.7 million); Section IV (∼20,000 below −1.5; ∼70,000 below −1; sample ∼2 million) | For each statement, a **count label** (our count against R22's number) and, where a sample is named, a separate **fraction label** (our count / our total × R22's sample size, against R22's number); each **agrees** or **disagrees**. "∼X" agrees if within X ± 5%; "almost/nearly 100,000" agrees if within 90,000–99,999; ">X" agrees if above X. A statement whose named sample differs from our total by more than 5% is also marked **sample differs** (the abstract always will). **Summary:** **abstract reproduced** if the abstract's count label agrees; **not reproduced** otherwise; its fraction label is reported next to it. For each inconsistent pair (18,000/20,000; >4,000/5,000; 100,000/70,000) we report which the file supports by count label: one, both, or neither |
| **T2a** σ_RGC | maximum-likelihood σ of a spherical Gaussian in Galactocentric radius for the [M/H] < −1.5 stars, in version (i) (R22's eq. 1 as written) and version (ii) (selection on the observed parallax), section 4.3; 200 bootstrap resamples; 100 known-answer mocks at σ = 2.7 kpc | If parallaxes are missing from the files and not fetched, both labels are **undetermined (data not in the files)** and the rules below do not apply. **Reproduction** (version (i)): **not reproduced** if the fit is at a bound (section 4.3); **reproduced** if σ̂ is within 2.4–3.0 kpc; **not reproduced** otherwise. **σ of the population** (version (ii)): **undetermined (fit at bound)** if the data fit is at a bound; **undetermined (method bias)** if the median mock bias of version (ii) exceeds 0.1 kpc in absolute value, whatever the interval; **undetermined (unmodelled selection)** if the load check L6 finds a parallax-dependent cut that is not in the likelihood; otherwise **consistent with 2.7 kpc** if the 95% interval lies within 2.4–3.0 kpc, **different** if it lies entirely outside, **undetermined** otherwise. The bias gate is tested at σ = 2.7 kpc only. Reported next to the labels: the mock bias distribution of both versions (median and its bootstrap standard error), version (ii) − (i), and the reference fits for −1.5 < [M/H] < −1 and −1 < [M/H] < −0.5 |
| **T2b** shape and 5 kpc | the section 4.3 version (ii) likelihood on the stars at Galactic latitude 5° or more from the plane: step 1, spherical against flattened Gaussian (q free); step 2, if step 1 prefers flattened, flattened Gaussian against flattened cored power law. Mock checks (100 each): false positive (q = 1 with a completeness falling towards the plane and with distance, not modelled in the fit), power (q = 0.5), step 2 (best flattened Gaussian) | If T2a is undetermined for missing data, the shape label and f₅ are **undetermined (data not in the files)**. **Checks first, overriding the step labels:** **undetermined** if any applicable check fails: fewer than 80 of 100 false-positive mocks give "spherical adequate", fewer than 80 of 100 power mocks give "flattened preferred", or (when step 2 is reached) fewer than 80 of 100 step-2 mocks give "flattened Gaussian adequate". Exception: if step 1 gives "flattened preferred" with the false-positive and power checks passed and only the step-2 check fails, the shape label is **flattened (step 2 undetermined)** and f₅ uses the flattened Gaussian. Pass counts are reported with their binomial errors (a rough calibration). **Step 1:** **flattened preferred** if 2ΔlnL > 10 and the profile-likelihood 95% interval of q (where 2ΔlnL from the maximum reaches 3.84) lies entirely below 0.8; **prolate preferred** if 2ΔlnL > 10 and that interval lies entirely above 1 (reported; f₅ then uses the flattened-Gaussian fit); **spherical adequate** otherwise. The same profile interval is used in the mocks; the bootstrap q interval on the data is reported alongside. **Step 2:** **power law preferred** if ΔBIC > 10 in its favour (N = the number of stars at latitude 5° or more, Δk = 1); **flattened Gaussian adequate** otherwise. **5 kpc:** the fraction f₅ of the chosen model's stars within a 3D radius of 5 kpc of the Centre (power law normalised within 18 kpc; the spherical model when the shape is undetermined), with a 95% interval from 200 bootstrap refits of that model: **undetermined** with the same reason when T2a version (ii) is undetermined for fit at bound, method bias, unmodelled selection or missing data (a straddling T2a interval does not propagate); otherwise **most within 5 kpc confirmed** if the interval lies entirely above 0.5, **not confirmed** if entirely below, **undetermined** otherwise. The control population (giants with −1 < [M/H] < −0.5 in the same footprint) is fitted the same way and reported only |
| **T3** rotation | J_φ/J_tot from the kinematics file, joined on `source_id`; primary sample 3 < R_apo < 7 kpc; 1000 bootstrap resamples. (a) the mean over all stars with [M/H] < −2; (b) the mean for −1.1 < [M/H] < −0.9; (c) the 10–90% width of a logistic fit to the means in 0.2 dex bins centred on −2.0, −1.8, …, −0.6. Known-answer width w₀ (section 4.5) | **(a)**, in this order, δ = 0.05: **no net rotation** if the 95% interval lies within [−0.05, 0.05] (more conservative than a two one-sided test at 90%; this takes precedence even if the interval excludes 0); **net rotation** if its lower end is above 0; **net counter-rotation** if its upper end is below 0; **undetermined** otherwise. **(b)** **rotation dominated** if the interval lies entirely above 0.5; **not rotation dominated** if entirely below 0.5; **undetermined** otherwise. **(c)** **undetermined (fit failed)** if the logistic fit does not converge on the data; **sharp** if the width interval lies entirely below w₀ + 0.1 dex; **gradual** if entirely above max(0.4 dex, w₀ + 0.1 dex); **undetermined** otherwise; w₀ is the primary one (from per-star [M/H] errors if the file gives them, otherwise from a 0.1 dex blur), the 0.15 and 0.2 dex variants are reported. The all-R_apo sample is reported as a variant with its own labels |
| **T4** leverage of the metallicity scale | under variants (i) [M/H] ± 0.1 dex; (ii) added Gaussian noise of 0.1 and 0.2 dex (10 realisations each); (iii) T_eff–log g edge removed within each 0.25 dex [M/H] bin (1st–99th and 5th–95th percentiles): the T2a version (ii) σ (point estimate on the shifted, noisy or trimmed [M/H] < −1.5 sample; version (i) reported), the T3 (a) and (b) labels of the primary sample, and the T6 mass with R22's own choices. Counts: elasticity Δln N per 0.1 dex against the slope-only prediction from the observed metallicity distribution | **robust** if, in every variant, σ changes by less than 0.3 kpc, the T3 (a) and (b) labels are unchanged, and the T6 mass (R22's choices) changes by less than a factor 3; in variant (ii) a label counts as changed if it differs from the baseline in at least 6 of the 10 realisations, and σ and the mass are the medians over the 10; a change into or out of "undetermined" in a downstream label counts as a change; the σ condition is skipped, and this is stated, when T2 is undetermined for missing data in the baseline. **sensitive** otherwise, naming the variants and quantities. Counts carry no label; a count that changes by more than a factor 2 in variant (ii) at 0.1 dex is flagged "dominated by scatter from above" (a heuristic) |
| **T5** GSE and halo stars | among the kinematics-file stars with [M/H] < −1.5: the fraction g with e ≥ 0.75 and R_apo ≥ 10 kpc, and the fraction a₅ with R_apo < 5 kpc; variants −1.9 < [M/H] < −1.2 and [M/H] < −1.2; 1000 bootstrap resamples | **g:** **minor** if the interval lies entirely below 0.10; **moderate** if it lies within 0.10–0.25; **major** if entirely above 0.25; **undetermined** otherwise. **a₅:** **most apocentres below 5 kpc confirmed** if the interval lies entirely above 0.5; **not confirmed** if entirely below; **undetermined** otherwise |
| **T6** mass | M = N × m_giant × f_bright × f, section 4.8 | no label: a table of M under each choice, and whether R22's own choices (N(< −1.5), 800 M☉, f_bright = 1, f = 2.5) with our count give at least 5×10⁷ M☉ |

**Overall reading.** Two readings, each formed mechanically from the labels.
- **Reproduction.** **"Not reproduced"** if any of these holds: T1's abstract is not reproduced; T2a's
  reproduction label is not reproduced; T3 (a) is net rotation or net counter-rotation; T3 (b) is not
  rotation dominated (a clear contradiction of R22's statement is not "partly"). **"R22's numbers
  reproduce from the public sample"** if T1's abstract is reproduced, T2a's reproduction label is
  reproduced, T3 (a) is no net rotation and T3 (b) is rotation dominated. **"Partly reproduced"**
  otherwise (an undetermined T3 label, or T2a's reproduction label undetermined for missing data),
  listing the tests.
- **Robustness of R22's picture.** **"Holds under our checks"** if T2a's σ of the population is
  consistent with 2.7 kpc, T2b's 5 kpc fraction is confirmed, T4 is robust, T5's g is minor or moderate
  and a₅ is confirmed. **"Challenged"** if T2a's σ is different, T2b's 5 kpc fraction is not confirmed,
  T4 is sensitive, T5's g is major or a₅ is not confirmed (naming which). **"Undetermined"** otherwise,
  naming the undetermined tests.

T2b's shape label, T3 (c) and T6 are reported separately and do not enter the readings.

**What would change our mind about the method.**
- If the load checks show that the metallicity file is not R22's sample (total below 1.0 million, or
  1% or more duplicated `source_id`s), the run stops and the reading is fixed by a dated amendment.
- If a known-answer check fails, the label it guards is undetermined, as stated in the table; the bias
  is reported, and a method change is possible only as a dated amendment followed by a new run.
- If the files lack parallaxes or photometry, T2 and the parallax-based parts of T6 are undetermined
  unless the user agrees to the server-side addition (section 3).

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| R22 metallicity file `xp_gc_mh.csv` | Zenodo record 7035810 (version v0.1; concept DOI 10.5281/zenodo.7035809, the one R22 cite), CC BY 4.0, via `ctx.http` (`https://zenodo.org/records/7035810/files/xp_gc_mh.csv`; the exact download URL is confirmed on the record page at implementation), MD5 7257c98622573a4a625571fc973859c5 | all rows | about 1.5 million rows ("1.5 million stars"), 98.5 MB |
| R22 kinematics file `xp_gc_kinematics.csv` | same record, `https://zenodo.org/records/7035810/files/xp_gc_kinematics.csv`, MD5 b220c27aacff1f2f03d5a1f2b5fca147 | all rows | about 1.2 million rows ("1.2 million stars"; R22 Section II.2: 1.58 million with RVS velocities, 1.25 million with RVS velocities and ϖ/σ_ϖ ≥ 5; Section II.4: orbits for about 1.25 million, with δv_RVS < 5 km/s), 115.3 MB |
| Optional: Gaia DR3 `source_id, l, b, parallax, parallax_error, phot_g_mean_mag, bp_rp` for the stars with [M/H] < −0.5 (the [M/H] < −1.5 stars for T2 and T6, plus the −1.5 to −0.5 stars for the reference fits and the T2b control population) | Gaia archive TAP, `gaiadr3.gaia_source`, via `ctx.tap`, queries on `source_id` lists of 2,000, sized first with `ctx.count` | only if load check L2 finds these columns missing, and only with the user's agreement (as run: section 4.13 — six columns without l, b, no count queries; 469,041 rows, about 23 MB, 235 queries) | the number of [M/H] < −0.5 stars, recorded at load (10⁵–10⁶ rows × 7 columns, about 10–40 MB, with proportionally more queries, about 50–500, counted first); if the user agrees only to the [M/H] < −1.5 stars (about 20,000 rows, 1–2 MB, about 10 queries), the reference fits and the control population are "not computed", the empirical luminosity function uses the [M/H] < −1.5 stars with ϖ/σ_ϖ > 10 (the isochrone variant if fewer than 500), and nothing else changes |

**The exception and the budget mechanism.** The two files exceed the 50 MB single-download limit and
together the 200 MB study budget. The user agreed on 2026-11-21 to download them once, keep them in the
system cache outside the project, and exceed the study budget for these two files (recorded in
`TODO.md`, T-021; `log.md`, 2026-11-21; plan
[`design/028-plan_*`](https://github.com/sudoghut/astrolab/blob/main/design/028-plan_m12-poor-old-heart-paper-study.md)).
- The per-file limit is lifted with `cap_consent` (T-038), naming that consent.
- The study budget needs a new core-library capability, built in the implementation stage with
  dual-gate review: a consent-gated budget exception for named files, mirroring `cap_consent`. It removes
  only the named files' bytes from a run's budget (it does not raise the budget), records the consent in
  the provenance, and changes no limit in `astrolab/config.py`. `--refresh`, and explorations run with
  refresh, must not re-download the two files. If the cache evicts a file, a new download needs the
  user's agreement again. The run cannot start until this mechanism has passed review.
- The optional TAP addition fits the normal budget once the named-file exception removes the two files'
  bytes. It is an additional fetch, made only with the user's agreement, and it must run before
  2026-11-25 or after the Gaia DR4 release day (the Gaia archive is announced offline from 2026-11-25 to
  12-02).

**Load-time checks** (before any test; each result is written to `results/load.json`).
- **L1 checksums.** Both MD5s must match. *Failure:* stop.
- **L2 columns.** The columns are mapped by name to `source_id`, [M/H], T_eff, log g (metallicity
  file) and `source_id`, J_R, J_φ, J_z, eccentricity, R_apo, and, if present, positions and velocities
  (kinematics file); the mapping is recorded. Also recorded: whether `l, b`, parallax, its error, G and
  BP − RP are present. *Failure:* without `source_id` or [M/H], stop; if several columns are candidates
  for one quantity, stop and fix the mapping by dated amendment; without actions, eccentricity or R_apo,
  T3 and T5 are undetermined (data not in the files); without parallaxes or photometry, see the
  optional TAP row.
- **L3 rows and duplicates.** Total rows of each file recorded. *Failure:* 1% or more duplicated
  `source_id`s: stop (section 2); below 1%: all copies of a duplicated `source_id` are dropped and the
  number recorded.
- **L4 join.** The fraction of kinematics rows whose `source_id` is in the metallicity file is
  recorded; below 99%, the join uses the matched rows and the fraction is stated.
- **L5 units and signs.** Among stars with [M/H] > −0.5 in the kinematics file, the median J_φ must be
  positive and the median R_apo between 2 and 15 (kpc). *Failure:* if the median J_φ is negative, the
  sign of J_φ is flipped and recorded; if it is exactly zero, stop and amend; if R_apo is out of range, its unit is identified from the file's
  header and recorded by dated amendment before any test.
- **L6 cuts between R22's query and the file.** Where the columns exist, histograms of ϖ (bins of
  0.01 mas), ϖ/σ_ϖ (0.1), BP magnitude and BP − RP (0.05 mag), l and b (0.5°) are compared with R22's
  query (parallax < 1 mas, |b| < 30°, |l| < 30°, BP < 15.5, 1.0 < BP − RP < 3.5, the luminosity cut). A cut
  on quantity X at c is declared if, inside the range R22's query allows, the histogram falls from at
  least 50 stars per bin to 0 at c. For ϖ/σ_ϖ, a cut is also declared if fewer than 0.01% of stars have
  ϖ/σ_ϖ < 1; this rule gives no value c and only feeds "undetermined (unmodelled selection)" or an
  amendment that adds the cut to the likelihood. A declared parallax-dependent cut (in ϖ or ϖ/σ_ϖ) not in section 4.3's likelihood makes
  T2a version (ii) "undetermined (unmodelled selection)", unless it is added to the likelihood by a dated
  amendment before any fit. Any declared tighter cut on another quantity (l, b, BP, BP − RP) is applied
  in the mocks.
- **L7 metallicity range.** Minimum, maximum and the 0.1th percentile of [M/H] are recorded, with the
  number of stars below −2.5.

## 4. Method

### 4.1 Coordinates and samples

- Galactocentric frame: R0 = 8.2 kpc, the Sun in the plane (z☉ = 0); x towards the Centre. These are our
  choices (R22 do not state theirs for eq. 1).
- Parallax zero point: ϖ_corr = ϖ + 0.02 mas for the model; cuts apply to the raw ϖ.
- Metal-poor sample for T2: all stars of the metallicity file with [M/H] < −1.5.
- Kinematics sample for T3 and T5: kinematics-file stars joined to the metallicity file, used as given
  (no further cut).
- Random seeds are fixed and saved in the results.

### 4.2 T1

Direct counts on the metallicity file. Labels as in section 2. The bands are fixed above; Poisson noise
(√N, about 1% at 18,000) is reported and not used.

### 4.3 T2a

- **Density along a line of sight.** For star i at (l_i, b_i), the true parallax ϖ (mas) maps to the
  distance d = 1/ϖ (kpc) and Galactocentric radius R(ϖ). n_i(ϖ) ∝ ϖ⁻⁴ ρ(x, y, z), here
  ρ = exp(−R²/(2σ²)). The likelihood is conditional on each star's direction; the footprint enters only
  through which stars are in the sample (and, in T2b, through the f₅ integral).
- **Grid.** 300 nodes, log-spaced in distance from 0.2 to 30 kpc. Check: doubling the nodes must change
  σ̂ by less than 0.01 kpc on the data; otherwise the grid is doubled until it does.
- **Version (i), R22 as written.** L_i = ∫ n_i(ϖ) N(ϖ_corr,i; ϖ, σ_ϖ,i) dϖ / ∫ n_i(ϖ) dϖ, both over
  true distances 1–30 kpc. R22's eq. 1 needs a range and does not state one; ours is fixed now: the
  query's parallax < 1 mas taken as a range in true distance (1 kpc), and 30 kpc as an outer limit
  beyond which a Gaussian of a few kpc around the Centre contributes nothing.
- **Version (ii), selection on the observed parallax.** With cut_i = min(1 mas, 100·10^(0.2(0.9 −
  (G_i − 1.5(BP − RP_i − 1))))) mas on the raw parallax, and the raw parallax distributed as
  N(ϖ − 0.02, σ_ϖ,i): L_i = ∫ n_i(ϖ) N(ϖ_corr,i; ϖ, σ_ϖ,i) dϖ / ∫ n_i(ϖ) Φ((cut_i − ϖ + 0.02)/σ_ϖ,i) dϖ, over
  0.2–30 kpc. Derivation of the selection term: ϖ is the true (zero-point-corrected) parallax; the raw
  parallax is ϖ_raw = ϖ_corr − 0.02 ~ N(ϖ − 0.02, σ_ϖ,i), so the probability that the raw parallax
  passes the cut is P(ϖ_raw < cut_i) = Φ((cut_i − (ϖ − 0.02))/σ_ϖ,i) = Φ((cut_i − ϖ + 0.02)/σ_ϖ,i). This is
  what "cuts on the raw ϖ" means here. The distance dependence that the BP < 15.5 limit and the
  luminosity cut introduce through the luminosity function is not in this likelihood; the mocks measure
  its effect.
- **Fit.** σ by bounded one-dimensional minimisation (Brent) on 0.5–10 kpc. A data fit within 0.05 kpc
  of a bound is "at the bound": version (i) is then not reproduced and version (ii) undetermined (fit at
  bound). Bootstrap and mock fits at a bound are kept at the bound value.
- **Intervals.** 200 bootstrap resamples of stars (a floor).
- **Reference fits.** Versions (i) and (ii) for −1.5 < [M/H] < −1 and −1 < [M/H] < −0.5, reported only:
  point fits (no bootstrap or mocks), on a fixed random subsample of 50,000 stars where a bin has more
  (seed 12012, stated in the results).
- **Known-answer mocks** (100, a floor), generated before the data are fitted:
  - *Positions.* 3D positions drawn from the model (a spherical Gaussian with σ = 2.7 kpc around the
    Centre) over the query's field (|l| < 30°, |b| < 30°) and true distances 0.5–30 kpc; the likelihood
    integrates over 0.2–30 kpc, which contains this range.
  - *Luminosity function.* The LF sample is the metallicity-file stars with ϖ/σ_ϖ > 10 and [M/H] < −1
    (all metallicities if fewer than 500 such stars). For each LF star, M′ = G − 1.5(BP − RP − 1) +
    5 log10(ϖ_corr/100) and its observed BP − RP are taken; its colour is dereddened with the extinction
    model below at its own (b, d). Each mock star draws one LF star: its M′ and intrinsic colour. We
    assume that the luminosity function does not depend on distance. Limitation: the LF sample already
    passed M′ < 0.9, so stars scattered in from just fainter magnitudes are missing and the bias may be
    understated.
  - *Extinction.* A_G = a·exp(−|b|/b_d)·min(d, 8 kpc)/8 kpc, with A_BP and E(BP − RP) from the Gaia DR3
    extinction coefficients (fixed at implementation, recorded by dated amendment before any fit).
    (a, b_d) are chosen on a fixed grid (a from 0 to 5 mag in steps of 0.05; b_d from 1° to 20° in steps
    of 0.5°): at each grid point one mock is simulated (with the LF dereddened by the same (a, b_d)), and
    the median and 90th percentile of observed BP − RP are compared with the data's metal-poor stars in
    |b| bins 0–5°, 5–10°, 10–20°, 20–30° (8 statistics for 2 parameters); the grid point with the least
    sum of squared differences is kept, ties broken by the smallest a, then the smallest b_d.
  - *Observed quantities.* G and BP from M′, the colour and A at the mock distance; parallax errors drawn
    in 0.25 mag bins of G by resampling the data's σ_ϖ within the bin; then every cut (parallax < 1 mas,
    the luminosity cut, BP < 15.5, 1.0 < BP − RP < 3.5, and any tighter cut declared by L6) applied to the
    simulated observed quantities.
  - *Size.* Mock stars are drawn until the post-cut count equals the data's number of [M/H] < −1.5 stars.
  Both versions are fitted to every mock; the bias is median(σ̂) − 2.7 kpc, with a bootstrap standard
  error over mocks.
- If parallaxes or photometry are missing (L2) and not fetched, T2a and T2b are "undetermined (data not
  in the files)".

### 4.4 T2b

- **Likelihood.** The version (ii) likelihood of section 4.3, conditional on each star's direction,
  applied to the stars at latitude |b| ≥ 5° (variants 3° and 8°, reported); ρ is replaced by each model.
- **Models.** Spherical Gaussian (σ); flattened Gaussian exp(−(x² + y² + z²/q²)/(2σ²)) with q in 0.2–1.5;
  flattened cored power law (r_q² + r_c²)^(−α/2), r_q² = x² + y² + z²/q², with r_c in 0.05–3 kpc, α in
  1–8, q in 0.2–1.5 (Kurbatov et al. 2024's single-component slope 3.4 and Aurora slope 4.5 are quoted
  for comparison).
- **Fits.** Nelder–Mead from 5 starts (the spherical σ̂ with q = 1, and four draws within the parameter
  ranges), the best kept. ΔBIC = 2ΔlnL − Δk·ln N in favour of the more complex model, with N the number
  of stars at |b| ≥ 5° and Δk = 1.
- **Profile interval of q.** q on a grid of step 0.05 over 0.2–1.5 (27 points), σ refitted at each.
  The value at q̂ is the Nelder–Mead flattened fit (σ fitted there); the profile is the grid values plus
  that node, and lnL_max is the larger of that fit and the best grid value. The 95% interval is where
  2Δ = 2[lnL_max − lnL_profile(q)] ≤ 3.84; its ends are found by linear interpolation of 2Δ between
  adjacent nodes. If 2Δ crosses 3.84 more than twice, the interval is [lowest crossing, highest
  crossing], including any interior region above 3.84, and is reported with a flag. If 2Δ stays below 3.84 at q = 0.2 or q = 1.5, that end of the interval is the
  grid edge. Check: lnL_profile(1.0) must equal the
  spherical fit's lnL (to 0.01). Used for the step-1 label on the data and in every mock.
- **Bootstrap.** 200 resamples of the |b| ≥ 5° stars, each refitting all three models (5 starts each);
  they give the f₅ interval of whichever model is chosen and the bootstrap q interval reported alongside.
- **Mocks** (100 each, floors), generated as in section 4.3 and cut at |b| ≥ 5°:
  - false positive: q = 1, σ = 2.7 kpc, with a completeness c(b, d) = 1 − 0.5·exp(−(|b| − 5°)/5°)·
    min(d, 8 kpc)/8 kpc applied as a random thinning. c(b, d) is deliberately not in the fitted
    likelihood. The check's scope is robustness to this specified completeness, which falls towards the
    plane and with distance, not to every possible unmodelled selection. If the data's σ̂ (T2a version
    (ii)) differs from 2.7 kpc by more than 0.2 kpc, a second set of 100 false-positive mocks is
    generated at σ̂, and the check must pass in both sets;
  - power: q = 0.5, σ = 2.7 kpc;
  - step 2 (only if step 2 is reached, after step 1 on the data): the best-fitting flattened Gaussian;
    the step-2 label is evaluated in every step-2 mock, whatever its step-1 outcome.
  If the false-positive or the power check fails, step 2 and its mocks are skipped and reported as not
  run.
- **5 kpc fraction.** f₅ = the model's star fraction within r < 5 kpc of the Centre (3D, all directions;
  the power law normalised within 18 kpc).
- **Control population.** Giants with −1 < [M/H] < −0.5 at |b| ≥ 5°, fitted with the same three models
  (5 starts each) and the q profile, point fits only (no bootstrap or mocks), on a fixed random subsample
  of 50,000 stars if there are more (seed 12012); reported only.

### 4.5 T3

- **Quantity.** J_φ/J_tot with J_tot = √(J_R² + J_φ² + J_z²), from the file's actions (sign fixed by L5).
  If the file gives positions and velocities, mean v_φ is reported too, also with R0 = 8.0 and 8.4 kpc;
  the actions themselves are not recomputed.
- **Samples.** Primary: 3 < R_apo < 7 kpc. Variant: all R_apo (its own labels, reported).
- **Statistics.** (a) mean over [M/H] < −2; (b) mean over −1.1 < [M/H] < −0.9; (c) means in 0.2 dex bins
  centred on −2.0, −1.8, …, −0.6 (8 bins), fitted with f = a + (b − a)/(1 + exp(−([M/H] − m)/s)),
  s in 0.01–2 dex, by least squares weighted by the bins' variances; the variances come from a first
  bootstrap pass of 1000 resamples and are then held fixed. Width = 2 ln 9 · |s|. A fit with s at a bound
  or not converged counts as not converged: on the data, T3 (c) is "undetermined (fit failed)"; in a
  bootstrap resample, it is kept at the bound value and the number of such resamples is reported. The
  labelled intervals come from a second pass of 1000 bootstrap resamples (a floor), refitting (c) each time.
- **Known answer w₀.** 100 mocks: each star keeps its [M/H] as the true value, gets J_φ/J_tot = 0 below
  −1.0 and 0.8 above, plus Gaussian scatter with the data's standard deviation in its bin (stars outside
  the 8 bins use the nearest bin's); the observed [M/H] is the true value plus N(0, e) with e the star's
  error if the file gives it (primary), otherwise 0.1 dex (primary when there are no errors), and 0.15,
  0.2 dex (variants); the mock is binned and fitted exactly as the data; w₀ = median width over the 100
  mocks (about 0.30 dex expected for 0.1 dex).

### 4.6 T4

- Variants: (i) [M/H] + 0.1 and − 0.1; (ii) [M/H] plus N(0, 0.1) and N(0, 0.2), 10 noise realisations
  each; (iii) in each 0.25 dex [M/H] bin, remove stars outside the 1st–99th (and, separately, 5th–95th)
  percentiles of T_eff or of log g.
- In each variant (each realisation in (ii)): T1 counts (elasticity); T2a σ in both versions, as point
  estimates on the variant's [M/H] < −1.5 sample (no new mocks or bootstrap); the T3 (a) and (b) labels of
  the primary sample (1000 new bootstrap resamples); the T6 mass with R22's choices. In variant (ii), σ
  and the mass are the medians over the 10 realisations, and a T3 label counts as changed if it differs
  from the baseline in at least 6 of them.
- Elasticity: Δln N per 0.1 dex shift; the slope-only prediction is ln 10 × (d log10 N/d[M/H]) at the
  cut, from the observed cumulative distribution over ±0.2 dex.

### 4.7 T5

Fractions g and a₅ over the joined kinematics stars with [M/H] < −1.5 (variants −1.9 < [M/H] < −1.2 and
[M/H] < −1.2), 1000 bootstrap resamples (a floor). The RVS, ϖ/σ_ϖ ≥ 5 and δv_RVS < 5 km/s selection
favours the near side of the Centre and so biases R_apo; this is stated with the result. The effect of
removing the g stars on the T1 count and the T6 mass is reported, extrapolating the RVS-subsample
fraction to the whole tail (an assumption).

### 4.8 T6

- N: N(< −1.5) from T1, and N × (1 − g) with g from T5.
- m_giant: 800 M☉ (R22), 1,000 and 2,000 M☉ (our reading of the M4 numbers).
- f_bright: the fraction of the [M/H] < −1.5 stars with ϖ_corr/σ_ϖ > 5 whose colour-corrected
  M_G = G − 1.5(BP − RP − 1) + 5 log10(ϖ_corr/100) is below 0.5 (the ϖ/σ_ϖ cut biases this towards
  nearer stars; stated); without parallaxes or photometry, f_bright = 1 and "not computed".
- f: 1 and 2.5.
- Output: a table of M for every combination, and whether R22's choices (N(< −1.5), 800, f_bright = 1,
  2.5) give at least 5×10⁷ M☉.

### 4.9 Explorations (no verdict)

Entries for README section 8, run with `python -m astrolab explore`, not part of the formal run:
σ per [M/H] bin (−2.5 to −2, −2 to −1.5, −1.5 to −1); an exponential slope fitted to the counts below
[M/H] = −2, compared with Chen et al. 2025's k ≈ 0.6–2.0 (only about 0.5 dex of their range overlaps);
J_φ/J_tot against [M/H] next to the old-disc regime ("older than the disc" cannot be tested here); the
metal-poor stars split by T5 orbit class, compared in extent and rotation (the proto-Galactic reading
cannot be tested here).

### 4.10 Cost and order

- **Order.** Download (once, under the budget exception) → L1–L7 → the extinction grid → the T2a
  known-answer mocks and the T2b false-positive and power mocks (they use the data's directions,
  magnitudes, colours and errors, but fit no model to the data's parallaxes) and the T3 w₀ mocks → T1 →
  T2a → T2b step 1 on the data → T2b step-2 mocks (only if step 2 is reached) → T2b step 2 → T3 → T5 →
  T6 → T4.
- **Cost.** A likelihood evaluation over about 20,000 stars × 300 nodes takes of order 0.1 s; a
  one-parameter fit about 25 evaluations, a two-parameter fit about 150, a three-parameter fit about 300
  (each per start).
  - Extinction grid: 101 × 39 ≈ 3,900 simulated mocks (no likelihood), about 1 hour.
  - T2a: 2 versions × (1 + 200 bootstrap + 100 mocks) one-parameter fits, about 30 minutes.
  - T2b bootstrap: 200 × (25 + 5 × 150 + 5 × 300) ≈ 455,000 evaluations, about 12.5 hours.
  - T2b mocks: per mock, the spherical fit, the flattened fit (5 starts) and the q profile (27 × 25);
    200 mocks ≈ 300,000 evaluations, about 8.5 hours; step-2 mocks (if reached) add the power-law fit,
    100 × (5 × 150 + 5 × 300) ≈ 225,000 evaluations, about 6 hours.
  - T3 (two bootstrap passes, 100–300 w₀ mocks), T1, T5, T6: minutes. T4: about 8 variants (10
    realisations in (ii)) × (2 one-parameter fits + T3), about 1 hour.
  - Reference fits and control population (point fits on at most 50,000 stars, about 0.25 s per
    evaluation): 2 bins × 2 versions × 25, plus 3 models × 5 starts and the q profile, about 3,000
    evaluations, about 15 minutes.
  - Second false-positive set (only if the data's σ̂ differs from 2.7 kpc by more than 0.2 kpc): 100 ×
    (25 + 5 × 150 + 27 × 25) ≈ 145,000 evaluations, about 4 hours.
  - Total about 30 hours on one core, or about 34 hours with the second false-positive set (the upper
    bound); if the false-positive or power check fails, step 2 and its mocks are not run (about 24–28
    hours). A short timing run measures it before the formal run.
- **Floors.** 200 bootstrap resamples (T2a, T2b), 1000 per pass (T3), 1000 (T5); 100 mocks per check
  (T2a, T2b, T3 w₀). These are not reduced. Because the projected time exceeds 12 hours, the run is
  checkpointed and continued in later idle periods; the counts stay.
- **Scheduling.** The formal run waits until no other study is running.
- **Results** (`results/`): `load.json`, `t1.json`, `t2.json`, `t3.json`, `t4.json`, `t5.json`,
  `t6.json`, `summary.json`, each below 1 MB (binned or summarised; no per-star tables).

### 4.11 Systematics we know about but do not test

- Purity of the metal-poor tail against independent spectroscopy (`gap_pure`): no unbiased
  spectroscopic subset is available (APOGEE is the training set; PIGS was pre-selected as metal-poor;
  GSP-Spec does not reach low [M/H]).
- The full selection function (dust map, crowding, XP completeness) beyond the latitude cut and the
  mock extinction model; the T2a bias gate is tested at σ = 2.7 kpc only.
- R22's potential, used for the actions and orbital parameters, taken as given.
- Ages and α abundances (not in the files).

### 4.12 Amendments before any fit (2026-11-21)

Implementation choices fixed on 2026-11-21 while writing `run.py` and its helper modules, before any data
file was downloaded or read (no fit has been made). Sections 1–4.11 are unchanged; where they leave a
detail open, it is fixed here. (This subsection replaces the earlier placeholder "4.12 Amendments before the
run: None yet.")

1. **L2 column names.** A column name is reduced to lower-case letters and digits ("[M/H]" → "mh",
   "phot_g_mean_mag" → "photgmeanmag") and compared with fixed candidate lists in `data012.py`
   (`MH_CANDIDATES`, `KIN_CANDIDATES`; for example [M/H]: mh, mhxgboost, mhxgb, xgbmh, xgboostmh, mhpred, mhxp,
   metallicity, feh; J_φ: jphi, lz, actphi, actionphi, jphikpckms; R_apo: rapo, apo, apocenter, apocentre, rmax).
   Several matches for one quantity, or no `source_id` or [M/H], stop the run (section 3, L2). T_eff and log g
   are needed only for T4 variant (iii), which is "not computed" without them.
2. **Positions.** If the metallicity file has no l, b but has ra, dec, l and b are computed with astropy
   (ICRS to Galactic). l is used in (−180°, 180°].
3. **L6 detection.** Histograms run over the populated range inside R22's allowed range, with bin edges at
   multiples of the bin width. A cut at c is declared where the outermost populated bin on one side has at
   least 50 stars and every bin beyond it, up to the end of the allowed range, is empty (an empty bin inside
   the populated range is a hole, not a cut; R22's own limits are range ends, not cuts). L6 uses all stars of
   the metallicity file and the raw parallax. Every declared cut with a value (including parallax-dependent
   ones) is applied in the mocks (section 4.3, "any tighter cut declared by L6").
4. **T2 sample and grid.** Stars with a non-finite l, b, ϖ, σ_ϖ, G or BP − RP, or σ_ϖ ≤ 0, are left out of the
   T2 likelihoods and counted (`t2.json: sample.n_dropped_nonfinite`). Metallicity bins are lo ≤ [M/H] < hi.
   The integrals are trapezoid sums in parallax over the log-spaced nodes; version (i) has its own 300 nodes
   log-spaced over 1–30 kpc, version (ii) 300 over 0.2–30 kpc. The node-doubling check is applied to both
   versions and stops at 1,200 nodes (memory: about 0.4 GB per likelihood at 20,000 stars); if it has not
   converged there, `t2.json: grid_check.passed` is false. Convergence is recorded per version
   (`grid_check.converged`): if version (i) has not converged, T2a's reproduction label is "undetermined (grid
   not converged)"; if version (ii) has not, T2a's σ of the population, T2b's shape and f₅ and T4's σ condition
   are (T4 is then that label unless another condition makes it "sensitive"). Either way both readings carry
   `pending_amendment` (with the reason codes `grid_not_converged_i` / `_ii`) and wait for a dated amendment. The
   mocks are fitted at 300 nodes before the data fit (section 4.10 order); if the check adopts more nodes,
   every mock is regenerated from its seed and refitted at the adopted number. The parallax Gaussian of each
   star is stored relative to its largest node (its logarithm kept separately), so a parallax outlier does not
   underflow in the single-precision matrices.
5. **Luminosity function.** The LF sample's ϖ/σ_ϖ > 10 uses the raw parallax (section 4.1: cuts on the raw ϖ).
   Each LF star's M′ is turned into an intrinsic M_G0 = M′ + 1.5(BP − RP − 1) − A_G, intrinsic colour
   BP − RP − E(BP − RP) and intrinsic BP − G, with the extinction model at its own (b, d = 1/ϖ_corr). A mock
   star at distance d gets G = M_G0 + μ(d) + A_G, BP − RP = colour₀ + E(BP − RP), BP = G + (BP − G)₀ + (A_BP − A_G).
   This needs BP magnitudes in the file (the mocks apply BP < 15.5); without them the run stops at L2 like the
   other missing T2 columns. The optional TAP addition of section 3 therefore also fetches
   `phot_bp_mean_mag` (documentation only: the addition is still made only with the user's agreement).
6. **Extinction coefficients.** Constant ratios A_G : A_BP : A_RP = 0.789 : 1.002 : 0.589 per unit A_V
   (Wang & Chen 2019, ApJ 877, 116), so A_BP = 1.270 A_G and E(BP − RP) = 0.523 A_G. This simplifies the
   colour-dependent Gaia DR3 law.
7. **Extinction grid.** Each grid point simulates one spherical mock at σ = 2.7 kpc with as many stars as the
   T2 sample, all grid points with the same random seed (common random numbers, so the comparison between
   grid points is not dominated by mock noise). The |b| bins are [lo, hi). A statistic missing in the mock or
   the data but not both (an empty |b| bin) adds a penalty of 100 instead of being dropped. Finished rows of
   the grid (one value of a) are checkpointed, so a pause loses at most one row.
8. **Mock parallax errors.** σ_ϖ is resampled from all stars of the metallicity file in the mock star's 0.25 mag
   G bin (the nearest populated bin if it is empty); the raw parallax is 1/d − 0.02 + N(0, σ_ϖ).
9. **T2b fits.** Nelder–Mead with bounds (xatol 10⁻⁴, fatol 10⁻⁴, at most 3,000 evaluations per start); σ of the
   flattened Gaussian on 0.5–10 kpc as in T2a. The power law's first start is r_c = 1 kpc, α = 3.4, q = the
   flattened fit's q; the four other starts of every model are uniform draws within its ranges. ΔBIC uses the
   number of stars fitted (the data's |b| ≥ 5° stars, or the mock's size). T2b mocks have as many stars as the
   data at |b| ≥ 5°. The data's power-law fit is always made and reported; it is labelled only at step 2. The
   latitude variants (3°, 8°) are point fits of the three models with the q profile, reported only. The
   bootstrap resamples the |b| ≥ 5° stars. The data's power-law fit is made together with the step-1 fits,
   before the step-2 mocks (section 4.10 lists step 2 after them); the step-2 mocks are drawn from the
   flattened-Gaussian fit and do not depend on the power-law fit, so the order does not change any number.
10. **Bounds.** σ is "at a bound" within 0.05 kpc of 0.5 or 10 kpc (section 4.3); the logistic s is at a bound
    within 0.1% of 0.01 or 2 dex.
11. **T3 bootstrap.** Each resample of the N stars of a T3 sample draws K ~ Binomial(N, n/N) stars uniformly
    from the n stars with [M/H] < −0.5 (the only ones any T3 statistic uses); this equals resampling all N in
    distribution. Bins are [c − 0.1, c + 0.1).
12. **Logistic fit.** Bins without stars or with zero bootstrap variance are left out; fewer than 5 usable bins
    count as not converged. Starting values: a and b the means of the first and last two bins, m = −1.2, s = 0.1
    (bounded trust-region least squares, `scipy.optimize.least_squares`). If no bootstrap resample gives a
    width, T3 (c) is "undetermined". T1's total counts the rows with a finite [M/H]; rows without one are
    reported (`t1.json: counts.n_nonfinite_mh`).
13. **w₀ mocks.** Made on the primary sample; mock J_φ/J_tot values are not clipped to [−1, 1]; the all-R_apo
    variant uses the primary w₀. The per-bin scatter is the standard deviation of the data's J_φ/J_tot in the
    bin of the star's [M/H].
14. **v_φ.** From the file's v_φ column, or from Galactocentric x, y, v_x, v_y, with the sign set so that the
    median of the [M/H] > −0.5 stars is positive. The R0 = 8.0 and 8.4 kpc variants are recomputed with
    astropy from heliocentric ra, dec, ϖ + 0.02, proper motions and radial velocity when the kinematics file
    has them (z☉ = 0, solar motion (11.1, 245, 7.3) km/s), otherwise "not computed".
15. **T4.** Noise is drawn per star of the metallicity file and the joined kinematics stars inherit it. Trimming
    keeps T_eff and log g within the percentiles (inclusive) of each 0.25 dex bin. The elasticity is reported at
    the cuts −2, −1.5 and −1. The "dominated by scatter from above" flag uses the median count over the ten
    0.1 dex realisations, a change by more than a factor 2 either way.
16. **Running.** Seeds: a base seed 20261121 with a named stream per task, and 12012 for the subsamples. The
    Zenodo URLs with `?download=1` were confirmed on the record page on 2026-11-21. The two files are fetched
    with `cap_consent` and `budget_consent` (both citing T-021 and this study's log); `allow_download` is true only
    when `PARAMS["first_download"]` is set (section 8). A formal run refuses counts below the floors of section
    4.10, a partial run (`parts` other than all six) and grid sizes other than the pre-registered ones. A paused
    run continues from its checkpoints: the checkpoint key hashes the effective PARAMS without the run-only keys
    (including `first_download`), the helper modules and `run.py` without its PARAMS literal, and the files'
    checksums. Each restart computes at least one checkpointed unit before the time guard can pause it. If L2
    finds T2 columns missing, the run stops and asks for the user's decision on the optional TAP
    addition (`PARAMS["t2_missing_ok"]` is set only if the user declines it).

### 4.13 Amendments after the download, before any fit (2026-11-23)

The formal first run of 2026-11-23 downloaded the two files (L1: both MD5s match) and stopped at L2. **Seen
before this amendment:** the column headers of both files (metallicity file: `source_id, ra, dec,
teff_xgboost, logg_xgboost, mh_xgboost_rgb`; kinematics file: `source_id, x, y, z, v_x, v_y, v_z, j_r, j_phi,
j_z, r_apo, ecc`), the first data row of each, and, to size the TAP addition for the user, the number of rows
of the metallicity file and of stars below three [M/H] values (1,586,888 rows; 469,041 below −0.5, 100,458
below −1.0, 30,589 below −1.5; no non-finite [M/H]). No other value was looked at and no fit was made.
The count below −1.5 is T1's own N(< −1.5) and an input of T6; it was seen before the formal run, and no
rule or threshold is changed here (T1's and T6's rules are those of sections 2 and 4.2, 4.8).
Sections 1–4.12 are unchanged except as stated here.

1. **L2 name of [M/H].** `mh_xgboost_rgb` (normalised `mhxgboostrgb`) is added to the [M/H] candidates in
   `data012.py`. It is the file's only metallicity column, and no other column matches any [M/H] candidate, so
   the mapping is not ambiguous. The kinematics columns map with the existing lists.
2. **The user's decision on the TAP addition.** The metallicity file has no ϖ, σ_ϖ, G, BP − RP or BP; it has
   ra, dec (l, b by 4.12 item 2). On 2026-11-23 the user agreed in chat to the full addition (offered: the
   full addition, the [M/H] < −1.5 stars only, or none). `PARAMS["gaia_addition"]` is true; `t2_missing_ok`
   stays false.
3. **The addition as run.** `gaiadr3.gaia_source`, columns `source_id, parallax, parallax_error,
   phot_g_mean_mag, bp_rp, phot_bp_mean_mag`, for the stars with [M/H] < −0.5 after L3 (469,041), on sorted
   `source_id` lists of 2,000 (235 queries) through `ctx.tap`, charged to the study budget. Against
   section 3's row: (a) `phot_bp_mean_mag` is fetched, as 4.12 item 5 already states; (b) l and b are not
   fetched: they come from the file's ra, dec for every star (4.12 item 2); (c) there is no `ctx.count`: a
   query lists at most 2,000 distinct `source_id`s and `gaia_source` has one row per `source_id`, so it
   returns at most that many rows, and `max_rows` is set to the list length so the guard refuses anything
   larger; the total is bounded by 469,041 rows × 6 columns (about 23 MB as 8-byte values). A count per
   list would double the number of queries and add nothing.
4. **Stars without the columns.** Stars with [M/H] ≥ −0.5 get no ϖ or photometry (NaN), and stars the
   archive does not return (none expected) are left out by 4.12 item 4; the numbers are recorded
   (`load.json: L2.addition`). A duplicated `source_id` in the reply, or one not asked for, stops the run.
   Every test that uses these columns selects stars below −0.5 (the T2 sample below −1.5, the reference fits
   −1.5 to −0.5, the T2b control −1.0 to −0.5, the LF below −1.0, T6 below −1.5), except two inputs that
   section 3 and 4.12 define on all stars of the file, which now use the stars with [M/H] < −0.5: L6's
   histograms of ϖ, ϖ/σ_ϖ, BP and BP − RP and the ϖ/σ_ϖ < 1 fraction rule (4.12 item 3; l and b still
   use every star; the fraction on this subset can differ from the whole file's in either direction), and the mock
   parallax-error sampler of 4.12 item 8 (and the LF fallback "all metallicities" in `run.mock_inputs`).
   T4's noise variants select the T2 sample on perturbed [M/H]; a star from [M/H] ≥ −0.5 scattered below
   −1.5 (a 5σ jump at 0.2 dex, about 0.3 stars expected) has no parallax and is left out.
5. **When.** The queries run before 2026-11-25, when the Gaia archive goes offline until the DR4 release
   day; their results are cached (Gaia DR3 does not change), so later runs and explorations read the
   cache. If they cannot finish in time, the run is repeated after the release day with nothing changed
   (completed queries stay cached). While the archive is offline, `--refresh` must not be used: it would
   query all 235 lists again and fail.
6. **Code and tests.** `run.gaia_addition` (called from the load step after L3, before l and b are
   computed); `test_s012_run.py`: `test_gaia_addition` (only [M/H] < −0.5, sorted, each id once, lists of
   at most the chunk size with `max_rows` equal to the list length, an unmatched id recorded, the pipeline
   completes on the merged columns), `test_gaia_addition_duplicate_stops` and
   `test_gaia_addition_unasked_id_stops`.
7. **f_bright without photometry (gate-2 review of this amendment).** The archive can return a parallax with
   no G or BP − RP. Such stars are left out of f_bright (section 4.8) instead of counting as faint, and the
   number of them among the stars passing f_bright's ϖ_corr/σ_ϖ > 5 cut is recorded (`t6.json`:
   `n_no_photometry`); T2 already leaves them out (4.12 item 4). The mock parallax-error sampler (4.12 item 8)
   needs only G and σ_ϖ, so stars without BP or BP − RP stay in it (`err_stars` counts its stars).
8. **Service (2026-11-23, after this amendment passed review).** The first live query found the ESA Gaia
   archive already in its downtime (every TAP request returned an "ESDC Archives downtime" page, two days
   before the announced 2026-11-25). The addition is therefore served by NOIRLab Astro Data Lab's mirror of
   the same table (`ctx.tap` service `datalab`, table `gaia_dr3.gaia_source`, same column names; the values are
   Gaia DR3's, not compared with the ESA archive here because it is offline). This replaces item 3's table
   and item 5's timing for the addition (the `--refresh` caution of item 5 now concerns only the two Zenodo
   files); everything else in items 3–7 is unchanged. Every id comes from Gaia DR3, so `n_unmatched` is
   expected to be 0; a non-zero count would point to an incomplete mirror. Seen while testing the mirror
   (two queries through `fetch.tap`: the first 5 ids, 39 s, and the first 2,000-id list, 5.7 s): the six
   columns of the first three stars, and, as a check for sentinel values on that cached list, the ranges of
   the five columns (no NULL; σ_ϖ > 0; G 8.1–15.4, BP − RP 1.00–3.47, BP ≤ 15.50, ϖ −1.11 to 0.97 mas). The
   run reuses that cached list, so its provenance entry carries the diagnostic's note; the others record the
   mirror.

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
| `parts` | which tests to run (`t1` always; `t2`, `t3`, `t4`, `t5`, `t6`) | any subset; `["t1", "t3", "t5", "t6"]` runs in minutes | cache only |
| `t2_mh_range` | [M/H] range of the T2 sample (lo ≤ [M/H] < hi) | e.g. `[-2.5, -2.0]`, `[-2.0, -1.5]`, `[-1.5, -1.0]` (σ per bin, section 4.9) | cache only |
| `t2a_boot`, `t2a_mocks`, `t2b_boot`, `t2b_mocks` | bootstrap resamples and mocks of T2 | an exploration may lower them (a formal run may not) | cache only |
| `t2b_bmin_deg` | latitude cut of T2b | 3–10 | cache only |
| `R0_kpc`, `plx_zp_mas` | Galactocentric distance of the Sun; parallax zero point | 8.0–8.4; 0.0–0.04 | cache only |
| `t3_rapo_kpc`, `t3_bin_centers`, `t3_delta` | T3 apocentre range, bins, equivalence margin | apocentre ranges within 1–15 kpc | cache only |
| `t4_noise_dex`, `t4_shift_dex` | T4 noise and shift | 0.05–0.3 | cache only |
| `t6_m_giant`, `t6_f` | T6 mass per giant and factor | any positive | cache only |
| `stop_after_hours` | pause (checkpointed) after this many hours; 0 = no limit | 0–24 | cache only |
| `gaia_addition` | fetch the missing T2 columns from Gaia DR3 for [M/H] < −0.5 (section 4.13) | true (user consent 2026-11-23); false with `t2_missing_ok` = true is the decline route. Since only [M/H] < −0.5 has parallaxes, `t2_mh_range`, `control_mh` and `ref_bins` above −0.5 leave no stars | cache after the first run (about 23 MB, 235 queries) |
| `first_download` | allow the one consented download of the two Zenodo files | `false` except in the single formal first run | new data: 213.8 MB, only with the user's recorded consent |

- **The first download.** The two files are downloaded once, under the user's exception of 2026-11-21 (T-021,
  `log.md`). The formal first run is started with `PARAMS["first_download"] = True` (`allow_download=True` in
  `ctx.http`); right after that run the value is set back to `False` and the change committed, so every later run
  and exploration reads the files from the cache only (`budget_consent` without `allow_download`). If the cache
  has evicted a file, a new download needs the user's agreement again (AGENTS.md 1.6); `--refresh` raises
  instead of re-downloading.
- Rerun with an override: `python -m astrolab explore 012-m12-poor-old-heart --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed). Loading and the L1–L7 checks take a few minutes on the
  1.5 million rows; `parts=["t1","t3","t5","t6"]` then runs in minutes, while T2 needs hours (an evaluation of the
  likelihood takes about 0.08–0.14 s at 20,000 stars and 300 nodes). Explorations keep their checkpoints in the
  cache under `s012_checkpoints/explore/<date>-<topic>/` (delete them when done), apart from the formal run's.
  Resetting `first_download` to `False` does not change the checkpoint key, so a formal run paused after the
  download continues from its checkpoints.
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 012-m12-poor-old-heart --tag <topic> --script explore/<name>.py`.
- Results files and keys: `load.json` (L1–L7: `L1` checksums, `L2` column mapping and presence, `L3_*`
  duplicates, `L4` join fraction, `L5` signs and units, `L6` declared cuts, `L7` [M/H] range); `t1.json`
  (`counts`, `statements` with count and fraction labels, `pairs`, `summary`); `t2.json` (`t2a`: `fits`,
  `intervals`, `mock_bias`, `reproduction_label`, `population_label`, `reference_fits`; `t2b`: `checks`, `data`
  with the step-1 fits and q profile, `step2`, `shape_label`, `f5`, `f5_interval`, `f5_label`,
  `latitude_variants`, `control`; `mocks`: LF, extinction grid; `grid_check`); `t3.json` (`primary`, `all_rapo`
  with intervals and labels, `w0`, `vphi`); `t4.json` (`label`, `broken`, `variants`, `elasticity`); `t5.json`
  (`samples` with g and a₅); `t6.json` (`table`, `r22_choices_mass`); `summary.json` (`labels`,
  `reading_reproduction`, `reading_robustness`, `timing`).
- Example questions:
  - "Is the extent different for the most metal-poor stars?" → `--set t2_mh_range=[-2.5,-2.0] --set parts=["t2"]`
    with fewer mocks (section 4.9, no verdict).
  - "Does the rotation trend depend on the apocentre range?" → `--set t3_rapo_kpc=[1.0,5.0] --set parts=["t3"]`.
  - "How does R0 change σ?" → `--set R0_kpc=8.0 --set parts=["t2"]`.
  - "How steep is the tail below −2?" (Chen et al. 2025) → a script `explore/tail_slope.py` fitting an
    exponential to the counts below −2.
  - "Do the GSE-like stars rotate differently?" (section 4.9) → a script splitting the T3 sample by the T5 orbit
    classes.
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.
