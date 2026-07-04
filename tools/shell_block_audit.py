#!/usr/bin/env python3
"""Exact verifier for the Part 2 shell-block identities.

The checker works directly with the accelerated odd Collatz map

    T(n) = (3*n + 1) / 2**v2(3*n + 1),  n odd.

It reproduces the manuscript's Phase-B shell coordinates for n == 1 mod 4:

    n = 1 + 2**r * t,  r = v2(n - 1),  t odd.

For r=3 it checks the stated return affine identity whenever the branch
re-enters r=3. For r=2 it checks the stated exit-plus-staircase identity
whenever the trajectory does not immediately terminate at 1.

This is a local identity verifier and bounded exploration tool. A passing scan
is not a global proof of the Collatz conjecture.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Iterable


def v2(n: int) -> int:
    if n <= 0:
        raise ValueError("v2 expects a positive integer")
    return (n & -n).bit_length() - 1


def odd_step(n: int) -> tuple[int, int]:
    if n <= 0 or n % 2 == 0:
        raise ValueError("odd_step expects a positive odd integer")
    numerator = 3 * n + 1
    shift = v2(numerator)
    return numerator >> shift, shift


def shell(n: int) -> tuple[int, int]:
    """Return (r,t) for a nontrivial Phase-B entry n == 1 mod 4."""
    if n <= 1 or n % 4 != 1:
        raise ValueError("shell expects n > 1 with n == 1 mod 4")
    r = v2(n - 1)
    return r, (n - 1) >> r


def next_phase_b(n: int, max_odd_steps: int = 10_000) -> tuple[int | None, list[tuple[int, int]]]:
    """Advance from one Phase-B entry to the next, recording odd-map steps.

    Returns None if the odd orbit reaches the fixed point 1 first.
    """
    if n <= 0 or n % 2 == 0 or n % 4 != 1:
        raise ValueError("next_phase_b expects a positive Phase-B entry")
    trace: list[tuple[int, int]] = []
    current = n
    for _ in range(max_odd_steps):
        current, shift = odd_step(current)
        trace.append((current, shift))
        if current == 1:
            return None, trace
        if current % 4 == 1:
            return current, trace
    raise RuntimeError("Phase-B search exceeded max_odd_steps")


def next_special_shell(n: int, max_segments: int = 10_000) -> tuple[int | None, list[tuple[int, int, int]]]:
    """Advance until the next Phase-B state with shell r in {2,3}."""
    current = n
    trace: list[tuple[int, int, int]] = []
    for _ in range(max_segments):
        current, _segment = next_phase_b(current)
        if current is None:
            return None, trace
        r, t = shell(current)
        trace.append((current, r, t))
        if r in (2, 3):
            return current, trace
    raise RuntimeError("special-shell search exceeded max_segments")


@dataclass(frozen=True)
class ReturnCheck:
    start: int
    b: int
    d: int
    target: int
    endpoint: int | None
    affine_ok: bool
    endpoint_ok: bool


@dataclass(frozen=True)
class ExitCheck:
    start: int
    e: int
    a: int
    c: int
    target: int | None
    endpoint: int | None
    affine_ok: bool
    endpoint_ok: bool
    terminal: bool


def verify_return_reentry(n: int) -> ReturnCheck | None:
    """Check Proposition 4.1 only on its stated even-c reentry branch.

    If the intermediate valuation c=v2(3**b*u-1) is odd, this is not the
    critical-shell reentry case and the function returns None.
    """
    r, t = shell(n)
    if r != 3:
        raise ValueError("verify_return_reentry expects shell r=3")

    b = v2(3 * t + 1)
    u = (3 * t + 1) >> b
    q = 3**b * u - 1
    c = v2(q)
    if c % 2:
        return None

    d = c // 2
    v = q >> c
    t_prime = 3 ** (d - 1) * v
    target = 1 + 8 * t_prime
    constant = 3 ** (d - 1) * (3**b - 2**b)
    affine_ok = (2 ** (b + 2 * d)) * t_prime == 3 ** (b + d) * t + constant
    endpoint, _trace = next_special_shell(n)
    return ReturnCheck(n, b, d, target, endpoint, affine_ok, endpoint == target)


def verify_exit_block(n: int) -> ExitCheck:
    """Check Propositions 5.1--5.2 for an r=2 shell entry.

    The q=0 case is the direct arrival at 1 and is labelled terminal rather
    than forced into the positive t1 notation used for nonterminal blocks.
    """
    r, x = shell(n)
    if r != 2:
        raise ValueError("verify_exit_block expects shell r=2")

    e = v2(3 * x + 1)
    v = (3 * x + 1) >> e
    a = v2(v + 1)
    u = (v + 1) >> a
    q = 3 ** (a - 1) * u - 1

    if q == 0:
        endpoint, _trace = next_special_shell(n)
        return ExitCheck(n, e, a, 0, 1, endpoint, True, endpoint is None, True)

    c = v2(q)
    t1 = q >> c
    d_const = 3 ** (a - 1) * (2**e + 1) - 2 ** (e + a)

    if c % 2 == 0:
        h = c // 2
        t_prime = 3 ** (h - 1) * t1
        target = 1 + 8 * t_prime
        affine_ok = (2 ** (e + a + 2 * h)) * t_prime == 3 ** (a + h - 1) * x + 3 ** (h - 1) * d_const
    else:
        h = (c + 1) // 2
        x_prime = 3 ** (h - 1) * t1
        target = 1 + 4 * x_prime
        affine_ok = (2 ** (e + a + 2 * h - 1)) * x_prime == 3 ** (a + h - 1) * x + 3 ** (h - 1) * d_const

    endpoint, _trace = next_special_shell(n)
    return ExitCheck(n, e, a, c, target, endpoint, affine_ok, endpoint == target, False)


def phase_b_entries(limit: int) -> Iterable[int]:
    for n in range(5, limit + 1, 4):
        yield n


def scan(limit: int) -> dict[str, int]:
    """Bounded identity scan over all Phase-B entries <= limit."""
    stats = {
        "return_reentries_checked": 0,
        "return_branch_skipped": 0,
        "exit_blocks_checked": 0,
        "terminal_exit_cases": 0,
        "failures": 0,
    }
    for n in phase_b_entries(limit):
        r, _t = shell(n)
        if r == 3:
            check = verify_return_reentry(n)
            if check is None:
                stats["return_branch_skipped"] += 1
            else:
                stats["return_reentries_checked"] += 1
                if not (check.affine_ok and check.endpoint_ok):
                    stats["failures"] += 1
                    print(f"RETURN MISMATCH: {check}")
        elif r == 2:
            check = verify_exit_block(n)
            if check.terminal:
                stats["terminal_exit_cases"] += 1
            else:
                stats["exit_blocks_checked"] += 1
            if not (check.affine_ok and check.endpoint_ok):
                stats["failures"] += 1
                print(f"EXIT MISMATCH: {check}")
    return stats


def self_test() -> None:
    # Critical-shell return example documented by direct arithmetic:
    # 41=1+8*5 -> 121=1+8*15.
    return_check = verify_return_reentry(41)
    assert return_check is not None
    assert return_check.target == 121
    assert return_check.affine_ok and return_check.endpoint_ok

    # Two nonterminal r=2 examples.
    for n, target in ((13, 5), (29, 13)):
        exit_check = verify_exit_block(n)
        assert exit_check.target == target
        assert exit_check.affine_ok and exit_check.endpoint_ok

    # A terminal r=2 case.
    terminal = verify_exit_block(5)
    assert terminal.terminal and terminal.endpoint is None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p_check = sub.add_parser("check", help="inspect one Phase-B shell entry")
    p_check.add_argument("n", type=int)
    p_scan = sub.add_parser("scan", help="bounded scan of shell formulas")
    p_scan.add_argument("--limit", type=int, default=100_000)
    sub.add_parser("self-test", help="run deterministic checks")
    args = parser.parse_args()

    if args.command == "self-test":
        self_test()
        print("self-test: PASS")
    elif args.command == "check":
        r, t = shell(args.n)
        print({"n": args.n, "r": r, "parameter": t})
        if r == 3:
            print(verify_return_reentry(args.n))
        elif r == 2:
            print(verify_exit_block(args.n))
        else:
            print("r>=4: rigid staircase state; not a block start")
    elif args.command == "scan":
        print(scan(args.limit))


if __name__ == "__main__":
    main()
