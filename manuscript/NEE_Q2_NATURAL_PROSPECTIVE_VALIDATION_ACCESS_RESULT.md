# Natural Q2 prospective validation — Stage-A access result

## Decision

`raw_byte_access_blocked_before_header_inspection`

This is an **access boundary, not an ecological result**.

## Locked source

- Lázaro, Fuster, Alomar & Totland (2020), *Ecological Applications* 30:e02099.
- Dryad doi:`10.5061/dryad.d51c59zzj`.
- locked file: `Visitation&Seedsetdata_Dryad.xlsx`.
- Dryad file id resolved prospectively: `241700`.

## Execution receipt

GitHub Actions:

- workflow: `Lazaro natural Q2 schema gate`;
- run id: `34667417734`;
- job id: `103482049317`;
- result: workflow/job `success` because the workflow is designed to preserve and report access STOPs rather than treating them as analysis errors;
- artifact id: `10289154222`;
- artifact name: `lazaro-natural-q2-schema`.

The schema adapter resolved dataset metadata and file metadata before trying any workbook content. The three fixed public byte routes returned:

- `https://datadryad.org/api/v2/files/241700/download` — HTTP 401;
- `https://datadryad.org/stash/downloads/file_stream/241700` — HTTP 403;
- `https://datadryad.org/downloads/file_stream/241700` — HTTP 403.

## Response firewall status

The run stopped before workbook header inspection. Therefore no project process read or computed:

- predictor values;
- seed-set values;
- species-specific outcome values;
- effect direction;
- cross-layer organization;
- strongest-joint-reserve values;
- model coefficients;
- held-out predictive scores;
- p-values.

No ecological null or support can be inferred from this run.

## Consequence for this preregistered attempt

The locked Lázaro attempt is closed at Stage A. Under the preregistration, do not:

- substitute seed mass for seed set;
- analyse published summary statistics as if they were row-level validation;
- change validation units;
- search alternate download routes inside this attempt;
- swap in a different natural system while preserving the same attempt identity.

A different public archive may be opened only as a **new, independently preregistered attempt** whose source and access qualification are fixed before response inspection.

## Methodological update for the next independent attempt

Because two scientifically strong Dryad candidates have now encountered the same public-byte boundary in this execution environment, the next candidate registry should add **machine-accessible raw rows** as an explicit pre-analysis qualification criterion. This is a representation/access requirement, not a biological selection rule.
