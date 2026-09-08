# FROZEN FALLBACK — NOT CURRENT-EVIDENCE COMPLETE FOR SUBMISSION

> The six-rule full-denominator audit below remains scientifically valid, but this standalone warning manuscript was frozen before the prospectively locked continuous last-refuge holdout. While the NEE flagship is active, this manuscript is not a simultaneous submission. Before any later reactivation, it must incorporate or explicitly report the last-refuge result (AUC 0.92734, +0.02135 beyond co-timed max q) and the predeclared `H_alpha` directional inversion (AUC 0.23253) without post-hoc sign rescue.

# Event-conditioned temporal precedence is not predictive warning validity

**Publication status:** frozen fallback, not current-evidence complete for submission. This manuscript preserves the six-rule full-denominator warning result, but it is not an active publication lane while the NEE flagship is under consideration. It does not make a joint-state or cross-system convergence claim.

## Abstract

We evaluated six predeclared and frozen baseline-relative genetic-diversity
thresholds against the full baseline-eligible denominator for the first time
under their frozen protocol, rather than only among trajectories that later
experienced functional-trait loss. We separate that event-conditioned ordering
object from full-denominator discrimination exactly. For a binary horizon
marker, perfect event-conditioned precedence forces sensitivity to one but
leaves non-event specificity unconstrained; binary-marker AUC is therefore
`(1 + specificity)/2` and can range from chance to perfect without changing the
perfect lead result. The two independently seeded finite-model ensembles were
audited without changing endpoints or rerunning trajectories. Every threshold
preceded every observed functional-trait loss in the inherited and fresh
ensembles (35/35 and 33/33), but every threshold also fired in every non-event
trajectory by the common horizon (48/48 and 49/49). Across the six repeated
threshold endpoints, these correspond to 408 event-threshold lead records and
582 non-event-threshold firing records; thresholds within a trajectory are
repeated endpoints, not independent biological replicates. The two ensembles
therefore attain the sharp worst-discrimination endpoint permitted by perfect
precedence: sensitivity 1, specificity 0, and binary-marker AUC 0.5.
Event-conditioned temporal precedence can thus reproduce perfectly while
supplying no horizon-level discrimination. The result invalidates these six
rules as predictive warnings in the tested state; it does not show that genetic
diversity contains no predictive information or that no alternative warning
statistic could succeed.

## Introduction

A precursor may occur before every observed failure and still be useless for
predicting which units will fail. The distinction is a denominator problem.
Event-conditioned ordering estimates whether a threshold precedes an event
among trajectories in which both threshold and event are observed. Predictive
warning validity additionally requires the rule not to fire indiscriminately in
trajectories that remain event-free through the same administrative horizon.

Early-warning research has established both why advance signals are attractive
and why their validation is difficult. Critical-transition theory identifies
conditions under which changes in system dynamics can precede abrupt shifts
(Scheffer et al. 2009), and experimental deterioration studies have demonstrated
pre-extinction signals in controlled populations (Drake & Griffen 2010). But
regime shifts can also occur without warning (Hastings & Wysham 2010), the power
to detect warning signals can be sharply limited (Boettiger & Hastings 2012),
and stochastic transitions can defeat generic early-warning expectations
(Boettiger & Hastings 2013). Natural-system evaluations therefore emphasize
prospective performance of specified indicators rather than temporal ordering
alone (Gsell et al. 2016).

Genetic diversity is nevertheless a biologically reasonable quantity to monitor.
Conservation genetics has long proposed genetic monitoring as a management tool
(Schwartz et al. 2007), genetic diversity can affect ecological performance
(Hughes et al. 2008), and genomic variation can be important for biodiversity
and ecosystem function (Stange et al. 2021). Those biological motivations do
not by themselves validate any particular diversity threshold as a predictive
warning. A candidate rule still has to discriminate future-event trajectories
from comparable non-event trajectories under a declared horizon and eligibility
contract.

