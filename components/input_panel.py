import streamlit as st

from utils.state_manager import capture_inputs, mark_dirty, reset_state
from components.analysis_constants import ANALYSIS_LABELS, ANALYSIS_OPTIONS

def render_input_panel() -> None:
    with st.container():
        # This marker applies the white card styling from app.py
        st.markdown("<div class='input-card-marker'></div>", unsafe_allow_html=True)
        
        # --- 1. ANALYSIS ROUTER ---
        st.markdown("<div class='panel-title'>WORKFLOW</div>", unsafe_allow_html=True)
        st.markdown("<div class='field-label'>Select Analysis Type</div>", unsafe_allow_html=True)
        
        options = [key for key, _, _ in ANALYSIS_OPTIONS]
        selected = st.session_state.get("current_analysis", "bubble_point")
        if selected not in options:
            selected = options[0]
            
        # Dropdown selector for the analysis mode
        st.session_state.current_analysis = st.selectbox(
            "Select Analysis Type",
            options=options,
            format_func=lambda key: ANALYSIS_LABELS.get(key, key),
            index=options.index(selected),
            label_visibility="collapsed",
            on_change=mark_dirty
        )
        
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

        # --- 2. PARAMETER GRID (1 Column) ---
        st.markdown("<div class='panel-title'>RESERVOIR PARAMETERS</div>", unsafe_allow_html=True)
        
        st.markdown("<div class='field-label'>API Gravity (°API)</div>", unsafe_allow_html=True)
        st.number_input(
            "API Gravity", min_value=1.0, max_value=100.0, step=0.1, 
            key="api_gravity", label_visibility="collapsed", on_change=mark_dirty
        )
        
        st.markdown("<div class='field-label'>Temperature (°F)</div>", unsafe_allow_html=True)
        st.number_input(
            "Temperature", min_value=50.0, max_value=400.0, step=1.0, 
            key="reservoir_temp_f", label_visibility="collapsed", on_change=mark_dirty
        )
        
        st.markdown("<div class='field-label'>Separator Press. (psia)</div>", unsafe_allow_html=True)
        st.number_input(
            "Separator Press.", min_value=50.0, max_value=5000.0, step=1.0, 
            key="separator_pressure_psia", label_visibility="collapsed", on_change=mark_dirty
        )

        st.markdown("<div class='field-label'>Gas Gravity (Air=1)</div>", unsafe_allow_html=True)
        st.number_input(
            "Gas Gravity", min_value=0.5, max_value=1.5, step=0.01, 
            key="gas_gravity", label_visibility="collapsed", on_change=mark_dirty
        )
        
        st.markdown("<div class='field-label'>Reservoir Press. (psia)</div>", unsafe_allow_html=True)
        st.number_input(
            "Reservoir Pressure", min_value=100.0, max_value=10000.0, step=1.0, 
            key="reservoir_pressure_psia", label_visibility="collapsed", on_change=mark_dirty
        )
        
        st.markdown("<div class='field-label'>Producing GOR (scf/STB)</div>", unsafe_allow_html=True)
        st.number_input(
            "Producing GOR", min_value=0.0, max_value=200000.0, step=10.0, 
            key="producing_gor_scfstb", label_visibility="collapsed", on_change=mark_dirty
        )

        st.markdown("<br>", unsafe_allow_html=True)

        # --- 3. ACTION BUTTONS ---
        st.button("▶ Run Analysis", type="primary", use_container_width=True, on_click=capture_inputs)
        st.button("Reset Parameters", use_container_width=True, on_click=reset_state)