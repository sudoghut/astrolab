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
  reason (for example "data not in the files", "method bias", "unmodelled selection").
- Labels are checked in the order written; the first that applies is the label.

| Test | Quantity | Labels (decision rules) |
|---|---|---|
| **T1** recount | counts in the metallicity file: N([M/H] < −2), N(< −1.5), N(−2.7 < [M/H] < −1.5), N(< −1), total N. R22's statements and their samples: abstract (∼18,000 for −2.7 < [M/H] < −1.5; sample 2 million); Section III.2 (>4,000 below −2; ∼18,000 below −1.5; almost 100,000 below −1; no sample named); Fig. 4 caption (∼5,000; ∼20,000; nearly 100,000; sample ∼1.7 million); Section IV (∼20,000 below −1.5; ∼70,000 below −1; sample ∼2 million) | For each statement, a **count label** (our count against R22's number) and, where a sample is named, a separate **fraction label** (our count / our total × R22's sample size, against R22's number); each **agrees** or **disagrees**. "∼X" agrees if within X ± 5%; "almost/nearly 100,000" agrees if within 90,000–99,999; ">X" agrees if above X. A statement whose named sample differs from our total by more than 5% is also marked **sample differs** (the abstract always will). **Summary:** **abstract reproduced** if the abstract's count label agrees; **not reproduced** otherwise; its fraction label is reported next to it. For each inconsistent pair (18,000/20,000; >4,000/5,000; 100,000/70,000) we report which the file supports by count label: one, both, or neither |
| **T2a** σ_RGC | maximum-likelihood σ of a spherical Gaussian in Galactocentric radius for the [M/H] < −1.5 stars, in version (i) (R22's eq. 1 as written) and version (ii) (selection on the observed parallax), section 4.3; 200 bootstrap resamples; 100 known-answer mocks at σ = 2.7 kpc | **Reproduction** (version (i)): **reproduced** if σ̂ is within 2.4–3.0 kpc; **not reproduced** otherwise. **σ of the population** (version (ii)): **undetermined (method bias)** if the median mock bias of version (ii) exceeds 0.1 kpc in absolute value, whatever the interval; **undetermined (unmodelled selection)** if the load check L6 finds a parallax-dependent cut that is not in the likelihood; otherwise **consistent with 2.7 kpc** if the 95% interval lies within 2.4–3.0 kpc, **different** if it lies entirely outside, **undetermined** otherwise. Reported next to the labels: the mock bias distribution of both versions (median and its bootstrap standard error), version (ii) − (i), and the reference fits for −1.5 < [M/H] < −1 and −1 < [M/H] < −0.5. If parallaxes are missing from the files and not fetched: both labels **undetermined (data not in the files)** |
| **T2b** shape and 5 kpc | within version (ii), stars at Galactic latitude 5° or more from the plane: step 1, spherical against flattened Gaussian (q free); step 2, if step 1 prefers flattened, flattened Gaussian against flattened cored power law. Mock checks (100 each): false positive (q = 1 with a completeness falling towards the plane), power (q = 0.5), step 2 (best flattened Gaussian) | **Step 1:** **flattened preferred** if 2ΔlnL > 10 and the 95% bootstrap interval of q lies entirely below 0.8; **spherical adequate** otherwise. **Step 2:** **power law preferred** if ΔBIC > 10 in its favour; **flattened Gaussian adequate** otherwise. **Undetermined** if any applicable check fails: fewer than 80 of 100 false-positive mocks give "spherical adequate", fewer than 80 of 100 power mocks give "flattened preferred", or (when step 2 is reached) fewer than 80 of 100 step-2 mocks give "flattened Gaussian adequate"; the step-2 check applies only when step 2 is reached. Pass counts are reported with their binomial errors (a rough calibration). **5 kpc:** the fraction f₅ of the preferred model's stars within a 3D radius of 5 kpc of the Centre (power law normalised within 18 kpc; the spherical model when the shape is undetermined; undetermined when T2a version (ii) is): **most within 5 kpc confirmed** if the 95% interval of f₅ lies entirely above 0.5; **not confirmed** if entirely below; **undetermined** otherwise |
| **T3** rotation | J_φ/J_tot from the kinematics file, joined on `source_id`; primary sample 3 < R_apo < 7 kpc; 1000 bootstrap resamples. (a) the mean over all stars with [M/H] < −2; (b) the mean for −1.1 < [M/H] < −0.9; (c) the 10–90% width of a logistic fit to the means in 0.2 dex bins centred on −2.0, −1.8, …, −0.6. Known-answer width w₀ (section 4.5) | **(a)**, in this order, δ = 0.05: **no net rotation** if the interval lies within [−0.05, 0.05]; **net rotation** if its lower end is above 0; **net counter-rotation** if its upper end is below 0; **undetermined** otherwise. **(b)** **rotation dominated** if the interval lies entirely above 0.5; **not rotation dominated** if entirely below 0.5; **undetermined** otherwise. **(c)** **sharp** if the width interval lies entirely below w₀ + 0.1 dex; **gradual** if entirely above max(0.4 dex, w₀ + 0.1 dex); **undetermined** otherwise; w₀ is the primary one (from per-star [M/H] errors if the file gives them, otherwise from a 0.1 dex blur), the 0.15 and 0.2 dex variants are reported. The all-R_apo sample is reported as a variant with its own labels |
| **T4** leverage of the metallicity scale | under variants (i) [M/H] ± 0.1 dex; (ii) added Gaussian noise of 0.1 and 0.2 dex; (iii) T_eff–log g edge removed within each 0.25 dex [M/H] bin (1st–99th and 5th–95th percentiles): T2a version (ii) σ (version (i) reported), the T3 labels, and the T6 mass with R22's own choices. Counts: elasticity Δln N per 0.1 dex against the slope-only prediction from the observed metallicity distribution | **robust** if, in every variant, σ changes by less than 0.3 kpc, every T3 label is unchanged, and the T6 mass (R22's choices) changes by less than a factor 3; a change into or out of "undetermined" in a downstream label counts as a change; the σ condition is skipped, and this is stated, when T2 is undetermined for missing data in the baseline. **sensitive** otherwise, naming the variants and quantities. Counts carry no label; a count that changes by more than a factor 2 in variant (ii) at 0.1 dex is flagged "dominated by scatter from above" (a heuristic) |
| **T5** GSE and halo stars | among the kinematics-file stars with [M/H] < −1.5: the fraction g with e ≥ 0.75 and R_apo ≥ 10 kpc, and the fraction a₅ with R_apo < 5 kpc; variants −1.9 < [M/H] < −1.2 and [M/H] < −1.2; 1000 bootstrap resamples | **g:** **minor** if the interval lies entirely below 0.10; **moderate** if it lies within 0.10–0.25; **major** if entirely above 0.25; **undetermined** otherwise. **a₅:** **most apocentres below 5 kpc confirmed** if the interval lies entirely above 0.5; **not confirmed** if entirely below; **undetermined** otherwise |
| **T6** mass | M = N × m_giant × f_bright × f, section 4.8 | no label: a table of M under each choice, and whether R22's own choices (N(< −1.5), 800 M☉, f_bright = 1, f = 2.5) with our count give at least 5×10⁷ M☉ |

