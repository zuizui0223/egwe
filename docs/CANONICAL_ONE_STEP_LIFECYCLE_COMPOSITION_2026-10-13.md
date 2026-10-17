# Actual operator composition: what can be inferred beyond the q threshold?

This prospective diagnostic composes the actual pinned EGWE next-interaction, high-allele selection, continuous-population and two-kernel recruitment formulas for the four-patch AA/RR matched-marginal states. Initial density is consistently N/K=40/40=1 in the interaction update, and the population growth update starts from N=40, K=40.

**It is only a one-step deterministic composition.** The population update is a Ricker-type exponential expression; it is not an extinction event, and it does not establish an absorbing functional-loss state. The recruited high-trait mass is a distributional quantity, not a measured offspring cohort. The actual complete model may have additional stochasticity, spatial movement, genotype transmission, and density feedback, so repeated application of this partial composition must not be called the full EGWE life-cycle.

The code reports mean/minimum/maximum conditional population next-step values and recruited high-trait mass, with explicit no-long-horizon and no-natural-evidence flags. This checks whether the previously identified trade-off between a deep local refuge and broad q threshold coverage is visible in immediate downstream quantities, rather than treating q>=0.625 as ecological persistence.

A full fate claim requires the complete parent simulator transition order, patch-specific carrying capacities, functional-loss event definition, and validation of the stochastic transition kernel or actual forward simulation against the pinned baseline. No such claim is made here.
