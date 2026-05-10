import streamlit as st
from calculations.pvt_properties import PVTInputs
from components.charts import build_chart
from components.interpretations import build_interpretations
from components.property_table import render_property_table

def render_hero_kpi(label: str, value: str, unit: str, icon: str = "bubble_chart") -> str:
    """Renders a prominent, gradient Hero card with a modern shadow."""
    return f"""
    <div style="background: linear-gradient(135deg, #006fbb 0%, #005a96 100%); 
                border-radius: 16px; padding: 24px 32px; 
                box-shadow: 0 10px 15px -3px rgba(0, 111, 187, 0.2), 0 4px 6px -2px rgba(0, 111, 187, 0.1); 
                color: #ffffff; display: flex; align-items: center; justify-content: space-between; height: 100%;">
        <div>
            <div style="font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.2px; color: #eaf4fb; margin-bottom: 8px; opacity: 0.8;">{label}</div>
            <div style="font-size: 44px; font-weight: 800; line-height: 1; letter-spacing: -1px;">
                {value} <span style="font-size: 18px; font-weight: 600; color: #eaf4fb; opacity: 0.7; margin-left: 4px;">{unit}</span>
            </div>
        </div>
        <div style="font-family: 'Material Symbols Outlined'; font-size: 60px; opacity: 0.15; font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 48;">
            {icon}
        </div>
    </div>
    """

def render_bubble_point_view(inputs: PVTInputs, rows_data: list[dict], fluid_info: dict, snapshot: dict, analysis_key: str):
    """Bespoke UI Layout specifically designed for Bubble Point Analysis."""
    
    # --- 1. Top Section: Hero & Classification ---
    col_hero, col_fluid = st.columns([1.6, 1])
    
    with col_hero:
        st.markdown(render_hero_kpi("Calculated Bubble Point", f"{inputs.bubble_point_psia:,.0f}", "psia"), unsafe_allow_html=True)
        
    with col_fluid:
        st.markdown(f"""
            <div class="fluid-tag-container">
                <div class="fluid-tag-label">Fluid Identity</div>
                <div class="fluid-tag-value">{fluid_info['name']}</div>
                <div class="fluid-tag-desc">{fluid_info['desc']}</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)
    
    # --- 2. Key Properties Row ---
    st.markdown("<div class='results-section-title'>Key Saturated Properties</div>", unsafe_allow_html=True)
    
    if rows_data:
        pb_data = rows_data[0]
        kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
        # Using a helper for consistent small KPIs
        from components.results_display import render_kpi_card
        with kpi_col1:
            st.markdown(render_kpi_card("Oil FVF (Bo)", f"{pb_data['Bo (RB/STB)']:.4f}", "RB/STB"), unsafe_allow_html=True)
        with kpi_col2:
            st.markdown(render_kpi_card("Oil Viscosity (μo)", f"{pb_data['muo (cp)']:.3f}", "cp"), unsafe_allow_html=True)
        with kpi_col3:
            st.markdown(render_kpi_card("Compressibility (co)", f"{pb_data['co (psi-1)']:.2e}", "psi⁻¹"), unsafe_allow_html=True)

    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    # --- 3. Dashboard Layout (Chart & Interpretation) ---
    col_chart, col_interp = st.columns([2, 1])
    
    with col_chart:
        fig = build_chart(analysis_key, rows_data, inputs.api, inputs.gas_gravity, inputs.temp_f, inputs.reservoir_pressure_psia)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color="#0f2942", family="Inter, sans-serif"),
            colorway=['#006fbb'],
            margin=dict(t=40, b=40, l=40, r=40)
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_interp:
        st.markdown(
            """
            <div style='background: #ffffff; border: 1px solid #d3e1ee; border-radius: 12px; padding: 20px; box-shadow: 0 2px 8px rgba(15, 41, 66, 0.02); height: 100%;'>
                <h4 style='margin-top: 0; color: #0f2942; font-size: 16px; font-weight: 600; margin-bottom: 16px;'>💡 Interpretation</h4>
                <ul style='color: #5b7b97; line-height: 1.6; font-size: 14px; padding-left: 20px; margin: 0;'>
            """, 
            unsafe_allow_html=True
        )
        for text in build_interpretations(analysis_key, rows_data, snapshot):
            st.markdown(f"<li style='margin-bottom: 8px;'>{text}</li>", unsafe_allow_html=True)
        st.markdown("</ul></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 32px;'></div>", unsafe_allow_html=True)

    # --- 4. Detailed Data Table ---
    st.markdown("<div class='results-section-title' style='margin-bottom: 16px; font-size: 18px; font-weight: 600; color: #0f2942;'>📋 Detailed Data</div>", unsafe_allow_html=True)
    render_property_table(rows_data)