The distinction is especially important here because diversity decline is
biologically plausible under deterioration and can therefore look compelling in
event-only sequences. A perfect lead count is not, by itself, evidence of
specificity, risk separation, or prospective discrimination. More strongly, the
event-only denominator does not contain the information needed to fix
specificity: holding every event trajectory and its perfect lead relation
constant, marker occurrence among non-events can vary from none to all. For a
binary horizon marker this allows AUC to vary from 1 to 0.5 while
event-conditioned precedence remains perfect. We test the sharp lower endpoint
of that possibility using two frozen ensembles in which the loss process was
defined before warning values were opened and all baseline-eligible non-events
were retained.

Our question is deliberately narrow: do six already frozen relative-diversity
rules distinguish trajectories with realised functional-trait loss from those
without loss by a common horizon? No threshold, seed, schedule, eligibility
rule, or endpoint was changed for this audit. The contribution is therefore not
a new generic early-warning statistic. It is a frozen-rule validity audit plus an
exact statement of what perfect event-conditioned precedence does and does not
identify about full-denominator discrimination.

## Methods

### Provenance and separation of ensembles

The inherited ensemble comes from the pinned scientific parent repository at
commit `dd8ee379d0d3518194c767d16402042525bc00dc` and its frozen validation run
`28500796310`. The fresh ensemble comes from the independently seeded Phase-V
run `32636847803`. Parent and extension trajectories were audited separately
and were never pooled.

The inherited ensemble attempted 100 trajectories and retained 83 that were
baseline-eligible under the frozen rule. Thirty-five reached realised
functional-trait loss and 48 remained event-free through the common horizon.
The fresh ensemble attempted 100 trajectories, retained 82 baseline-eligible
trajectories, observed 33 losses, and retained 49 horizon non-events.

### Frozen warning rules

The six endpoints were the first post-baseline generations at which either
`H_alpha` or `H_gamma` declined by 5%, 10%, or 20% from its own baseline. The
fresh ensemble used the same endpoints without recalibration. The historical
`strict_replication` decision required sufficient valid warning/loss pairs and
all valid pairs to be leads; it was a rule about ordering among valid event
pairs, not a predictive-validity classification.

### Full-denominator audit

For every endpoint and ensemble, the audit restored all baseline-eligible
trajectories. It recorded whether the threshold fired by the administrative
horizon and whether realised functional-trait loss occurred by that horizon.
It then reported sensitivity, false-positive rate, specificity, positive and
negative predictive value, and AUC for the binary horizon marker.

Non-events remain right-censored for event-time inference but are known
event-free controls at the shared horizon. Endpoints within a trajectory are
repeated measurements, not independent biological replicates. Continuous AUC
was not introduced because the locked rules do not supply a common-time
continuous score. Fixed ramp-end summaries are retained only as secondary
descriptions.

### Exact denominator theorem for a binary horizon marker

Let `Y=1` denote loss by the common horizon and `M=1` denote marker firing by
that horizon. Perfect event-conditioned precedence implies `M=1` for every
`Y=1` trajectory, hence sensitivity is exactly one. Let `n_0` be the number of
non-events and let `f` of them be marker-positive. The event-conditioned lead
statement places no restriction on `f`, so

```text
specificity = (n_0 - f) / n_0.
```

Every finite specificity grid point from zero to one can therefore coexist with
the same perfect event lead result. For a binary score, the ROC curve contains
only `(0,0)`, `(FPR,TPR)` and `(1,1)`, so its trapezoidal area is

```text
AUC = (sensitivity + specificity) / 2.
```

Under perfect precedence,

```text
AUC = (1 + specificity) / 2
    = 1 - f/(2 n_0).
```

