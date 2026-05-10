import streamlit as st
from calculations.pvt_properties import PVTInputs
from components.charts import build_chart
from components.interpretations import build_interpretations
from components.property_table import render_property_table

def render_hero_kpi(label: str, value: str, unit: str, icon: str = "compress") -> str:
    """Renders a prominent, indigo-gradient Hero card for compressibility."""
    return f"""
    <div style="background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%); border-radius: 16px; padding: 24px 32px; box-shadow: 0 6px 16px rgba(99, 102, 241, 0.2); color: #ffffff; display: flex; align-items: center; justify-content: space-between; height: 100%;">
        <div>
            <div style="font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: #eef2ff; margin-bottom: 8px; opacity: 0.9;">{label}</div>
            <div style="font-size: 42px; font-weight: 800; line-height: 1;">
                {value} <span style="font-size: 18px; font-weight: 600; color: #eef2ff; opacity: 0.8; margin-left: 4px;">{unit}</span>
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

def render_compressibility_view(inputs: PVTInputs, rows_data: list[dict], fluid_info: dict, snapshot: dict, analysis_key: str):
    """Bespoke UI Layout specifically designed for Isothermal Compressibility Analysis."""
    
    # --- 1. The Hero Section ---
    col_hero, col_fluid = st.columns([1.5, 1])
    
    # Extract co at reservoir pressure
    res_co = rows_data[0]['co (psi-1)'] if rows_data else 0.0
    
    with col_hero:
        # Note: Using scientific notation for co is standard in the industry
        st.markdown(render_hero_kpi("Compressibility @ Pr", f"{res_co:.2e}", "psi⁻¹", "compress"), unsafe_allow_html=True)
        
    with col_fluid:
        st.markdown(f"""
            <div class="fluid-tag-container">
                <div class="fluid-tag-label">Reservoir Energy</div>
                <div class="fluid-tag-value">{fluid_info['name']}</div>
                <div class="fluid-tag-desc">Determines the volume of oil expansion per unit pressure drop. Critical for undersaturated drive analysis.</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    
    # --- 2. Key Volumetric Metrics ---
    st.markdown("<div class='results-section-title'>Expansion Properties</div>", unsafe_allow_html=True)
    
    if rows_data:
        pb_co = next((r['co (psi-1)'] for r in rows_data if r['P (psia)'] <= inputs.bubble_point_psia), rows_data[-1]['co (psi-1)'])
        
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        with kpi_col1:
            st.markdown(render_kpi_card("Co at Bubble Point", f"{pb_co:.2e}", "psi⁻¹"), unsafe_allow_html=True)
        with kpi_col2:
            # Typical oil co ranges from 5 to 30 x 10^-6 psi^-1
            st.markdown(render_kpi_card("Solution GOR", f"{inputs.rs_pb:,.0f}", "scf/STB"), unsafe_allow_html=True)
        with kpi_col3:
            st.markdown(render_kpi_card("Temp. Influence", f"{inputs.temp_f:.1f}", "°F"), unsafe_allow_html=True)

    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)

    # --- 3. Tabs Section ---
    tabs = st.tabs(["📊 Compressibility Chart", "📋 Detailed Data", "💡 Drive Analysis"])

    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        fig = build_chart(analysis_key, rows_data, inputs.api, inputs.gas_gravity, inputs.temp_f, inputs.reservoir_pressure_psia)
        
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#0f2942", family="Inter, sans-serif"),
            colorway=['#6366f1'], # Indigo for Compressibility
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