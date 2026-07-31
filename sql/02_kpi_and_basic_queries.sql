-- =============================================================================
-- SQL File: 02_kpi_and_basic_queries.sql
-- Description: Core business metrics, sales/profit trends, category/regional breakdowns
-- =============================================================================

USE sales_analytics_db;

-- 1. Executive KPIs (Total Sales, Total Profit, Profit Margin %, AOV, Avg Discount)
SELECT 
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS overall_profit_margin_pct,
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_order_value,
    ROUND(AVG(discount) * 100, 2) AS average_discount_pct
FROM sales_transactions;

-- 2. Monthly Sales & Profit Trend
SELECT 
    DATE_FORMAT(order_date, '%Y-%m') AS year_month,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS monthly_sales,
    ROUND(SUM(profit), 2) AS monthly_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY DATE_FORMAT(order_date, '%Y-%m')
ORDER BY year_month ASC;

-- 3. Yearly Sales & Profit Trend (YoY Growth Preparation)
SELECT 
    YEAR(order_date) AS sales_year,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS yearly_sales,
    ROUND(SUM(profit), 2) AS yearly_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY YEAR(order_date)
ORDER BY sales_year ASC;

-- 4. Sales and Profitability by Product Category
SELECT 
    product_category,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100, 2) AS avg_discount_pct
FROM sales_transactions
GROUP BY product_category
ORDER BY total_sales DESC;

-- 5. Sales and Profitability by Sub Category
SELECT 
    product_category,
    sub_category,
    SUM(quantity) AS total_units_sold,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY product_category, sub_category
ORDER BY total_sales DESC;

-- 6. Sales and Profitability by Region
SELECT 
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY region
ORDER BY total_sales DESC;

-- 7. Top 10 States by Sales Revenue
SELECT 
    state,
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales_transactions
GROUP BY state, region
ORDER BY total_sales DESC
LIMIT 10;

-- 8. Top 10 Cities by Sales Revenue
SELECT 
    city,
    state,
    region,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales_transactions
GROUP BY city, state, region
ORDER BY total_sales DESC
LIMIT 10;

-- 9. Orders and Revenue Breakdown by Payment Method
SELECT 
    payment_mode,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND((SUM(sales) / (SELECT SUM(sales) FROM sales_transactions)) * 100, 2) AS sales_share_pct
FROM sales_transactions
GROUP BY payment_mode
ORDER BY total_sales DESC;

-- 10. Discount Level Impact on Profitability
SELECT 
    discount AS discount_rate,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
FROM sales_transactions
GROUP BY discount
ORDER BY discount ASC;
