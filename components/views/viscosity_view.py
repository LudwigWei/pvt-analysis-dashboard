import streamlit as st
import plotly.graph_objects as go
from calculations.pvt_properties import PVTInputs
from components.charts import build_chart
from components.interpretations import build_interpretations
from components.property_table import render_property_table

def render_hero_kpi(label: str, value: str, unit: str, icon: str = "water_drop") -> str:
    """Renders a prominent, gradient Hero card for the primary output."""
    return f"""
    <div style="background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%); border-radius: 16px; padding: 24px 32px; box-shadow: 0 6px 16px rgba(59, 130, 246, 0.2); color: #ffffff; display: flex; align-items: center; justify-content: space-between; height: 100%;">
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

def render_viscosity_view(inputs: PVTInputs, rows_data: list[dict], fluid_info: dict, snapshot: dict, analysis_key: str):
    """Bespoke UI Layout specifically designed for Viscosity Analysis."""
    
    # --- 1. The Hero Section ---
    col_hero, col_fluid = st.columns([1.5, 1])
    
    # Extract viscosity at reservoir pressure (usually the first row in generate_rows)
    res_visc = rows_data[0]['muo (cp)'] if rows_data else 0.0
    
    with col_hero:
        st.markdown(render_hero_kpi("Viscosity at Res. Pressure", f"{res_visc:.3f}", "cp", "water_drop"), unsafe_allow_html=True)
        
    with col_fluid:
        st.markdown(f"""
            <div class="fluid-tag-container">
                <div class="fluid-tag-label">Fluid Mobility</div>
                <div class="fluid-tag-value">{fluid_info['name']}</div>
                <div class="fluid-tag-desc">Viscosity measures the internal resistance to flow. Lower values indicate better mobility.</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    # --- 2. Key Mobility Metrics ---
    st.markdown("<div class='results-section-title'>Critical Mobility Points</div>", unsafe_allow_html=True)
    
    if rows_data:
        # Find the row closest to calculated bubble point for comparison
        pb_visc = next((r['muo (cp)'] for r in rows_data if r['P (psia)'] <= inputs.bubble_point_psia), rows_data[-1]['muo (cp)'])
        gas_visc = rows_data[0]['mug (cp)']
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        with kpi_col1:
            st.markdown(render_kpi_card("Viscosity at Pb", f"{pb_visc:.3f}", "cp"), unsafe_allow_html=True)
        with kpi_col2:
            st.markdown(render_kpi_card("Gas Viscosity", f"{gas_visc:.4f}", "cp"), unsafe_allow_html=True)
        with kpi_col3:
            st.markdown(render_kpi_card("API Gravity", f"{inputs.api:.1f}", "°API"), unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # --- 3. Tabs Section ---
    tabs = st.tabs(["📊 Viscosity Curves", "📋 Detailed Data", "💡 Mobility Analysis"])

    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        fig = build_chart(analysis_key, rows_data, inputs.api, inputs.gas_gravity, inputs.temp_f, inputs.reservoir_pressure_psia)
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#0f2942", family="Inter, sans-serif"),
            colorway=['#3b82f6'], # Royal Blue for Viscosity
            margin=dict(t=40, b=40, l=40, r=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        render_property_table(rows_data)

    with tabs[2]:
        st.markdown("<br><div style='color: #0f2942; line-height: 1.6;'>", unsafe_allow_html=True)
        for text in build_interpretations(analysis_key, rows_data, snapshot):
            st.markdown(f"<li>{text}</li>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)