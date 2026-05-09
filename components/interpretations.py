from typing import List


def build_interpretations(
    analysis_key: str, rows_data: List[dict], snapshot: dict
) -> List[str]:
    if not rows_data:
        return ["No results to interpret yet."]

    first = rows_data[0]
    last = rows_data[-1]
    rs_drop = first["Rs (scf/STB)"] - last["Rs (scf/STB)"]
    bo_drop = first["Bo (RB/STB)"] - last["Bo (RB/STB)"]
    muo_change = last["muo (cp)"] - first["muo (cp)"]
    co_change = last["co (psi-1)"] - first["co (psi-1)"]

    pr = snapshot.get("reservoir_pressure_psia", 0.0)

    if analysis_key == "bubble_point":
        return [
            "Bubble point indicates onset of gas liberation; Rs declines as pressure drops.",
            f"Rs drops by {rs_drop:.1f} scf/STB across the pressure range.",
            f"Bo shrinks by {bo_drop:.4f} RB/STB, indicating volume contraction.",
            f"At reservoir pressure {pr:.0f} psia, expect lower oil mobility as gas evolves.",
        ]
    if analysis_key == "viscosity":
        trend = "increases" if muo_change > 0 else "decreases"
        return [
            f"Oil viscosity {trend} as pressure declines; lighter ends flash off.",
            f"Viscosity change across range is {muo_change:.4f} cp.",
            "Higher viscosity implies reduced mobility and lower productivity index.",
            "Operational impact: greater drawdown may be needed to sustain rates.",
        ]
    if analysis_key == "compressibility":
        trend = "increases" if co_change > 0 else "decreases"
        return [
            f"Oil compressibility {trend} as pressure drops.",
            f"co changes by {co_change:.3e} psi-1 across the range.",
            "Higher co means stronger volume sensitivity to pressure changes.",
            "Reserve estimates become more pressure-sensitive at low pressure.",
        ]
    return [
        "Phase envelope outlines the two-phase region for this fluid.",
        "If reservoir conditions cross the envelope, liquid dropout or gas liberation occurs.",
        "Use Pr and Tr location relative to the curve to predict phase behavior.",
    ]
