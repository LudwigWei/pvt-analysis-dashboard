from __future__ import annotations

import streamlit as st

from calculations.fluid_classification import classify_fluid
from calculations.pvt_properties import PVTInputs, generate_rows
from calculations.bubble_point import bubble_point_pressure  # <-- Imported the correlation
from components.charts import build_chart
from components.fluid_card import render_fluid_card
from components.interpretations import build_interpretations
from components.property_table import render_property_table
from components.analysis_constants import ANALYSIS_LABELS
from utils.state_manager import navigate_to_inputs


def render_kpi_card(label: str, value: str, unit: str, color: str) -> None:
    """Helper function to render a clean, light-mode KPI card with colored values."""
    html = f"""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 18px; margin-bottom: 14px; box-shadow: 0 4px 6px rgba(15,23,42,0.02);">
        <div style="font-size: 10px; color: #64748b; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px;">{label}</div>
        <div style="font-size: 24px; font-weight: 700; color: {color};">
            {value} <span style="font-size: 12px; font-weight: 600; color: #94a3b8; margin-left: 2px;">{unit}</span>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_results_display() -> None:
    calculated = st.session_state.get("calculated", False)
    
    # Empty state when user first loads the app
    if not calculated:
        st.info("👈 Please select an analysis type, enter your reservoir parameters, and click 'Run Analysis' to view results.")
        return

    # Grab the current analysis type from the Left Panel's state
    analysis_key = st.session_state.get("current_analysis", "bubble_point")
    analysis_name = ANALYSIS_LABELS.get(analysis_key, analysis_key)

    # --- TOP BAR: Back Button & Title ---
    col_back, col_title = st.columns([1, 4])
    with col_back:
        st.button("← Back to Edit Parameters", on_click=navigate_to_inputs, use_container_width=True)
    with col_title:
        st.markdown(f"<h2 style='margin-top: 0; color: #0f172a;'>{analysis_name} Analysis</h2>", unsafe_allow_html=True)
        
    st.markdown("<hr style='margin-top: 0; margin-bottom: 24px; border-top: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

    snapshot = st.session_state.get("input_snapshot", {})

    api = snapshot.get("api_gravity", 35.0)
    gas_gravity = snapshot.get("gas_gravity", 0.65)
    temp_f = snapshot.get("reservoir_temp_f", 180.0)
    reservoir_pressure_psia = snapshot.get("reservoir_pressure_psia", 2500.0)
    producing_gor = snapshot.get("producing_gor_scfstb", 650.0)

    # --- THE ENGINEERING FIX ---
    # Dynamically calculate Bubble Point based on Standing's correlation
    calculated_pb = bubble_point_pressure(producing_gor, gas_gravity, temp_f, api)

    # Perform Calculations with mathematically accurate inputs
    inputs = PVTInputs(
        api=api,
        gas_gravity=gas_gravity,
        temp_f=temp_f,
        bubble_point_psia=calculated_pb,
        rs_pb=producing_gor,
        reservoir_pressure_psia=reservoir_pressure_psia, # <-- Pass the variable here
    )
    rows_data = generate_rows(inputs)

    # --- 1. TOP BANNER: Fluid Classification ---
    fluid_info = classify_fluid(api, producing_gor)
    
    # Optional UX upgrade: Let the user see what Bubble Point the tool calculated!
    # We append the calculated Pb to the fluid card description for maximum clarity.
    fluid_info["desc"] += f" <b>Calculated Bubble Point: {calculated_pb:,.0f} psia.</b>"
    
    render_fluid_card(fluid_info)

    # Main Results Container
    st.markdown("<div class='results-card'>", unsafe_allow_html=True)
    st.markdown("<div class='analysis-header'>Results Summary</div>", unsafe_allow_html=True)

    # --- 2. MIDDLE GRID: Key Metrics (2x3) ---
    if rows_data:
        pb_data = rows_data[0] # Taking the highest pressure row (usually Bubble Point)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            render_kpi_card("BO AT PB", f"{pb_data['Bo (RB/STB)']:.4f}", "RB/STB", "#0284c7")  # Corporate Blue
            render_kpi_card("BG AT PB", f"{pb_data['Bg (RB/Mscf)']:.5f}", "RB/Mscf", "#16a34a") # Green
        with col2:
            render_kpi_card("MO AT PB", f"{pb_data['muo (cp)']:.3f}", "cp", "#d97706")          # Amber
            render_kpi_card("MG AT PB", f"{pb_data['mug (cp)']:.5f}", "cp", "#7c3aed")          # Purple
        with col3:
            render_kpi_card("Z-FACTOR", f"{pb_data['Z-factor']:.4f}", "dimensionless", "#0d9488") # Teal
            render_kpi_card("CO AT PB", f"{pb_data['co (psi-1)']:.2e}", "psi⁻¹", "#dc2626")       # Red

    st.markdown("<br>", unsafe_allow_html=True)

    # --- 3. BOTTOM SECTION: Tabs ---
    tabs = st.tabs(["Property Table", "Charts", "Interpretation"])

    with tabs[0]:
        render_property_table(rows_data)

    with tabs[1]:
        with st.container():
            st.markdown("<div class='chart-card-marker'></div>", unsafe_allow_html=True)
            fig = build_chart(
                analysis_key,
                rows_data,
                api,
                gas_gravity,
                temp_f,
                reservoir_pressure_psia,
            )
            # Update plot styling to fit light mode better
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color="#334155")
            )
            st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        st.markdown("<div style='color: #334155; padding: 10px 0;'>", unsafe_allow_html=True)
        for text in build_interpretations(analysis_key, rows_data, snapshot):
            st.markdown(f"- {text}")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)