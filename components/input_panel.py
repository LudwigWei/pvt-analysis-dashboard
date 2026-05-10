import streamlit as st

from utils.state_manager import capture_inputs, mark_dirty, reset_state
from components.analysis_constants import ANALYSIS_LABELS, ANALYSIS_OPTIONS

def render_input_panel() -> None:
    # Custom CSS for our card-style radio button selector using st.radio
    st.markdown(
        """
        <style>
        /* Card-style radio button container for Analysis Selection */
        div[data-testid="stRadio"] > div[role="radiogroup"] {
            display: grid !important;
            grid-template-columns: repeat(4, 1fr) !important;
            gap: 16px !important;
            width: 100% !important;
            justify-content: center !important;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label {
            background-color: #ffffff;
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px 12px;
            cursor: pointer;
            text-align: center;
            transition: all 0.2s ease;
            box-shadow: 0 2px 4px rgba(15,23,42,0.02);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
            margin: 0 !important;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
            border-color: #94a3b8;
            box-shadow: 0 4px 6px rgba(15,23,42,0.04);
            transform: translateY(-2px);
        }
        /* Style when checked (Streamlit uses aria-checked on label or input, target active state) */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
            border-color: #0284c7 !important;
            background-color: #f0f9ff !important;
        }
        /* Hide the actual radio circle */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child {
            display: none !important;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:last-child {
            font-weight: 700;
            color: #0f172a;
            font-size: 16px;
            width: 100%;
            text-align: center;
        }
        
        .section-header {
            font-size: 16px;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 16px;
            padding-bottom: 8px;
            border-bottom: 1px solid #f1f5f9;
        }
        /* Center the section header when needed */
        .section-header.centered {
            text-align: center;
            border-bottom: none;
            margin-bottom: 16px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- 1. PARAMETER GRID CARD ---
    with st.container():
        st.markdown("<div class='bento-card-marker'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Reservoir Parameters</div>", unsafe_allow_html=True)
        
        # We use a 3-column grid for the inputs
        col1, col2, col3 = st.columns(3, gap="large")
        
        with col1:
            st.markdown("<div class='field-label'>API Gravity (°API)</div>", unsafe_allow_html=True)
            st.number_input(
                "API Gravity", min_value=1.0, max_value=100.0, step=0.1, 
                key="api_gravity", label_visibility="collapsed", on_change=mark_dirty
            )
            
            st.markdown("<div class='field-label'>Gas Gravity (Air=1)</div>", unsafe_allow_html=True)
            st.number_input(
                "Gas Gravity", min_value=0.5, max_value=1.5, step=0.01, 
                key="gas_gravity", label_visibility="collapsed", on_change=mark_dirty
            )

        with col2:
            st.markdown("<div class='field-label'>Temperature (°F)</div>", unsafe_allow_html=True)
            st.number_input(
                "Temperature", min_value=50.0, max_value=400.0, step=1.0, 
                key="reservoir_temp_f", label_visibility="collapsed", on_change=mark_dirty
            )
            
            st.markdown("<div class='field-label'>Reservoir Press. (psia)</div>", unsafe_allow_html=True)
            st.number_input(
                "Reservoir Pressure", min_value=100.0, max_value=10000.0, step=1.0, 
                key="reservoir_pressure_psia", label_visibility="collapsed", on_change=mark_dirty
            )
            
        with col3:
            st.markdown("<div class='field-label'>Separator Press. (psia)</div>", unsafe_allow_html=True)
            st.number_input(
                "Separator Press.", min_value=50.0, max_value=5000.0, step=1.0, 
                key="separator_pressure_psia", label_visibility="collapsed", on_change=mark_dirty
            )
            
            st.markdown("<div class='field-label'>Producing GOR (scf/STB)</div>", unsafe_allow_html=True)
            st.number_input(
                "Producing GOR", min_value=0.0, max_value=200000.0, step=10.0, 
                key="producing_gor_scfstb", label_visibility="collapsed", on_change=mark_dirty
            )

        st.markdown("<br>", unsafe_allow_html=True)

    # --- 2. ANALYSIS ROUTER (CARD-STYLE) ---
    with st.container():
        st.markdown("<div class='bento-card-marker'></div>", unsafe_allow_html=True)
        st.markdown("<div class='section-header centered'>Select Analysis Type</div>", unsafe_allow_html=True)
        
        options = [key for key, _, _ in ANALYSIS_OPTIONS]
        selected = st.session_state.get("current_analysis", "bubble_point")
        if selected not in options:
            selected = options[0]
            
        # Radio selector styled as cards
        st.session_state.current_analysis = st.radio(
            "Select Analysis Type",
            options=options,
            format_func=lambda key: ANALYSIS_LABELS.get(key, key),
            index=options.index(selected),
            label_visibility="collapsed",
            on_change=mark_dirty,
            horizontal=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- 3. ACTION BUTTONS ---
    b_col1, b_col2, b_col3 = st.columns([1, 2, 1])
    with b_col2:
        st.button("▶ Run Analysis", type="primary", use_container_width=True, on_click=capture_inputs)
    with b_col3:
        st.button("Reset Parameters", use_container_width=True, on_click=reset_state)