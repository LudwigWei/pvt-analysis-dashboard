import streamlit as st

from components.input_panel import render_input_panel
from components.results_display import render_results_display
from utils.state_manager import init_state


def apply_base_styles() -> None:
    st.markdown(
        """
        <style>
        /* Ensure the main background color stays pure white */
        .stApp {
            background-color: #ffffff;
        }

        /* Hide the default Streamlit header (Deploy button, menu, etc.) */
        header[data-testid="stHeader"] {
            display: none !important;
        }

        /* Remove the massive default padding at the top of the app */
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
        }

        /* Top Navigation Bar */
        .navbar {
            background-color: transparent;
            border-bottom: 1px solid #e2e8f0;
            padding: 8px 0px 16px 0px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar-brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        .navbar-logo {
            background: #0f172a; /* Dark slate for high contrast */
            color: #ffffff;
            font-weight: 700;
            font-size: 13px;
            padding: 6px 10px;
            border-radius: 6px;
            letter-spacing: 0.5px;
        }
        .navbar-title {
            font-size: 18px;
            font-weight: 700;
            color: #0f172a;
            margin: 0;
            padding: 0;
        }
        .navbar-subtitle {
            font-size: 13px;
            color: #64748b;
            margin-left: 12px;
            border-left: 1px solid #cbd5e1;
            padding-left: 12px;
        }
        .navbar-right {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            color: #64748b;
            font-weight: 600;
            letter-spacing: 0.3px;
        }

        /* Target the Left Column directly (Input Panel) */
        div[data-testid="stColumn"]:has(.input-card-marker) {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 14px;
            padding: 24px 20px;
            box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
        }

        /* Bento-Style Card Containers */
        div[data-testid="stVerticalBlock"]:has(> div.element-container .bento-card-marker) {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 16px;
            padding: 10px 24px;
            box-shadow: 0 4px 20px rgba(15, 23, 42, 0.03);
            margin-bottom: 24px;
        }

        /* Hide Number Input Steppers */
        button[data-testid="stNumberInputStepDown"],
        button[data-testid="stNumberInputStepUp"] {
            display: none !important;
        }

        /* Input Panel Typography and Elements */
        .panel-title {
            color: #64748b;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 1px;
            margin: 2px 2px 14px 2px;
        }
        .field-label {
            font-size: 13px;
            font-weight: 600;
            color: #64748b;
            margin-bottom: 4px;
        }
        .divider {
            border-bottom: 1px solid #e2e8f0;
            margin: 10px 0 12px 0;
        }
        
        /* Premium Streamlit Number Inputs & Dropdowns */
        .stNumberInput div[data-baseweb="input"] {
            background-color: #f8fafc !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 0 !important;
            overflow: hidden;
        }
        .stNumberInput div[data-baseweb="input"]:focus-within {
            border-color: #0284c7 !important;
            box-shadow: 0 0 0 1px #0284c7 !important;
        }
        /* Remove internal borders or separation artifacts */
        .stNumberInput div[data-baseweb="base-input"] {
            background-color: transparent !important;
            border: none !important;
        }
        .stNumberInput input {
            color: #0f172a !important;
            font-weight: 500 !important;
            padding: 8px 12px !important;
            background-color: transparent !important;
        }

        .stSelectbox > div > div {
            background: #f8fafc !important;
            color: #0f172a !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
        }
        .stSelectbox > div > div:focus-within {
            border-color: #0284c7 !important;
            box-shadow: 0 0 0 1px #0284c7 !important;
        }

        .stButton > button {
            border-radius: 8px !important;
            border: 1px solid #cbd5e1 !important;
            background: #ffffff !important;
            color: #334155 !important;
            font-weight: 600 !important;
        }
        .stButton > button[data-testid="baseButton-primary"] {
            background: #0284c7 !important;
            border: 1px solid #0284c7 !important;
            color: #ffffff !important;
        }
        .stButton > button[data-testid="baseButton-primary"]:hover {
            background: #0369a1 !important;
            border-color: #0369a1 !important;
        }
        .stButton > button:hover:not([data-testid="baseButton-primary"]) {
            border-color: #94a3b8 !important;
            color: #0f172a !important;
            background: #f1f5f9 !important;
        }

        /* Main Analysis & Results typography */
        .analysis-header {
            background: #ffffff;
            color: #0f172a;
            padding: 8px 12px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            border: 1px solid #e2e8f0;
        }

        /* Property Table */
        .property-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            font-family: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
        }
        .property-table th,
        .property-table td {
            border: 1px solid #e2e8f0;
            padding: 8px 10px;
            text-align: left;
            color: #334155;
            white-space: nowrap;
        }
        .property-table th {
            background: #f8fafc;
            color: #475569;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 10px;
            letter-spacing: 0.05em;
        }
        
        /* Fluid Classification Card */
        .fluid-card {
            background: #ffffff;
            border: 1px solid #e2e8f0;
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px rgba(15,23,42,0.02);
        }
        .fluid-label {
            font-size: 10px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .fluid-name {
            font-size: 18px;
            font-weight: 700;
            color: #0f172a;
            margin-top: 6px;
        }
        .fluid-desc {
            font-size: 12px;
            color: #475569;
            margin-top: 4px;
        }

        /* Clean up unused/broken wrapper classes */
        .input-card-marker, .chart-card-marker { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="navbar">
            <div class="navbar-brand">
                <div class="navbar-logo">PVT</div>
                <div>
                    <span class="navbar-title">PVT Analysis System</span>
                    <span class="navbar-subtitle">Reservoir Engineering</span>
                </div>
            </div>
            <div class="navbar-right">
                Standing • Beggs-Robinson • Papay • LGE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(
    page_title="PVT Analysis System", 
    page_icon="🛢️", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

init_state()
apply_base_styles()
render_header()

# Route based on the current view state
current_view = st.session_state.get("current_view", "inputs")

if current_view == "inputs":
    render_input_panel()
else:
    render_results_display()