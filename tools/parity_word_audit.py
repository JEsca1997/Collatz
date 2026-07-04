#!/usr/bin/env python3
"""Exact audit tools for the accelerated odd Collatz map.

For odd n, define T(n) = (3*n + 1) / 2**v2(3*n + 1).

This file is intentionally an exploration / falsification tool.  Its bounded
searches do not prove global statements about Collatz.

It implements the exact prefix identity for a valuation word a_0,...,a_{k-1}:

    2**A_k * n_k = 3**k * n_0 + B_k,
    A_k = sum(a_j),
    B_k = sum(3**(k-1-j) * 2**A_j for j in range(k)).

The tool can:
  * extract actual odd-map valuation words from integer seeds;
  * compute the unique residue class modulo 2**A_k attached to a word;
  * verify a word against an integer seed;
  * search bounded valuation words for exact positive cycle candidates;
  * report bounded prefixes whose linear multiplier 3**k / 2**A_k is >= 1.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from itertools import product
from typing import Iterable, Sequence


def v2(n: int) -> int:
    """Return the exponent of 2 in a positive integer n."""
    if n <= 0:
        raise ValueError("v2 expects a positive integer")
    return (n & -n).bit_length() - 1


def odd_step(n: int) -> tuple[int, int]:
    """One accelerated Collatz step from a positive odd integer."""
    if n <= 0 or n % 2 == 0:
        raise ValueError("odd_step expects a positive odd integer")
    numerator = 3 * n + 1
    a = v2(numerator)
    return numerator >> a, a


@dataclass(frozen=True)
class WordData:
    word: tuple[int, ...]
    total_exponent: int
    numerator_constant: int

    @property
    def length(self) -> int:
        return len(self.word)

    @property
    def modulus(self) -> int:
        return 1 << self.total_exponent

    def linear_noncontracting(self) -> bool:
        """Exact comparison: 3**k / 2**A >= 1, without floating point."""
        return 3 ** self.length >= 2 ** self.total_exponent


def word_data(word: Sequence[int]) -> WordData:
    """Compute A_k and B_k in the exact affine prefix identity."""
    if any(a < 1 for a in word):
        raise ValueError("valuation words must contain positive integers")
    total = 0
    constant = 0
    # If 2**A_j*n_j = 3**j*n_0 + B_j, then
    # B_{j+1} = 3*B_j + 2**A_j.
    for a in word:
        constant = 3 * constant + (1 << total)
        total += a
    return WordData(tuple(word), total, constant)


def word_start_residue(word: Sequence[int]) -> tuple[int, int]:
    """Return (r, 2**A) with n_0 == r mod 2**A for this word.

    The congruence is 3**k*n_0 + B_k == 0 (mod 2**A_k).  Since 3 is
    invertible modulo powers of two, r is unique.
    """
    data = word_data(word)
    if not data.word:
        return 0, 1
    inverse = pow(3 ** data.length, -1, data.modulus)
    residue = (-data.numerator_constant * inverse) % data.modulus
    return residue, data.modulus


def realized_by(start: int, word: Sequence[int]) -> bool:
    """Check exact valuation equality at every accelerated odd step."""
    if start <= 0 or start % 2 == 0:
        return False
    n = start
    for expected in word:
        n, actual = odd_step(n)
        if actual != expected:
            return False
    return True


def orbit_word(start: int, steps: int) -> tuple[list[int], list[int]]:
    """Return (odd orbit values, valuations), beginning at an odd seed."""
    if steps < 0:
        raise ValueError("steps must be nonnegative")
    values = [start]
    valuations: list[int] = []
    n = start
    for _ in range(steps):
        n, a = odd_step(n)
        valuations.append(a)
        values.append(n)
    return values, valuations


def cycle_candidate(word: Sequence[int]) -> int | None:
    """Return a positive integer n with T_word(n)=n, if this word gives one.

    This is an exact test for a cycle with the prescribed valuation word.
    A returned candidate is independently verified against the word.
    """
    data = word_data(word)
    denominator = (1 << data.total_exponent) - 3 ** data.length
    if denominator <= 0 or data.numerator_constant % denominator != 0:
        return None
    start = data.numerator_constant // denominator
    if start <= 0 or start % 2 == 0:
        return None
    if not realized_by(start, word):
        return None
    values, _ = orbit_word(start, data.length)
    return start if values[-1] == start else None


def bounded_cycle_search(max_length: int, max_valuation: int) -> list[tuple[tuple[int, ...], int]]:
    """Exhaustively search a finite valuation box for exact odd-map cycles."""
    if max_length < 1 or max_valuation < 1:
        raise ValueError("bounds must be positive")
    found: list[tuple[tuple[int, ...], int]] = []
    alphabet = range(1, max_valuation + 1)
    for length in range(1, max_length + 1):
        for word in product(alphabet, repeat=length):
            candidate = cycle_candidate(word)
            if candidate is not None:
                found.append((word, candidate))
    return found


def scan_prefixes(limit: int, steps: int) -> list[dict[str, object]]:
    """Collect exact prefix data from odd seeds below limit.

    A record is included whenever its linear multiplier is noncontracting.
    This is evidence collection only; it says nothing about unsearched seeds.
    """
    if limit < 3 or steps < 1:
        return []
    records: list[dict[str, object]] = []
    for start in range(1, limit, 2):
        values, word = orbit_word(start, steps)
        for k in range(1, len(word) + 1):
            data = word_data(word[:k])
            if data.linear_noncontracting():
                residue, modulus = word_start_residue(data.word)
                records.append(
                    {
                        "start": start,
                        "prefix_length": k,
                        "word": data.word,
                        "A": data.total_exponent,
                        "linear_numerator": 3 ** k,
                        "linear_denominator": 2 ** data.total_exponent,
                        "residue": residue,
                        "modulus": modulus,
                        "endpoint": values[k],
                    }
                )
    return records


def run_self_test() -> None:
    """Minimal exact checks for the identities implemented here."""
    # 1 is the known fixed point of the accelerated odd map with valuation word (2).
    assert odd_step(1) == (1, 2)
    assert cycle_candidate((2,)) == 1

    # The standard odd orbit from 5 begins 5 -> 1, with valuation 4.
    values, word = orbit_word(5, 1)
    assert values == [5, 1]
    assert word == [4]
    residue, modulus = word_start_residue((4,))
    assert modulus == 16 and residue == 5
    assert realized_by(5, (4,))

    # Check the affine identity on a nontrivial prefix.
    values, word = orbit_word(7, 3)
    data = word_data(word)
    assert (1 << data.total_exponent) * values[-1] == 3 ** data.length * 7 + data.numerator_constant


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_orbit = sub.add_parser("orbit", help="print an exact odd-map orbit word")
    p_orbit.add_argument("start", type=int)
    p_orbit.add_argument("--steps", type=int, default=20)

    p_cycles = sub.add_parser("cycles", help="bounded exact valuation-word cycle search")
    p_cycles.add_argument("--max-length", type=int, default=8)
    p_cycles.add_argument("--max-valuation", type=int, default=6)

    p_scan = sub.add_parser("scan", help="scan bounded seeds for noncontracting prefixes")
    p_scan.add_argument("--limit", type=int, default=1000)
    p_scan.add_argument("--steps", type=int, default=20)
    p_scan.add_argument("--show", type=int, default=25)

    sub.add_parser("self-test", help="run deterministic identity checks")
    args = parser.parse_args()

    if args.command == "self-test":
        run_self_test()
        print("self-test: PASS")
    elif args.command == "orbit":
        values, word = orbit_word(args.start, args.steps)
        data = word_data(word)
        print(f"values={values}")
        print(f"valuations={word}")
        print(f"A={data.total_exponent}, B={data.numerator_constant}")
        print(f"linear_ratio=3^{data.length}/2^{data.total_exponent}")
    elif args.command == "cycles":
        found = bounded_cycle_search(args.max_length, args.max_valuation)
        for word, start in found:
            print(f"cycle_candidate start={start} word={word}")
        print(f"searched box: length<={args.max_length}, valuation<={args.max_valuation}, found={len(found)}")
    elif args.command == "scan":
        records = scan_prefixes(args.limit, args.steps)
        for record in records[: args.show]:
            print(record)
        print(f"noncontracting prefix records={len(records)} (bounded evidence only)")


if __name__ == "__main__":
    main()
