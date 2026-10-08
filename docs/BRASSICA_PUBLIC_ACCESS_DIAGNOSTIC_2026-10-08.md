# Brassica public archive acquisition: first executed receipt (2026-10-08)

**No ecological result / no phenotype, visitation, genotype, paternity or functional-outcome record opened.**

## Reproduced access condition

The outcome-blind GitHub Actions source gate ran as workflow **37765671081**, job **113272606054**, archived output artifact **11544298078** (`brassica-header-only-source-gate`). The workflow itself passed its safety and unit tests. The actual Dryad API ZIP fetch returned:

```json
{
  "status": "ACCESS_OR_SCHEMA_STOP",
  "error_type": "HTTPError",
  "error_detail": "HTTP Error 401: Unauthorized",
  "source": "https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.tdz08kqdr/download",
  "outcome_values_opened": false
}
```

This is **a source-acquisition/access stop**, not proof that the ZIP is empty, that a plant/patch visitation key is absent, or that the H-R hypothesis failed.

Dryad's public dataset landing page lists a ~1.67 MB `Leventhal_et_al_2026.zip` and a README, but its REST API documentation notes that some file-download endpoints require an authenticated session. A publicly indexed README is not a successful raw-schema inspection.

## Next path, before any outcome values

An independent metadata-only probe checks:
- official dataset/versions/files API responses;
- HTTP status for the dataset download path;
- public landing-page HTML download **link paths only**, without tokens, cookies or data rows.

If a genuinely public user-facing download URL is provided by Dryad, the schema-only ZIP reader may use that documented source, retaining DOI, exact URL path, SHA-256 and role-specific CSV headers. Do not bypass access restrictions or invent a file ID. If no authorized public archive fetch succeeds, keep the status `ACCESS_OR_SCHEMA_STOP` and request an authorized archive copy only as a last resort.

## Validation boundary

The first workflow's scientific admissibility registry reports **0/5** new programmes confirmed for full H-R, and all five published dataset entries were **not raw-inspected** at the time of this record. The old label `raw_bytes_inspected=fail` was corrected to `unknown`, because no verified failed schema check occurred. Confirmatory H-R evidence, model portability and future-fit statistics remain unestablished.

### Primary provenance
- [Dryad published dataset and README](https://doi.org/10.5061/dryad.tdz08kqdr)
- GitHub Actions run `37765671081` and artifact `11544298078`
- [Dryad API documentation](https://github.com/datadryad/dryad-app/blob/main/documentation/apis/README.md)
- [Dryad API-account/access documentation](https://github.com/datadryad/dryad-app/blob/main/documentation/apis/api_accounts.md)