**Overall reading.** Two readings, each formed mechanically from the labels.
- **Reproduction.** **"R22's numbers reproduce from the public sample"** if T1's abstract is reproduced,
  T2a's reproduction label is reproduced, T3 (a) is no net rotation and T3 (b) is rotation dominated.
  **"Not reproduced"** if T1's abstract or T2a's reproduction label is not reproduced. **"Partly
  reproduced"** otherwise, listing the tests.
- **Robustness of R22's picture.** **"Holds under our checks"** if T2a's σ of the population is
  consistent with 2.7 kpc, T2b's 5 kpc fraction is confirmed, T4 is robust, T5's g is minor or moderate
  and a₅ is confirmed. **"Challenged"** if T2a's σ is different, T2b's 5 kpc fraction is not confirmed,
  T4 is sensitive, T5's g is major or a₅ is not confirmed (naming which). **"Undetermined"** otherwise,
  naming the undetermined tests.

T2b's shape label, T3 (c) and T6 are reported separately and do not enter the readings.

**What would change our mind about the method.**
- If the load checks show that the metallicity file is not R22's sample (total below 1.0 million, or
  more than 1% duplicated `source_id`s), the run stops and the reading is fixed by a dated amendment.
- If a known-answer check fails, the label it guards is undetermined, as stated in the table; the bias
  is reported, and a method change is possible only as a dated amendment followed by a new run.
- If the files lack parallaxes or photometry, T2 and the parallax-based part of T6 are undetermined
  unless the user agrees to the server-side addition (section 3).

## 3. Data (with size estimate)

