"""Optional Streamlit presentation for the generated control-tower report."""

from pathlib import Path
import sys

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from control_tower.report import build_report


DATA_DIR = Path(__file__).parents[1] / "data"
report = build_report(DATA_DIR)

st.set_page_config(page_title="E-commerce Growth Control Tower", layout="wide")
st.title("E-commerce Growth Control Tower")
st.caption("Synthetic portfolio data — diagnostic demonstration only")

campaigns = pd.DataFrame(report["campaigns"])
col1, col2, col3, col4 = st.columns(4)
col1.metric("Spend", f"{campaigns['spend'].sum():.2f}")
col2.metric("Link clicks", f"{campaigns['link_clicks'].sum():,}")
col3.metric("Purchases", f"{campaigns['purchases'].sum():,}")
col4.metric("Revenue", f"{campaigns['revenue'].sum():.2f}")

st.subheader("Campaign diagnostics")
st.dataframe(campaigns, use_container_width=True, hide_index=True)

st.subheader("Recommendations")
st.dataframe(pd.DataFrame(report["recommendations"]), use_container_width=True, hide_index=True)

st.subheader("Platform/site reconciliation")
st.dataframe(pd.DataFrame(report["reconciliation"]), use_container_width=True, hide_index=True)
