import streamlit as st
import pandas as pd

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Delivery Delay Intelligence Dashboard",
    layout="wide"
)

# =================================================
# LOAD DATA
# =================================================
@st.cache_data
def load_data():
    return pd.read_csv("data/final_intelligence_output.csv")

df = load_data()

# Safety check
if df.empty:
    st.error("Dataset is empty. Please check CSV file.")
    st.stop()

# =================================================
# REQUIRED COLUMNS CHECK
# =================================================
required_cols = [
    "order_id", "traffic_level", "weather",
    "delayed", "root_cause",
    "delay_risk_score", "ml_explanation"
]

missing = [c for c in required_cols if c not in df.columns]
if missing:
    st.error(f"Missing columns in CSV: {missing}")
    st.stop()

# =================================================
# RISK CATEGORY
# =================================================
def risk_category(score):
    if score > 0.8:
        return "High"
    elif score > 0.4:
        return "Medium"
    else:
        return "Low"

df["risk_category"] = df["delay_risk_score"].apply(risk_category)

# =================================================
# SIDEBAR FILTERS
# =================================================
st.sidebar.title("🔎 Filters")

traffic_filter = st.sidebar.multiselect(
    "Traffic Level",
    options=df["traffic_level"].unique(),
    default=list(df["traffic_level"].unique())
)

weather_filter = st.sidebar.multiselect(
    "Weather",
    options=df["weather"].unique(),
    default=list(df["weather"].unique())
)

risk_filter = st.sidebar.multiselect(
    "Risk Category",
    options=["Low", "Medium", "High"],
    default=["Low", "Medium", "High"]
)

filtered_df = df[
    (df["traffic_level"].isin(traffic_filter)) &
    (df["weather"].isin(weather_filter)) &
    (df["risk_category"].isin(risk_filter))
]

# =================================================
# TITLE
# =================================================
st.title("🚚 Delivery Delay Root Cause Intelligence Dashboard")
st.caption("Explainable ML‑based delay analysis with decision support")

# =================================================
# KPI SECTION
# =================================================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Deliveries", len(filtered_df))
col2.metric("Delayed Deliveries", filtered_df["delayed"].sum())
col3.metric("High‑Risk Orders", (filtered_df["delay_risk_score"] > 0.8).sum())
col4.metric("Avg Delay Risk", round(filtered_df["delay_risk_score"].mean(), 2))

st.divider()

# =================================================
# CHARTS (SAFE)
# =================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Delay Risk Distribution")
    if not filtered_df.empty:
        st.bar_chart(filtered_df["risk_category"].value_counts())
    else:
        st.info("No data for selected filters")

with col2:
    st.subheader("📊 Root Cause Breakdown")
    if not filtered_df.empty:
        st.bar_chart(filtered_df["root_cause"].value_counts())
    else:
        st.info("No data for selected filters")

st.divider()

# =================================================
# HIGH‑RISK TABLE
# =================================================
st.subheader("⚠ High‑Risk Deliveries")

if filtered_df.empty:
    st.warning("No deliveries available for selected filters.")
else:
    search_id = st.text_input("🔍 Search Order ID")

    table_df = filtered_df[filtered_df["risk_category"] == "High"]

    if search_id:
        table_df = table_df[
            table_df["order_id"].astype(str).str.contains(search_id)
        ]

    st.dataframe(
        table_df.sort_values("delay_risk_score", ascending=False),
        width="stretch"
    )

st.divider()

# =================================================
# ORDER EXPLANATION PANEL (CRASH‑SAFE)
# =================================================
st.subheader("🔍 Order‑Level Explanation")

if filtered_df.empty:
    st.warning("No orders available for explanation.")
else:
    selected_order = st.selectbox(
        "Select an Order ID",
        filtered_df["order_id"].unique()
    )

    selected_rows = filtered_df[
        filtered_df["order_id"] == selected_order
    ]

    if selected_rows.empty:
        st.warning("Selected order not available with current filters.")
    else:
        row = selected_rows.iloc[0]

        st.markdown(f"""
        ### 📦 Order ID: `{row['order_id']}`

        - **Delay Risk Score:** `{round(row['delay_risk_score'], 3)}`
        - **Risk Category:** `{row['risk_category']}`
        - **Primary Root Cause:** `{row['root_cause']}`

        #### 🧠 ML Explanation
        > {row['ml_explanation']}
        """)

        # =================================================
        # ACTION RECOMMENDATIONS
        # =================================================
        st.subheader("🛠 Recommended Actions")

        actions = []

        if "Traffic" in row["root_cause"]:
            actions.append("🚦 Reroute delivery to avoid traffic congestion")

        if "Weather" in row["root_cause"]:
            actions.append("🌧 Add buffer time due to adverse weather")

        if "Warehouse" in row["root_cause"]:
            actions.append("🏭 Prioritize warehouse dispatch")

        if row["delay_risk_score"] > 0.8:
            actions.append("⚠ Monitor delivery closely (High Risk)")

        if actions:
            for act in actions:
                st.write(act)
        else:
            st.write("✅ No immediate action required")

# =================================================
# INSIGHTS PANEL
# =================================================
with st.expander("📌 Key Insights"):
    if not filtered_df.empty:
        st.write(f"""
        • High‑risk deliveries: **{(filtered_df['delay_risk_score'] > 0.8).sum()}**  
        • Most common root cause: **{filtered_df['root_cause'].mode()[0]}**  
        • Average delay risk: **{round(filtered_df['delay_risk_score'].mean(), 2)}**
        """)
    else:
        st.info("No insights available for selected filters.")
