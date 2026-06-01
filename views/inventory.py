import streamlit as st
import plotly.express as px


def render(data):
    st.title("📦 Inventory")
    st.caption("Ombor holati, zaxira qiymati va kam qolgan tovarlar")

    inv = data["inventory"]
    out_of_stock = int((inv["Status"] == "Out of Stock").sum())
    low_stock = int((inv["Status"] == "Low Stock").sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Items (SKU)", f"{len(inv)}")
    c2.metric("Inventory Value", f"${inv['Value'].sum():,.0f}")
    c3.metric("Low Stock", f"{low_stock}", delta_color="inverse")
    c4.metric("Out of Stock", f"{out_of_stock}", delta_color="inverse")

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Kategoriya bo'yicha qiymat")
        fig = px.bar(data["inv_by_cat"], x="Category", y="Value",
                     color="Value", color_continuous_scale="Oranges")
        fig.update_layout(height=320, margin=dict(t=10, b=0))
        st.plotly_chart(fig, width="stretch")
    with col_b:
        st.subheader("Status taqsimoti")
        status_count = inv["Status"].value_counts().reset_index()
        status_count.columns = ["Status", "Count"]
        fig2 = px.pie(status_count, names="Status", values="Count", hole=0.45,
                      color="Status",
                      color_discrete_map={"OK": "#16a34a",
                                          "Low Stock": "#f59e0b",
                                          "Out of Stock": "#ef4444"})
        fig2.update_layout(height=320, margin=dict(t=10, b=0))
        st.plotly_chart(fig2, width="stretch")

    alerts = inv[inv["Status"] != "OK"].sort_values("Stock")
    if not alerts.empty:
        st.subheader("⚠️ Diqqat talab tovarlar (qayta buyurtma kerak)")
        st.dataframe(alerts[["SKU", "Item", "Category", "Stock",
                             "ReorderLevel", "Status"]],
                     width="stretch", hide_index=True)

    st.subheader("To'liq ombor ro'yxati")
    cat = st.selectbox("Kategoriya:", ["Hammasi"] + sorted(inv["Category"].unique()))
    show = inv if cat == "Hammasi" else inv[inv["Category"] == cat]
    st.dataframe(show, width="stretch", hide_index=True)
