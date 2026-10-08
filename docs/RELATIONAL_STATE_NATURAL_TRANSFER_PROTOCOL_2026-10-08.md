# Relational-state natural transfer: prospective eligibility and falsification protocol

Status: **design-only / not executed / no empirical result**. This is a new independent test proposal, not an amendment to the frozen NEE simulations or a reinterpretation of the null natural strongest-refuge transfer.

## Ecological question

When fragmented populations have comparable marginal census, interaction, trait and genetic measurements, does **patchwise co-location of effective interaction and trait/genetic support** explain future realised reproductive function beyond those marginals? Does any advantage persist when cohort, dispersal and mating processes are held out?

## Distinct hypotheses and falsifiers

- **H-R (relational information):** a model using pre-outcome patchwise interaction–trait/genetic association improves held-out future functional outcome over a model using the identical marginals and sampling effort. **Falsifier:** no predeclared improvement in out-of-sample predictive loss; do not interpret a within-sample fit or post-hoc sign as support.
- **H-O (operator mechanism):** measured effective mating, recruitment or movement modifies the H-R association in a direction prospectively specified from the biological system, not from fitted outcomes. **Falsifier:** effect is absent or changes sign across independent systems/cohorts; do not silently reinterpret all movement as beneficial.
- **H-P (portability):** the same measured state carries comparable future information across independent urban/island systems after origin/history is supplied. **Falsifier:** held-out origin/history continues to add information, or relational measurements fail to transfer. Urban and island geography are not assumed equivalent.

## Admission before outcomes

1. Archive source identity, legal access, raw schema and fixed version/hash. Separate original measurements from reconstructed proxies.
2. Define ecological unit as population/site × observation window × cohort, and establish the future functional endpoint and genuine forward time ordering **without inspecting outcome values**.
3. Require multiple local patches and simultaneous or explicitly harmonized measurements of effective interaction, trait/genetic state and sampling effort. A regional mean, pan-trap abundance or geographic distance alone does not identify patchwise co-location.
4. Freeze sampling completeness, repeated measures, within-site dependence, missingness and independent validation units. Stop if no defensible independent held-out sites/cohorts/time windows exist.
5. Document whether movement means allele-frequency mixing, pollen movement, whole-individual dispersal, or observed partner movement. Never substitute these operators.
6. Keep the already-failed natural strongest-refuge transfer as a distinct locked negative boundary; it must not be pooled with this prospective hypothesis.

## Candidate state and comparisons

At pre-outcome time t, record patch-level effective interaction `I_j`, realised focal trait `T_j`, genetic/cohort state `G_j`, census `N_j`, functional outcome sampling effort `E_j`, and process-specific movement/mating `C_j`. Define a relational predictor (e.g. weighted covariance or co-location of I with T/G) **only after a source's measurement scale and direction are declared and before opening future outcomes**. Do not import the finite model's coefficients 0.6/0.3/0.1 or q*=0.625 into nature.

- **M0:** pre-outcome marginals, baseline function, season, cohort, effort and relevant history.
- **M1:** M0 plus a preregistered patchwise relational coordinate.
- **M2 (secondary):** M1 plus prospectively measured effective movement/mating/recruitment; test effect modification only where independently measured.
- **M3 (portability):** M1 or M2 plus origin/history label; assess residual information on entirely held-out ecological units.

Primary contrast: paired held-out predictive loss `Loss(M0)-Loss(M1)` on the same folds. Declare the scoring rule (e.g. negative log-likelihood for a binary future endpoint), direction, minimum meaningful gain, uncertainty method and family of comparisons **before outcomes are opened**. Report confidence intervals and negative/zero improvements, not just p values. Do not claim causation from predictive improvement alone.

## Measurement pitfalls and stop rules

- Interaction counts without effective pollen transfer, successful mating or function may be invalid proxies. Test proxy adequacy independently.
- Trait and allele marginals measured on different patches/cohorts cannot establish their spatial covariance.
- An all-patch loss endpoint structurally favours a strongest-patch summary; test a non-all-patch endpoint where feasible, but freeze it prospectively.
- If the endpoint is contemporaneous rather than future, this is state association, **not** early warning.
- If only six eligible time points or fewer than the source-specific independent replication requirement remain, do not borrow the unrelated Ya Ha Tinda 11-year gate; set a justified system-specific minimum before outcomes.
- Do not call missing access, invalid metadata or lack of power a biological null.

## Existing evidence boundary (not new results)

The NEE finite closure has a matched-marginal transition difference up to 0.2543 and an isolated q-dependent sorting DID +6.883 pp. Its continuous strongest-refuge predictor improves AUC over co-timed max q by +0.02135, but under no migration, two fixed AA/RR initial templates and an all-patch loss endpoint. A first natural strongest-refuge transfer reported no detected incremental information (delta NLL M1-M0=-0.0003211; 95% CI [-0.0009825,+0.0003422]). These facts motivate, but do not validate, H-R/H-O/H-P.

**Next executable gate:** inventory a single independently sourced dataset with patch-aligned effective interaction, trait/genetic/cohort measurements and later function. Only after it passes the outcome-blind schema/time/independence gate should a scoring protocol and prediction code be frozen. If none passes, report `NOT_IDENTIFIABLE`, not a positive or negative biological finding.
