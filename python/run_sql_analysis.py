import sqlite3
import pandas as pd
import os

def run_sql_demonstration():
    csv_path = os.path.join("dataset", "sales_data.csv")
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found. Run generate_dataset.py first.")
        return
        
    print("==================================================================")
    print("      EXECUTING SQL ANALYTICS ON SALES_TRANSACTIONS TABLE         ")
    print("==================================================================")

    # 1. Load CSV into SQLite in-memory database
    conn = sqlite3.connect(":memory:")
    df = pd.read_csv(csv_path)
    
    # Rename columns to snake_case for standard SQL queries
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    df.to_sql("sales_transactions", conn, index=False, if_exists="replace")
    
    # Enable column formatting in pandas print
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    # Query 1: Core Executive KPIs
    q1 = """
    SELECT 
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS overall_profit_margin_pct,
        COUNT(DISTINCT order_id) AS total_orders,
        COUNT(DISTINCT customer_id) AS total_customers,
        ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS average_order_value,
        ROUND(AVG(discount) * 100, 2) AS average_discount_pct
    FROM sales_transactions;
    """
    print("\n--- 1. EXECUTIVE KPIS SUMMARY ---")
    print(pd.read_sql_query(q1, conn))

    # Query 2: Monthly Sales & Profit Trend (First 6 Months)
    q2 = """
    SELECT 
        strftime('%Y-%m', order_date) AS year_month,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(sales), 2) AS monthly_sales,
        ROUND(SUM(profit), 2) AS monthly_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
    FROM sales_transactions
    GROUP BY strftime('%Y-%m', order_date)
    ORDER BY year_month ASC
    LIMIT 6;
    """
    print("\n--- 2. MONTHLY SALES TREND (SAMPLE REVENUE VELOCITY) ---")
    print(pd.read_sql_query(q2, conn))

    # Query 3: Top 5 Customers by Spend (Using DENSE_RANK Window Function)
    q3 = """
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
    WHERE spend_rank <= 5;
    """
    print("\n--- 3. TOP 5 CUSTOMERS BY SPEND (DENSE_RANK WINDOW FUNCTION) ---")
    print(pd.read_sql_query(q3, conn))

    # Query 4: Category Profitability Breakdown
    q4 = """
    SELECT 
        product_category,
        SUM(quantity) AS total_units_sold,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
    FROM sales_transactions
    GROUP BY product_category
    ORDER BY total_sales DESC;
    """
    print("\n--- 4. CATEGORY PROFITABILITY BREAKDOWN ---")
    print(pd.read_sql_query(q4, conn))

    # Query 5: Discount Level Impact on Profitability
    q5 = """
    SELECT 
        discount AS discount_rate,
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(SUM(profit), 2) AS total_profit,
        ROUND((SUM(profit) / SUM(sales)) * 100, 2) AS profit_margin_pct
    FROM sales_transactions
    GROUP BY discount
    ORDER BY discount ASC;
    """
    print("\n--- 5. DISCOUNT RATE VS PROFIT MARGIN EROSION ---")
    print(pd.read_sql_query(q5, conn))

    # Query 6: Customer RFM Segmentation Analysis
    q6 = """
    WITH CustomerLTV AS (
        SELECT 
            customer_id,
            customer_name,
            COUNT(DISTINCT order_id) AS order_frequency,
            ROUND(SUM(sales), 2) AS monetary_value
        FROM sales_transactions
        GROUP BY customer_id, customer_name
    ),
    CustomerSegments AS (
        SELECT 
            customer_id,
            customer_name,
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
    """
    print("\n--- 6. CUSTOMER SEGMENTATION REVENUE CONTRIBUTION ---")
    print(pd.read_sql_query(q6, conn))

    conn.close()
    print("\n==================================================================")
    print("           SQL DEMONSTRATION EXECUTED SUCCESSFULLY!               ")
    print("==================================================================")

if __name__ == "__main__":
    run_sql_demonstration()
