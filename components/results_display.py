from __future__ import annotations

import streamlit as st

from calculations.fluid_classification import classify_fluid
from calculations.pvt_properties import PVTInputs, generate_rows
from components.charts import build_chart
from components.fluid_card import render_fluid_card
from components.interpretations import build_interpretations
from components.property_table import render_property_table

def render_kpi_card(label: str, value: str, unit: str, color: str) -> None:
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
    
    if not calculated:
        st.info("👈 Please select an analysis type, enter your reservoir parameters, and click 'Run Analysis' to view results.")
        return

    analysis_key = st.session_state.get("current_analysis", "bubble_point")
    snapshot = st.session_state.get("input_snapshot", {})

    api = snapshot.get("api_gravity", 35.0)
    gas_gravity = snapshot.get("gas_gravity", 0.65)
    temp_f = snapshot.get("reservoir_temp_f", 180.0)
    reservoir_pressure_psia = snapshot.get("reservoir_pressure_psia", 2500.0)

    inputs = PVTInputs(
        api=api,
        gas_gravity=gas_gravity,
        temp_f=temp_f,
        bubble_point_psia=reservoir_pressure_psia,
        rs_pb=snapshot.get("producing_gor_scfstb", 650.0),
    )
    rows_data = generate_rows(inputs)

    # --- 1. TOP BANNER: Fluid Classification ---
    fluid_info = classify_fluid(api, snapshot.get("producing_gor_scfstb", 650.0))
    render_fluid_card(fluid_info)

    # Cleaned up header (No raw HTML div wrapper)
    st.markdown("<div style='margin: 24px 0 16px 0; font-size: 14px; font-weight: 700; color: #0f172a; text-transform: uppercase; letter-spacing: 0.5px;'>Results Summary</div>", unsafe_allow_html=True)

    # --- 2. MIDDLE GRID: Key Metrics (2x3) ---
    if rows_data:
        pb_data = rows_data[0] 
        col1, col2, col3 = st.columns(3)
        with col1:
            render_kpi_card("BO AT PB", f"{pb_data['Bo (RB/STB)']:.4f}", "RB/STB", "#0284c7")  
            render_kpi_card("BG AT PB", f"{pb_data['Bg (RB/Mscf)']:.5f}", "RB/Mscf", "#16a34a") 
        with col2:
            render_kpi_card("MO AT PB", f"{pb_data['muo (cp)']:.3f}", "cp", "#d97706")          
            render_kpi_card("MG AT PB", f"{pb_data['mug (cp)']:.5f}", "cp", "#7c3aed")          
        with col3:
            render_kpi_card("Z-FACTOR", f"{pb_data['Z-factor']:.4f}", "dimensionless", "#0d9488") 
            render_kpi_card("CO AT PB", f"{pb_data['co (psi-1)']:.2e}", "psi⁻¹", "#dc2626")       

    # --- 3. BOTTOM SECTION: Tabs ---
    tabs = st.tabs(["📈 Graph", "📊 Property Table"])

    with tabs[0]:
        fig = build_chart(analysis_key, rows_data, api, gas_gravity, temp_f, reservoir_pressure_psia)
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color="#334155"))
        st.plotly_chart(fig, use_container_width=True)
            
        st.markdown(
            """
            <div style='color: #334155; padding: 16px 8px 8px 8px; border-top: 1px solid #e2e8f0; margin-top: 8px;'>
                <h4 style='margin-bottom: 12px; color: #0f172a; font-size: 14px; font-weight: 700;'>📝 Analysis Interpretation</h4>
            </div>
            """, unsafe_allow_html=True
        )
        for text in build_interpretations(analysis_key, rows_data, snapshot):
            st.markdown(f"- <span style='color: #475569; font-size: 14px;'>{text}</span>", unsafe_allow_html=True)

    with tabs[1]:
        render_property_table(rows_data)