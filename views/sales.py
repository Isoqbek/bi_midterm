import streamlit as st
import plotly.express as px


def render(data):
    st.title("📈 Sales Analysis")
    st.caption("Sotuv trendlari, hudud va mahsulot bo'yicha tahlil, pipeline")

    k = data["kpis"]
    st_trend = data["sales_trend"]
    total_sales = st_trend["Sales"].sum()
    avg_deal = data["deals"]["Value"].mean()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Sales (12m)", f"${total_sales:,.0f}", f"{k['revenue_growth']:.1f}%")
    c2.metric("Active Deals", f"{k['active_deals']}")
    c3.metric("Avg Deal Size", f"${avg_deal:,.0f}")
    c4.metric("Closed Won", f"{int((data['deals']['Stage']=='Closed Won').sum())}")

    st.divider()

    st.subheader("Oylik sotuv vs reja (Target)")
    fig = px.line(st_trend, x="Month", y=["Sales", "Target"], markers=True,
                  color_discrete_sequence=["#2563eb", "#94a3b8"])
    fig.update_layout(height=320, margin=dict(t=10, b=0), legend_title_text="")
    st.plotly_chart(fig, width="stretch")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Hudud bo'yicha sotuv")
        fig2 = px.bar(data["sales_by_region"], x="Region", y="Sales",
                      color="Sales", color_continuous_scale="Blues")
        fig2.update_layout(height=320, margin=dict(t=10, b=0))
        st.plotly_chart(fig2, width="stretch")
    with col_b:
        st.subheader("Mahsulot bo'yicha sotuv")
        fig3 = px.bar(data["sales_by_product"], x="Sales", y="Product",
                      orientation="h", color="Sales",
                      color_continuous_scale="Teal")
        fig3.update_layout(height=320, margin=dict(t=10, b=0))
        st.plotly_chart(fig3, width="stretch")

    st.subheader("Sales Pipeline (bitimlar)")
    stage_filter = st.multiselect(
        "Bosqich bo'yicha filtr:",
        options=sorted(data["deals"]["Stage"].unique()),
        default=sorted(data["deals"]["Stage"].unique()),
    )
    df = data["deals"][data["deals"]["Stage"].isin(stage_filter)]
    st.dataframe(df, width="stretch", hide_index=True)
