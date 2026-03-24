"""
Ramanujan-sum spectral diagnostics on token-ID sequences (whitepaper §spectral-style).

Projects scalar token indices onto classical Ramanujan sums c_q(n); reports energy
concentration in low orders. This is an interpretability layer, not the full
embedding-level RCP from the paper.
"""

from __future__ import annotations

import cmath
import math
from typing import Any


def _ramanujan_sum_c(q: int, n: int) -> complex:
    """c_q(n) = sum_{1<=k<=q, gcd(k,q)=1} exp(2π i k n / q)."""
    if q <= 0:
        return 0j
    s = 0j
    twopi = 2 * math.pi
    for k in range(1, q + 1):
        if math.gcd(k, q) == 1:
            s += cmath.exp(1j * twopi * k * n / q)
    return s


def spectral_energy_metrics(
    token_ids: list[int],
    *,
    max_q: int = 32,
    max_len: int = 512,
) -> dict[str, Any] | None:
    """
    Compute |R_q|^2 where R_q = sum_i x_i c_q(i), x_i = token ID as float.

    Returns None if sequence is too short or exceeds max_len (skip heavy path).
    """
    n = len(token_ids)
    if n < 2 or n > max_len:
        return None
    max_q = min(max_q, n)
    x = [float(t) for t in token_ids]
    energies: list[tuple[int, float]] = []
    for q in range(1, max_q + 1):
        r_q = 0j
        for i in range(1, n + 1):
            r_q += x[i - 1] * _ramanujan_sum_c(q, i)
        energies.append((q, abs(r_q) ** 2))
    total = sum(e for _, e in energies) + 1e-30
    sorted_e = sorted(energies, key=lambda t: -t[1])
    top5 = sum(e for _, e in sorted_e[:5]) / total
    top8 = sorted_e[:8]
    return {
        "max_q": max_q,
        "sequence_length": n,
        "total_projection_energy": round(float(total), 4),
        "top_orders": [
            {"q": q, "energy_fraction": round(e / total, 6)} for q, e in top8
        ],
        "energy_in_top5_orders_fraction": round(float(top5), 6),
    }
