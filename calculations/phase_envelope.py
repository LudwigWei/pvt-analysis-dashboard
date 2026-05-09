from typing import Tuple


def _linspace(start: float, stop: float, count: int) -> list[float]:
    if count <= 1:
        return [start]
    step = (stop - start) / (count - 1)
    return [start + step * i for i in range(count)]


def phase_envelope_curve(
    api: float, gas_gravity: float, temp_f: float, reservoir_pressure_psia: float
) -> Tuple[list[float], list[float]]:
    tpc = 169.2 + 349.5 * gas_gravity - 74.0 * gas_gravity * gas_gravity
    ppc = 756.8 - 131.0 * gas_gravity - 3.6 * gas_gravity * gas_gravity
    tc_f = tpc - 459.67
    pc = ppc
    t_arr = _linspace(60.0, tc_f * 1.05, 80)
    p_bub = []
    safe_t = []
    for t in t_arr:
        ratio = (tc_f - t) / tc_f if tc_f != 0 else 0.0
        if ratio <= 0:
            continue
        ratio = max(ratio, 0.0)
        p_bub.append(max(0.0, pc * (1.0 - (ratio ** 1.4))))
        safe_t.append(t)
    return safe_t, p_bub
