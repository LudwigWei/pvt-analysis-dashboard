import time # <-- Make sure to import time
import streamlit as st

from calculations.fluid_classification import classify_fluid
from calculations.pvt_properties import PVTInputs, generate_rows
from calculations.bubble_point import bubble_point_pressure
from components.analysis_constants import ANALYSIS_LABELS
from utils.state_manager import navigate_to_inputs

# Import modular views
from components.views.bubble_point_view import render_bubble_point_view
from components.views.viscosity_view import render_viscosity_view
from components.views.compressibility_view import render_compressibility_view
from components.views.phase_envelope_view import render_phase_envelope_view


def render_kpi_card(label: str, value: str, unit: str, color: str = "#0f2942") -> str:
    """Renders a standard, clean bento KPI card."""
    return f"""
    <div style="background: #ffffff; border: 1px solid #d3e1ee; border-radius: 12px; padding: 16px 20px; box-shadow: 0 2px 8px rgba(15, 41, 66, 0.02); height: 100%;">
        <div style="font-size: 11px; color: #5b7b97; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px;">{label}</div>
        <div style="font-size: 24px; font-weight: 700; color: {color}; line-height: 1.1;">
            {value} <span style="font-size: 12px; font-weight: 600; color: #8ba3b6; margin-left: 2px;">{unit}</span>
        </div>
    </div>
    """


