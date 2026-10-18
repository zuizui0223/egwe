# Pinned full-life-cycle AA/RR pilot — 2026-10-18

## Source recovery

The former repository URL `zuizui0223/eco-genetic-criticality` redirects to `zuizui0223/egc`. The exact upstream commit `dd8ee379d0d3518194c767d16402042525bc00dc` contains `causal_model/multipatch_criticality_dynamics.py` and `causal_model/symmetric_allele_mutation_closure.py`. GitHub Actions checks out that exact commit and imports its real `simulate_with_symmetric_allele_mutation` function. No source reconstruction, reimplementation of the transition kernel, or change to the parent simulator is made.

## Predeclared pilot

Four equal-area patches, initial N=K=40, q=(.65,.75,.85,.95), and bundle=(.2,.4,.6,.8). AA assigns trait mass and high-allele frequency in the same ascending order as q. RR reverses both while retaining their marginals. Initial trait distributions are two-point masses at z=0 and z=1 with high mass equal to the bundle; they are synthetic initial conditions, not observed trait measurements.

The EGC update uses the actual trait-bin recruitment, population update, selection, population-weighted allele migration, symmetric mutation (rate 0), and finite binomial genetic drift. Explicit pilot settings: feedback=4.5, barrier=.5025, q coefficients .6/.3/.1, density capacity 40, two-kernel recruitment, inheritance weight .5, finite trait-bin recruitment, migration .1, 12 generations, paired seeds 101–104. These are an **exploratory source-connected pilot**, not a reproduction of the flagship's frozen AA/RR baseline or a preregistered confirmatory effect.

**Event:** first generation >=1 in which no patch has `realised_high_trait_occupied`. This is a first-passage diagnostic of *realised high-investment trait occupancy*, not population extinction and **not an absorbing event**: the two-kernel recruitment can regenerate high trait mass in later generations. First-passage risk must not be described as permanent ecological loss. Population N is floored at 1 in this source.

A 4-seed pilot can validate end-to-end execution and reveal direction, but cannot establish robust comparative event probabilities or uncertainty. The result must be reported as exploratory with the exact event count, and any later confirmatory experiment needs independent seeds, fixed horizon/endpoint, parameter variation and adequate power.

## Claim boundary

This directly executes the original pinned stochastic life-cycle code, unlike PR #227's conditional one-step composition. It does **not** make the finite model an empirically validated natural eco-genetic warning system. No historical AUC, source hashes, natural-null evidence or NEE manuscript is changed.

## Executed first pilot (GitHub Actions 39090630981)

The exact upstream checkout passed. The exploratory 12-generation, 4 paired-seed run reported **AA 1/4 (25%)** versus **RR 3/4 (75%)** for the first generation in which no patch had realised high-investment trait occupancy; AA−RR event-rate difference **−0.50**. This is a *pilot observation in the specified stochastic simulation*, not a confidence-supported ecological generalization, and the event is nonabsorbing. The run artifact is [12122527263](https://github.com/zuizui0223/egwe/actions/runs/39090630981/artifacts/12122527263).

The generic protocol CI initially failed because its standalone repository checkout lacked `EGC_PINNED_ROOT`; this is a test environment failure, not a failure of the pinned simulator or biological hypothesis. The integration test now skips only in that generic environment. The dedicated CI must still checkout the exact pinned upstream and execute the real test and simulation. Neither run may claim an absorbing extinction endpoint.
