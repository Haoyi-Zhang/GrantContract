# Weakest Observable Grant Contracts — artifact

This repository is the executable companion to **Weakest Observable Grant Contracts for Bounded Coherence Bridges**. It contains an owned finite model, a generic observer synthesizer for the declared one-shot plant class, two bridge encodings, retained deterministic outputs, proof notes, tests, and source/claim ledgers.

## Result and scope

For a finite acyclic plant with one irreversible controllable `grant`, let `W` be the states from which forced grant universally terminates in a declared good state, and let `K(h)` be the physical states compatible with visible history `h`. The unique greatest correct observation-based contract is

```text
C* = { reachable h | K(h) is a subset of W }.
```

A correct nonblocking contract exists exactly when every reachable environment-quiescent pair `(q,h)` has `K(h) subset W`. `src/contracts.py` implements the finite constructive algorithm: reverse-DAG kernel computation, hidden-closure observer construction, greatest permission, and the exact quiescence test. It rejects cyclic inputs, phase overlap, pre-grant or nonterminal good states, and a second grant rather than applying an inapplicable theorem.

The bounded bridge fixes one producer, one consumer, one release/acquire episode, one data line, one final demand read, one controllable grant, and an initial old-response count in `[0,K]`. No transition creates new stale traffic. For raw acknowledgment timing and any deterministic receipt map `rho`, a correct nonblocking contract exists exactly when the symbol `rho(0)` is not reused for any positive pending count. Thus two receipt classes are necessary and sufficient for `K>=1`; the bit `[p=0]` is a matching implementation. Drain-before-acknowledge and persistent generation filtering establish the same stable fact inside the mechanism.

The detailed Boolean `K=1` encoding and the parameterized count encoding are separately implemented but share authorship and mathematical premises. Their reachable labeled plants are isomorphic at `K=1`; this is finite corroboration, not independent external validation. No CXL, MemGlue, C3, vCXLGen, ShimGen, Synapse, commercial hierarchy, recurrent protocol, or full C11 implementation is claimed to satisfy the theorem premises.

## Retained evidence

The retained scientific outputs contain:

- 25 parameterized plants and 50 greatest contracts for `K=0,...,4`;
- 1,993 parameterized transition, kernel, knowledge, prediction, transfer, and receipt checks, with no reported mismatch;
- an exhaustive tiny-plant meta-oracle covering 486 plants, all 1,188 contracts over their reachable histories, and all 75 canonical receipt partitions through bound four, with zero disagreement and two targeted mutants killed;
- five detailed `K=1` plants, ten controlled cases, 140 maximal paths, 132 completed paths, and eight blocked paths;
- 270 completed-event profiles, 2,892 candidates, 2,877 background-admitted graphs, 2,848 target-good graphs, and 199 minimum source-word certificates;
- explicit unsafe-grant and missed-safe-grant mutants, distinct operational failure signatures, and semantic target mutations.

These are exhaustive results only inside the retained finite universes. They are not probabilities, workload coverage, hardware error rates, latency, throughput, or a proof by induction from `K<=4`.

## Validation commands

Requirements are Python 3 and its standard library on POSIX/Linux, including `resource`. The scientific code uses one worker, no randomness, no network, no solver, no model API, no GPU, and no private data.

From the repository root:

```sh
python -m unittest discover -s tests -v
python verify.py --output results
```

The current suite contains **69 deterministic tests**. `verify.py` checks the eleven retained stable outputs, explicit contract-audit fields, the tiny-plant meta-oracle, the pinned public-source audit, and the 33-record reference ledger. These commands validate the delivered package without rerunning the entire scientific enumeration.

A fresh full replay is available as a separate action:

```sh
python reproduce.py --output reproduced
python verify.py --output reproduced
```

`reproduced` must not exist or must be empty. A successful replay establishes deterministic agreement with the delivered finite results. It does not mechanize the handwritten general proofs, make same-authorship implementations independent, or discharge a simulation for a real protocol.

## Repository map

| Path | Role |
|---|---|
| `src/contracts.py` | Generic exact synthesis for explicit finite acyclic one-shot grant plants |
| `src/parametric_bridge.py` | Counted-response plants, exact kernels, knowledge sets, contracts, modeled taxonomy, and receipt partition helper |
| `src/metaoracle.py` | Exhaustive direct-path oracle for the declared 486-plant universe and all receipt partitions through bound four |
| `src/bridge.py` | Detailed `K=1` physical plants, policies, complete paths, and observation fibers |
| `src/bridge_study.py` | Detailed path summaries, MP trace maps, suffix checks, and paired witnesses |
| `src/model.py` | Finite read/write event-graph construction and separately structured semantic oracle |
| `src/observe.py` | Completed-observation fibers, exact masks, hitting sets, and rectangularity diagnostics |
| `proofs/observable-grants.md` | General contract, nonblocking, monotonicity, lifting, receipt, taxonomy, and product proofs |
| `proofs/operational-bridge.md` | Detailed `K=1` transition, progress, and MP mapping argument |
| `proofs/finite-contracts.md` | Completed-outcome quotient and information diagnostics |
| `tests/` | 69 deterministic regression, mutation, synthesis, source-audit, and metadata tests |
| `results/` | Retained stable outputs plus resource, reproduction, and accounting records |
| `claim_evidence_ledger.csv` | Claim-to-proof/check/result traceability |
| `reference_audit.csv` | 33 cited records: 31 scholarly works, one author corrigendum, and one pinned public artifact |
| `public_protocol_audit.csv` | Five immutable source facts and explicit non-lifting boundaries for the vCXLGen audit |
| `external_resources.csv` | Scholarly, official, and public-artifact source inventory with integration boundaries |

The eleven stable result files are:

```text
graphs.csv
observations.csv
summary.json
witnesses.json
bridge-plants.json
bridge-guards.json
bridge-cases.json
bridge-observations.json
bridge-summary.json
parametric-summary.json
metaoracle-summary.json
```

Resource and campaign records are intentionally excluded from stable-value equality because timings vary and the campaign history is noncompliant.

## Reproducibility and campaign accounting

The retained outputs contain 18,963 declared finite obligations. A prior clean replay measured the first 14,568 of them with one worker, approximately 1.38 process-CPU seconds after imports, and about 95.5 MiB peak RSS; the later 4,395-obligation tiny-plant meta-oracle is not included in those timing figures. These are checker costs, not architecture measurements.

The cumulative campaign ceiling was not satisfied. The original 100,000-obligation ceiling was exceeded, and a later prospective 160,000 ceiling was also exceeded. The documented conservative lower bound is updated after every known full-universe invocation; subsequent partial test invocations were not individually metered, so no exact all-in total or remaining reserve is asserted. The final revision validates retained results and builds the paper but deliberately does not run another full `reproduce.py` campaign. See `results/campaign-accounting.json`.

## Provenance and license

Project-specific source is MIT-licensed. External papers and public artifacts are cited or inventoried but not redistributed. The public vCXLGen artifact is inspected only as qualitative evidence that one model path separates ordinary ACK, pending-ack state, a zero-tested ALL_ACKS trigger, and later completion. File-local notices are preserved in the audit; no upstream source is redistributed, modified, benchmarked, or claimed to satisfy this model.

ChatGPT (GPT-5.6 Sol Pro) was used substantively for mathematics, implementation, finite checking, literature comparison, figures, tables, and drafting. The named human authors remain responsible for independent verification, authorship eligibility, originality, disclosure, and any external use. No submission, acceptance, or independent peer review is asserted.
