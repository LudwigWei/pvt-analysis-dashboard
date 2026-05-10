from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class PVTInputs:
    api: float
    gas_gravity: float
    temp_f: float
    bubble_point_psia: float
    rs_pb: float
    reservoir_pressure_psia: float  # Added to support the undersaturated region


def calc_rs(api: float, gas_gravity: float, temp_rankine: float, pressure_psia: float) -> float:
    x = 0.0125 * api - 0.00091 * (temp_rankine - 460.0)
    rs = gas_gravity * ((pressure_psia / 18.2 + 1.4) * (10 ** x)) ** 1.205
    return max(rs, 0.0)


def calc_bo(api: float, gas_gravity: float, rs: float, temp_rankine: float) -> float:
    go = api / (131.5 + api)
    f = rs * (gas_gravity / go) ** 0.5 + 1.25 * (temp_rankine - 460.0)
    return 0.9759 + 0.000120 * (f ** 1.2)


def calc_muo(api: float, temp_rankine: float, rs: float) -> float:
    x = (temp_rankine - 460.0) ** -1.163 * (2.718281828 ** (6.9824 - 0.04463 * api))
    dead = 10 ** x - 1.0
    a = 10.715 * (rs + 100.0) ** -0.515
    b = 5.44 * (rs + 150.0) ** -0.338
    return max(a * (max(dead, 0.001) ** b), 0.01)


def calc_co(api: float, gas_gravity: float, rs: float, temp_rankine: float, pressure_psia: float, bo: float) -> float:
    numerator = 5.615 * rs + 17.2 * (temp_rankine - 460.0) - 1180.0 * gas_gravity + 12.61 * api - 1433.0
    return abs(numerator / (1.0e5 * pressure_psia * bo))


def calc_pseudocritical(gas_gravity: float) -> tuple[float, float]:
    tpc = 168.0 + 325.0 * gas_gravity - 12.5 * gas_gravity * gas_gravity
    ppc = 677.0 + 15.0 * gas_gravity - 37.5 * gas_gravity * gas_gravity
    return tpc, ppc


def calc_z(ppr: float, tpr: float) -> float:
    z = 1.0 - (3.52 * ppr) / (10 ** (0.9813 * tpr)) + (0.274 * ppr * ppr) / (10 ** (0.8157 * tpr))
    return max(z, 0.1)


def calc_bg(temp_rankine: float, pressure_psia: float, z: float) -> float:
    return 0.00504 * z * temp_rankine / pressure_psia


def calc_mug(temp_rankine: float, pressure_psia: float, gas_gravity: float, z: float) -> float:
    mg = 28.97 * gas_gravity
    rho = (pressure_psia * mg) / (z * 10.73 * temp_rankine)
    k = ((9.4 + 0.02 * mg) * temp_rankine ** 1.5) / (209.0 + 19.0 * mg + temp_rankine)
    x = 3.5 + 986.0 / temp_rankine + 0.01 * mg
    y = 2.4 - 0.2 * x
    return max(1.0e-4 * k * (2.718281828 ** (x * (max(rho / 62.4, 0.001) ** y))), 0.005)


def generate_rows(inputs: PVTInputs, steps: int = 15) -> List[dict]:
    t_rankine = inputs.temp_f + 460.0
    tpc, ppc = calc_pseudocritical(inputs.gas_gravity)
    tpr = t_rankine / tpc

    rows = []
    # Always start simulation from the actual Reservoir Pressure
    max_pressure = max(inputs.reservoir_pressure_psia, inputs.bubble_point_psia)
    
    for i in range(steps + 1):
        pressure = max(max_pressure * (1.0 - i / steps), 100.0)
        
        # Rs is capped at Rs_pb for pressures above Bubble Point (Undersaturated Region)
        rs = min(calc_rs(inputs.api, inputs.gas_gravity, t_rankine, pressure), inputs.rs_pb)
        
        # Calculate base saturated properties
        bo = calc_bo(inputs.api, inputs.gas_gravity, rs, t_rankine)
        muo = calc_muo(inputs.api, t_rankine, rs)
        co = calc_co(inputs.api, inputs.gas_gravity, rs, t_rankine, pressure, bo)
        
        # --- Undersaturated Adjustments ---
        if pressure > inputs.bubble_point_psia:
            # Bo shrinks slightly as pressure increases above Pb
            bo = bo * (1.0 - co * (pressure - inputs.bubble_point_psia))
            # Viscosity increases slightly as pressure increases above Pb
            muo = muo * ((pressure / inputs.bubble_point_psia) ** 0.25)

        z = calc_z(pressure / ppc, tpr)
        bg = calc_bg(t_rankine, pressure, z)
        mug = calc_mug(t_rankine, pressure, inputs.gas_gravity, z)
        
        rows.append({
            "P (psia)": pressure,
            "Rs (scf/STB)": rs,
            "Bo (RB/STB)": bo,
            "muo (cp)": muo,
            "co (psi-1)": co,
            "Z-factor": z,
            "Bg (RB/Mscf)": bg,
            "mug (cp)": mug,
        })

    return rows