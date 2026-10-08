# Ya Ha Tinda teaching-mirror Love–Otto metric sampling stability

Date: 2026-10-08

Status: **exploratory, outcome-free measurement diagnostic; not a future-warning test and not a modification of the frozen Ya Ha Tinda protocol.**

## Reason for this audit

The pinned researcher teaching mirror contains just one year (2004) with enough collared females for the locked n>=10 window. It therefore cannot validate prospective demographic prediction. It can answer an earlier measurement question:

> How much does the Love–Otto spatial-cohesion CV ratio depend on **which ten GPS-collared females** are selected from the 10–12 observed on each eligible day?

This matters because a daily spatial CV change could reflect different sampled animals rather than a real change in the entire herd's geometry.

## Source and provenance

- Source: `EliGurarie/BrazilMove2024`, commit `447d2882e8d14a67db429a6ef74c307dd2354866`.
- File: `data/Elk_GPS_data.csv`.
- Immutable Git blob: `2d5e8b124bc02b63a7b2f171004c7027b412cbe3`.
- Source link to Movebank study `897981076` is explicitly stated by the teaching repository.
- UTC semantics of timezone-naive timestamps are documented by the related teaching source `EliGurarie/MovementEcologyBook`.
- This is a partial educational redistribution, not the full authoritative long-term Movebank archive.

## Fixed measurement audit

The study's existing movement-only diagnostic identified 43 eligible days in 2004 under:

- September 15–November 15, local `America/Edmonton`;
- a single nearest-noon fix within 6.5 hours per individual-day;
- at least ten unique GPS females per day.

Those 43 days had observed sample sizes:

- n=10: 17 days, one possible ten-animal set;
- n=11: 14 days, eleven possible ten-animal sets per day;
- n=12: 12 days, sixty-six possible sets per day.

The new diagnostic:

1. verifies the raw source Git blob SHA;
2. projects GPS coordinates with the NAD83/GRS80 UTM zone 11N forward formula;
3. computes the exact Love–Otto `CV_ind / CV_pop` using sample-SD distances;
4. enumerates **all** ten-animal subsets on each eligible day;
5. reports within-day between-subset variability and compares it descriptively with day-to-day changes in daily subset means.

The deliberate distinction from the frozen primary protocol is that this diagnostic enumerates subsets exhaustively; the later primary annual estimator still uses 100 deterministic SHA256 subsamples, only if the complete official archive passes all eligibility gates. No decision rule or data source for the primary test changes.

## Scientific claim ceiling

- The sampling variation here is **conditional on the animals that happened to be collared**, not uncertainty about the unseen whole herd.
- Day-to-day spatial change could reflect rut, migration composition, collar deployment and other ecological factors; it is not a fragmentation-induced collapse measurement.
- A sample-subset SD cannot be substituted for an effect size, predictive AUC or demographic warning confidence interval.
- All future-demography values remain unopened.
- The original eleven-year requirement for the Ya Ha Tinda test remains unaltered.

## Reproduction

The public GitHub Actions workflow `.github/workflows/yht-mirror-sampling-audit.yml` downloads the pinned **teaching** source and runs:

```bash
python scripts/audit_yht_mirror_sampling.py \
  --source-csv Elk_GPS_data.csv \
  --output yht_mirror_sampling_diagnostic.json
```

Only the aggregate JSON result is uploaded as a workflow artifact, never the full raw GPS CSV. The final evaluated summary, when checked against the pinned GitHub action result, should be stored separately with its actual workflow provenance.
