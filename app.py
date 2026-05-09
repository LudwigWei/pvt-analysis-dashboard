import streamlit as st

from components.input_panel import render_input_panel
from components.results_display import render_results_display
from utils.state_manager import init_state


def apply_base_styles() -> None:
    st.markdown(
        """
        <style>
        .app-header {
            background: linear-gradient(180deg, #0b2f57 0%, #0a2646 100%);
            color: #ffffff;
            padding: 18px 22px;
            border-radius: 10px;
            margin-bottom: 16px;
        }
        .app-header h1 {
            font-size: 24px;
            margin: 0 0 4px 0;
        }
        .app-header .subtitle {
            font-size: 13px;
            opacity: 0.9;
        }
        div[data-testid="stVerticalBlock"]:has(.input-card-marker):not(:has(div[data-testid="stVerticalBlock"]:has(.input-card-marker))) {
            background: #0f1624;
            border: 1px solid #1f2a3d;
            border-radius: 14px;
            padding: 16px 16px 8px 16px;
            box-shadow: 0 10px 26px rgba(5, 10, 20, 0.45);
        }
        .input-card-marker {
            height: 0;
            overflow: hidden;
        }
        .panel-title {
            color: #9fb4d1;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 1px;
            margin: 2px 2px 14px 2px;
        }
        .badge {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: #2b66a7;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            margin-top: 22px;
        }
        .field-label {
            font-size: 12px;
            font-weight: 600;
            color: #e2e8f0;
            margin-bottom: 4px;
        }
        .unit-text {
            font-size: 11px;
            color: #8fa2c0;
            margin-top: 34px;
        }
        .divider {
            border-bottom: 1px solid #1f2a3d;
            margin: 10px 0 12px 0;
        }
        .stNumberInput input {
            background: #1c2433 !important;
            color: #f8fafc !important;
            border: 1px solid #2a3447 !important;
            border-radius: 10px !important;
            padding: 10px 12px !important;
        }
        .stButton > button {
            border-radius: 10px !important;
        }
        .analysis-card,
        .results-card {
            background: #0f1624;
            border: 1px solid #1f2a3d;
            border-radius: 14px;
            padding: 14px 16px 12px 16px;
            box-shadow: 0 10px 26px rgba(5, 10, 20, 0.45);
            margin-bottom: 16px;
        }
        .analysis-header {
            background: #1f6f5c;
            color: #ffffff;
            padding: 8px 12px;
            border-radius: 10px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            margin-bottom: 10px;
        }
        .analysis-selector {
            height: 0;
            overflow: hidden;
        }
        div[data-testid="stRadio"] > div[role="radiogroup"] {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 10px;
        }
        div[data-testid="stRadio"] label {
            background: #1c2433;
            border: 1px solid #2a3447;
            border-radius: 12px;
            padding: 16px 12px;
            min-height: 72px;
            color: #e2e8f0;
            font-weight: 600;
            text-align: center;
        }
        div[data-testid="stRadio"] label:has(input:checked) {
            background: #111827;
            border-color: #475569;
            box-shadow: 0 6px 14px rgba(15, 23, 42, 0.35);
        }
        div[data-testid="stRadio"] input {
            display: none;
        }
        div[data-testid="stVerticalBlock"]:has(.chart-card-marker) {
            background: #0b1220;
            border: 1px solid #1f2a3d;
            border-radius: 12px;
            padding: 12px;
        }
        .chart-card-marker {
            height: 0;
            overflow: hidden;
        }
        .property-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            font-family: "IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
        }
        .property-table th,
        .property-table td {
            border: 1px solid #273449;
            padding: 6px 8px;
            text-align: left;
            color: #e2e8f0;
            white-space: nowrap;
        }
        .property-table th {
            background: #111827;
            color: #94a3b8;
            font-weight: 500;
            text-transform: uppercase;
            font-size: 10px;
            letter-spacing: 0.04em;
        }
        .fluid-card {
            background: #111827;
            border: 1px solid #1f2a3d;
            border-radius: 12px;
            padding: 12px 14px;
            margin-bottom: 12px;
        }
        .fluid-label {
            font-size: 10px;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }
        .fluid-name {
            font-size: 18px;
            font-weight: 600;
            color: #e2e8f0;
            margin-top: 6px;
        }
        .fluid-desc {
            font-size: 12px;
            color: #94a3b8;
            margin-top: 4px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header() -> None:
    st.markdown(
        """
        <div class="app-header">
            <h1>PVT Analysis System</h1>
            <div class="subtitle">Pressure • Volume • Temperature Analysis</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="PVT Analysis System", layout="wide")
init_state()
apply_base_styles()
render_header()

left_col, right_col = st.columns([1, 3], gap="large")
with left_col:
    render_input_panel()

with right_col:
    render_results_display()
