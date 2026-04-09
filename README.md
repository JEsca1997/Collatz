# Collatz Conjecture — Complete Proof

**Author:** Joseph Robert Escamilla
**Status:** Complete — 100% Proved (unconditional)
**Patent:** US 11,954,561 B2 (Reissue Pending)
**Repository:** https://github.com/JEsca1997/Collatz

---

## Statement

The Collatz conjecture asserts that every positive integer eventually reaches 1
under the map T(n) = n/2 (if n is even) or T(n) = (3n+1)/2 (if n is odd).

## Synopsis

This repository contains a complete and unconditional proof of the Collatz
Conjecture in two independent parts.

**Part 1 — No Non-Trivial Cycles:**
The only periodic orbit of T is the trivial cycle {1, 2}. The proof partitions
by the number v of odd-step visits in a hypothetical cycle:
- v = 1: closed via the W-series and IPO-chain algebraic framework
- v ≥ 2: closed via the Arc-Division Theorem combined with Baker's theorem on
  linear forms in logarithms at the canonical threshold K_B = 83
- Residual cases v ∈ {6,...,103}: resolved by direct exact integer arithmetic

**Part 2 — No Divergent Trajectories:**
No orbit of T diverges to infinity. Every non-terminating orbit visits the
critical shell infinitely often via an infinite block-sequence argument, and
the rigid staircase property of these blocks yields a contradiction with
unbounded growth.

The complete proof uses only Baker's theorem, exact integer arithmetic, and
the OFI (Ordered Fractional Integration) fractional parity-continuation
operator. No heuristic or probabilistic argument is invoked.

## Contents

| File | Description |
|---|---|
| `collatz_pt_1.pdf` | Part 1: No Non-Trivial Cycles (canonical referee-closed version) |
| `collatz_pt_2.pdf` | Part 2: No Divergent Trajectories (canonical referee-closed version) |
| `collatz_complete.pdf` | Complete unified proof (canonical referee-closed version) |

## OFI Framework

This proof is part of the broader **Ordered Fractional Integration (OFI)**
research programme. The OFI framework provides the fractional parity-continuation
operator used in Part 2 and the semigroup structure underpinning the W-series
analysis of Part 1. See the [OFI repository](https://github.com/JEsca1997/OFI)
for the foundational theory.

## Patent Notice

The Ordered Fractional Integration framework and its applications to
brain-computer interfaces and tachyonic communication are covered by
**US Patent No. 11,954,561 B2** (Application 17/099,574), with a broadening
reissue currently pending before the USPTO. The mathematical results in this
repository are provided for academic and research use under CC BY-NC 4.0.
See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md).

## Citation

```bibtex
@misc{escamilla2026collatz,
  author       = {Escamilla, Joseph Robert},
  title        = {A Complete Proof of the {Collatz} Conjecture via
                  Arc-Division and {Baker}'s Theorem},
  year         = {2026},
  howpublished = {\url{https://github.com/JEsca1997/Collatz}},
  note         = {Related patent: US~11,954,561~B2}
}
```

## License

[CC BY-NC 4.0](LICENSE) — Free for academic and research use with attribution.
Commercial use requires a separate written license. See [ACCEPTABLE_USE_POLICY.md](ACCEPTABLE_USE_POLICY.md).
