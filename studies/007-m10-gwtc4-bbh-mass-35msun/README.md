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

**R1 (sample reconstruction).** Rules (section 4, step 2) applied to the GWOSC lists give an O4a set
S_O4a and a GWTC-3.0 set S_O3. P26's O4a event list (Zenodo `o4a_event_list.tar`) is the comparison
target only. Pre-declared, direction-known differences:
- (a) the 90% lower bound (5th percentile) of m2 as a proxy for P26's 1% lower limit can only add
  events: an extra event counts as type (a) if its m2 90% lower bound is between 3 and 5 M☉;
- (b) none other.
**"reproduced"** if: S_O4a contains every event of P26's O4a list, every extra event is of type (a),
there are at most 2 such extras, |S_O4a| − |extras| = 84, and |S_O3| is within 69 ± 2 with every
difference listed and attributed. Otherwise **"not reproduced"**, with each difference listed. The
GWOSC top-level `far` is the minimum over search pipelines (GWOSC event-portal documentation;
checked on one event), so the FAR cut is P26's "at least one pipeline" criterion; if the fetched
JSON contradicts this for any event (top-level `far` larger than a per-pipeline search value
present in the same JSON), R1 is downgraded to **"described"**.

**R2 (descriptive, no verdict).** With the S_O4a ∪ S_O3 sample (P26's list for O4a membership if R1
is "reproduced", else our rule): N_lo = number with median m1 in [10, 35) M☉, N_hi = number in
[35, 100] M☉. Prediction for N_hi from N_lo under p(m1) ∝ m1^(−1.7) VT(m1), VT(m1) = (m1/10)^2.2 for
m1 < M_t and constant above, for M_t ∈ {30, 50, 80, ∞} M☉:
N_hi,pred = N_lo × ∫_35^100 p dm1 / ∫_10^35 p dm1. Reported: N_hi/N_hi,pred and the Poisson
probability of ≤ N_hi given N_hi,pred, for each M_t; and the median fractional 90% width of m1 for
events with median m1 in [30, 40] M☉ (how much medians blur a break).

**R3 (exploration, no verdict).** Unbinned maximum likelihood on the medians in [10, 100] M☉ with
p(m1) ∝ f(m1) VT(m1) (same VT family and M_t values), normalised numerically on [10, 100]: (A) a
broken power law f with free λ1, λ2 ∈ [−2, 10] and m_break ∈ [20, 60]; (B) (A) plus a Gaussian peak
with μ ∈ [25, 45], σ ∈ [1, 10] and weight ∈ [0, 1]. Reported per M_t: λ2 − λ1 of (A) and 2Δln L of
(B) against (A). Not a reproduction of P26: no measurement uncertainty, no injections.

**R4 (descriptive).** Percentile of GW231123's median total mass among the sample's medians (not
P26's "maximum detectable mass" statistic).

## 3. Data (with size estimate)

| Input | Source | Selection | Est. size |
|---|---|---|---|
| GWTC-4.0 events | GWOSC `https://gwosc.org/eventapi/json/GWTC-4.0/` via `ctx.http` | 129 events (list header) | ~0.25 MB |
| GWTC-2.1-confident events | GWOSC `https://gwosc.org/eventapi/json/GWTC-2.1-confident/` via `ctx.http` | O3a plus updated GWTC-1 BBHs | < 0.5 MB (checked by the guarded fetch) |
| GWTC-3-confident events | GWOSC `https://gwosc.org/eventapi/json/GWTC-3-confident/` via `ctx.http` | O3b | < 0.5 MB |
| P26 O4a event list | Zenodo 16911563 `o4a_event_list.tar` via `ctx.http`, read in memory (bounded reads, names only) | event names | 10 kB |

Total under 2 MB. Nothing from the 35 GB population release other than the 10 kB list; no
injection files, no posterior files, no per-event JSON loops (AGENTS.md 1.2, 1.5).

## 4. Method

1. **Fetch and parse** the three GWOSC lists and the tar. Fields: `commonName`, `far`,
   `mass_1_source`, `mass_2_source`, their `_lower` offsets (negative numbers; bound = value +
   offset), `total_mass_source`, `GPS`. Events with a null m1 or m2 are excluded and listed.
2. **Selection.**
   - O4a: events in the GWTC-4.0 list with GPS in O4a (2023-05-24 to 2024-01-16; earlier events,
     such as the engineering-run GW230518_125908, excluded), `far` < 1 per year, m1 and m2 90% lower
     bounds > 3 M☉; GW230630_070659 excluded (data quality, P26).
   - GWTC-3.0: union of GWTC-2.1-confident and GWTC-3-confident, deduplicated by `commonName`
     (GWTC-3 takes precedence), `far` < 1 per year, m1 and m2 90% lower bounds > 3 M☉.
   - From the tar: event names matched by the pattern GW\d{6}_\d{6} (or GW\d{6}), compared by name.
3. **R1** as in section 2.
4. **R2, R3, R4** on the medians of the sample (section 2). Numerical integrals on a grid of 2000
   points in [10, 100] M☉; R3 maximised with scipy `minimize` (L-BFGS-B) from 20 fixed starting
   points (seed 0), best value kept.

Systematics to keep in view: medians instead of posteriors; different PE priors and waveform
versions across catalogues; GWOSC "confident" lists use p_astro > 0.5 or FAR < 1/yr, not exactly
P26's sample definition; a one-dimensional toy VT(m1) (the real sensitivity depends on both masses
and redshift).

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
| `mass_bound` | `"p90"` (90% lower bound proxy) or `"median"` | either | cache only |
| `lambda1` | slope used for the R2 prediction | 1–3 | cache only |

- Rerun with an override: `python -m astrolab explore 007-m10-gwtc4-bbh-mass-35msun --tag <topic> --set KEY=VALUE`
  (outputs in `explore/<date>-<topic>/`, not committed; seconds from cache).
- Analyses `run.py` does not cover: a script `explore/<name>.py` with `def main(ctx)`, run with
  `python -m astrolab explore 007-m10-gwtc4-bbh-mass-35msun --tag <topic> --script explore/<name>.py`.
- Results files and keys (planned): `results/r1.json` (`n_o4a`, `n_o3`, `missing`, `extra`,
  `verdict`); `results/r2.json` (`n_lo`, `n_hi`, per-turnover predictions and ratios, `width_30_40`);
  `results/r3.json` (per-turnover fits); `results/r4.json`; `results/sample.json` (the event table).
- Example questions: "what if VT turns over at 40 M☉?" → `--set turnovers=[40]`; "does the R2 count
  change with the 30 M☉ split?" → `--set m_split=30`.
- Findings that change what we know go into `log.md` (and the wiki article) on a branch.
