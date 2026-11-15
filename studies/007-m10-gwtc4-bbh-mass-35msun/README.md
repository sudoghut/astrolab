# M10 GWTC-4.0 BBH mass spectrum: the 35 Msun feature and the event sample

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
the R2–R4 sample defined under R2 (all masses, GW231123 included) (not P26's
"maximum detectable mass" statistic).

## 3. Data (with size estimate)

| Input | Source | Selection | Est. size |
|---|---|---|---|
| GWTC-4.0 events | GWOSC `https://gwosc.org/eventapi/json/GWTC-4.0/` via `ctx.http` | 129 events (list header) | ~0.25 MB |
| GWTC-1-confident, GWTC-2.1-confident, GWTC-3-confident | GWOSC `https://gwosc.org/eventapi/json/<list>/` via `ctx.http` | O1–O3b confident events | each < 0.5 MB |
| GWTC-2.1-marginal, GWTC-3-marginal | GWOSC `https://gwosc.org/eventapi/json/<list>/` via `ctx.http` | marginal events (for type ii) | each < 0.5 MB |
| P26 O4a event list | Zenodo 16911563 `o4a_event_list.tar` via `ctx.http`, read in memory (bounded reads) | event names | 10 kB |

Total under 3 MB; the guarded fetch checks each size. Nothing from the 35 GB population release
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

Filled after running. Link to `web/index.html` and key numbers in `results/`.

## 6. Referee notes

Independent critique: selection effects, systematics, alternative explanations.

## 7. Open questions

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
- Results files and keys (planned): `results/r1.json` (`n_o4a`, `n_o3`, `target_size`, `missing`,
  `extra`, `named_checks`, `gwtc1_missing`, `verdict`); `results/r2.json` (`n_lo`, `n_hi`, `n_outside_range`, `per_turnover` with `f_pred`, `frac_obs`,
  `ratio`, `binom_p`; `width_30_40`);
  `results/r3.json` (per-turnover fits); `results/r4.json`; `results/sample.json` (the event table).
- Example questions: "what if VT turns over at 40 M☉?" → `--set turnovers=[40]`; "does the R2 count
  change with the 30 M☉ split?" → `--set m_split=30`.
- Findings that change what we know go into `log.md` (and the wiki article) on a branch.
