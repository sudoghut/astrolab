# M10 GWTC-4.0 BBH mass spectrum: the 35 Msun feature and the event sample

> 中文：[README.zh.md](README.zh.md)

> Sections 1-4 were written on 2026-11-15 BEFORE run.py and before any data were fetched
> (pre-registration; derived from part 3 of the wiki article
> [Study-007](https://github.com/sudoghut/astrolab/blob/main/docs/wiki/Study-007-gwtc4-bbh-mass-35msun.md)
> and design plan 016). Later edits to them must carry a dated note.

## 1. Question

The GWTC-4.0 population paper (LVK 2026, ApJL 1005, L51, arXiv:2508.18083; "P26") infers the
binary-black-hole (BBH) primary-mass spectrum from 153 events (84 from O4a, 69 from GWTC-3.0) and
reports a feature at 35 M☉ above which the spectrum steepens. The population inference needs
event posteriors and injection sets far beyond this project's data limits (AGENTS.md section 1.5),
so this study works only at the level of the published event summaries:

1. **R1.** Does the 153-event sample follow from the public GWOSC event lists with P26's cuts?
2. **R2 (descriptive).** How many events have median m1 above and below 35 M☉, and how does that
   compare with a single power law (P26's λ1 = 1.7) times a toy selection function with a turnover?
3. **R3 (exploration).** In a point-estimate toy fit, how do the slope difference and a peak at
   35 M☉ depend on the selection turnover?
4. **R4 (descriptive).** Where does GW231123 sit in the rebuilt sample's total-mass distribution?

The Lean argument (`argument/`) decomposes P26's 35 M☉ feature into two routes and four gaps. This
study checks its sample premise (R1) and explores, without decision, the gap on the high-mass
selection function (R2, R3).

## 2. Hypotheses and decision criteria

Tolerances are fixed here and are not changed after results are seen.

**R1 (sample reconstruction).** The rules of section 4, step 2 applied to the GWOSC lists give an O4a
set S_O4a and a GWTC-3.0 set S_O3.

*O4a comparison target.* P26's list in Zenodo `o4a_event_list.tar` is the comparison target only.
Before comparing, the run records the tar's members and the names found in them (pattern
GW\d{6}_\d{6}, or GW\d{6} for old-style names). The target T is the set of those names whose
full GWyymmdd_hhmmss time, converted to GPS, falls in the O4a window (section 4, the same half-open
interval). Names are matched on the GWyymmdd_hhmmss string (a
GWOSC version suffix such as `-v1` is ignored). If T is empty or |T| ≠ 84, the target is ambiguous
and R1 is **"described"** (the members and counts are reported).
Allowed difference (type a): S_O4a may contain extra events whose m2 90% lower bound lies in
(3, 5] M☉ (the 5th percentile used as a proxy for P26's 1% lower limit can only add events).
**O4a part reproduced** if T ⊆ S_O4a and every extra is of type (a), with at most 2 extras.

*GWTC-3.0 part.* No published list of the 69 events is used; the count is the criterion.
Allowed difference types: (i) the mass proxy (adds events, as above); (ii) events with FAR < 1/yr
missing from both the confident and the marginal GWOSC lists (removes events; not measurable here: a
shortfall is noted as possibly type ii or iii); (iii) PE or FAR version differences between the GWOSC lists and the
values P26 used (reported per event when a GWTC-2.1 and a GWTC-3 entry disagree). **GWTC-3.0 part
reproduced** if |S_O3| = 69 ± 2, and, when |S_O3| > 69, the number of S_O3 events with an m2 90% lower
bound in (3, 5] M☉ is at least |S_O3| − 69 (a shortfall of 1 or 2 passes without attribution); the
named checks below must all pass. Named checks (each must be excluded, with the reason recorded): GW170817, GW190425,
GW190814, GW190917_114630, GW190426_152155, GW200105_162426, GW200115_042309. An event excluded
because it has no PE masses in the lists counts as "excluded (no PE)", not as a failed check.

**R1 verdict:** "not reproduced" if the GWTC-3.0 part fails or the O4a part fails with an
unambiguous target; "described" if the GWTC-3.0 part is reproduced and the O4a target is ambiguous
(the O4a part is then reported descriptively); "reproduced" if both parts are reproduced. Every
difference is listed. The FAR cut uses GWOSC's
top-level `far`, documented as the lowest FAR over search pipelines (event-portal documentation;
checked on GW150914). The list JSONs carry no per-pipeline FAR, so this rests on the documentation;
GWOSC's minimum may include a pipeline P26 did not use, which would show up as an extra outside
type (a) and give "not reproduced".

**R2 (descriptive, no verdict).** Sample (also for R3 and R4): T ∪ S_O3 when the O4a part is
reproduced, so that the O4a events are exactly P26's (any allowed type-a extras are dropped);
otherwise S_O4a ∪ S_O3. Events with median m1 outside [10, 100] M☉ are excluded from R2 and R3 and counted
(GW231123, m1 ≈ 137 M☉, is one). N_lo = number with median m1 in [10, 35) M☉, N_hi = number in
[35, 100] M☉. Observed-frame density p(m1) ∝ m1^(−λ1) VT(m1) with λ1 = 1.7 (P26's value, fitted
with the real injection-based selection, not this toy), VT(m1) = (m1/10)^2.2 for m1 < M_t and
(M_t/10)^2.2 for m1 ≥ M_t (continuous; M_t = ∞ gives p ∝ m1^0.5 throughout), M_t ∈ {30, 50, 80, ∞}
M☉. With I_lo = ∫_10^35 p and I_hi = ∫_35^100 p: the predicted fraction f = I_hi/(I_lo + I_hi);
reported per M_t: N_hi/(N_lo + N_hi) against f, and the binomial probability of ≤ N_hi events in
n = N_lo + N_hi trials with probability f. Caveat: [10, 35) contains the 10 M☉ peak, which is not a
λ1 power law, so the prediction is biased and a ratio below 1 is expected even without a 35 M☉
feature. Also reported: the median over events with median m1 in [30, 40] M☉ of the fractional 90% width
(upper offset − lower offset)/median m1, i.e. (m1,95 − m1,5)/m1,50 with the 90% interval taken as
the 5th to 95th percentiles; events without both offsets are
skipped and counted.

**R3 (exploration, no verdict).** Unbinned maximum likelihood on the medians in [10, 100] M☉,
p(m1) = f(m1) VT(m1) / ∫_10^100 f VT, with f ∝ m1^(−λ) (larger λ is steeper) and the same VT family
and M_t values. (A) broken power law: λ1, λ2 ∈ [−2, 10], m_break ∈ [20, 60], continuous at the break.
(B) mixture f = (1 − w) BPL/∫BPL + w N(μ, σ)/∫N, both normalised on [10, 100], μ ∈ [25, 45],
σ ∈ [1, 10], w ∈ [0, 1]. scipy `minimize` (L-BFGS-B) from 20 starting points drawn uniformly within the parameter bounds with
seed 0 (the bounds stay fixed when `m_range` changes), plus
for (B) the best (A) fit with w = 0, so that 2Δln L ≥ 0. Reported per M_t: λ2 − λ1 of (A) (flagged when
m_break is at a bound), 2Δln L of (B) against (A), and the fitted μ, σ and w of (B). The peak centre
is free in [25, 45] M☉, so this is a movable-peak exploration: a gain from a peak away from 35 M☉ is
reported as such, not as support for a 35 M☉ peak. No p-value is attached (w = 0 is a boundary).
m_break and M_t are expected to be degenerate when M_t lies in [20, 60]. Not a reproduction of P26.

**R4 (descriptive).** Percentile of GW231123's median total mass among the median total masses of
the R2–R4 sample defined under R2 (all masses, GW231123 included). *Dated amendment, 2026-11-15,
before any data were fetched:* GWOSC gives no `total_mass_source` for some events (for example the
GWTC-1 list); for those the sum of the medians m1 + m2 is used and the number of such events is
reported (found by the code review, not from the data) (not P26's
"maximum detectable mass" statistic).

## 3. Data (with size estimate)

| Input | Source | Selection | Est. size |
|---|---|---|---|
| GWTC-4.0 events | GWOSC `https://gwosc.org/eventapi/json/GWTC-4.0/` via `ctx.http` | 129 events (list header) | ~0.25 MB |
| GWTC-1-confident, GWTC-2.1-confident, GWTC-3-confident | GWOSC `https://gwosc.org/eventapi/json/<list>/` via `ctx.http` | O1–O3b confident events | each < 0.5 MB |
| GWTC-2.1-marginal, GWTC-3-marginal | GWOSC `https://gwosc.org/eventapi/json/<list>/` via `ctx.http` | marginal events (for type ii) | each < 0.5 MB |
| P26 O4a event list | Zenodo 16911563 `o4a_event_list.tar` via `ctx.http`, read in memory (bounded reads) | event names | 10 kB |

Total under 3.5 MB (six lists at under 0.5 MB each plus 10 kB), far below the 200 MB study budget; the
guarded fetch checks each size. Nothing from the 35 GB population release
other than the 10 kB list; no injection files, no posterior files, no per-event JSON loops
(AGENTS.md 1.2, 1.5).

## 4. Method

1. **Fetch and parse** the six GWOSC lists and the tar. Fields: `commonName`, `far`,
   `mass_1_source`, `mass_2_source` and their `_lower` offsets (signed; bound = value + offset),
   `total_mass_source`, `GPS`. Events with a null m1, m2 or `far` are excluded and listed.
2. **Selection.**
   - O4a: events in the GWTC-4.0 list with GPS in [1368975618, 1389456018) (2023-05-24 15:00 UTC
     to 2024-01-16 16:00 UTC; earlier events such as the engineering-run GW230518_125908 excluded),
     `far` < 1 per year, m1 and m2 90% lower bounds > 3 M☉, GW230630_070659 excluded (data quality,
     P26).
   - GWTC-3.0: union of GWTC-1-confident, GWTC-2.1-confident, GWTC-3-confident, GWTC-2.1-marginal
     and GWTC-3-marginal, deduplicated by `commonName` with precedence GWTC-3 > GWTC-2.1 > GWTC-1
     (confident before marginal within a catalogue); `far` < 1 per year; m1 and m2 90% lower bounds
     > 3 M☉. Check: all ten GWTC-1 BBHs (GW150914, GW151012, GW151226, GW170104, GW170608, GW170729,
     GW170809, GW170814, GW170818, GW170823) are present; any missing one is reported.
3. **R1** as in section 2.
4. **R2, R3, R4** on the medians of the sample (section 2). Integrals on a grid of 2000 points in
   [10, 100] M☉.

Systematics to keep in view: medians instead of posteriors; different PE priors and waveform
versions across catalogues; GWOSC lists differ from P26's sample definition; a one-dimensional toy
VT(m1) (the real sensitivity depends on both masses and redshift).

## 5. Results

Run 2026-11-15 (`python -m astrolab run 007`, 13 s; seven guarded fetches, 0.46 MB in total). Page:
[`web/index.html`](web/index.html). Numbers below are from `results/*.json`.

**R1 (verdict): not reproduced, by the pre-registered rule.**

- *O4a part: reproduced.* The O4a target T from P26's tar has 84 names. Selecting from the GWOSC
  GWTC-4.0 list (O4a window, FAR < 1 /yr, both 90% lower mass bounds > 3 M☉, GW230630_070659
  excluded) gives the same 84 events: none missing, no extras.
- *O1–O3 part: not reproduced.* |S_O3| = 59 against 69 ± 2. All seven named checks pass (the
  neutron-star events are excluded by the mass bound; GW190426_152155 has no PE in the list).
- *Cause.* The ten O1/O2 BBHs are taken from GWTC-2.1-confident: under the registered precedence
  (GWTC-3 > GWTC-2.1 > GWTC-1) its re-analysed v2 entries replace the GWTC-1 ones
  (`r1.json: precedence_overlaps`). Those GWOSC GWTC-2.1 rows carry no `far`, while the GWTC-1 rows
  of the same events do. The registered rule excludes an event without a FAR, so all ten drop out.
  59 + 10 = 69.
- *Post hoc (exploration, 2026-11-15, not a verdict).* `explore/gwtc1_far.py` keeps the registered
  precedence for the masses but, when the kept row has no FAR, takes it from the first
  lower-precedence list that has one. This affects exactly the ten events. Their GWTC-1 FARs are
  10⁻⁷ to 4.2×10⁻⁵ /yr, except GW151012 (7.9×10⁻³ /yr) and GW170729 (0.02 /yr). These match the
  lowest-over-pipelines values in GWTC-1 (arXiv:1811.12907, Sec. IV: GW151012 has 0.17 /yr in PyCBC
  and 7.92×10⁻³ /yr in GstLAL; GW170729 has 1.36, 0.18 and 0.02 /yr in PyCBC, GstLAL and cWB).
  The run then gives |S_O3| = 69 and R1 "reproduced": 84 + 69 = 153, the same total as P26's
  sample (the O4a part is the same set; whether the 69 are the same set is open question 1).
- *Reading.* The registered verdict stays "not reproduced". The shortfall comes from how the public
  lists store FARs (no FAR on the re-analysed rows), not from P26's selection; the rule did not
  anticipate a FAR on a lower-precedence list only. The R2–R4 numbers below use the registered
  sample of 84 + 59 = 143 events. The post-hoc 153-event values are given alongside.

**R2 (descriptive).** N(10–35 M☉) = 60 and N(35–100 M☉) = 79 (4 events outside 10–100 M☉), so 0.568
of the events are above 35 M☉. Prediction from λ1 = 1.7 times the toy VT:

| M_t (M☉) | predicted fraction ≥ 35 | observed / predicted | P(≤ N_hi) | post hoc 153: ratio, P |
|---|---|---|---|---|
| 30 | 0.493 | 1.15 | 0.97 | 1.10, 0.90 |
| 50 | 0.714 | 0.80 | 1.8×10⁻⁴ | 0.76, 7.7×10⁻⁶ |
| 80 | 0.806 | 0.70 | 1.3×10⁻¹⁰ | 0.67, 3.4×10⁻¹³ |
| ∞ | 0.819 | 0.69 | 7.8×10⁻¹² | 0.66, 1.2×10⁻¹⁴ |

There is a deficit above 35 M☉ unless the toy VT turns over near 30 M☉. As registered, the low bin
contains the 10 M☉ peak, so the prediction is biased and the deficit is not by itself evidence of
a 35 M☉ steepening. The median fractional 90% width of m1 at 30–40 M☉ is 0.45 (37 events, none
skipped; 0.43 for 42 events post hoc). Single-event mass uncertainties are thus about half the mass,
so a feature narrower than about 15 M☉ is smeared out in the medians.

**R3 (exploration, no verdict).** Point-estimate fits to the 139 medians in 10–100 M☉:

| M_t (M☉) | A: λ1, λ2, m_break | λ2 − λ1 | B: μ, σ, w | 2Δln L (B vs A) |
|---|---|---|---|---|
| 30 | 3.67, 1.48, 20.0 (bound) | −2.18 | 39.5, 6.5, 0.14 | 25.0 |
| 50 | 2.27, 3.79, 42.2 | 1.51 | 36.2, 5.7, 0.09 | 19.6 |
| 80 | 2.25, 5.42, 44.0 | 3.16 | 32.6, 10.0 (bound), 0.18 | 16.7 |
| ∞ | 2.26, 5.70, 45.0 | 3.44 | 32.9, 10.0 (bound), 0.18 | 15.3 |

- With a VT that keeps rising past 50 M☉, model A finds a steepening at 42–45 M☉ (λ2 − λ1 = 1.5–3.4).
  With M_t = 30 the break is driven to its lower bound and reverses. The break location and the
  sign of the steepening therefore depend on the toy selection function, as registered (m_break and
  M_t are degenerate).
- Model B gains 2Δln L = 15–25 in every case. The fitted peak is at 33–40 M☉ (centre free in
  25–45 M☉) with weight 0.09–0.18. In every B fit the broken power law's m_break sits at its lower
  bound of 20 M☉, and for M_t ≥ 80 the peak width is at its upper bound of 10 M☉.
- The B "peak" thus also absorbs the 20–45 M☉ shape and is not a narrow 35 M☉ over-density.
- Post hoc (153 events), model A's slopes move by less than 0.2 and μ by less than 2 M☉; 2Δln L = 17–27.
  Model B's λ1 moves by up to 0.65, and σ is at its upper bound for M_t = 30, 80 and ∞.
- These are toy point estimates. No injections were used and no p-value is attached.

**R4 (descriptive).** GW231123 is in the sample. Its median total mass is 236 M☉, the 100th
percentile: the heaviest of the 143 events (and of the 153 post hoc). No total mass had to be filled
from m1 + m2: GWOSC gives `total_mass_source` for every event in the sample, including the GWTC-1
ones.

## 6. Referee notes

Independent referee, 2026-11-15. The referee subagent saw only the pre-registration, the code and
`results/`; it re-analysed the cached inputs and did not edit or download anything. Triage of each
point (fixed / accepted / rejected):

1. **The ten O1/O2 BBHs are lost to null FARs on the GWTC-2.1 rows** (serious; found independently
   of our own diagnosis). *Accepted.* Recorded under section 5. The registered verdict stays "not
   reproduced". The FAR-fallback exploration (`explore/gwtc1_far.py`) gives 69 and 153. The referee
   also notes that the registered GWTC-1 check tested only presence in the lists, not in the sample,
   so it could not catch this: *accepted* as a weakness of the check as designed. With the fallback
   the type-(i) count is 6 (GW151226 joins), which does not matter at exactly 69.
2. **R3 model-B fits sit on bounds; only A's break is flagged** (moderate). *Accepted, and
   explored.* The bounds are disclosed in section 5; the pre-registration flags only A's break.
   `explore/r3_wide_bounds.py` (post hoc) reruns R3 on the 153 events with m_break in [10.5, 60] and
   σ in [1, 25]. The fitted m_break and σ are then interior (m_break 15–18 M☉); μ keeps its
   registered range [25, 45].
   - For M_t = 30, 50 and 80 the peak is at μ = 38.9, 35.7 and 34.4 M☉ with σ = 6.2, 5.2 and 8.1 M☉
     and w = 0.09–0.14; 2Δln L = 21–25.
   - For M_t = ∞ it becomes a broad bump, μ = 25.1 M☉ (next to its lower bound of 25) and
     σ = 14.7 M☉; 2Δln L = 19.3.
   - So for M_t = 30, 50 and 80 the bump sits at 34–39 M☉ (three point-estimate fits to medians),
     while at M_t = ∞ it is a broad, bound-limited shoulder; whether it is a narrow peak depends on the
     selection model. This matches section 5's reading.
3. **R4 is trivially 100** (minor). *Accepted.* GW231123's 236 M☉ exceeds the next-highest median
   total mass (153 M☉) by far, so the percentile carries little information. It is kept as
   registered.
4. **Trapezoid step at m_split** (minor). *Accepted*; the error is about half a grid cell, which is
   negligible.
5. **Pile-up of medians at the 35 M☉ split** (systematic). Ten medians fall in [35, 36), six of them
   exactly 35.6. *Accepted* as a limitation of R2:
   - N_hi is 90, 81 and 69 for splits at 33, 35 and 37 M☉ (153 events);
   - scattering the medians within their errors lowers the high fraction by about 0.04 (referee's
     crude estimate from 0.568 on the registered 143 events, not a deconvolution; the 153-event
     fraction is 0.544).
   R2 is descriptive, and this is part of why it carries no verdict.
6. **R2 is decided by the toy VT** (systematic). *Accepted*; this was registered as the reason R2
   is descriptive. The binomial probabilities assume exact medians and a true toy model; they are
   not evidence for a 35 M☉ feature.
7. **The 10 M☉ peak and the cut at 10 M☉** (systematic). *Accepted*; already registered as a caveat
   of R2. In R3 the low-mass segment fits the falling side of the 10 M☉ peak.
8. **Which PE the GWOSC medians come from** (systematic). For O4a, P26's list names 43 NRSur7dq4
   and 41 "Mixed" PE labels, and it is not confirmed which run GWOSC's GWTC-4.0 medians use. Across
   O1–O3 the registered precedence mixes catalogue PE (for example GW170729's m1 median is 50.2 or
   54.7 M☉ depending on the catalogue). *Accepted limitation*; it affects R2–R4 values, not R1's
   counts.
9. **The same count of 69 need not be the same set** (systematic). Several events lie near the FAR
   cut (for example GW190413_052954 at 0.82 /yr and GW200216 at 0.35 /yr inside; GW190926_050336 at
   1.1 /yr and GW200210_092254 at 1.2 /yr outside). *Accepted*; registered as open question 1.
10. **Two lists in the tar** (76 full-spectrum ⊂ 84 BBH-only). *Accepted, harmless here*: the union
    equals the 84-event list, and T has no neutron-star events.
11. **Literature** (IDs as given by the referee; those marked unverified by it are not used here):
    non-parametric 10 and 35 M☉ features (arXiv:2011.04502, 2109.06137, 2302.07289); the GWTC-3
    population sample of 69 BBHs (arXiv:2111.03634); selection effects (arXiv:1809.02063); why a
    maximum-mass percentile is uninformative (arXiv:1911.05882).

## 7. Open questions

1. Is the post-hoc 69 the *same set* as the GWTC-3 population paper's 69 BBHs (arXiv:2111.03634),
   not just the same count? This needs that paper's small event-list file (referee test (e)).
   *Answered 2026-11-16 (T-026; post hoc, no verdict changes):* yes. The paper's data release
   (Zenodo 11254021, `table_data.tar.gz`, 4.9 kB, via `ctx.http`) holds Table 1 (76 events) and
   Table 3 (the 7 events whose components may be neutron stars: GW170817, GW190425, GW190426,
   GW190814, GW190917, GW200105, GW200115). Table 1 has no BBH column; Table 1 minus Table 3 gives
   69 events, the paper's stated BBH count, and that set equals our post-hoc 69 (the 59 O1–O3 events
   of `results/sample.json` plus the ten O1/O2 BBHs of the FAR fallback) once our short names
   GW190412 and GW190521 are read as GW190412_053044 and GW190521_030229. Script:
   `explore/gwtc3_pop_events.py`.
2. Does the bump near 35 M☉ in R3 survive a real (injection-based) selection function instead of
   the toy VT? It needs only summary products, not the 35 GB release.
3. Should the pre-registration template for list-based reconstructions say how to handle a field
   that is missing in the preferred list but present in a lower-precedence one?

## 8. Exploring via chat

How a coding agent answers "what if" questions about this study without touching `results/`
(rules: AGENTS.md section 2).

| Knob (`PARAMS`) | Meaning | Safe range | Cache only, or new data (size)? |
|---|---|---|---|
| `vt_slope` | exponent a of the toy VT(m1) below the turnover | 1.5–3 | cache only |
| `turnovers` | list of turnover masses M_t (M☉; `null` = none) | 20–150 | cache only |
| `m_split` | mass separating the R2 bins | 25–45 | cache only |
| `m_range` | mass range of R2 and R3 (M☉) | [5, 150] at most | cache only |
| `far_max` | FAR threshold (per year) | 0.1–2 | cache only (changes the sample: not an R1 verdict) |
| `mass_bound` | `"p90"` (90% lower bound proxy) or `"median"` | either | cache only (`"median"` changes the R1 sample: not an R1 verdict) |
| `lambda1` | slope used for the R2 prediction | 1–3 | cache only |
| `n_starts`, `seed` | R3 starting points and seed | 5–100 | cache only |

- Rerun with an override: `python -m astrolab explore 007-m10-gwtc4-bbh-mass-35msun --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; seconds from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 007-m10-gwtc4-bbh-mass-35msun --tag <topic> --script explore/<name>.py`.
- Results files and keys: `results/r1.json` (`n_o4a`, `n_o3`, `target_size`, `missing`,
  `missing_reasons`, `extra`, `named_checks`, `gwtc1`, `gwtc1_missing`, `excluded_o4a`, `excluded_o3`,
  `precedence_overlaps`, `o4a_part`, `o3_part`, `verdict`); `results/r2.json` (`n_lo`, `n_hi`, `n_outside_range`, `per_turnover` with `f_pred`, `frac_obs`,
  `ratio`, `binom_p`; `width_30_40`);
  `results/r3.json` (per-turnover fits); `results/r4.json`; `results/sample.json` (the event table).
- Example questions: "what if VT turns over at 40 M☉?" → `--set turnovers=[40]`; "does the R2 count
  change with the 30 M☉ split?" → `--set m_split=30`.
- Existing explorations (post hoc): `explore/gwtc1_far.py` takes a null FAR from a lower-precedence list
  (the ten O1/O2 BBHs) and reruns everything: `python -m astrolab explore 007 --tag gwtc1-far --script explore/gwtc1_far.py`;
  `explore/r3_wide_bounds.py` adds wider R3 bounds on top: `--tag r3-wide-bounds --script explore/r3_wide_bounds.py`.
- Findings that change what we know go into `log.md` (and the wiki article) on a branch.