def render_skeleton_loader():
    """Renders an animated CSS skeleton layout that mimics the dashboard."""
    st.markdown("""
        <style>
        @keyframes pulse-skeleton {
            0% { background-color: #f4f8fb; opacity: 1; }
            50% { background-color: #e2e8f0; opacity: 0.6; }
            100% { background-color: #f4f8fb; opacity: 1; }
        }
        .skel-pulse {
            animation: pulse-skeleton 1.5s infinite ease-in-out;
        }
        .skel-top { display: flex; gap: 16px; margin-bottom: 24px; margin-top: 10px; align-items: center; }
        .skel-btn { width: 42px; height: 42px; border-radius: 50%; }
        .skel-title { width: 300px; height: 38px; border-radius: 8px; }
        .skel-hero { height: 160px; width: 100%; border-radius: 16px; margin-bottom: 32px; }
        .skel-kpis { display: flex; gap: 16px; margin-bottom: 32px; }
        .skel-kpi { height: 100px; flex: 1; border-radius: 12px; }
        .skel-body { display: flex; gap: 16px; }
        .skel-chart { height: 450px; flex: 2; border-radius: 12px; }
        .skel-side { flex: 1; display: flex; flex-direction: column; gap: 16px; }
        .skel-fluid { height: 140px; border-radius: 12px; }
        .skel-interp { flex-grow: 1; min-height: 294px; border-radius: 12px; }
        </style>
        
        <div>
            <div class="skel-top">
                <div class="skel-pulse skel-btn"></div>
                <div class="skel-pulse skel-title"></div>
            </div>
            <hr style='margin-top: 12px; margin-bottom: 24px; border-top: 1px solid #d3e1ee;'>
            <div class="skel-pulse skel-hero"></div>
            <div class="skel-kpis">
                <div class="skel-pulse skel-kpi"></div>
                <div class="skel-pulse skel-kpi"></div>
                <div class="skel-pulse skel-kpi"></div>
            </div>
            <div class="skel-body">
                <div class="skel-pulse skel-chart"></div>
                <div class="skel-side">
                    <div class="skel-pulse skel-fluid"></div>
                    <div class="skel-pulse skel-interp"></div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def apply_results_css():
    """Global CSS for the Results pages."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24..48,100..700,0..1,-50..200');
        
        /* --- Fixed Circular Back Button using Marker --- */
        .back-btn-marker { display: none; }

        div[data-testid="stColumn"]:has(.back-btn-marker) button {
            border: 1px solid #d3e1ee !important;
            background: #ffffff !important;
            border-radius: 50% !important;
            width: 42px !important;
            height: 42px !important;
            min-width: 42px !important;
            max-width: 42px !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.2s ease !important;
            overflow: hidden !important;
        }

        div[data-testid="stColumn"]:has(.back-btn-marker) button div,
        div[data-testid="stColumn"]:has(.back-btn-marker) button span,
        div[data-testid="stColumn"]:has(.back-btn-marker) button p {
            font-family: 'Material Symbols Outlined' !important;
            font-size: 24px !important;
            color: #5b7b97 !important;
            margin: 0 !important;
            line-height: 42px !important;
            white-space: nowrap !important;
            word-break: keep-all !important; 
            letter-spacing: normal !important;
            display: block !important;
            text-align: center !important;
        }

        div[data-testid="stColumn"]:has(.back-btn-marker) button:hover {
            border-color: #006fbb !important;
            background: #eaf4fb !important;
            transform: translateX(-2px);
            box-shadow: 0 4px 12px rgba(0, 111, 187, 0.1) !important;
        }
        
        div[data-testid="stColumn"]:has(.back-btn-marker) button:hover p,
        div[data-testid="stColumn"]:has(.back-btn-marker) button:hover span {
            color: #006fbb !important;
        }

        div[data-testid="stHorizontalBlock"]:has(.back-btn-marker) {
            align-items: center !important;
        }

        .results-section-title { 
            font-size: 18px; font-weight: 700; color: #0f2942; margin-bottom: 16px; margin-top: 8px; 
        }
        
        /* --- Refactored Fluid Tag Style (Side Column) --- */
        .fluid-tag-container { 
            background: #ffffff; 
            border: 1px solid #d3e1ee; 
            border-radius: 12px; 
            padding: 24px; 
            height: auto; 
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            align-items: flex-start;
            box-shadow: 0 2px 8px rgba(15, 41, 66, 0.02);
        }
        .fluid-tag-left {
            display: flex;
            flex-direction: column;
            width: 100%;
        }
        .fluid-tag-label { 
            font-size: 11px; color: #8ba3b6; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; 
        }
        .fluid-tag-value { 
            font-size: 20px; font-weight: 800; color: #0f2942; line-height: 1.2;
        }
        .fluid-tag-desc { 
            font-size: 13px; color: #5b7b97; line-height: 1.5; font-weight: 500; text-align: left; margin-top: 12px; width: 100%;
        }

        div[data-testid="column"]:has(.fluid-tag-container) {
            display: flex !important;
            flex-direction: column !important;
            height: 100% !important;
        }

        /* --- Equal Height Layout for Chart & Interp Row --- */
        div[data-testid="stHorizontalBlock"]:has(.dash-chart-marker) {
            align-items: stretch !important;
        }
        div[data-testid="stHorizontalBlock"]:has(.dash-chart-marker) > div[data-testid="column"] > div[data-testid="stVerticalBlock"] {
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
        }
        div[data-testid="stVerticalBlock"]:has(> div > div > div > div > .dash-chart-marker) {
            background: #ffffff !important; 
            border: 1px solid #d3e1ee !important; 
            border-radius: 12px !important; 
            padding: 20px !important; 
            box-shadow: 0 2px 8px rgba(15, 41, 66, 0.02) !important; 
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
        }
        div.element-container:has(.dash-interp-marker) {
            flex-grow: 1 !important;
            display: flex !important;
            flex-direction: column !important;
            margin-top: 16px !important; 
        }
        .dash-interp-marker {
            flex-grow: 1 !important;
            display: flex !important;
            flex-direction: column !important;
        }
        
        div[data-testid="stVerticalBlock"]:has(> div > div > div > div > .dash-table-marker) {
            background: #ffffff !important; 
            border: 1px solid #d3e1ee !important; 
            border-radius: 12px !important; 
            padding: 20px !important; 
            box-shadow: 0 2px 8px rgba(15, 41, 66, 0.02) !important;
        }

        /* Streamlit Tabs */
        div[data-testid="stTabs"] button { font-weight: 600 !important; color: #5b7b97 !important; }
        div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] { color: #006fbb !important; }
        div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] > div[data-testid="stMarkdownContainer"] > p { font-weight: 700 !important; }
        div[data-baseweb="tab-highlight"] { background-color: #006fbb !important; }
        </style>
    """, unsafe_allow_html=True)


def render_results_display() -> None:
    calculated = st.session_state.get("calculated", False)
    if not calculated:
        st.info("👈 Please select an analysis type, enter your parameters, and click 'Run Analysis'.")
        return

    apply_results_css()

    # --- SKELETON LOADER TRANSITION ---
    if st.session_state.get("show_skeleton", False):
        skeleton_placeholder = st.empty()
        with skeleton_placeholder:
            render_skeleton_loader()
        
        # Pause for 800ms to allow the user to see the loading effect
        time.sleep(0.8)
        
        # Clear the skeleton and update state so it doesn't run again
        skeleton_placeholder.empty()
        st.session_state.show_skeleton = False

    # --- NORMAL HEADER ---
    analysis_key = st.session_state.get("current_analysis", "bubble_point")
    analysis_name = ANALYSIS_LABELS.get(analysis_key, analysis_key)

    header_col1, header_col2 = st.columns([0.2, 4], gap="small")
    
    with header_col1:
        st.markdown('<div class="back-btn-marker"></div>', unsafe_allow_html=True)
        st.button("arrow_back", on_click=navigate_to_inputs)
        
    with header_col2:
        st.markdown(f"""
            <div style='display: flex; flex-direction: column; justify-content: center; height: 100%;'>
                <div style='font-size: 24px; font-weight: 800; color: #0f2942; line-height: 1.1;'>{analysis_name} Analysis</div>
                <div style='font-size: 13px; font-weight: 500; color: #5b7b97; margin-top: 4px;'>
                    Reviewing calculated {analysis_name.lower()} properties and thermodynamic behavior
                </div>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("<hr style='margin-top: 12px; margin-bottom: 24px; border-top: 1px solid #d3e1ee;'>", unsafe_allow_html=True)

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

    if analysis_key == "bubble_point":
        render_bubble_point_view(inputs, rows_data, fluid_info, snapshot, analysis_key)
    elif analysis_key == "viscosity":
        render_viscosity_view(inputs, rows_data, fluid_info, snapshot, analysis_key)
    elif analysis_key == "compressibility":
        render_compressibility_view(inputs, rows_data, fluid_info, snapshot, analysis_key)
    elif analysis_key == "phase_envelope":
        render_phase_envelope_view(inputs, rows_data, fluid_info, snapshot, analysis_key)