Thus perfect precedence is compatible with binary-marker AUC from 0.5 to 1.0.
When `f=n_0`, specificity is zero and AUC is 0.5. Positive predictive value is
then event prevalence, `n_1/(n_1+n_0)`. A complete proof, sharpness argument and
independent pairwise-ranking verification are provided in
`docs/PRECEDENCE_DISCRIMINATION_THEOREM_2026-09-03.md` and
`tests/test_precedence_discrimination_theorem.py`.

## Results

### Event-conditioned ordering reproduced

For each of the six endpoints, the inherited rule crossed before all 35
observed losses. The independently seeded fresh ensemble reproduced the same
valid-pair ordering for all 33 observed losses. The corresponding counts were
therefore 35/35 and 33/33, with zero ties or lags in the frozen valid-pair
classification.

This preserves the historical `strict_replication` decision as a protocol fact:
conditional on observing both a threshold crossing and a loss, the crossing
preceded the loss in both ensembles.

### The same rules fired in every non-event trajectory

Every one of the six endpoints also crossed by the horizon in all 48 inherited
non-event trajectories and all 49 fresh non-event trajectories. Consequently,
for every endpoint in both ensembles, sensitivity was 1.0, false-positive rate
was 1.0, specificity was 0, and binary-marker AUC was 0.5. Positive predictive
value equalled event prevalence, 0.422 in the inherited ensemble and 0.402 in
the fresh ensemble; negative predictive value was undefined because no
trajectory remained marker-negative.

Summed across the six repeated threshold endpoints, the audit contains 408
event-threshold lead records and 582 non-event-threshold firing records. These
counts are descriptive endpoint records only: the six thresholds evaluated on
one trajectory are repeated measurements and are not treated as 990 independent
biological trajectories.

Fixed ramp-end AUC ranged from `0.500` to `0.538` in the inherited ensemble and
from `0.500` to `0.510` in the fresh ensemble. These secondary fixed-time
summaries do not rescue the frozen horizon rules.

### Both ensembles attain the sharp lower discrimination endpoint

The exact denominator theorem sharpens the interpretation of these counts. A
perfect event-conditioned lead result does not itself force chance
classification: it is also compatible with specificity one and AUC one if no
non-event fires. The observed result is stronger. Because all non-events fired,
both ensembles attain `f=n_0`, the sharp minimum binary AUC compatible with the
perfect-sensitivity constraint. Thus the contrast is not merely “there were
false positives.” The frozen warning rules reproduce perfect temporal ordering
while occupying the worst full-denominator discrimination endpoint available to
a binary marker with sensitivity one.

## Discussion

### Temporal precedence is not warning validity

The two ensembles show the strongest possible separation between an
event-conditioned ordering claim and a predictive claim. The ordering result
reproduced without exception, yet the full-denominator classifier performed at
chance because every event and every non-event crossed the same rules. The
correct conclusion is therefore:

> Event-conditioned temporal precedence can be perfectly reproducible while
> full-denominator predictive warning validity is absent.

The theorem identifies why this is possible. Event-conditioned perfect
precedence fixes the event side of the confusion matrix but leaves the non-event
side mathematically unspecified. Predictive discrimination cannot be recovered
from the event denominator because its missing quantity is precisely how often
the same rule fires when the event does not occur.

This result complements, rather than contradicts, the broader early-warning
literature. Early-warning signals can exist under some dynamics (Scheffer et al.
2009; Drake & Griffen 2010), can be weak or absent under others (Hastings &
Wysham 2010; Boettiger & Hastings 2013), and can be difficult to detect with
finite noisy data (Boettiger & Hastings 2012; Gsell et al. 2016). Our result
addresses a different failure mode: even when a predeclared threshold has
perfect observed lead ordering, the rule can still have no prospective
horizon-level discrimination if it fires just as reliably in non-events.

Loss-process calibration remains necessary: a warning cannot be interpreted
without a declared target event, eligibility rule, and horizon. Calibration is
not sufficient, however, because selecting only trajectories with both warning
and loss removes the observations needed to estimate false-positive behaviour.
The same principle applies to biologically motivated genetic monitoring: the
importance of genetic or genomic variation (Schwartz et al. 2007; Hughes et al.
2008; Stange et al. 2021) motivates what may be worth measuring, not the
predictive validity of a particular frozen threshold.

