import time
import streamlit as st

from components.input_panel import render_input_panel
from components.results_display import render_results_display
from utils.state_manager import init_state


def render_splash_screen() -> None:
    """Renders an ultra-premium, frameless splash overlay with just the animated icon."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24..48,100..700,0..1,-50..200');
        
        /* --- Deep Layered Background --- */
        .splash-container {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: linear-gradient(135deg, #f4f8fb 0%, #eaf4fb 50%, #ffffff 100%);
            display: flex; flex-direction: column;
            justify-content: center; align-items: center;
            z-index: 999999;
            font-family: "Inter", sans-serif;
            overflow: hidden;
        }

        /* Ambient glowing orb */
        .splash-glow {
            position: absolute;
            width: 500px; height: 500px;
            background: radial-gradient(circle, rgba(0, 111, 187, 0.08) 0%, transparent 60%);
            border-radius: 50%;
            z-index: 1;
            animation: breathe-glow 4s ease-in-out infinite alternate;
            pointer-events: none;
        }

        @keyframes breathe-glow {
            0% { transform: scale(0.8); opacity: 0.5; }
            100% { transform: scale(1.2); opacity: 1; }
        }

        /* --- Frameless Content Wrapper --- */
        .splash-content {
            position: relative;
            z-index: 2;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            opacity: 0;
            animation: fade-up-splash 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }

        @keyframes fade-up-splash {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* --- Orbital Loader + Icon --- */
        .loader-wrapper {
            position: relative;
            width: 80px; height: 80px;
            display: flex; justify-content: center; align-items: center;
        }

        .orbital-ring {
            position: absolute;
            width: 100%; height: 100%;
            border-radius: 50%;
            border: 2px solid rgba(0, 111, 187, 0.1);
            border-top-color: #006fbb;
            border-right-color: rgba(0, 111, 187, 0.4);
            animation: spin-ring 1.2s cubic-bezier(0.5, 0.1, 0.5, 0.9) infinite;
        }

        .water-drop-icon {
            font-size: 40px;
            color: #006fbb;
            animation: pulse-drop 2.4s ease-in-out infinite;
        }

        @keyframes spin-ring {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes pulse-drop {
            0%, 100% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.05); opacity: 1; drop-shadow: 0 4px 12px rgba(0,111,187,0.2); }
        }
        </style>
        
        <div class="splash-container">
            <div class="splash-glow"></div>
            <div class="splash-content">
                <div class="loader-wrapper">
                    <div class="orbital-ring"></div>
                    <span class="material-symbols-outlined water-drop-icon" style="font-variation-settings: 'FILL' 1;">water_drop</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
def apply_base_styles() -> None:
    st.markdown(
        """
        <style>
        /* Main App Background (Pure White) */
        .stApp { background-color: #ffffff; }

        /* Hide the default Streamlit header */
        header[data-testid="stHeader"] { display: none !important; }

        /* Remove the massive default padding at the top of the app */
        .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }

        /* Top Navigation Bar */
        .navbar {
            background-color: transparent; border-bottom: 1px solid #d3e1ee;
            padding: 8px 0px 16px 0px; margin-bottom: 24px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .navbar-brand { display: flex; align-items: center; gap: 12px; }
        .navbar-logo {
            background: #006fbb; color: #ffffff; font-weight: 700; font-size: 13px;
            padding: 6px 10px; border-radius: 6px; letter-spacing: 0.5px;
        }
        .navbar-title { font-size: 18px; font-weight: 700; color: #0f2942; margin: 0; padding: 0; }
        .navbar-subtitle {
            font-size: 13px; color: #5b7b97; margin-left: 12px;
            border-left: 1px solid #d3e1ee; padding-left: 12px;
        }

        /* Target the Left Column directly (Input Panel) */
        div[data-testid="stColumn"]:has(.input-card-marker) {
            background: #ffffff; border: 1px solid #d3e1ee; border-radius: 14px;
            padding: 24px 20px; box-shadow: 0 4px 15px rgba(15, 41, 66, 0.04);
        }

        /* Bento-Style Card Containers */
        div[data-testid="stVerticalBlock"]:has(> div.element-container .bento-card-marker) {
            background: #ffffff; border: 1px solid #d3e1ee; border-radius: 16px;
            padding: 24px 28px !important; box-shadow: 0 4px 20px rgba(15, 41, 66, 0.03); margin-bottom: 24px;
        }

        /* Hide Number Input Steppers */
        button[data-testid="stNumberInputStepDown"],
        button[data-testid="stNumberInputStepUp"] { display: none !important; }
        
        /* --- Premium Oceanic Buttons --- */
        div[data-testid="stButton"] > button {
            border-radius: 8px !important; border: 1px solid #d3e1ee !important;
            background: #ffffff !important; color: #0f2942 !important; 
            font-weight: 600 !important; transition: all 0.2s ease;
        }
        
        /* Premium Primary CTA Button (Run Analysis) */
        div[data-testid="stButton"] > button[kind="primary"] {
            background: linear-gradient(135deg, #006fbb 0%, #005a96 100%) !important;
            border: none !important; color: #ffffff !important; font-size: 14px !important;
            font-weight: 700 !important; letter-spacing: 0.5px !important;
            padding: 12px 24px !important; box-shadow: 0 4px 12px rgba(0, 111, 187, 0.25) !important;
            transition: all 0.3s ease !important;
        }
        
        /* Hover Effect: Lift and Glow */
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            transform: translateY(-2px) !important; box-shadow: 0 6px 16px rgba(0, 111, 187, 0.35) !important;
            background: linear-gradient(135deg, #007dd1 0%, #0062a3 100%) !important; border: none !important;
        }
        
        /* Active (Click) Effect: Press Down */
        div[data-testid="stButton"] > button[kind="primary"]:active {
            transform: translateY(0px) !important; box-shadow: 0 2px 8px rgba(0, 111, 187, 0.25) !important;
            border: none !important;
        }

        /* Main Analysis & Results typography */
        .analysis-header {
            background: #ffffff; color: #0f2942; padding: 8px 12px; border-radius: 10px;
            font-size: 12px; font-weight: 700; text-transform: uppercase;
            letter-spacing: 0.5px; margin-bottom: 12px; border: 1px solid #d3e1ee;
        }

        /* Property Table */
        .property-table {
            width: 100%; border-collapse: collapse; font-size: 12px;
            font-family: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
        }
        .property-table th,
        .property-table td {
            border: 1px solid #d3e1ee; padding: 8px 10px; text-align: left;
            color: #0f2942; white-space: nowrap;
        }
        .property-table th {
            background: #f4f8fb; color: #5b7b97; font-weight: 600;
            text-transform: uppercase; font-size: 10px; letter-spacing: 0.05em;
        }
        
        /* Fluid Classification Card */
        .fluid-card {
            background: #ffffff; border: 1px solid #d3e1ee; border-radius: 12px;
            padding: 14px 16px; margin-bottom: 12px; box-shadow: 0 4px 6px rgba(15, 41, 66, 0.02);
        }
        .fluid-label { font-size: 10px; color: #5b7b97; text-transform: uppercase; letter-spacing: 0.08em; }
        .fluid-name { font-size: 18px; font-weight: 700; color: #0f2942; margin-top: 6px; }
        .fluid-desc { font-size: 12px; color: #5b7b97; margin-top: 4px; }

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

# --- INITIAL APP LOAD SPLASH SCREEN ---
if st.session_state.get("show_splash", True):
    splash_placeholder = st.empty()
    with splash_placeholder:
        render_splash_screen()
    
    # Hold the splash screen for 1.5 seconds to build anticipation
    time.sleep(1.5)
    
    # Mark splash as complete and force a clean rerun to load the real UI
    st.session_state.show_splash = False
    st.rerun()

# --- NORMAL APP FLOW ---
apply_base_styles()
render_header()

# Route based on the current view state
current_view = st.session_state.get("current_view", "inputs")

if current_view == "inputs":
    render_input_panel()
else:
    render_results_display()