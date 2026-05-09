from typing import List

import streamlit as st


def render_property_table(rows_data: List[dict]) -> None:
    rows = "".join(
        [
            (
                "<tr>"
                f"<td>{r['P (psia)']:.0f}</td>"
                f"<td>{r['Rs (scf/STB)']:.2f}</td>"
                f"<td>{r['Bo (RB/STB)']:.5f}</td>"
                f"<td>{r['muo (cp)']:.4f}</td>"
                f"<td>{r['co (psi-1)']:.3e}</td>"
                f"<td>{r['Z-factor']:.4f}</td>"
                f"<td>{r['Bg (RB/Mscf)']:.5f}</td>"
                f"<td>{r['mug (cp)']:.5f}</td>"
                "</tr>"
            )
            for r in rows_data
        ]
    )
    table_html = (
        "<table class='property-table'>"
        "<thead><tr>"
        "<th>P (psia)</th>"
        "<th>Rs (scf/STB)</th>"
        "<th>Bo (RB/STB)</th>"
        "<th>muo (cp)</th>"
        "<th>co (psi-1)</th>"
        "<th>Z-factor</th>"
        "<th>Bg (RB/Mscf)</th>"
        "<th>mug (cp)</th>"
        "</tr></thead>"
        f"<tbody>{rows}</tbody></table>"
    )
    st.markdown(table_html, unsafe_allow_html=True)
