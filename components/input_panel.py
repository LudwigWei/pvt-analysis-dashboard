import streamlit as st

from utils.state_manager import capture_inputs, mark_dirty, reset_state
from components.analysis_constants import ANALYSIS_LABELS, ANALYSIS_OPTIONS

def render_input_panel() -> None:
    st.markdown(
        """
        <style>
        /* --- Import Google Material Symbols --- */
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0');

        /* Force Flexbox & Equal Heights */
        div[data-testid="stElementContainer"]:has(div[data-testid="stRadio"]),
        div[data-testid="stRadio"], div[data-testid="stRadio"] > div { width: 100% !important; display: block !important; }
        div[data-testid="stHorizontalBlock"]:has(.equal-height-marker) { align-items: stretch !important; }
        div[data-testid="column"]:has(.equal-height-marker) { display: flex !important; flex-direction: column !important; }
        div[data-testid="stVerticalBlock"]:has(> div.element-container .equal-height-marker) { height: 100% !important; flex-grow: 1 !important; display: flex; flex-direction: column; }

        /* 1x4 Vertical List Layout for Radio Buttons */
        div[data-testid="stRadio"] > div[role="radiogroup"] { 
            display: flex !important; 
            flex-direction: column !important; 
            gap: 10px !important; 
            width: 100% !important; 
        }
        
        div[data-testid="stRadio"] > div[role="radiogroup"] > label {
            background-color: #ffffff;
            border: 1px solid #d3e1ee;
            border-radius: 12px;
            padding: 14px 16px;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 1px 2px rgba(15, 41, 66, 0.02);
            display: flex !important; 
            flex-direction: row !important;
            justify-content: flex-start !important; 
            align-items: center !important;
            margin: 0 !important;
            width: 100%;
        }
        
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
            border-color: #8ba3b6; 
        }
        
        div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {
            border-color: #006fbb !important; 
            background-color: #eaf4fb !important; 
            box-shadow: 0 0 0 1px #006fbb !important;
        }
        
        div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:first-child { display: none !important; }
        
        /* CSS Grid to split Icon, Title, and Subtitle */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:last-child {
            font-weight: 700;
            color: #0f2942; 
            font-size: 14px; 
            width: 100%; 
            display: grid;
            grid-template-columns: 44px 1fr; /* Space for the icon */
            grid-template-rows: auto auto;
            align-items: center; 
            text-align: left;
            line-height: 1.2;
        }

        /* --- Unified Material Icon Styling --- */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:last-child::before {
            font-family: 'Material Symbols Outlined';
            font-size: 26px;
            color: #8ba3b6; /* Muted default color */
            font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
            grid-column: 1;
            grid-row: 1 / span 2;
            display: flex;
            justify-content: flex-start;
            align-items: center;
            transition: all 0.2s ease;
        }

        /* Hover & Active states change icon color and fill it in */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover > div:last-child::before {
            color: #006fbb;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"] > div:last-child::before,
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) > div:last-child::before {
            color: #006fbb;
            font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;
        }

        /* Subtitle Placement */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label > div:last-child::after {
            grid-column: 2;
            grid-row: 2;
            font-size: 11px;
            color: #5b7b97;
            font-weight: 500;
            margin-top: 4px;
        }

        /* Content Injection per Option (Using Material Ligatures) */
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(1) > div:last-child::before { content: "bubble_chart"; }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(1) > div:last-child::after { content: "Gas expansion & oil shrinkage limits"; }

        div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(2) > div:last-child::before { content: "water_drop"; }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(2) > div:last-child::after { content: "Fluid mobility & flow resistance"; }

        div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(3) > div:last-child::before { content: "compress"; }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(3) > div:last-child::after { content: "Volumetric change under pressure"; }

        div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(4) > div:last-child::before { content: "area_chart"; }
        div[data-testid="stRadio"] > div[role="radiogroup"] > label:nth-child(4) > div:last-child::after { content: "P-T thermodynamic boundaries"; }


        /* --- Enhanced Headers with Subtitles --- */
        .bento-header-wrapper {
            display: flex; align-items: flex-start; margin-bottom: 20px; padding-bottom: 12px;
            border-bottom: 1px solid #d3e1ee; 
        }
        .header-text-group { display: flex; flex-direction: column; gap: 4px; }
        .header-title { font-size: 17px; font-weight: 700; color: #0f2942; line-height: 1.2; letter-spacing: -0.2px; }
        .header-subtitle { font-size: 12px; font-weight: 500; color: #5b7b97; line-height: 1.4; }

        /* --- Clean Input Headers (Title + Unit Only) --- */
        .input-header-row { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 6px !important; padding: 0 2px; }
        .field-title { font-size: 13px; font-weight: 600; color: #0f2942; letter-spacing: 0.2px; }
        .field-unit { font-size: 11px; font-weight: 600; color: #5b7b97; }

        /* --- Bottom Helper Text --- */
        .field-hint-bottom { font-size: 11px; font-weight: 500; color: #8ba3b6; text-align: left; margin-top: -4px; margin-bottom: 16px; padding-left: 2px; }

        /* --- Unified, Crisp Input Borders --- */
        div[data-testid="stNumberInput"] { margin-bottom: 0px !important; }
        .stNumberInput div[data-baseweb="input"] {
            background-color: #ffffff !important;
            border: 1px solid #d3e1ee !important; 
            border-radius: 8px !important;
            box-shadow: 0 1px 2px rgba(15, 41, 66, 0.02) !important;
            transition: all 0.2s ease;
        }
        .stNumberInput input { color: #0f2942 !important; font-weight: 500 !important; }
        .stNumberInput div[data-baseweb="input"]:focus-within {
            border-color: #006fbb !important; 
            box-shadow: 0 0 0 2px rgba(0, 111, 187, 0.1) !important;
        }
        
        /* --- OPTIMIZED BUTTON GAP --- */
        div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stButton"]) { 
            margin-top: -16px !important; 
            margin-bottom: 0px !important; 
        }
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
            st.number_input("API Gravity", min_value=1.0, max_value=100.0, step=0.1, key="api_gravity", format="%g", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 1 - 100</div>", unsafe_allow_html=True)
            
            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>Gas Gravity</span>
                    <span class='field-unit'>Air=1</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("Gas Gravity", min_value=0.5, max_value=1.5, step=0.01, key="gas_gravity", format="%g", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 0.5 - 1.5</div>", unsafe_allow_html=True)

            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>Temperature</span>
                    <span class='field-unit'>°F</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("Temperature", min_value=50.0, max_value=400.0, step=1.0, key="reservoir_temp_f", format="%g", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 50 - 400</div>", unsafe_allow_html=True)

        with p_col2:
            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>Reservoir Pressure</span>
                    <span class='field-unit'>psia</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("Reservoir Pressure", min_value=100.0, max_value=10000.0, step=1.0, key="reservoir_pressure_psia", format="%g", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 100 - 10,000</div>", unsafe_allow_html=True)
            
            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>Separator Pressure</span>
                    <span class='field-unit'>psia</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("Separator Press.", min_value=50.0, max_value=5000.0, step=1.0, key="separator_pressure_psia", format="%g", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 50 - 5,000</div>", unsafe_allow_html=True)
            
            st.markdown("""
                <div class='input-header-row'>
                    <span class='field-title'>Producing GOR</span>
                    <span class='field-unit'>scf/STB</span>
                </div>
            """, unsafe_allow_html=True)
            st.number_input("Producing GOR", min_value=0.0, max_value=200000.0, step=10.0, key="producing_gor_scfstb", format="%g", label_visibility="collapsed", on_change=mark_dirty)
            st.markdown("<div class='field-hint-bottom'>Range: 0 - 200,000</div>", unsafe_allow_html=True)

    with col_side:
        with st.container():
            st.markdown(
                """
                <div class='bento-card-marker equal-height-marker'></div>
                <div class='bento-header-wrapper'>
                    <div class='header-text-group'>
                        <div class='header-title'>Analysis Type</div>
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

        st.button("▶ Run Analysis", type="primary", use_container_width=True, on_click=capture_inputs)