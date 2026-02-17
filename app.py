import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Inventory-Aware Marketing Allocation", layout="wide")

st.title("📊 Inventory-Aware Marketing Resource Allocation System")

st.markdown("""
AI-powered system to optimize **Promotion %, Manpower Allocation, and Marketing Channels**
based on inventory and predicted demand.
""")

# ---------------- FILE UPLOAD ----------------

col1, col2 = st.columns(2)

with col1:
    inventory_file = st.file_uploader("Upload Inventory CSV", type=["csv"])

with col2:
    demand_file = st.file_uploader("Upload Demand Prediction CSV", type=["csv"])

if inventory_file is not None and demand_file is not None:

    inventory = pd.read_csv(inventory_file)
    demand = pd.read_csv(demand_file)

    df = pd.merge(inventory, demand, on="product_id")

    # ---------------- LOGIC ----------------

    def calculate_allocation(row):
        score = (row["predicted_demand"] * 0.6) + (row["current_stock"] * 0.4)

        if row["current_stock"] <= 30:
            promotion = 0
            manpower = 0
            channel = "Pause Ads"

        elif score >= 80:
            promotion = 80
            manpower = 4
            channel = "Social Media + Google Ads"

        elif score >= 60:
            promotion = 60
            manpower = 3
            channel = "Social Media"

        elif score >= 40:
            promotion = 40
            manpower = 2
            channel = "Email Marketing"

        else:
            promotion = 20
            manpower = 1
            channel = "Basic Ads"

        return pd.Series([promotion, manpower, channel])

    df[["promotion_percentage", "manpower_required", "marketing_channels"]] = df.apply(calculate_allocation, axis=1)

    # ---------------- FILTER ----------------

    st.sidebar.header("🔎 Filter Products")
    selected_product = st.sidebar.selectbox("Select Product", ["All"] + list(df["product_id"].unique()))

    if selected_product != "All":
        df = df[df["product_id"] == selected_product]

    # ---------------- KPI SUMMARY ----------------

    total_products = len(df)
    avg_promotion = round(df["promotion_percentage"].mean(), 2)
    total_manpower = df["manpower_required"].sum()

    k1, k2, k3 = st.columns(3)

    k1.metric("Total Products", total_products)
    k2.metric("Average Promotion %", f"{avg_promotion}%")
    k3.metric("Total Manpower Required", total_manpower)

    st.divider()

    # ---------------- DATA TABLE ----------------

    st.subheader("📋 Marketing Allocation Results")
    st.dataframe(df, width="stretch")

    # ---------------- PROMOTION CHART ----------------

    st.subheader("📈 Promotion Percentage per Product")
    fig1 = px.bar(
        df,
        x="product_id",
        y="promotion_percentage",
        text="promotion_percentage",
        title="Promotion Allocation",
    )
    fig1.update_traces(textposition="outside")
    fig1.update_layout(yaxis_title="Promotion %")
    st.plotly_chart(fig1, width="stretch")

    # ---------------- MANPOWER CHART ----------------

    st.subheader("👥 Manpower Allocation per Product")
    fig2 = px.bar(
        df,
        x="product_id",
        y="manpower_required",
        text="manpower_required",
        title="Manpower Requirement",
    )
    fig2.update_traces(textposition="outside")
    fig2.update_layout(yaxis_title="Number of Staff")
    st.plotly_chart(fig2, width="stretch")

    # ---------------- CHANNEL PIE ----------------

    st.subheader("📣 Marketing Channel Distribution")
    channel_counts = df["marketing_channels"].value_counts().reset_index()
    channel_counts.columns = ["marketing_channels", "count"]

    fig3 = px.pie(
        channel_counts,
        names="marketing_channels",
        values="count",
        title="Channel Distribution",
    )
    st.plotly_chart(fig3, width="stretch")

    # ---------------- DOWNLOAD ----------------

    st.subheader("⬇️ Download Report")
    csv = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Marketing Allocation Report (CSV)",
        data=csv,
        file_name="marketing_allocation_report.csv",
        mime="text/csv",
    )

else:
    st.info("Please upload both Inventory and Demand CSV files to proceed.")

