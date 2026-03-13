"""Utilities for admittance and tap calculations used by Y-bus builder."""

from __future__ import annotations

import cmath
import math


def series_admittance(r: float, x: float) -> complex:
    z = complex(r, x)
    if abs(z) < 1e-14:
        raise ValueError("Branch impedance r + jx is zero; cannot compute admittance")
    return 1.0 / z


def tap_complex(ratio: float, angle_deg: float) -> complex:
    tap_mag = ratio if ratio != 0.0 else 1.0
    angle_rad = math.radians(angle_deg)
    return tap_mag * cmath.exp(1j * angle_rad)
