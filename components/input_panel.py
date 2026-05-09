from typing import Optional

import streamlit as st

from utils.state_manager import capture_inputs, mark_dirty, reset_state


def _input_row(
    index: int,
    label: str,
    key: str,
    min_value: float,
    max_value: float,
    step: float,
    unit: str,
    help_text: Optional[str] = None,
) -> None:
    col_num, col_field, col_unit = st.columns([0.12, 0.6, 0.28])
    with col_num:
        st.markdown(f"<div class='badge'>{index}</div>", unsafe_allow_html=True)
    with col_field:
        st.markdown(f"<div class='field-label'>{label}</div>", unsafe_allow_html=True)
        st.number_input(
            label,
            min_value=min_value,
            max_value=max_value,
            step=step,
            format="%g",
            key=key,
            label_visibility="collapsed",
            help=help_text,
            on_change=mark_dirty,
        )
    with col_unit:
        st.markdown(f"<div class='unit-text'>{unit}</div>", unsafe_allow_html=True)


def render_input_panel() -> None:
    with st.container():
        st.markdown("<div class='input-card-marker'></div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='panel-title'>FLUID &amp; RESERVOIR DATA</div>",
            unsafe_allow_html=True,
        )

        _input_row(
            1,
            "API Gravity",
            "api_gravity",
            min_value=1.0,
            max_value=100.0,
            step=0.1,
            unit="°API",
            help_text="Degrees API",
        )
        _input_row(
            2,
            "Gas Gravity",
            "gas_gravity",
            min_value=0.5,
            max_value=1.5,
            step=0.01,
            unit="SG",
            help_text="Air = 1.0",
        )
        _input_row(
            3,
            "Reservoir Temperature",
            "reservoir_temp_f",
            min_value=50.0,
            max_value=400.0,
            step=1.0,
            unit="°F",
            help_text="Degrees Fahrenheit",
        )

        _input_row(
            4,
            "Reservoir Pressure",
            "reservoir_pressure_psia",
            min_value=100.0,
            max_value=10000.0,
            step=1.0,
            unit="psia",
            help_text="Reservoir pressure",
        )
        _input_row(
            5,
            "Separator Pressure",
            "separator_pressure_psia",
            min_value=50.0,
            max_value=5000.0,
            step=1.0,
            unit="psia",
            help_text="Separator pressure",
        )
        _input_row(
            6,
            "Producing GOR",
            "producing_gor_scfstb",
            min_value=0.0,
            max_value=200000.0,
            step=10.0,
            unit="scf/STB",
            help_text="Used for fluid classification",
        )

        col_calc, col_reset = st.columns(2)
        with col_calc:
            st.button("Calculate", type="primary", use_container_width=True, on_click=capture_inputs)
        with col_reset:
            st.button("Reset", on_click=reset_state, use_container_width=True)
