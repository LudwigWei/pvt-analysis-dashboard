from typing import List, Tuple

import plotly.graph_objects as go

from calculations.phase_envelope import phase_envelope_curve


def _get_series(
    analysis_key: str,
    rows: List[dict],
    api: float,
    gas_gravity: float,
    temp_f: float,
    reservoir_pressure_psia: float,
) -> Tuple[List[float], List[float], str, str]:
    if analysis_key == "bubble_point":
        pressure = [row["P (psia)"] for row in rows]
        bo = [row["Bo (RB/STB)"] for row in rows]
        return pressure, bo, "Pressure (psia)", "Bo (RB/STB)"
    if analysis_key == "viscosity":
        pressure = [row["P (psia)"] for row in rows]
        mu = [row["muo (cp)"] for row in rows]
        return pressure, mu, "Pressure (psia)", "Viscosity (cp)"
    if analysis_key == "compressibility":
        pressure = [row["P (psia)"] for row in rows]
        co = [row["co (psi-1)"] for row in rows]
        return pressure, co, "Pressure (psia)", "Compressibility (psi-1)"
    temperature, pressure = phase_envelope_curve(
        api, gas_gravity, temp_f, reservoir_pressure_psia
    )
    return temperature, pressure, "Temperature (F)", "Pressure (psia)"


def build_chart(
    analysis_key: str,
    rows: List[dict],
    api: float,
    gas_gravity: float,
    temp_f: float,
    reservoir_pressure_psia: float,
) -> go.Figure:
    x_vals, y_vals, x_label, y_label = _get_series(
        analysis_key, rows, api, gas_gravity, temp_f, reservoir_pressure_psia
    )
    title = {
        "bubble_point": "Bubble Point: Pressure vs Bo",
        "viscosity": "Viscosity: Viscosity vs Pressure",
        "compressibility": "Compressibility: Co vs Pressure",
        "phase_envelope": "Phase Envelope: Pressure vs Temperature",
    }.get(analysis_key, "Analysis Chart")
    fig = go.Figure(
        data=[go.Scatter(x=x_vals, y=y_vals, mode="lines+markers")]
    )
    fig.update_layout(
        title=title,
        title_x=0.02,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title=x_label,
        yaxis_title=y_label,
        height=360,
    )
    return fig
