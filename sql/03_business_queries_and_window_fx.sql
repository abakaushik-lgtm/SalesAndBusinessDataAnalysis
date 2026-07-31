-- =============================================================================
-- SQL File: 03_business_queries_and_window_fx.sql
-- Description: Advanced SQL featuring CTEs, Window Functions (RANK, DENSE_RANK, SUM OVER, LAG OVER), 
--              Customer Segmentation, Repeat/New customer logic, and Loss Leader Analysis.
-- =============================================================================

USE sales_analytics_db;

-- 1. Top 10 Customers by Total Spend (using DENSE_RANK Window Function)
WITH CustomerSpend AS (
    SELECT 
        customer_id,
        customer_name,
        gender,
        ROUND(SUM(sales), 2) AS total_spend,
        ROUND(SUM(profit), 2) AS total_profit,
        COUNT(DISTINCT order_id) AS total_orders,
        DENSE_RANK() OVER (ORDER BY SUM(sales) DESC) AS spend_rank
    FROM sales_transactions
    GROUP BY customer_id, customer_name, gender
)
SELECT spend_rank, customer_id, customer_name, gender, total_orders, total_spend, total_profit
FROM CustomerSpend
WHERE spend_rank <= 10;

-- 2. Dense Rank Customers by Total Profitability
WITH CustomerProfitability AS (
    SELECT 
        customer_id,
        customer_name,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        DENSE_RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
    FROM sales_transactions
    GROUP BY customer_id, customer_name
)
SELECT profit_rank, customer_id, customer_name, total_sales, total_profit
FROM CustomerProfitability
WHERE profit_rank <= 10;

-- 3. Top 10 Most Profitable Products (using RANK Window Function)
WITH ProductPerformance AS (
    SELECT 
        product_id,
        product_name,
        product_category,
        sub_category,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        RANK() OVER (ORDER BY SUM(profit) DESC) AS profit_rank
    FROM sales_transactions
    GROUP BY product_id, product_name, product_category, sub_category
)
SELECT profit_rank, product_id, product_name, product_category, sub_category, total_sales, total_profit
FROM ProductPerformance
WHERE profit_rank <= 10;

-- 4. Bottom 10 Least Profitable Products (Loss Leaders / Margin Drag)
WITH ProductLossLeaders AS (
    SELECT 
        product_id,
        product_name,
        product_category,
        sub_category,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        RANK() OVER (ORDER BY SUM(profit) ASC) AS worst_profit_rank
    FROM sales_transactions
    GROUP BY product_id, product_name, product_category, sub_category
)
SELECT worst_profit_rank, product_id, product_name, product_category, sub_category, total_sales, total_profit
FROM ProductLossLeaders
WHERE worst_profit_rank <= 10;

-- 5. Cumulative / Running Total Sales & Profit Over Time (Window Function)
WITH DailyAggregates AS (
    SELECT 
        order_date,
        ROUND(SUM(sales), 2) AS daily_sales,
        ROUND(SUM(profit), 2) AS daily_profit
    FROM sales_transactions
    GROUP BY order_date
)
SELECT 
    order_date,
    daily_sales,
    SUM(daily_sales) OVER (ORDER BY order_date ASC) AS running_total_sales,
    daily_profit,
    SUM(daily_profit) OVER (ORDER BY order_date ASC) AS running_total_profit
FROM DailyAggregates;

-- 6. Month-over-Month (MoM) Sales Growth using LAG() Window Function
WITH MonthlySales AS (
    SELECT 
        DATE_FORMAT(order_date, '%Y-%m') AS year_month,
        ROUND(SUM(sales), 2) AS current_month_sales
    FROM sales_transactions
    GROUP BY DATE_FORMAT(order_date, '%Y-%m')
)
SELECT 
    year_month,
    current_month_sales,
    LAG(current_month_sales, 1) OVER (ORDER BY year_month ASC) AS previous_month_sales,
    ROUND(
        ((current_month_sales - LAG(current_month_sales, 1) OVER (ORDER BY year_month ASC)) 
        / LAG(current_month_sales, 1) OVER (ORDER BY year_month ASC)) * 100, 2
    ) AS mom_growth_pct
FROM MonthlySales;

-- 7. Customer Segmentation Analysis (RFM / Lifetime Value Tiers)
WITH CustomerLTV AS (
    SELECT 
        customer_id,
        customer_name,
        COUNT(DISTINCT order_id) AS order_frequency,
        ROUND(SUM(sales), 2) AS monetary_value,
        MAX(order_date) AS last_order_date
    FROM sales_transactions
    GROUP BY customer_id, customer_name
),
CustomerSegments AS (
    SELECT 
        customer_id,
        customer_name,
        order_frequency,
        monetary_value,
        CASE 
            WHEN monetary_value >= 10000 THEN 'VIP / High Value'
            WHEN monetary_value BETWEEN 5000 AND 9999.99 THEN 'Tier 2 / Mid-High Value'
            WHEN monetary_value BETWEEN 2000 AND 4999.99 THEN 'Tier 3 / Moderate Value'
            ELSE 'Tier 4 / Low Value'
        END AS customer_segment
    FROM CustomerLTV
)
SELECT 
    customer_segment,
    COUNT(customer_id) AS customer_count,
    ROUND(AVG(monetary_value), 2) AS avg_segment_spend,
    ROUND(SUM(monetary_value), 2) AS total_segment_revenue,
    ROUND((SUM(monetary_value) / (SELECT SUM(sales) FROM sales_transactions)) * 100, 2) AS revenue_contribution_pct
FROM CustomerSegments
GROUP BY customer_segment
ORDER BY total_segment_revenue DESC;

-- 8. Repeat vs New Customer Analysis
WITH FirstCustomerOrder AS (
    SELECT 
        customer_id,
        MIN(order_date) AS first_order_date
    FROM sales_transactions
    GROUP BY customer_id
),
TransactionClassification AS (
    SELECT 
        st.order_id,
        st.customer_id,
        st.order_date,
        st.sales,
        CASE 
            WHEN st.order_date = fco.first_order_date THEN 'New Customer Order'
            ELSE 'Repeat Customer Order'
        END AS order_type
    FROM sales_transactions st
    JOIN FirstCustomerOrder fco ON st.customer_id = fco.customer_id
)
SELECT 
    order_type,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND((SUM(sales) / (SELECT SUM(sales) FROM sales_transactions)) * 100, 2) AS sales_pct
FROM TransactionClassification
GROUP BY order_type;
