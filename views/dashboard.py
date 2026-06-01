import streamlit as st
import plotly.express as px


def render(data):
    st.title("🏢 Business Intelligence — Dashboard")
    st.caption("Kompaniya bo'yicha umumiy ko'rsatkichlar (KPI) va asosiy trendlar")

    k = data["kpis"]

    # ---- KPI metrics (columns) ----
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"${k['total_revenue']:,.0f}",
              f"{k['revenue_growth']:.1f}%")
    c2.metric("Active Deals", f"{k['active_deals']}", "pipeline")
    c3.metric("Inventory Value", f"${k['inventory_value']:,.0f}",
              f"-{k['low_stock']} low stock", delta_color="inverse")
    c4.metric("Employee Count", f"{k['employee_count']}",
              f"+{k['open_positions']} open")

    st.divider()

    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.subheader("Daromad vs Xarajat (12 oy)")
        fin = data["finance"]
        fig = px.bar(fin, x="Month", y=["Revenue", "Expenses"],
                     barmode="group",
                     color_discrete_sequence=["#2563eb", "#ef4444"])
        fig.update_layout(height=340, margin=dict(t=10, b=0),
                          legend_title_text="")
        st.plotly_chart(fig, width="stretch")

    with col_b:
        st.subheader("Sotuv bo'yicha hudud")
        reg = data["sales_by_region"]
        fig2 = px.pie(reg, names="Region", values="Sales", hole=0.45)
        fig2.update_layout(height=340, margin=dict(t=10, b=0))
        st.plotly_chart(fig2, width="stretch")

    st.subheader("Sof foyda dinamikasi")
    fig3 = px.area(data["finance"], x="Month", y="Profit",
                   color_discrete_sequence=["#16a34a"])
    fig3.update_layout(height=280, margin=dict(t=10, b=0))
    st.plotly_chart(fig3, width="stretch")