| Input | Source (service / URL) | Selection | Est. rows / size |
|---|---|---|---|
| R22 metallicity file `xp_gc_mh.csv` | Zenodo record 7035810 (version v0.1; concept DOI 10.5281/zenodo.7035809, the one R22 cite), CC BY 4.0, via `ctx.http` (`https://zenodo.org/records/7035810/files/xp_gc_mh.csv`; the exact download URL is confirmed on the record page at implementation), MD5 7257c98622573a4a625571fc973859c5 | all rows | about 1.5 million rows ("1.5 million stars"), 98.5 MB |
| R22 kinematics file `xp_gc_kinematics.csv` | same record, `https://zenodo.org/records/7035810/files/xp_gc_kinematics.csv`, MD5 b220c27aacff1f2f03d5a1f2b5fca147 | all rows | about 1.2 million rows ("1.2 million stars"; R22 Section II.4: about 1.25 million with RVS velocities and ϖ/σ_ϖ ≥ 5), 115.3 MB |
| Optional: Gaia DR3 `source_id, l, b, parallax, parallax_error, phot_g_mean_mag, bp_rp` for the [M/H] < −1.5 stars | Gaia archive TAP, `gaiadr3.gaia_source`, via `ctx.tap`, about 10 queries on `source_id` lists of 2,000, sized first with `ctx.count` | only if load check L2 finds these columns missing, and only with the user's agreement | about 20,000 rows × 7 columns, 1–2 MB |

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
  user's agreement again.
- The optional TAP addition fits the normal budget once the exception is in place; it is an additional
  fetch and is made only with the user's agreement (Gaia archive announced offline 2026-11-25 to 12-02).

**Load-time checks** (before any test; each result is written to `results/load.json`).
- **L1 checksums.** Both MD5s must match. *Failure:* stop.
- **L2 columns.** The columns are mapped by name to `source_id`, [M/H], T_eff, log g (metallicity
  file) and `source_id`, J_R, J_φ, J_z, eccentricity, R_apo, and, if present, positions and velocities
  (kinematics file); the mapping is recorded. Also recorded: whether `l, b`, parallax, its error, G and
  BP − RP are present. *Failure:* without `source_id` or [M/H], stop; without actions, eccentricity or
  R_apo, T3 and T5 are undetermined (data not in the files); without parallaxes or photometry, see the
  optional TAP row.
- **L3 rows and duplicates.** Total rows of each file recorded; duplicated `source_id`s must be below
  1%. *Failure:* stop (section 2).
- **L4 join.** The fraction of kinematics rows whose `source_id` is in the metallicity file is
  recorded; below 99%, the join uses the matched rows and the fraction is stated.
- **L5 units and signs.** Among stars with [M/H] > −0.5 in the kinematics file, the median J_φ must be
  positive and the median R_apo between 2 and 15 (kpc). *Failure:* if J_φ is negative for these stars,
  its sign is flipped and recorded; if R_apo is out of range, its unit is identified from the file's
  header and recorded by dated amendment before any test.
- **L6 cuts between R22's query and the file.** Where the columns exist: minimum and maximum of
  parallax, ϖ/σ_ϖ, |b|, l (folded to ±180°), BP magnitude, BP − RP; compared with R22's query
  (parallax < 1 mas, |b| < 30°, |l| < 30°, BP < 15.5, 1.0 < BP − RP < 3.5, the luminosity cut). A
  parallax-dependent cut not in section 4.3's likelihood (for example a minimum ϖ/σ_ϖ in the
  metallicity file) makes T2a version (ii) "undetermined (unmodelled selection)", unless it is added to
  the likelihood by a dated amendment before any fit.
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
  distance d = 1/ϖ (kpc) and Galactocentric radius R(ϖ). n_i(ϖ) ∝ ϖ⁻⁴ exp(−R(ϖ)²/(2σ²)).
- **Grid.** 300 nodes, log-spaced in distance from 0.2 to 30 kpc. Check: doubling the nodes must change
  σ̂ by less than 0.01 kpc on the data; otherwise the grid is doubled until it does.
