# Power BI Interactive Dashboard Design & Layout Guide

This guide details the layout, visual hierarchy, filtering mechanisms, and interaction design for the 6-page interactive Power BI report suite.

---

## 🎨 Color Palette & Design System
- **Primary Theme**: Slate Dark / Modern Corporate Clean
- **Primary Blue**: `#2B5C8F` (Revenue, Quantity)
- **Success Green**: `#27AE60` (Profit, High Margins)
- **Warning Amber**: `#F39C12` (Moderate Margins, Medium Priority)
- **Danger Red**: `#E74C3C` (Losses, High Discount Penalties)
- **Neutral Dark**: `#1E293B` (Backgrounds, Headers)
- **Neutral Light**: `#F8FAFC` (Card backgrounds)

---

## 📌 Global Slicers & Header Navigation Bar
Positioned across the top header of **all 6 pages**:
- **Year Slicer**: Multi-select dropdown (2023, 2024, 2025)
- **Region Slicer**: Buttons / Dropdown (West, East, Central, South)
- **Category Slicer**: Buttons (Technology, Furniture, Office Supplies)
- **Payment Mode Slicer**: Dropdown (Credit Card, Debit Card, PayPal, UPI, Net Banking)
- **Customer Search Bar**: Text / Dropdown search by Customer Name

---

## 📄 Dashboard Pages Breakdown

### Page 1: Executive Dashboard (C-Suite Summary)
**Objective**: High-level overview of enterprise health, revenue, margin %, and strategic targets.
- **KPI Cards (Top Banner)**:
  - `Total Sales`: `$13.36M`
  - `Total Profit`: `$1.44M`
  - `Profit Margin %`: `10.76%`
  - `Total Orders`: `10,000`
  - `Average Order Value (AOV)`: `$1,336.16`
- **Visual 1 (Line & Stacked Column)**: Monthly Sales & YoY Growth Trend (X-axis: Month, Column: Total Sales, Line: YoY Growth %).
- **Visual 2 (Donut Chart)**: Revenue Contribution by Product Category.
- **Visual 3 (Filled Map)**: Regional Sales & Margin Heatmap by US State.
- **Visual 4 (Table Visual)**: Top 5 Regions and States by Profitability.

---

### Page 2: Sales Dashboard (Revenue & Seasonality)
**Objective**: Deep-dive into revenue channels, order volume, seasonality, and transaction metrics.
- **KPI Cards**: Total Sales, Total Units Sold (`27,686`), Average Units per Order (`2.77`), AOV.
- **Visual 1 (Ribbon Chart)**: Sub-Category Sales Rank Changes across 2023, 2024, and 2025.
- **Visual 2 (Clustered Bar Chart)**: Order Volume & Revenue by Payment Method (Credit Card leads at 45%).
- **Visual 3 (Line Chart)**: Daily / Weekly Sales Velocity with Trendline & 3-Month Moving Average.
- **Visual 4 (Tree Map)**: Order Priority vs Revenue Distribution (Critical, High, Medium, Low).

---

### Page 3: Profit Dashboard (Margins & Discount Toxicity)
**Objective**: Analyze profit drivers, discount margin erosion, loss-leader sub-categories, and cost penalties.
- **KPI Cards**: Total Profit, Overall Margin %, Total Shipping Overhead (`$744.18K`), High-Discount Loss (`$182.4K`).
- **Visual 1 (Waterfall Chart)**: Gross Sales -> Discount Losses -> Shipping Costs -> Net Profit.
- **Visual 2 (Scatter Plot)**: Discount Rate % vs Profit Margin % per Transaction (Highlighting red zone >30% discount).
- **Visual 3 (Clustered Horizontal Bar Chart)**: Sub-Category Profitability Breakdown (Highlighting Furniture Tables/Bookcases margin drag).
- **Visual 4 (Decomposition Tree)**: Profit Drill-down by Region -> Category -> Sub-Category -> Product Name.

---

### Page 4: Customer Dashboard (Segmentation & LTV)
**Objective**: Customer lifetime value, RFM segmentation, repeat purchase velocity, and top spenders.
- **KPI Cards**: Total Unique Customers (`1,199`), Repeat Customer Rate (`99.83%`), Avg Spend per Customer (`$11,143.94`).
- **Visual 1 (Pie / Donut Chart)**: Customer Tier Breakdown (VIP >$10k, Tier 2, Tier 3, Tier 4).
- **Visual 2 (Stacked Bar Chart)**: Age & Gender Distribution vs Average Lifetime Spend.
- **Visual 3 (Matrix Visual with Heatmap formatting)**: Top 10 Customers by Revenue with Order Frequency, Total Spend, Total Profit, and Customer Rank.
- **Visual 4 (Scatter Chart)**: Recency vs Lifetime Value (LTV).

---

### Page 5: Regional Dashboard (Geographic Inefficiencies)
**Objective**: Regional expansion drivers, state-level margin disparities, and logistics costs.
- **KPI Cards**: West Region Revenue (`$3.28M`), Central Revenue (`$3.72M`), East Revenue (`$3.10M`), South Revenue (`$3.26M`).
- **Visual 1 (Shape Map / Choropleth)**: State-level Profit Margin % Heatmap.
- **Visual 2 (Stacked Column Chart)**: Sales vs Shipping Cost by Region.
- **Visual 3 (Matrix Visual)**: Drill-through table for Region -> State -> City with Sales, Profit, Margin %, and Shipping Cost.
- **Visual 4 (Bar Chart)**: Top 10 Cities by Net Profitability.

---

### Page 6: Product Dashboard (Product Portfolio Pareto)
**Objective**: Product line optimization, inventory velocity, top earners, and bottom loss leaders.
- **KPI Cards**: Total Active Products (`21`), Top Product Sales (`Apple MacBook Pro 16`), Margin Leader (`Office Supplies - Art 27.8%`).
- **Visual 1 (Pareto Chart / Line & Stacked Column)**: Product Sales Cumulative % (80/20 Rule Analysis).
- **Visual 2 (Clustered Bar Chart)**: Top 10 Most Profitable Products vs Bottom 5 Loss Leaders.
- **Visual 3 (Scatter Plot)**: Unit Price vs Units Sold (Price Elasticity Curve).
- **Visual 4 (Table Visual with Data Bars)**: Sub-Category Drill-down with Units Sold, Total Revenue, Total Profit, and Average Discount.

---

## 🔄 Interaction & Filtering Logic
1. **Cross-Filtering**: Clicking any Category bar filters all trend lines, customer segments, and geographic maps on that page.
2. **Drill-Through Action**: Right-clicking any State on the Regional Dashboard opens a detailed drill-through page for city-level customer orders.
3. **Tooltip Pages**: Hovering over any Sub-Category shows a micro-chart displaying top 3 products and margin percentage.
