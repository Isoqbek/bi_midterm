import streamlit as st
import plotly.express as px


def render(data):
    st.title("💰 Finance")
    st.caption("Daromad, xarajat, foyda marjasi va xarajatlar tarkibi")

    k = data["kpis"]
    fin = data["finance"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"${k['total_revenue']:,.0f}")
    c2.metric("Total Expenses", f"${fin['Expenses'].sum():,.0f}",
              delta_color="inverse")
    c3.metric("Net Profit", f"${k['net_profit']:,.0f}")
    c4.metric("Avg Margin", f"{k['profit_margin']:.1f}%")

    st.divider()

    st.subheader("Daromad, Xarajat va Foyda dinamikasi")
    fig = px.line(fin, x="Month", y=["Revenue", "Expenses", "Profit"],
                  markers=True,
                  color_discrete_sequence=["#2563eb", "#ef4444", "#16a34a"])
    fig.update_layout(height=340, margin=dict(t=10, b=0), legend_title_text="")
    st.plotly_chart(fig, width="stretch")

    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Foyda marjasi (%)")
        fig2 = px.area(fin, x="Month", y="Margin",
                       color_discrete_sequence=["#7c3aed"])
        fig2.update_layout(height=300, margin=dict(t=10, b=0))
        st.plotly_chart(fig2, width="stretch")
    with col_b:
        st.subheader("Xarajatlar tarkibi")
        fig3 = px.pie(data["expense_breakdown"], names="Category",
                      values="Amount", hole=0.4)
        fig3.update_layout(height=300, margin=dict(t=10, b=0))
        st.plotly_chart(fig3, width="stretch")

    st.subheader("Moliyaviy jadval")
    st.dataframe(fin, width="stretch", hide_index=True)