### Claim boundary

This audit rejects predictive validity for the six frozen 5%, 10%, and 20%
`H_alpha`/`H_gamma` rules in these two symmetric finite-model ensembles. It
does not establish a universal genetic threshold, show that diversity contains
no predictive information generally, test every continuous score, or imply
that an independently specified multivariate warning could not discriminate.
The denominator theorem is likewise limited to the declared binary horizon
marker; continuous and time-dependent prediction objects require their own
validation theory. No endpoint rerun or post-result threshold search is
authorised by this negative result.

The separately calibrated Protocol-003 domains remain bounded portability
evidence. They do not identify a single-factor direction effect and are not a
substitute for the full-denominator result presented here.

## Data and code availability

The compact 1,200-row trajectory-endpoint table is stored at
`artifacts/warning_validity/trajectory_endpoint_records.csv` and is fixed by
`artifacts/warning_validity/source_manifest.json` with SHA-256
`65295c612042557abb46115a2c408b883f0b516c8d5af974423b895f54a7c7ab`.
The derived JSON and publication table are
`artifacts/prepublication_review/warning_validity_audit.json` and
`manuscript/tables/warning_validity_audit.csv`. The audit implementation,
denominator-theorem helper and tests are version controlled. Frozen trajectories
and results were not modified for this manuscript split.

## References

Boettiger, C. & Hastings, A. (2012). Quantifying limits to detection of early warning for critical transitions. *Journal of the Royal Society Interface*, **9**, 2527–2539. doi:10.1098/rsif.2012.0125

Boettiger, C. & Hastings, A. (2013). No early warning signals for stochastic transitions: insights from large deviation theory. *Proceedings of the Royal Society B*, **280**, 20131372. doi:10.1098/rspb.2013.1372

Drake, J.M. & Griffen, B.D. (2010). Early warning signals of extinction in deteriorating environments. *Nature*, **467**, 456–459. doi:10.1038/nature09389

Gsell, A.S., Scharfenberger, U., Özkundakci, D., Walters, A.W., Hansson, L.-A., Janssen, A.B.G., Nõges, P., Reid, P.C., Schindler, D.E., van Donk, E., Dakos, V. & Adrian, R. (2016). Evaluating early-warning indicators of critical transitions in natural aquatic ecosystems. *Proceedings of the National Academy of Sciences USA*, **113**, E8089–E8095. doi:10.1073/pnas.1608242113

Hastings, A. & Wysham, D.B. (2010). Regime shifts in ecological systems can occur with no warning. *Ecology Letters*, **13**, 464–472. doi:10.1111/j.1461-0248.2010.01439.x

Hughes, A.R., Inouye, B.D., Johnson, M.T.J., Underwood, N. & Vellend, M. (2008). Ecological consequences of genetic diversity. *Ecology Letters*, **11**, 609–623. doi:10.1111/j.1461-0248.2008.01179.x

Scheffer, M., Bascompte, J., Brock, W.A., Brovkin, V., Carpenter, S.R., Dakos, V., Held, H., van Nes, E.H., Rietkerk, M. & Sugihara, G. (2009). Early-warning signals for critical transitions. *Nature*, **461**, 53–59. doi:10.1038/nature08227

Schwartz, M.K., Luikart, G. & Waples, R.S. (2007). Genetic monitoring as a promising tool for conservation and management. *Trends in Ecology & Evolution*, **22**, 25–33. doi:10.1016/j.tree.2006.08.009

Stange, M., Barrett, R.D.H. & Hendry, A.P. (2021). The importance of genomic variation for biodiversity, ecosystems and people. *Nature Reviews Genetics*, **22**, 89–105. doi:10.1038/s41576-020-00288-7
