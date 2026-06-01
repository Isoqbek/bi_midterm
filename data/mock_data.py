"""
Mock biznes ma'lumotlari generatori.
Barcha ma'lumotlar seed bilan generatsiya qilinadi => KPI'lar barqaror bo'ladi.
Real loyihada bu joyni database / API bilan almashtirish mumkin.
"""
import numpy as np
import pandas as pd

SEED = 16


def _months(n=12):
    return pd.date_range(end=pd.Timestamp.today().normalize().replace(day=1),
                         periods=n, freq="MS")


def generate_data():
    rng = np.random.default_rng(SEED)
    months = _months(12)
    month_labels = [m.strftime("%b %Y") for m in months]

    # ----------------------------- SALES -----------------------------
    regions = ["North", "South", "East", "West", "Central"]
    products = ["Alpha CRM", "Beta Cloud", "Gamma Analytics",
                "Delta Security", "Omega Suite"]

    base = np.linspace(120_000, 210_000, 12)
    noise = rng.normal(0, 12_000, 12)
    monthly_sales = np.clip(base + noise, 80_000, None).round(0)

    sales_trend = pd.DataFrame({
        "Month": month_labels,
        "Sales": monthly_sales,
        "Target": (base * 1.05).round(0),
    })

    sales_by_region = pd.DataFrame({
        "Region": regions,
        "Sales": (rng.dirichlet(np.ones(len(regions))) * monthly_sales.sum()).round(0),
    }).sort_values("Sales", ascending=False)

    sales_by_product = pd.DataFrame({
        "Product": products,
        "Sales": (rng.dirichlet(np.ones(len(products))) * monthly_sales.sum()).round(0),
        "Units": rng.integers(120, 900, len(products)),
    }).sort_values("Sales", ascending=False)

    stages = ["Lead", "Qualified", "Proposal", "Negotiation", "Closed Won"]
    deals = pd.DataFrame({
        "Deal": [f"DEAL-{1000+i}" for i in range(40)],
        "Account": rng.choice(
            ["Acme Co", "Globex", "Initech", "Umbrella", "Soylent",
             "Hooli", "Stark Ind", "Wayne Ent", "Wonka", "Cyberdyne"], 40),
        "Stage": rng.choice(stages, 40, p=[0.30, 0.22, 0.20, 0.15, 0.13]),
        "Owner": rng.choice(["Dilnoza", "Sardor", "Madina", "Jasur"], 40),
        "Value": rng.integers(5_000, 120_000, 40),
    })
    active_deals = int((deals["Stage"] != "Closed Won").sum())

    # --------------------------- INVENTORY ---------------------------
    categories = ["Hardware", "Software License", "Accessories", "Spare Parts", "Office"]
    items = []
    for i in range(28):
        cat = rng.choice(categories)
        stock = int(rng.integers(0, 500))
        reorder = int(rng.integers(40, 120))
        price = round(float(rng.uniform(15, 1200)), 2)
        items.append({
            "SKU": f"SKU-{2000+i}",
            "Item": f"{cat} Item {i+1}",
            "Category": cat,
            "Stock": stock,
            "ReorderLevel": reorder,
            "UnitPrice": price,
            "Value": round(stock * price, 2),
        })
    inventory = pd.DataFrame(items)
    inventory["Status"] = np.where(
        inventory["Stock"] == 0, "Out of Stock",
        np.where(inventory["Stock"] < inventory["ReorderLevel"], "Low Stock", "OK"))

    inv_by_cat = (inventory.groupby("Category", as_index=False)["Value"]
                  .sum().sort_values("Value", ascending=False))

    # ---------------------------- FINANCE ----------------------------
    revenue = monthly_sales * rng.uniform(1.15, 1.30, 12)
    expenses = revenue * rng.uniform(0.62, 0.78, 12)
    profit = revenue - expenses
    finance = pd.DataFrame({
        "Month": month_labels,
        "Revenue": revenue.round(0),
        "Expenses": expenses.round(0),
        "Profit": profit.round(0),
    })
    finance["Margin"] = (finance["Profit"] / finance["Revenue"] * 100).round(1)

    expense_breakdown = pd.DataFrame({
        "Category": ["Salaries", "Marketing", "Operations", "R&D", "Other"],
        "Amount": (rng.dirichlet([5, 2, 3, 2, 1]) * expenses.sum()).round(0),
    })

    # ------------------------------- HR ------------------------------
    departments = ["Engineering", "Sales", "Marketing", "Support", "Finance", "HR"]
    headcount = pd.DataFrame({
        "Department": departments,
        "Employees": rng.integers(8, 60, len(departments)),
        "OpenPositions": rng.integers(0, 6, len(departments)),
    })
    total_employees = int(headcount["Employees"].sum())

    attrition = pd.DataFrame({
        "Month": month_labels,
        "Hires": rng.integers(2, 10, 12),
        "Leavers": rng.integers(0, 6, 12),
    })
    attrition["AttritionRate"] = (
        attrition["Leavers"] / total_employees * 100).round(2)
    avg_tenure = round(float(rng.uniform(2.4, 4.6)), 1)

    # ------------------------------ KPI ------------------------------
    kpis = {
        "total_revenue": float(finance["Revenue"].sum()),
        "active_deals": active_deals,
        "inventory_value": float(inventory["Value"].sum()),
        "employee_count": total_employees,
        "net_profit": float(finance["Profit"].sum()),
        "profit_margin": float(finance["Margin"].mean()),
        "low_stock": int((inventory["Status"] != "OK").sum()),
        "open_positions": int(headcount["OpenPositions"].sum()),
        "avg_attrition": float(attrition["AttritionRate"].mean()),
        "avg_tenure": avg_tenure,
        "revenue_growth": float(
            (finance["Revenue"].iloc[-1] / finance["Revenue"].iloc[0] - 1) * 100),
    }

    return {
        "sales_trend": sales_trend,
        "sales_by_region": sales_by_region,
        "sales_by_product": sales_by_product,
        "deals": deals,
        "inventory": inventory,
        "inv_by_cat": inv_by_cat,
        "finance": finance,
        "expense_breakdown": expense_breakdown,
        "headcount": headcount,
        "attrition": attrition,
        "kpis": kpis,
    }
