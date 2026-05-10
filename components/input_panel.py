import streamlit as st

from utils.state_manager import capture_inputs, mark_dirty, reset_state
from components.analysis_constants import ANALYSIS_LABELS, ANALYSIS_OPTIONS

def render_input_panel() -> None:
    st.markdown(
        """
        <style>
        /* Force Flexbox & Equal Heights */
        div[data-testid="stElementContainer"]:has(div[data-testid="stRadio"]),
        div[data-testid="stRadio"], div[data-testid="stRadio"] > div { width: 100% !important; display: block !important; }
        div[data-testid="stHorizontalBlock"]:has(.equal-height-marker) { align-items: stretch !important; }
        div[data-testid="column"]:has(.equal-height-marker) { display: flex !important; flex-direction: column !important; }
        div[data-testid="stVerticalBlock"]:has(> div.element-container .equal-height-marker) { height: 100% !important; flex-grow: 1 !important; display: flex; flex-direction: column; }

        /* 2x2 Bento Grid for Radio Buttons */
        div[data-testid="stRadio"] > div[role="radiogroup"] { display: grid !important; grid-template-columns: 1fr 1fr !important; gap: 12px !important; width: 100% !important; }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label {
            background-color: #ffffff;
            border: 1px solid #d3e1ee; /* Pale Blue Border */
            border-radius: 12px;
            padding: 16px 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 1px 2px rgba(15, 41, 66, 0.02);
            display: flex !important; flex-direction: column !important; justify-content: center !important; align-items: center !important;
            min-height: 100px; margin: 0 !important;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
            border-color: #8ba3b6; /* Slightly darker border on hover */
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
            border-color: #006fbb !important; /* Ocean Blue */
            background-color: #eaf4fb !important; /* Ocean Wash */
            box-shadow: 0 0 0 1px #006fbb !important;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child { display: none !important; }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:last-child {
            font-weight: 600;
            color: #0f2942; /* Deep Navy */
            font-size: 13px; width: 100%; text-align: center; display: flex; flex-direction: column; align-items: center; gap: 8px; 
        }

        /* --- Enhanced Headers with Subtitles --- */
        .bento-header-wrapper {
            display: flex; align-items: flex-start; margin-bottom: 28px; padding-bottom: 16px;
            border-bottom: 1px solid #d3e1ee; /* Pale Blue Border */
        }
        .header-text-group { display: flex; flex-direction: column; gap: 4px; }
        .header-title { font-size: 17px; font-weight: 700; color: #0f2942; line-height: 1.2; letter-spacing: -0.2px; }
        .header-subtitle { font-size: 12px; font-weight: 500; color: #5b7b97; line-height: 1.4; }

        /* --- Clean Input Headers (Title + Unit Only) --- */
        .input-header-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 6px !important; padding: 0 2px; }
        .field-title { font-size: 13px; font-weight: 600; color: #0f2942; letter-spacing: 0.2px; }
        .field-unit { font-size: 11px; font-weight: 600; color: #5b7b97; }

        /* --- Bottom Helper Text --- */
        .field-hint-bottom { font-size: 11px; font-weight: 500; color: #8ba3b6; text-align: left; margin-top: -6px; margin-bottom: 24px; padding-left: 2px; }

        /* --- Unified, Crisp Input Borders --- */
        div[data-testid="stNumberInput"] { margin-bottom: 0px !important; }
        .stNumberInput div[data-baseweb="input"] {
            background-color: #ffffff !important;
            border: 1px solid #d3e1ee !important; /* Pale Blue Border */
            border-radius: 8px !important;
            box-shadow: 0 1px 2px rgba(15, 41, 66, 0.02) !important;
            transition: all 0.2s ease;
        }
        .stNumberInput input { color: #0f2942 !important; font-weight: 500 !important; }
        .stNumberInput div[data-baseweb="input"]:focus-within {
            border-color: #006fbb !important; /* Ocean Blue */
            box-shadow: 0 0 0 2px rgba(0, 111, 187, 0.1) !important;
        }
        div[data-testid="stVerticalBlock"] > div:has(> button) { margin-bottom: 0px; }
        </style>
        """,
        unsafe_allow_html=True
    )

    col_main, col_side = st.columns([1.6, 1], gap="medium")

    with col_main:
        st.markdown(
            """
            <div class='bento-card-marker equal-height-marker'></div>
            <div class='bento-header-wrapper'>
                <div class='header-text-group'>
                    <div class='header-title'>Reservoir Parameters</div>
                    <div class='header-subtitle'>Define the base fluid properties and physical conditions</div>
                </div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        p_col1, p_col2 = st.columns(2, gap="medium")
        
        with p_col1:
            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>API Gravity</span>
                    <span class='field-unit'>°API</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("API Gravity", min_value=1.0, max_value=100.0, step=0.1, key="api_gravity", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 1 - 100</div>", unsafe_allow_html=True)
            
            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>Gas Gravity</span>
                    <span class='field-unit'>Air=1</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("Gas Gravity", min_value=0.5, max_value=1.5, step=0.01, key="gas_gravity", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 0.5 - 1.5</div>", unsafe_allow_html=True)

            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>Temperature</span>
                    <span class='field-unit'>°F</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("Temperature", min_value=50.0, max_value=400.0, step=1.0, key="reservoir_temp_f", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 50 - 400</div>", unsafe_allow_html=True)

        with p_col2:
            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>Reservoir Pressure</span>
                    <span class='field-unit'>psia</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("Reservoir Pressure", min_value=100.0, max_value=10000.0, step=1.0, key="reservoir_pressure_psia", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 100 - 10,000</div>", unsafe_allow_html=True)
            
            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>Separator Pressure</span>
                    <span class='field-unit'>psia</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("Separator Press.", min_value=50.0, max_value=5000.0, step=1.0, key="separator_pressure_psia", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 50 - 5,000</div>", unsafe_allow_html=True)
            
            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>Producing GOR</span>
                    <span class='field-unit'>scf/STB</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("Producing GOR", min_value=0.0, max_value=200000.0, step=10.0, key="producing_gor_scfstb", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 0 - 200,000</div>", unsafe_allow_html=True)

    with col_side:
        with st.container():
            st.markdown(
                """
                <div class='bento-card-marker equal-height-marker'></div>
                <div class='bento-header-wrapper'>
                    <div class='header-text-group'>
                        <div class='header-title'>Configuration</div>
                        <div class='header-subtitle'>Select the PVT property model to simulate</div>
                    </div>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            options = [key for key, _, _ in ANALYSIS_OPTIONS]
            selected = st.session_state.get("current_analysis", "bubble_point")
            if selected not in options:
                selected = options[0]
                
            st.session_state.current_analysis = st.radio(
                "Select Analysis Type",
                options=options,
                format_func=lambda key: ANALYSIS_LABELS.get(key, key),
                index=options.index(selected),
                label_visibility="collapsed",
                on_change=mark_dirty,
                horizontal=True
            )

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        
        # Single, dominant Call-To-Action button
        st.button("▶ Run Analysis", type="primary", use_container_width=True, on_click=capture_inputs)