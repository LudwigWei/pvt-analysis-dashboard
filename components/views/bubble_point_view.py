from __future__ import annotations

import streamlit as st

from calculations.fluid_classification import classify_fluid
from calculations.pvt_properties import PVTInputs, generate_rows
from calculations.bubble_point import bubble_point_pressure
from components.charts import build_chart
from components.interpretations import build_interpretations
from components.property_table import render_property_table
from components.analysis_constants import ANALYSIS_LABELS
from utils.state_manager import navigate_to_inputs


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

def render_hero_kpi(label: str, value: str, unit: str, icon: str = "bubble_chart") -> str:
    """Renders a prominent, gradient Hero card for the primary output."""
    return f"""
    <div style="background: linear-gradient(135deg, #006fbb 0%, #005a96 100%); border-radius: 16px; padding: 24px 32px; box-shadow: 0 6px 16px rgba(0, 111, 187, 0.2); color: #ffffff; display: flex; align-items: center; justify-content: space-between; height: 100%;">
        <div>
            <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #eaf4fb; margin-bottom: 8px; opacity: 0.9;">{label}</div>
            <div style="font-size: 42px; font-weight: 800; line-height: 1;">
                {value} <span style="font-size: 18px; font-weight: 600; color: #eaf4fb; opacity: 0.8; margin-left: 4px;">{unit}</span>
            </div>
        </div>
        <div style="font-family: 'Material Symbols Outlined'; font-size: 56px; opacity: 0.2; font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 48;">
            {icon}
        </div>
    </div>
    """

def apply_results_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24..48,100..700,0..1,-50..200');
        
        .results-section-title {
            font-size: 18px; font-weight: 700; color: #0f2942; margin-bottom: 16px; margin-top: 8px;
        }
        
        /* Streamlit Tabs Styling */
        div[data-testid="stTabs"] button {
            font-weight: 600 !important;
            color: #5b7b97 !important;
        }
        div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
            color: #006fbb !important;
        }
        div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] > div[data-testid="stMarkdownContainer"] > p {
            font-weight: 700 !important;
        }
        div[data-baseweb="tab-highlight"] {
            background-color: #006fbb !important;
        }
        
        /* Fluid Classification Tag */
        .fluid-tag-container {
            background: #f4f8fb; border: 1px solid #d3e1ee; border-radius: 12px; padding: 16px 20px; height: 100%;
        }
        .fluid-tag-label { font-size: 11px; color: #5b7b97; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 6px; }
        .fluid-tag-value { font-size: 16px; font-weight: 700; color: #0f2942; }
        .fluid-tag-desc { font-size: 12px; color: #5b7b97; margin-top: 4px; line-height: 1.4; }
        </style>
    """, unsafe_allow_html=True)


def render_bubble_point_view(inputs: PVTInputs, rows_data: list[dict], fluid_info: dict, snapshot: dict, analysis_key: str):
    """Bespoke UI Layout specifically designed for Bubble Point Analysis."""
    
    # --- 1. The Hero Section ---
    col_hero, col_fluid = st.columns([1.5, 1])
    
    with col_hero:
        # Display the dynamically calculated Bubble Point
        st.markdown(render_hero_kpi("Calculated Bubble Point", f"{inputs.bubble_point_psia:,.0f}", "psia"), unsafe_allow_html=True)
        
    with col_fluid:
        # Display the fluid classification cleanly
        st.markdown(f"""
            <div class="fluid-tag-container">
                <div class="fluid-tag-label">Fluid Classification</div>
                <div class="fluid-tag-value">{fluid_info['name']}</div>
                <div class="fluid-tag-desc">{fluid_info['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    # --- 2. Key Properties at Pb ---
    st.markdown("<div class='results-section-title'>Saturated Liquid Properties (at Pb)</div>", unsafe_allow_html=True)
    
    if rows_data:
        pb_data = rows_data[0] # Highest pressure row (Bubble Point limit)
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        with kpi_col1:
            st.markdown(render_kpi_card("Formation Volume Factor (Bo)", f"{pb_data['Bo (RB/STB)']:.4f}", "RB/STB"), unsafe_allow_html=True)
        with kpi_col2:
            st.markdown(render_kpi_card("Oil Viscosity (μo)", f"{pb_data['muo (cp)']:.3f}", "cp"), unsafe_allow_html=True)
        with kpi_col3:
            st.markdown(render_kpi_card("Isothermal Compressibility (co)", f"{pb_data['co (psi-1)']:.2e}", "psi⁻¹"), unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # --- 3. Tabs Section ---
    tabs = st.tabs(["📊 Pressure Profile Charts", "📋 Raw Tabular Data", "💡 Engineering Interpretation"])

    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        fig = build_chart(
            analysis_key,
            rows_data,
            inputs.api,
            inputs.gas_gravity,
            inputs.temp_f,
            inputs.reservoir_pressure_psia,
        )
        # Apply Oceanic Theme to Plotly
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#0f2942", family="Inter, sans-serif"),
            colorway=['#006fbb'], # Ocean Blue line
            margin=dict(t=40, b=40, l=40, r=40)
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0', zeroline=False)
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0', zeroline=False)
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        render_property_table(rows_data)

    with tabs[2]:
        st.markdown("<br><div style='color: #0f2942; line-height: 1.6;'>", unsafe_allow_html=True)
        for text in build_interpretations(analysis_key, rows_data, snapshot):
            st.markdown(f"<li>{text}</li>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)


def render_results_display() -> None:
    calculated = st.session_state.get("calculated", False)
    
    if not calculated:
        st.info("👈 Please select an analysis type, enter your parameters, and click 'Run Analysis'.")
        return

    apply_results_css()

    # --- GLOBAL TOP BAR: Back Button & Title ---
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

    # --- VIEW ROUTER ---
    # By separating these, we can build custom, highly-specific UIs for Viscosity, Compressibility, etc. next!
    if analysis_key == "bubble_point":
        render_bubble_point_view(inputs, rows_data, fluid_info, snapshot, analysis_key)
    else:
        # Temporary fallback for the other tools until we design them
        st.warning(f"Custom UI for {analysis_name} is currently under construction. Rendering default view.")
        render_bubble_point_view(inputs, rows_data, fluid_info, snapshot, analysis_key)