- **Version (i), R22 as written.** L_i = ∫ n_i(ϖ) N(ϖ_corr,i; ϖ, σ_ϖ,i) dϖ / ∫ n_i(ϖ) dϖ, both over
  true distances 1–30 kpc (the query's parallax < 1 mas taken as a range in true distance).
- **Version (ii), selection on the observed parallax.** With cut_i = min(1 mas, 100·10^(0.2(0.9 −
  (G_i − 1.5(BP − RP_i − 1))))) mas on the raw parallax, and the raw parallax distributed as
  N(ϖ − 0.02, σ_ϖ,i): L_i = ∫ n_i(ϖ) N(ϖ_corr,i; ϖ, σ_ϖ,i) dϖ / ∫ n_i(ϖ) Φ((cut_i − ϖ + 0.02)/σ_ϖ,i) dϖ, over
  0.2–30 kpc. The distance dependence that the BP < 15.5 limit and the luminosity cut introduce through
  the luminosity function is not in this likelihood; the mocks measure its effect.
- **Fit.** σ by bounded one-dimensional minimisation (Brent) on 0.5–10 kpc; a solution within 0.05 kpc
  of a bound is reported as at the bound and the label is undetermined.
- **Intervals.** 200 bootstrap resamples of stars (a floor).
- **Reference fits.** Versions (i) and (ii) for −1.5 < [M/H] < −1 and −1 < [M/H] < −0.5, reported only.
- **Known-answer mocks** (100, a floor), generated before the data are fitted:
  - positions: a spherical Gaussian with σ = 2.7 kpc around the Centre, restricted to the query's field
    (|l| < 30°, |b| < 30°) and 1–30 kpc;
  - absolute magnitudes and intrinsic colours: drawn jointly from an empirical luminosity function, the
    metallicity-file stars with ϖ/σ_ϖ > 10 and [M/H] < −1 (all metallicities if fewer than 500 such stars),
    after correcting them for extinction with the colour term of R22's cut; variant: an isochrone red-giant
    branch and red clump ([M/H] = −1.5, 12 Gyr), reported only;
  - extinction: A_G = a·exp(−|b|/b_d)·min(d, 8 kpc)/8 kpc, with A_BP and E(BP − RP) from the Gaia DR3
    extinction coefficients (fixed at implementation, recorded by dated amendment before any fit); a and
    b_d chosen so that the mocks' median and 90th percentile of observed BP − RP match the data's
    metal-poor stars;
  - parallax errors drawn from the data's σ_ϖ as a function of G; then every cut (parallax < 1 mas,
    the luminosity cut, BP < 15.5, 1.0 < BP − RP < 3.5) applied to the simulated observed quantities;
  - mock size: the number of data stars with [M/H] < −1.5.
  Both versions are fitted to every mock; the bias is median(σ̂) − 2.7 kpc, with a bootstrap standard
  error over mocks.
- If parallaxes or photometry are missing (L2) and not fetched, T2a and T2b are "undetermined (data not
  in the files)".

### 4.4 T2b

- **Footprint.** Only stars with |b| ≥ 5° (variants 3° and 8°, reported), with the same footprint in the
  normalisation integrals of version (ii).
- **Models.** Spherical Gaussian (σ); flattened Gaussian exp(−(x² + y² + z²/q²)/(2σ²)) with q in 0.2–1.5;
  flattened cored power law (r_q² + r_c²)^(−α/2), r_q² = x² + y² + z²/q², with r_c in 0.05–3 kpc, α in
  1–8, q in 0.2–1.5 (Kurbatov et al. 2024's single-component slope 3.4 and Aurora slope 4.5 are quoted
  for comparison).
- **Fits.** Nelder–Mead from 5 starts (the spherical σ̂ with q = 1, and four prior-range draws), the best
  kept. ΔBIC = 2ΔlnL − Δk·ln N in favour of the more complex model.
- **q interval.** 200 bootstrap resamples of the flattened fit.
- **Mocks** (100 each, floors), generated as in section 4.3 with the footprint:
  - false positive: q = 1, σ = 2.7 kpc, with a completeness c(b) = 1 − 0.5·exp(−(|b| − 5°)/5°) applied
    as a random thinning;
  - power: q = 0.5, σ = 2.7 kpc;
  - step 2 (only if step 2 is reached): the best-fitting flattened Gaussian.
- **5 kpc fraction.** f₅ = the model's star fraction within r < 5 kpc of the Centre (3D, all directions;
  the power law normalised within 18 kpc), with a 95% interval from the bootstrap of the chosen model.

### 4.5 T3

- **Quantity.** J_φ/J_tot with J_tot = √(J_R² + J_φ² + J_z²), from the file's actions (sign fixed by L5).
  If the file gives positions and velocities, mean v_φ is reported too, also with R0 = 8.0 and 8.4 kpc;
  the actions themselves are not recomputed.
- **Samples.** Primary: 3 < R_apo < 7 kpc. Variant: all R_apo (its own labels, reported).
- **Statistics.** (a) mean over [M/H] < −2; (b) mean over −1.1 < [M/H] < −0.9; (c) means in 0.2 dex bins
  centred on −2.0, −1.8, …, −0.6 (8 bins), fitted with f = a + (b − a)/(1 + exp(−([M/H] − m)/s)) by
  least squares weighted by the bins' bootstrap variances; width = 2 ln 9 · s. 1000 bootstrap resamples
  of stars (a floor), refitting (c) each time.
