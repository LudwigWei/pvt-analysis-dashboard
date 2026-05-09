from __future__ import annotations

import streamlit as st

from calculations.fluid_classification import classify_fluid
from calculations.pvt_properties import PVTInputs, generate_rows
from components.analysis_selector import render_analysis_selector
from components.charts import build_chart
from components.fluid_card import render_fluid_card
from components.interpretations import build_interpretations
from components.property_table import render_property_table


def render_results_display() -> None:
    analysis_key = render_analysis_selector()

    calculated = st.session_state.get("calculated", False)
    if not calculated:
        return

    snapshot = st.session_state.get("input_snapshot", {})

    api = snapshot["api_gravity"]
    gas_gravity = snapshot["gas_gravity"]
    temp_f = snapshot["reservoir_temp_f"]
    reservoir_pressure_psia = snapshot["reservoir_pressure_psia"]

    inputs = PVTInputs(
        api=api,
        gas_gravity=gas_gravity,
        temp_f=temp_f,
        bubble_point_psia=reservoir_pressure_psia,
        rs_pb=snapshot["producing_gor_scfstb"],
    )
    rows_data = generate_rows(inputs)

    fluid_info = classify_fluid(api, snapshot["producing_gor_scfstb"])
    render_fluid_card(fluid_info)

    st.markdown("<div class='results-card'>", unsafe_allow_html=True)
    st.markdown("<div class='analysis-header'>Results Display</div>", unsafe_allow_html=True)

    tabs = st.tabs(["Graph", "Property Table", "Interpretation"])

    with tabs[0]:
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
            st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        render_property_table(rows_data)

    with tabs[2]:
        for text in build_interpretations(analysis_key, rows_data, snapshot):
            st.markdown(f"- {text}")

    st.markdown("</div>", unsafe_allow_html=True)
