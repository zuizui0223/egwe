# When is a lost trait actually unrecoverable? Joint high-trait / allele absorption in pinned EGC

**19 October 2026.** New model-specific mathematical analysis. This uses exactly `zuizui0223/egc@dd8ee379d0d3518194c767d16402042525bc00dc`. It is not a natural evolutionary reappearance result, a molecular model of anthocyanin reactivation, or a newly estimated long-horizon ecological functional-loss probability.

## Scientific question

The source-pinned mechanistic experiment in [EGWE PR #230](https://github.com/zuizui0223/egwe/pull/230) established that losing all visible high-investment trait individuals does not necessarily prevent subsequent appearance: under allele-seeded two-kernel recruitment, **47/128 AA** and **51/128 RR** new trajectories had at least one reappearance by generation 24, whereas resident-trait-only recruitment had no reappearance.

But this leaves a deeper question: **when do the *observable phenotype* and the *capacity to produce it* both disappear?** We must distinguish the two because the state \(T=0\) can be reached while the hidden genetic coordinate \(p\) is still positive.

## Exact classification from the source life cycle

Let \(T_j\) denote observed high-trait-bin individuals and \(p_j\) the source's high-allele frequency. Let `h<1` specify the allele-seeded fraction in the two-kernel recruit distribution. The finite life cycle recruits based on **resident** \(p_t\) and \(q_t\), before mutation/drift creates \(p_{t+1}\).

| Current state | Source conditions | Can any high trait occur at t+1? | Biological interpretation ceiling |
| --- | --- | --- | --- |
| \(T_j=0\) for every j; at least one \(p_j>0\) | two-kernel, \(h<1\), positive next population and floor-bounded trait fitness | **Yes, with positive probability** | phenotypic absence does not imply capacity absent |
| \(T_j=0\), \(p_j=0\) for every j | two-kernel, no mutation, no external allele import | **No, at every future step** | joint high-trait/high-allele zero is an absorbing class in this closure |
| \(T_j=0\), \(p_j=0\) for every j | two-kernel, recurrent symmetric allele mutation \(0<\mu<0.5\) | **No at t+1; possible later after allele restoration** | allele mutation creates an opportunity, not immediate high phenotype |
| \(T_j=0\), any p | resident-trait-only, no trait mutation/import | **No at every future step** | phenotype-only zero is absorbing because the allele is disconnected from trait recruitment |

These are mathematical statements about the specified finite trait-bin and allele-seeding life-cycle rules. A landscape or island population in nature may have different developmental regulation, seed banks, recolonisation, diploid dominance or molecular ancestry, and therefore need different evidence.

### Exact conditional allele-return probability when the gene pool was zero

Assume \(p_{j,t}=0\) across every patch and the population is closed. Local allele selection keeps zero at zero; source-defined allele-frequency migration among zero patches stays zero. Symmetric mutation next maps zero to

\[
p_{j,\mathrm{mut}}=\mu.
\]

The fixed source then applies binomial drift with gene copy count

\[
c_j=\max\!\left(2,\operatorname{round}(2N_{e,j,t+1})\right),
\]

where \(N_{e,j,t+1}\) comes from the **same pinned source's** `_effective_size(N_next,q_next,params)`, not a guessed genome copy number. Conditional on the computed \(c_j\), independent finite drift draws imply

\[
\boxed{
\Pr\big(\exists j:p_{j,t+1}>0\mid p_t\equiv0,\mu,c_j\big)
=1-(1-\mu)^{\sum_j c_j}.
}
\]

If \(\mu=0\), this is exactly zero: the allele cannot return from its global loss through the closed model's selection or internal migration. If \(\mu>0\), the probability is strictly positive for positive gene-copy counts.

**Timing matters.** Even when \(p_{t+1}>0\) occurs, trait recruitment at generation t used resident \(p_t=0\). Therefore the high phenotype remains zero at t+1. A high-trait recruit can first occur at **t+2**, *conditional on* the allele surviving in \(p_{t+1}\) and the two-kernel recruitment providing high-trait mass. This is a source-specific one-generation lag, not evidence for a biologically universal waiting time or new mutation at the pigmentation locus.

### Same visible state, different return probability

The model's source operator offers a direct witness to information hidden by phenotypic state summaries.

Construct two hypothetical one-patch states with **identical current high-trait occupancy (zero), interaction \(q=0.2\), population and recruitment mode**, but different resident allele frequencies \(p=0\) versus \(p=0.4\). Under two-kernel recruitment:

- \(p=0\) makes next-generation high-trait recruitment **exactly impossible**;
- \(p=0.4\) gives a **strictly positive** next-generation high-trait recruitment probability.

A summary that contains only observed phenotype and current interaction/population cannot determine both transitions. **This is an exact one-step insufficiency witness for a phenotype-only state, not for a summary that already retains the allele frequency.** It is related to, but distinct from, the earlier matched-marginal spatial alignment theorem: here the hidden genotype values are deliberately different.

### Even potential high-trait nonviability does not prevent a transient expression

The pinned source's trait-performance surface at high trait \(z=1\) is below its viability threshold when \(q=0.2\). But the recruit selection weights have a strictly positive floor, so an allele-seeded high-trait recruit still has nonzero sampling probability even in this unfavorable interaction state.

**Appearance is not self-sustaining maintenance.** A positive conditional probability of high-trait reappearance says nothing by itself about whether the trait can increase, establish a viable component or persist through environmental deterioration. This is precisely why the earlier PR #229 result distinguished first global absence from final occupancy.

## Source checks and execution

- `scripts/egc_joint_trait_gene_absorption.py` uses the pinned source's `_effective_size`, source-trait performance and the prior exact conditional recruitment formula without reconstructing the simulator.
- Dedicated tests confirm the binomial mutant-allele probability against source random draws, verify global joint zero remains zero through seven true source generations when mutation is off, and verify that turning allele mutation on can restore \(p\) one generation before high-trait recruitment is possible.
- A separate hidden-allele witness uses the **same visible trait and q** to show conditional high-trait recovery risk differs with latent p, even below the high-trait viability threshold.

This result is fully internal to the specified eco-genetic closure. The genetic state variable p is an allele-frequency coordinate, not proof that the plant's actual genomic/regulatory pathway for lost flower pigmentation remains available. Nothing here establishes anthocyanin reactivation, homology, or natural trait re-evolution.

## Relation to the main EGWE question

The ecological distinction is now more precise: **a fragmented population may have lost the expressed function while retaining the genetic means to produce the trait, or it may have lost both.** Those are not equivalent futures. A genuine biological test would need both a prospective phenotype/functional endpoint and a validated genetic-developmental capacity assay in the same population/cohort; observation of white flowers alone, or neutral heterozygosity alone, cannot establish the irreversible loss of pigmentation capacity.

No original NEE manuscript, simulation seed lock, source pin, natural first-transfer null or EGWEE results are modified by this theorem note.
