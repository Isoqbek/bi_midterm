"""
Specialized agent'lar. Har biri:
  - keywords: qaysi savollarga javob berishini aniqlaydi (EN + UZ)
  - context(data): LLM uchun ma'lumot konteksti (matn)
  - handle(query, data): LLM bo'lmaganda ishlatiladigan qoidaga asoslangan javob
"""


class BaseAgent:
    name = "Base"
    icon = "🤖"
    keywords: list[str] = []

    def matches(self, query: str) -> int:
        q = query.lower()
        return sum(1 for k in self.keywords if k in q)

    def context(self, data) -> str:
        return ""

    def handle(self, query: str, data) -> str:
        return ""


class SalesAgent(BaseAgent):
    name = "Sales Agent"
    icon = "📈"
    keywords = ["sales", "revenue", "deal", "pipeline", "region", "product",
                "sell", "sotuv", "savdo", "daromad", "bitim", "mahsulot",
                "hudud", "region", "target", "reja"]

    def context(self, data) -> str:
        k = data["kpis"]
        top_region = data["sales_by_region"].iloc[0]
        top_product = data["sales_by_product"].iloc[0]
        return (
            f"SALES DATA:\n"
            f"- 12 oylik jami sotuv: ${data['sales_trend']['Sales'].sum():,.0f}\n"
            f"- Faol bitimlar (active deals): {k['active_deals']}\n"
            f"- Eng kuchli hudud: {top_region['Region']} (${top_region['Sales']:,.0f})\n"
            f"- Eng ko'p sotilgan mahsulot: {top_product['Product']} (${top_product['Sales']:,.0f})\n"
            f"- Pipeline bosqichlari taqsimoti: "
            f"{data['deals']['Stage'].value_counts().to_dict()}\n"
        )

    def handle(self, query: str, data) -> str:
        k = data["kpis"]
        tr = data["sales_by_region"].iloc[0]
        tp = data["sales_by_product"].iloc[0]
        return (
            f"**{self.icon} {self.name}**\n\n"
            f"- 12 oylik jami sotuv: **${data['sales_trend']['Sales'].sum():,.0f}**\n"
            f"- Faol bitimlar: **{k['active_deals']}**\n"
            f"- Yetakchi hudud: **{tr['Region']}** (${tr['Sales']:,.0f})\n"
            f"- Top mahsulot: **{tp['Product']}** (${tp['Sales']:,.0f})\n"
            f"- O'sish (1-oydan oxirgi oygacha): **{k['revenue_growth']:.1f}%**"
        )


class InventoryAgent(BaseAgent):
    name = "Inventory Agent"
    icon = "📦"
    keywords = ["inventory", "stock", "warehouse", "item", "sku", "reorder",
                "supply", "ombor", "zaxira", "tovar", "qoldiq", "mahsulot soni"]

    def context(self, data) -> str:
        k = data["kpis"]
        low = data["inventory"][data["inventory"]["Status"] != "OK"]
        return (
            f"INVENTORY DATA:\n"
            f"- Ombor umumiy qiymati: ${k['inventory_value']:,.0f}\n"
            f"- Jami SKU'lar: {len(data['inventory'])}\n"
            f"- Kam qolgan / tugagan tovarlar: {k['low_stock']}\n"
            f"- Eng qimmat kategoriya: {data['inv_by_cat'].iloc[0]['Category']}\n"
            f"- Diqqat talab tovarlar: {low['Item'].head(5).tolist()}\n"
        )

    def handle(self, query: str, data) -> str:
        k = data["kpis"]
        cat = data["inv_by_cat"].iloc[0]
        return (
            f"**{self.icon} {self.name}**\n\n"
            f"- Ombor qiymati: **${k['inventory_value']:,.0f}**\n"
            f"- Jami SKU: **{len(data['inventory'])}**\n"
            f"- Kam/tugagan zaxira: **{k['low_stock']}** ta tovar e'tibor talab qiladi\n"
            f"- Eng qimmat kategoriya: **{cat['Category']}** (${cat['Value']:,.0f})"
        )


class FinanceAgent(BaseAgent):
    name = "Finance Agent"
    icon = "💰"
    keywords = ["finance", "profit", "expense", "cost", "margin", "cash",
                "budget", "moliya", "foyda", "xarajat", "byudjet", "marja",
                "daromad", "balans"]

    def context(self, data) -> str:
        k = data["kpis"]
        top_exp = data["expense_breakdown"].sort_values("Amount", ascending=False).iloc[0]
        return (
            f"FINANCE DATA:\n"
            f"- Jami daromad (12 oy): ${k['total_revenue']:,.0f}\n"
            f"- Sof foyda: ${k['net_profit']:,.0f}\n"
            f"- O'rtacha foyda marjasi: {k['profit_margin']:.1f}%\n"
            f"- Eng katta xarajat: {top_exp['Category']} (${top_exp['Amount']:,.0f})\n"
        )

    def handle(self, query: str, data) -> str:
        k = data["kpis"]
        e = data["expense_breakdown"].sort_values("Amount", ascending=False).iloc[0]
        return (
            f"**{self.icon} {self.name}**\n\n"
            f"- Jami daromad: **${k['total_revenue']:,.0f}**\n"
            f"- Sof foyda: **${k['net_profit']:,.0f}**\n"
            f"- O'rtacha marja: **{k['profit_margin']:.1f}%**\n"
            f"- Eng katta xarajat moddasi: **{e['Category']}** (${e['Amount']:,.0f})"
        )


class HRAgent(BaseAgent):
    name = "HR Agent"
    icon = "👥"
    keywords = ["hr", "employee", "headcount", "attrition", "hiring", "staff",
                "team", "tenure", "xodim", "hodim", "ishchi", "jamoa",
                "ishga olish", "ketish", "kadr"]

    def context(self, data) -> str:
        k = data["kpis"]
        top_dept = data["headcount"].sort_values("Employees", ascending=False).iloc[0]
        return (
            f"HR DATA:\n"
            f"- Jami xodimlar: {k['employee_count']}\n"
            f"- O'rtacha attrition (ketish): {k['avg_attrition']:.2f}%\n"
            f"- Ochiq vakansiyalar: {k['open_positions']}\n"
            f"- O'rtacha ish staji: {k['avg_tenure']} yil\n"
            f"- Eng katta bo'lim: {top_dept['Department']} ({top_dept['Employees']} kishi)\n"
        )

    def handle(self, query: str, data) -> str:
        k = data["kpis"]
        d = data["headcount"].sort_values("Employees", ascending=False).iloc[0]
        return (
            f"**{self.icon} {self.name}**\n\n"
            f"- Jami xodimlar: **{k['employee_count']}**\n"
            f"- O'rtacha attrition: **{k['avg_attrition']:.2f}%**\n"
            f"- Ochiq vakansiyalar: **{k['open_positions']}**\n"
            f"- Eng katta bo'lim: **{d['Department']}** ({d['Employees']} kishi)"
        )


ALL_AGENTS = [SalesAgent(), InventoryAgent(), FinanceAgent(), HRAgent()]
