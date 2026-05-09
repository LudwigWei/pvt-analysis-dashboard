import math
from typing import Tuple


def bubble_point_pressure(rs_scf_stb: float, gas_gravity: float, temp_f: float, api: float) -> float:
    pb = 18.2 * (((rs_scf_stb / gas_gravity) ** 0.83) * (10 ** ((0.00091 * temp_f) - (0.0125 * api))) - 1.4)
    return pb


def oil_formation_volume_factor(v_reservoir: float, v_stocktank: float) -> float:
    if v_stocktank == 0:
        raise ValueError("v_stocktank must be non-zero")
    return v_reservoir / v_stocktank


def solution_gor_standing(pressure_psia: float, gas_gravity: float, temp_f: float, api: float) -> float:
    exponent = (pressure_psia / 18.2 + 1.4)
    rs = gas_gravity * (exponent ** (1.0 / 0.83)) * (10 ** ((0.0125 * api) - (0.00091 * temp_f)))
    return rs


def bubble_point_curve(
    pressures_psia: list[float], gas_gravity: float, temp_f: float, api: float
) -> Tuple[list[float], list[float]]:
    rs_values = [solution_gor_standing(p, gas_gravity, temp_f, api) for p in pressures_psia]
    return pressures_psia, rs_values
