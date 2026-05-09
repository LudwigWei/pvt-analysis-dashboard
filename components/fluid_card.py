import streamlit as st


def render_fluid_card(fluid_info: dict) -> None:
    st.markdown(
        """
        <div class="fluid-card">
            <div class="fluid-label">Fluid Classification</div>
            <div class="fluid-name">{}</div>
            <div class="fluid-desc">{}</div>
        </div>
        """.format(fluid_info["name"], fluid_info["desc"]),
        unsafe_allow_html=True,
    )
