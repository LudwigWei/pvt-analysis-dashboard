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


def apply_results_css():
    """Global CSS for the Results pages."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24..48,100..700,0..1,-50..200');
        
        /* --- Fixed Circular Back Button --- */
        div[data-testid="stColumn"]:has(button[key="back_btn"]) button {
            border: 1px solid #d3e1ee !important;
            background: #ffffff !important;
            border-radius: 50% !important;
            width: 42px !important;
            height: 42px !important;
            min-width: 42px !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transition: all 0.2s ease !important;
        }

        div[data-testid="stColumn"]:has(button[key="back_btn"]) button span,
        div[data-testid="stColumn"]:has(button[key="back_btn"]) button p {
            font-family: 'Material Symbols Outlined' !important;
            font-size: 24px !important;
            color: #5b7b97 !important;
            margin: 0 !important;
            line-height: 1 !important;
            white-space: nowrap !important;
            display: inline-block !important;
        }

        div[data-testid="stColumn"]:has(button[key="back_btn"]) button:hover {
            border-color: #006fbb !important;
            background: #eaf4fb !important;
            transform: translateX(-2px);
            box-shadow: 0 4px 12px rgba(0, 111, 187, 0.1) !important;
        }
        
        div[data-testid="stColumn"]:has(button[key="back_btn"]) button:hover span,
        div[data-testid="stColumn"]:has(button[key="back_btn"]) button:hover p {
            color: #006fbb !important;
        }

        div[data-testid="stHorizontalBlock"]:has(button[key="back_btn"]) {
            align-items: center !important;
        }

        .results-section-title { 
            font-size: 18px; font-weight: 700; color: #0f2942; margin-bottom: 16px; margin-top: 8px; 
        }
        
        /* --- Updated Fluid Tag Style --- */
        .fluid-tag-container { 
            background: #ffffff; 
            border: 1px solid #d3e1ee; 
            border-radius: 16px; 
            padding: 24px 28px; 
            height: 100%; 
            display: flex;
            flex-direction: column;
            justify-content: center;
            box-shadow: 0 4px 6px -1px rgba(15, 41, 66, 0.02), 0 2px 4px -1px rgba(15, 41, 66, 0.01);
        }
        .fluid-tag-label { 
            font-size: 11px; color: #8ba3b6; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 8px; 
        }
        .fluid-tag-value { 
            font-size: 20px; font-weight: 800; color: #0f2942; line-height: 1.2;
        }
        .fluid-tag-desc { 
            font-size: 13px; color: #5b7b97; margin-top: 8px; line-height: 1.5; font-weight: 500;
        }

        div[data-testid="column"]:has(.fluid-tag-container) {
            display: flex !important;
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

    analysis_key = st.session_state.get("current_analysis", "bubble_point")
    analysis_name = ANALYSIS_LABELS.get(analysis_key, analysis_key)

    # --- MINIMALIST HEADER ---
    header_col1, header_col2 = st.columns([0.2, 4], gap="small")
    
    with header_col1:
        st.button("arrow_back", on_click=navigate_to_inputs, key="back_btn")
        
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