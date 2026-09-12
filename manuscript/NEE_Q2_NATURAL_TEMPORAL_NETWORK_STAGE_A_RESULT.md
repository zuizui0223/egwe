# Ren natural Q2 temporal-network attempt — Stage-A result

## Decision

`prospective_next_interaction_not_identifiable_from_archive`

This is a **representation/identifiability boundary, not an ecological null**.

## Locked source and execution

- study: Ren, Si & Ding (2022), doi:`10.1111/ecog.06102`;
- dataset: Dryad doi:`10.5061/dryad.rv15dv484`;
- machine-access mirror: Zenodo record `6519751`;
- primary archive MD5 verified: `2_null_model_background_data.rar` = `40d028ed6a72d35e37d06b1b5240a72d`;
- temporal archive MD5 verified: `3_span_1CV.rar` = `6239f2eeebd4b7e7387cd6bde515c6ed`.

The response-blind archive-member workflow established the following members without extraction:

- `2_null_model_background_data/pool.interactions.csv`;
- `2_null_model_background_data/S48_network.csv`;
- `3_span_1CV/all_ints_spatial.csv`;
- `3_span_1CV/all_ints_temporal.csv`;
- `3_span_1CV/ints_S_1CV_spatial.csv`;
- `3_span_1CV/ints_S_1CV_temporal.csv`.

A separate Stage-A header-only workflow then read row 1 and no lower row.

## Header evidence

The primary null-model package exposes:

- `pool.interactions.csv`: unnamed row index + `pl`, `po`, `links`, `link_prob`;
- `S48_network.csv`: unnamed row index + pollinator columns (`PO...`), i.e. one named site-network representation rather than a site-by-year key.

The temporal/stability package exposes two **separately marginalised** representations:

- `all_ints_temporal.csv`: unnamed row index + `t2017`, `t2018`, `t2019`, `int`;
- `all_ints_spatial.csv`: unnamed row index + mainland/island columns (`B0`, `B01`...`S48`), but no year field;
- the corresponding `ints_S_1CV_*` files retain the same temporal-only versus spatial-only split and add stability columns.

Thus the archive exposes interaction identity across years **or** across sites, but the Stage-A representation does not expose a joint `site × year × plant × pollinator` key from which the same island can be followed through a `t -> t+1` edge transition.

## Why the preregistered test cannot open

The prospective contract required all of:

- independent site identifier;
- at least three ordered time points;
- plant identity;
- pollinator identity;
- year-specific edge state;
- the same site followed across at least two `t -> t+1` transitions.

The header/source representation fails the last requirement. Joining the temporal table to the spatial table would require inventing the missing site-by-year allocation of interactions. That would manufacture the very cross-layer organization the analysis is supposed to test.

Therefore no Stage-B model contract is opened and no raw edge row is read.

## Response firewall receipt

No project process inspected or computed:

- row 2 or below in any deposited CSV;
- any interaction count or matrix cell;
- any species/interactions stability value;
- any year-to-year edge outcome;
- any coefficient, effect direction, model fit, log loss, AUC or p-value.

## Scientific interpretation

This attempt cannot validate or refute the NEE Q2 natural prediction. It does reveal a directly relevant representation boundary: the public archive preserves temporal and spatial interaction marginals separately but does not preserve the joint site-time edge state required for prospective transition prediction.

That observation may be used only as a data-representation lesson. It is **not** evidence that cross-layer organization predicts natural fate.

## Stop rule

Do not:

- infer site-year edges by multiplying or matching separate temporal and spatial marginals;
- use the authors' stability index as a substitute next-year outcome;
- open row values to search for an undocumented join key;
- switch to a favorable subset of islands/interactions;
- call this an external validation result.

A subsequent natural-system attempt must be independently preregistered and must require a machine-accessible **joint space × time × interaction** representation before response inspection.