- **Known answer w₀.** 100 mocks: each star keeps its [M/H] as the true value, gets J_φ/J_tot = 0 below
  −1.0 and 0.8 above, plus Gaussian scatter with the data's standard deviation within its bin; the
  observed [M/H] is the true value plus N(0, e) with e the star's error if the file gives it (primary),
  otherwise 0.1 dex (primary when there are no errors), and 0.15, 0.2 dex (variants); the mock is binned
  and fitted exactly as the data; w₀ = median width over the 100 mocks (about 0.30 dex expected for
  0.1 dex).

### 4.6 T4

- Variants: (i) [M/H] + 0.1 and − 0.1; (ii) [M/H] plus N(0, 0.1) and N(0, 0.2), each the median over 10
  noise realisations; (iii) in each 0.25 dex [M/H] bin, remove stars outside the 1st–99th (and,
  separately, 5th–95th) percentiles of T_eff or of log g.
- In each variant: T1 counts (elasticity), T2a σ in both versions (point estimates; no new mocks or
  bootstrap), T3 labels (1000 new bootstrap resamples), T6 mass with R22's choices.
- Elasticity: Δln N per 0.1 dex shift; the slope-only prediction is ln 10 × (d log10 N/d[M/H]) at the
  cut, from the observed cumulative distribution over ±0.2 dex.

### 4.7 T5

Fractions g and a₅ over the joined kinematics stars with [M/H] < −1.5 (variants −1.9 < [M/H] < −1.2 and
[M/H] < −1.2), 1000 bootstrap resamples (a floor). The RVS and ϖ/σ_ϖ ≥ 5 selection favours the near
side of the Centre and so biases R_apo; this is stated with the result. The effect of removing the g
stars on the T1 count and the T6 mass is reported, extrapolating the RVS-subsample fraction to the whole
tail (an assumption).

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

- **Order.** Download (once, under the budget exception) → L1–L7 → T2a and T2b known-answer mocks
  (they use the data's directions, magnitudes and errors, but fit no σ to the data) and the T3 w₀ mocks →
  T1 → T2a → T2b → T3 → T5 → T6 → T4.
- **Cost.** A likelihood evaluation over about 20,000 stars × 300 nodes takes of order 0.1 s; a
  one-parameter fit about 25 evaluations, a two- or three-parameter fit about 150–300. T2a: 2 versions ×
  (1 + 200 bootstrap + 100 mocks) one-parameter fits, about 30 minutes. T2b: 200 bootstrap two-parameter
  fits and 200–300 mocks × 2–3 models, about 3 hours. T3, T5, T1, T6: minutes. T4: about 8 variants ×
  (2 one-parameter fits + T3), under 30 minutes. Total about 4–5 hours on one core; a short timing run
  measures it before the formal run.
- **Floors.** 200 bootstrap resamples (T2a, T2b), 1000 (T3, T5); 100 mocks per check (T2a, T2b, T3 w₀).
  These are not reduced. If the projected time exceeds 12 hours, the run is checkpointed and continued in
  later idle periods; the counts stay.
- **Scheduling.** The formal run waits until no other study is running.
- **Results** (`results/`): `load.json`, `t1.json`, `t2.json`, `t3.json`, `t4.json`, `t5.json`,
  `t6.json`, `summary.json`, each below 1 MB (binned or summarised; no per-star tables).

### 4.11 Systematics we know about but do not test

- Purity of the metal-poor tail against independent spectroscopy (`gap_pure`): no unbiased
  spectroscopic subset is available (APOGEE is the training set; PIGS was pre-selected as metal-poor;
  GSP-Spec does not reach low [M/H]).
- The full selection function (dust map, crowding, XP completeness) beyond the latitude cut and the
  mock extinction model.
- R22's potential, used for the actions and orbital parameters, taken as given.
- Ages and α abundances (not in the files).

### 4.12 Amendments before the run

None yet.

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

- Rerun with an override: `python -m astrolab explore 012-m12-poor-old-heart --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; about N s from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 012-m12-poor-old-heart --tag <topic> --script explore/<name>.py`.
- Results files and keys: TODO (`results/<file>.json`: key - meaning).
- Example questions: TODO (question -> knob or script an agent would use).
- Findings that change what we know go into `log.md` (and, for a paper study, the wiki article)
  on a branch.

