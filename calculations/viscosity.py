import math


def dead_oil_viscosity(api: float) -> float:
    mu_od = (10 ** (3.0324 - (0.02023 * api))) - 1.0
    return mu_od


def saturated_oil_viscosity(a: float, mu_od: float, b: float) -> float:
    return a * (mu_od ** b)


def undersaturated_oil_viscosity(mu_sat: float, pressure_psia: float, pb_psia: float) -> float:
    if pb_psia <= 0:
        raise ValueError("pb_psia must be positive")
    factor = (pressure_psia / pb_psia) ** 0.25
    return mu_sat * factor
