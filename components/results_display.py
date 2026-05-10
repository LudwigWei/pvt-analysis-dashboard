import streamlit as st

from calculations.fluid_classification import classify_fluid
from calculations.pvt_properties import PVTInputs, generate_rows
from calculations.bubble_point import bubble_point_pressure
from components.analysis_constants import ANALYSIS_LABELS
from utils.state_manager import navigate_to_inputs

# Import your new modular views
from components.views.bubble_point_view import render_bubble_point_view
# from components.views.viscosity_view import render_viscosity_view
# from components.views.compressibility_view import render_compressibility_view
# from components.views.phase_envelope_view import render_phase_envelope_view


def apply_results_css():
    """Global CSS for the Results pages."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24..48,100..700,0..1,-50..200');
        
        .results-section-title { font-size: 18px; font-weight: 700; color: #0f2942; margin-bottom: 16px; margin-top: 8px; }
        
        /* Streamlit Tabs Styling */
        div[data-testid="stTabs"] button { font-weight: 600 !important; color: #5b7b97 !important; }
        div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] { color: #006fbb !important; }
        div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] > div[data-testid="stMarkdownContainer"] > p { font-weight: 700 !important; }
        div[data-baseweb="tab-highlight"] { background-color: #006fbb !important; }
        
        /* Fluid Classification Tag */
        .fluid-tag-container { background: #f4f8fb; border: 1px solid #d3e1ee; border-radius: 12px; padding: 16px 20px; height: 100%; }
        .fluid-tag-label { font-size: 11px; color: #5b7b97; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
        .fluid-tag-value { font-size: 16px; font-weight: 700; color: #0f2942; }
        .fluid-tag-desc { font-size: 12px; color: #5b7b97; margin-top: 4px; line-height: 1.4; }
        </style>
    """, unsafe_allow_html=True)


def render_results_display() -> None:
    calculated = st.session_state.get("calculated", False)
    
    if not calculated:
        st.info("👈 Please select an analysis type, enter your parameters, and click 'Run Analysis'.")
        return

    apply_results_css()

    # --- GLOBAL TOP BAR ---
    analysis_key = st.session_state.get("current_analysis", "bubble_point")
    analysis_name = ANALYSIS_LABELS.get(analysis_key, analysis_key)

    col_back, col_title = st.columns([1, 4])
    with col_back:
        st.button("← Back to Edit", on_click=navigate_to_inputs, use_container_width=True)
    with col_title:
        st.markdown(f"<h2 style='margin-top: -6px; color: #0f2942;'>{analysis_name} Analysis</h2>", unsafe_allow_html=True)
        
    st.markdown("<hr style='margin-top: 8px; margin-bottom: 24px; border-top: 1px solid #d3e1ee;'>", unsafe_allow_html=True)

    # --- DATA PREPARATION ---
    snapshot = st.session_state.get("input_snapshot", {})
    api = snapshot.get("api_gravity", 35.0)
    gas_gravity = snapshot.get("gas_gravity", 0.65)
    temp_f = snapshot.get("reservoir_temp_f", 180.0)
    reservoir_pressure_psia = snapshot.get("reservoir_pressure_psia", 2500.0)
    producing_gor = snapshot.get("producing_gor_scfstb", 650.0)

    calculated_pb = bubble_point_pressure(producing_gor, gas_gravity, temp_f, api)

    inputs = PVTInputs(
        api=api,
        gas_gravity=gas_gravity,
        temp_f=temp_f,
        bubble_point_psia=calculated_pb,
        rs_pb=producing_gor,
        reservoir_pressure_psia=reservoir_pressure_psia, 
    )
    
    rows_data = generate_rows(inputs)
    fluid_info = classify_fluid(api, producing_gor)

    # --- THE ROUTER ---
    if analysis_key == "bubble_point":
        render_bubble_point_view(inputs, rows_data, fluid_info, snapshot, analysis_key)
    elif analysis_key == "viscosity":
        st.warning("Viscosity View under construction.")
        # render_viscosity_view(inputs, rows_data, fluid_info, snapshot, analysis_key)
    elif analysis_key == "compressibility":
        st.warning("Compressibility View under construction.")
        # render_compressibility_view(inputs, rows_data, fluid_info, snapshot, analysis_key)
    elif analysis_key == "phase_envelope":
        st.warning("Phase Envelope View under construction.")
        # render_phase_envelope_view(inputs, rows_data, fluid_info, snapshot, analysis_key)