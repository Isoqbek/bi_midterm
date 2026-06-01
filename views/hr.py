import streamlit as st
import plotly.express as px


def render(data):
    st.title("👥 HR Analytics")
    st.caption("Xodimlar soni, ishga olish/ketish va attrition tahlili")

    k = data["kpis"]
    hc = data["headcount"]
    attr = data["attrition"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Employees", f"{k['employee_count']}")
    c2.metric("Avg Attrition", f"{k['avg_attrition']:.2f}%", delta_color="inverse")
    c3.metric("Open Positions", f"{k['open_positions']}")
    c4.metric("Avg Tenure", f"{k['avg_tenure']} yil")

    st.divider()

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Bo'lim bo'yicha xodimlar")
        fig = px.bar(hc.sort_values("Employees"), x="Employees",
                     y="Department", orientation="h", color="Employees",
                     color_continuous_scale="Purples")
        fig.update_layout(height=340, margin=dict(t=10, b=0))
        st.plotly_chart(fig, width="stretch")
    with col_b:
        st.subheader("Ochiq vakansiyalar")
        fig2 = px.bar(hc, x="Department", y="OpenPositions",
                      color="OpenPositions", color_continuous_scale="Reds")
        fig2.update_layout(height=340, margin=dict(t=10, b=0))
        st.plotly_chart(fig2, width="stretch")

    st.subheader("Ishga olish vs Ketish (oylik)")
    fig3 = px.bar(attr, x="Month", y=["Hires", "Leavers"], barmode="group",
                  color_discrete_sequence=["#16a34a", "#ef4444"])
    fig3.update_layout(height=300, margin=dict(t=10, b=0), legend_title_text="")
    st.plotly_chart(fig3, width="stretch")

    st.subheader("Attrition rate trendi (%)")
    fig4 = px.line(attr, x="Month", y="AttritionRate", markers=True,
                   color_discrete_sequence=["#dc2626"])
    fig4.update_layout(height=260, margin=dict(t=10, b=0))
    st.plotly_chart(fig4, width="stretch")
