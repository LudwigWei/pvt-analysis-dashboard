import streamlit as st

DEFAULT_INPUTS = {
    "api_gravity": 35.0,
    "gas_gravity": 0.65,
    "reservoir_temp_f": 180.0,
    "reservoir_pressure_psia": 3500.0,
    "separator_pressure_psia": 120.0,
    "producing_gor_scfstb": 650.0,
    "current_analysis": "bubble_point",
    "calculated": False,
    "input_snapshot": {},
    "current_view": "inputs",
}

INPUT_KEYS = [
    "api_gravity",
    "gas_gravity",
    "reservoir_temp_f",
    "reservoir_pressure_psia",
    "separator_pressure_psia",
    "producing_gor_scfstb",
]


def init_state() -> None:
    for key, value in DEFAULT_INPUTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_state() -> None:
    for key, value in DEFAULT_INPUTS.items():
        st.session_state[key] = value
    st.session_state.calculated = False
    st.session_state.input_snapshot = {}


def capture_inputs() -> None:
    st.session_state.input_snapshot = {
        key: float(st.session_state.get(key, 0.0)) for key in INPUT_KEYS
    }
    st.session_state.calculated = True
    st.session_state.current_view = "results"


def navigate_to_inputs() -> None:
    st.session_state.current_view = "inputs"


def mark_dirty() -> None:
    st.session_state.calculated = False
