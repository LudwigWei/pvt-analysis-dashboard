import streamlit as st

from components.input_panel import render_input_panel
from components.results_display import render_results_display
from utils.state_manager import init_state


def apply_base_styles() -> None:
    st.markdown(
        """
        <style>
        /* Main App Background (Pure White) */
        .stApp {
            background-color: #ffffff;
        }

        /* Hide the default Streamlit header */
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
            border-bottom: 1px solid #d3e1ee;
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
            background: #006fbb; 
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
            color: #0f2942;
            margin: 0;
            padding: 0;
        }
        .navbar-subtitle {
            font-size: 13px;
            color: #5b7b97;
            margin-left: 12px;
            border-left: 1px solid #d3e1ee;
            padding-left: 12px;
        }

        /* Target the Left Column directly (Input Panel) */
        div[data-testid="stColumn"]:has(.input-card-marker) {
            background: #ffffff;
            border: 1px solid #d3e1ee;
            border-radius: 14px;
            padding: 24px 20px;
            box-shadow: 0 4px 15px rgba(15, 41, 66, 0.04);
        }

        /* Bento-Style Card Containers */
        div[data-testid="stVerticalBlock"]:has(> div.element-container .bento-card-marker) {
            background: #ffffff;
            border: 1px solid #d3e1ee;
            border-radius: 16px;
            padding: 24px 28px !important;
            box-shadow: 0 4px 20px rgba(15, 41, 66, 0.03);
            margin-bottom: 24px;
        }

        /* Hide Number Input Steppers */
        button[data-testid="stNumberInputStepDown"],
        button[data-testid="stNumberInputStepUp"] {
            display: none !important;
        }
        
        /* --- Premium Oceanic Buttons --- */
        div[data-testid="stButton"] > button {
            border-radius: 8px !important;
            border: 1px solid #d3e1ee !important;
            background: #ffffff !important;
            color: #0f2942 !important; 
            font-weight: 600 !important;
            transition: all 0.2s ease;
        }
        
        /* Premium Primary CTA Button (Run Analysis) */
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #006fbb 0%, #005a96 100%) !important;
            border: none !important;
            color: #ffffff !important;
            font-size: 14px !important;
            font-weight: 700 !important;
            letter-spacing: 0.5px !important;
            padding: 12px 24px !important;
            box-shadow: 0 4px 12px rgba(0, 111, 187, 0.25) !important;
            transition: all 0.3s ease !important;
        }
        
        /* Hover Effect: Lift and Glow */
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(0, 111, 187, 0.35) !important;
            background: linear-gradient(135deg, #007dd1 0%, #0062a3 100%) !important;
            border: none !important;
        }
        
        /* Active (Click) Effect: Press Down */
        div[data-testid="stButton"] > button[kind="primary"]:active {
            transform: translateY(0px) !important;
            box-shadow: 0 2px 8px rgba(0, 111, 187, 0.25) !important;
            border: none !important;
        }

        /* Main Analysis & Results typography */
        .analysis-header {
            background: #ffffff;
            color: #0f2942;
            padding: 8px 12px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            border: 1px solid #d3e1ee;
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
            border: 1px solid #d3e1ee;
            padding: 8px 10px;
            text-align: left;
            color: #0f2942;
            white-space: nowrap;
        }
        .property-table th {
            background: #f4f8fb;
            color: #5b7b97;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 10px;
            letter-spacing: 0.05em;
        }
        
        /* Fluid Classification Card */
        .fluid-card {
            background: #ffffff;
            border: 1px solid #d3e1ee;
            border-radius: 12px;
            padding: 14px 16px;
            margin-bottom: 12px;
            box-shadow: 0 4px 6px rgba(15, 41, 66, 0.02);
        }
        .fluid-label {
            font-size: 10px;
            color: #5b7b97;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .fluid-name {
            font-size: 18px;
            font-weight: 700;
            color: #0f2942;
            margin-top: 6px;
        }
        .fluid-desc {
            font-size: 12px;
            color: #5b7b97;
            margin-top: 4px;
        }

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