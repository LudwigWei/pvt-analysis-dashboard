import streamlit as st

from components.input_panel import render_input_panel
from components.results_display import render_results_display
from utils.state_manager import init_state


def apply_base_styles() -> None:
    st.markdown(
        """
        <style>
        /* Main App Background (Faint Ice Blue) */
        .stApp {
            background-color: #ffffff;
        }

        header[data-testid="stHeader"] { display: none !important; }
        .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }

        /* Top Navigation Bar */
        .navbar {
            background-color: transparent;
            border-bottom: 1px solid #d3e1ee; /* Pale Blue Border */
            padding: 8px 0px 16px 0px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .navbar-brand { display: flex; align-items: center; gap: 12px; }
        
        .navbar-logo {
            background: #006fbb; /* Ocean Blue */
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
            color: #0f2942; /* Deep Navy */
            margin: 0; padding: 0;
        }
        .navbar-subtitle {
            font-size: 13px;
            color: #5b7b97; /* Steel Blue */
            margin-left: 12px;
            border-left: 1px solid #d3e1ee;
            padding-left: 12px;
        }
        .navbar-right {
            background: #ffffff;
            border: 1px solid #d3e1ee; /* Pale Blue Border */
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 11px;
            color: #5b7b97; /* Steel Blue */
            font-weight: 600;
            letter-spacing: 0.3px;
        }

        /* Bento-Style Card Containers */
        div[data-testid="stVerticalBlock"]:has(> div.element-container .bento-card-marker) {
            background: #ffffff;
            border: 1px solid #d3e1ee; /* Pale Blue Border */
            border-radius: 16px;
            padding: 28px 32px;
            box-shadow: 0 4px 20px rgba(15, 41, 66, 0.04); /* Adjusted shadow for navy tint */
            margin-bottom: 24px;
        }

        /* Hide Number Input Steppers */
        button[data-testid="stNumberInputStepDown"],
        button[data-testid="stNumberInputStepUp"] { display: none !important; }
        
        /* --- Buttons --- */
        .stButton > button {
            border-radius: 8px !important;
            border: 1px solid #d3e1ee !important;
            background: #ffffff !important;
            color: #0f2942 !important; 
            font-weight: 600 !important;
            transition: all 0.2s ease;
        }
        
        /* Premium Primary CTA Button (Run Analysis) */
        .stButton > button[data-testid="baseButton-primary"] {
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
        .stButton > button[data-testid="baseButton-primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 16px rgba(0, 111, 187, 0.35) !important;
            background: linear-gradient(135deg, #007dd1 0%, #0062a3 100%) !important;
        }
        
        /* Active (Click) Effect: Press Down */
        .stButton > button[data-testid="baseButton-primary"]:active {
            transform: translateY(0px) !important;
            box-shadow: 0 2px 8px rgba(0, 111, 187, 0.25) !important;
        }

        /* Results typography & tables (for results_display.py) */
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
        .property-table th { background: #f4f8fb; color: #5b7b97; border: 1px solid #d3e1ee; }
        .property-table td { border: 1px solid #d3e1ee; color: #0f2942; }
        .fluid-card { border: 1px solid #d3e1ee; }
        .fluid-label { color: #5b7b97; }
        .fluid-name { color: #0f2942; }
        .fluid-desc { color: #5b7b97; }

        .bento-card-marker, .chart-card-marker { display: none; }
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