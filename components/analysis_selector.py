import streamlit as st

from components.analysis_constants import ANALYSIS_LABELS, ANALYSIS_OPTIONS


def render_analysis_selector() -> str:
    st.markdown("<div class='analysis-card'>", unsafe_allow_html=True)
    st.markdown("<div class='analysis-header'>Select Analysis</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("<div class='analysis-selector'></div>", unsafe_allow_html=True)
        options = [key for key, _, _ in ANALYSIS_OPTIONS]
        selected = st.session_state.get("current_analysis", "bubble_point")
        if selected not in options:
            selected = options[0]
        st.session_state.current_analysis = st.radio(
            "",
            options=options,
            format_func=lambda key: ANALYSIS_LABELS.get(key, key),
            index=options.index(selected),
            horizontal=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    return st.session_state.current_analysis
