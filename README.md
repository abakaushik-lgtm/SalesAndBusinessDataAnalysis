# 📊 Sales & Business Data Analysis - End-to-End Enterprise Analytics Project

[![SQL](https://img.shields.io/badge/SQL-MySQL_8.0-blue.svg)](https://www.mysql.com/)
[![Python](https://img.shields.io/badge/Python-3.11-green.svg)](https://www.python.org/)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-yellow.svg)](https://powerbi.microsoft.com/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 📌 Executive Summary & Business Problem Statement
**Global Retail Corp** is a multi-region retail enterprise experiencing revenue growth alongside margin contraction in specific product categories and regional territories. Despite generating **$13.36M in gross sales** over a 3-year period (2023–2025), executive leadership lacked visibility into discount toxicity thresholds, regional logistics cost drains, and customer lifetime value segmentation.

This project delivers a **Senior Data Analyst portfolio-grade solution** by building an end-to-end data pipeline, SQL database architecture, Python exploratory data analysis (EDA), and an interactive **6-page Power BI dashboard suite**.

---

## 🚀 Key Project Accomplishments
- **Processed 10,000 Order Transactions**: Cleaned, structured, and validated transactional data across 21 cities and 3 product categories.
- **Identified $180,000+ Margin Recovery Opportunity**: Discovered that promotional discounts ≥30% turn profit margins negative (-8.2%) and recommended a 20% discount cap.
- **Engineered Advanced SQL Pipeline**: Created production queries and views utilizing CTEs, `RANK()`, `DENSE_RANK()`, `SUM() OVER()`, `LAG() OVER()`, and customer RFM logic.
- **Designed 6 Interactive Power BI Pages**: Integrated DAX measures for YoY growth, running totals, customer LTV tiers, and interactive cross-filtering.

---

## 📁 Repository Structure

```
c:/Users/garvi/Documents/Data Science Projects/Sales and Business Data Analysis/
├── dataset/
│   └── sales_data.csv                      # Synthetic dataset with 10,000 realistic records
├── sql/
│   ├── 01_schema_and_import.sql            # MySQL Table schema, DDL, indexes, and import scripts
│   ├── 02_kpi_and_basic_queries.sql        # Core aggregation queries, monthly/yearly trends, payment split
│   ├── 03_business_queries_and_window_fx.sql # Advanced SQL: CTEs, Window functions (RANK, DENSE_RANK, LAG, SUM OVER)
│   └── 04_views_and_reports.sql            # Reusable Views for Power BI & Executive reporting
├── python/
│   ├── generate_dataset.py                 # Reproducible Python script to generate the 10,000 record dataset
│   └── sales_eda_analysis.py               # Data cleaning, IQR outlier detection, descriptive stats, and plot exporting
├── power_bi/
│   ├── DAX_Measures.md                     # Comprehensive repository of DAX measures
│   └── Dashboard_Design_Guide.md           # Page-by-page layout visual specs, slicers, and color themes
├── images/
│   ├── monthly_sales_trend.png             # Monthly Sales vs Profit trend line chart
│   ├── category_profitability.png          # Sub-Category revenue vs profit margin bar chart
│   ├── regional_performance.png            # Regional performance comparison chart
│   ├── discount_impact_analysis.png        # Discount rate vs profit margin bar chart
│   └── customer_segmentation.png           # Customer LTV tier pie chart
├── results/
│   ├── business_insights.md                # 20+ Data-driven business insights
│   ├── recommendations.md                  # 15 Strategic recommendations for business growth
│   ├── resume_bullet_points.md             # 4 ATS-friendly resume bullet points with metrics
│   └── interview_questions_and_answers.md  # 25 Data Analyst interview Q&As based on this project
└── README.md                               # Project documentation
```

---

## 🛠️ Technology Stack & Analytical Methods
| Component | Tool / Library | Key Focus & Techniques |
| :--- | :--- | :--- |
| **Database & SQL** | MySQL 8.0 | Schema Design, Indexing, CTEs, Window Functions (`RANK`, `DENSE_RANK`, `LAG`, `SUM OVER`), Views |
| **Data Science / EDA** | Python (Pandas, NumPy) | Data Hygiene, Type Casting, IQR Outlier Detection, Correlation Matrix, GroupBy Aggregations |
| **Data Visualization** | Matplotlib | High-resolution chart exporting (300 DPI), Trend lines, Sub-category bar charts |
| **Business Intelligence**| Power BI Desktop | DAX Time Intelligence (`TOTALYTD`, `SAMEPERIODLASTYEAR`), Star Schema Modeling, Interactive Slicers |
| **Spreadsheets** | Microsoft Excel | Pivot Tables, Conditional Formatting, KPI summaries |

---

## 📈 Visualizations & Data Analysis Highlights

### 1. Monthly Sales & Profit Trend (2023 - 2025)
Sales demonstrate strong seasonal spikes in Q4 (November–December) driven by corporate holiday procurement.

![Monthly Sales Trend](images/monthly_sales_trend.png)

---

### 2. Discount Rate Impact on Profit Margin (%)
Analysis reveals that profit margins drop into negative territory when discount rates reach **30% or higher**.

![Discount Impact Analysis](images/discount_impact_analysis.png)

---

### 3. Category & Sub-Category Profitability Comparison
While **Technology** leads total volume, **Furniture (Tables & Bookcases)** suffers from severe profit compression (2.53% overall margin) due to shipping overhead and discounting.

![Category Profitability](images/category_profitability.png)

---

### 4. Regional Sales & Profit Distribution
The **Central Region** is the leading revenue ($3.72M) and profit ($413K) generator, followed closely by the West, South, and East regions.

![Regional Performance](images/regional_performance.png)

---

### 5. Customer Lifetime Value (LTV) Segmentation
The customer base is categorized into 4 spend tiers, with **VIP Buyers (LTV > $10,000)** contributing over **34.2%** of total revenue.

![Customer Segmentation](images/customer_segmentation.png)

---

## 📊 Core Business Insights Summary

1. **Enterprise Revenue & Profit**: Total Revenue reached **$13,361,589.81** with a Net Profit of **$1,437,443.18** (Overall Profit Margin of **10.76%**).
2. **Technology Dominance**: Technology products generate **71.25% of total sales** ($9.52M) and **90.19% of net profit** ($1.30M).
3. **Furniture Margin Erosion**: Furniture generates **$3.67M** in sales but only **$92.95K in profit** (Margin: **2.53%**), acting as an operational drag.
4. **Office Supplies Margin Leader**: Office Supplies delivers the highest profit margin percentage at **27.81%**.
5. **Discount Toxicity Threshold**: Discounts ≥30% pull profit margins down to **-8.2%**, resulting in net negative orders.
6. **High Customer Retention**: Repeat customer rate stands at **99.83%** across 1,199 unique buyers.

*For all 20 detailed insights, see [results/business_insights.md](file:///c:/Users/garvi/Documents/Data%20Science%20Projects/Sales%20and%20Business%20Data%20Analysis/results/business_insights.md).*

---

## 💡 Top Strategic Recommendations

1. **Enforce 20% Hard Discount Cap**: Eliminate discounts >30% to prevent negative-margin orders, salvaging an estimated **$180,000+ annually**.
2. **Restructure Furniture Freight Fees**: Shift bulky item shipping costs to distance-and-weight surcharges to recover **$120,000+** in shipping subsidies.
3. **Cross-Sell High-Margin Office Supplies**: Create automated checkout bundles pairing high-margin items (Art, Cardstock) with high-ticket Laptops/Phones.
4. **VIP Loyalty & Retention Program**: Establish dedicated account management for top VIP clients (LTV > $10k), who generate 34.2% of total revenue.
5. **Regional Fulfillment Hub Expansion**: Expand warehouse stocking in the **Central ($3.72M)** and **West ($3.28M)** regions prior to Q4 peak.

*For all 15 actionable recommendations, see [results/recommendations.md](file:///c:/Users/garvi/Documents/Data%20Science%20Projects/Sales%20and%20Business%20Data%20Analysis/results/recommendations.md).*

---

## 🚀 How to Run This Project Locally

### Prerequisites
- Python 3.8+
- MySQL Server 8.0+ / MySQL Workbench
- Power BI Desktop (Optional, for .pbix visualization)

### Step 1: Clone the Repository & Generate Dataset
```bash
git clone https://github.com/your-username/sales-business-data-analysis.git
cd sales-business-data-analysis

# Generate synthetic dataset (10,000 records)
python python/generate_dataset.py
```

### Step 2: Execute Python EDA & Generate Visualizations
```bash
python python/sales_eda_analysis.py
```

### Step 3: Run Database Scripts in MySQL
1. Open MySQL Workbench.
2. Execute `sql/01_schema_and_import.sql` to create the schema and load `dataset/sales_data.csv`.
3. Run `sql/02_kpi_and_basic_queries.sql`, `sql/03_business_queries_and_window_fx.sql`, and `sql/04_views_and_reports.sql`.

---

## 🔮 Future Improvements
- **Automated Airflow Pipeline**: Schedule daily incremental ingestion of sales data into Snowflake or AWS Redshift.
- **Predictive Demand Forecasting**: Build a SARIMAX or Prophet time series model in Python to forecast Q4 inventory requirements.
- **Customer Churn Machine Learning**: Implement a Random Forest classifier to predict customer churn probability based on purchase recency and frequency.
