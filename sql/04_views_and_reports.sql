-- =============================================================================
-- SQL File: 04_views_and_reports.sql
-- Description: Production-ready Database Views for Power BI Reporting & Executive Dashboards
-- =============================================================================

USE sales_analytics_db;

-- 1. Executive Summary KPIs View
CREATE OR REPLACE VIEW vw_executive_kpis AS
SELECT 
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_percentage,
    COUNT(DISTINCT order_id) AS total_order_volume,
    COUNT(DISTINCT customer_id) AS active_customer_base,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    ROUND(AVG(discount) * 100, 2) AS average_discount_rate
FROM sales_transactions;

-- 2. Monthly Performance Trend View
CREATE OR REPLACE VIEW vw_monthly_sales_trend AS
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS year_month,
    YEAR(order_date) AS order_year,
    MONTH(order_date) AS order_month,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(sales), 2) AS gross_sales,
    ROUND(SUM(profit), 2) AS net_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS margin_percentage
FROM sales_transactions
GROUP BY DATE_FORMAT(order_date, '%Y-%m'), YEAR(order_date), MONTH(order_date);

-- 3. Product Category & Sub-Category Performance View
CREATE OR REPLACE VIEW vw_category_profitability AS
SELECT 
    product_category,
    sub_category,
    COUNT(DISTINCT order_id) AS total_orders,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM sales_transactions
GROUP BY product_category, sub_category;

-- 4. Regional & Geographic Sales View
CREATE OR REPLACE VIEW vw_regional_performance AS
SELECT 
    region,
    state,
    city,
    COUNT(DISTINCT customer_id) AS customer_count,
    COUNT(DISTINCT order_id) AS order_count,
    ROUND(SUM(sales), 2) AS regional_sales,
    ROUND(SUM(profit), 2) AS regional_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS margin_pct
FROM sales_transactions
GROUP BY region, state, city;

-- 5. Customer RFM & LTV Summary View
CREATE OR REPLACE VIEW vw_customer_summary AS
SELECT 
    customer_id,
    customer_name,
    gender,
    age,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS lifetime_spend,
    ROUND(SUM(profit), 2) AS lifetime_profit_generated,
    MIN(order_date) AS first_purchase_date,
    MAX(order_date) AS latest_purchase_date,
    CASE 
        WHEN SUM(sales) >= 10000 THEN 'VIP / High Value'
        WHEN SUM(sales) BETWEEN 5000 AND 9999.99 THEN 'Tier 2 / Mid-High'
        WHEN SUM(sales) BETWEEN 2000 AND 4999.99 THEN 'Tier 3 / Moderate'
        ELSE 'Tier 4 / Low'
    END AS customer_tier
FROM sales_transactions
GROUP BY customer_id, customer_name, gender, age;
