import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Ensure output directory exists
os.makedirs("images", exist_ok=True)
os.makedirs("results", exist_ok=True)

# Set global Matplotlib aesthetics for modern, clean visual presentation
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8

def run_full_analysis():
    # 1. Load Dataset
    df_path = os.path.join("dataset", "sales_data.csv")
    df = pd.read_csv(df_path)
    print("==================================================")
    print(f"LOADED DATASET: {df.shape[0]} rows, {df.shape[1]} columns")
    print("==================================================")

    # 2. Data Cleaning & Validation
    print("\n--- 1. DATA CLEANING & VALIDATION ---")
    null_counts = df.isnull().sum()
    print("Null values per column:")
    print(null_counts[null_counts > 0] if null_counts.sum() > 0 else "No null values found!")

    duplicates = df.duplicated().sum()
    print(f"Duplicates count: {duplicates}")
    if duplicates > 0:
        df = df.drop_duplicates().reset_index(drop=True)
        print("Duplicates removed.")

    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Ship Date'] = pd.to_datetime(df['Ship Date'])
    df['Year'] = df['Order Date'].dt.year
    df['YearMonth'] = df['Order Date'].dt.to_period('M')

    # 3. Descriptive Statistics
    print("\n--- 2. DESCRIPTIVE STATISTICS ---")
    numeric_cols = ['Quantity', 'Unit Price', 'Discount', 'Sales', 'Profit', 'Shipping Cost']
    desc_stats = df[numeric_cols].describe().T
    desc_stats['skewness'] = df[numeric_cols].skew()
    print(desc_stats[['mean', 'std', 'min', '50%', 'max', 'skewness']])

    # 4. Outlier Detection (IQR Method)
    print("\n--- 3. OUTLIER DETECTION (IQR METHOD) ---")
    for col in ['Sales', 'Profit', 'Shipping Cost']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        print(f"{col}: Q1={Q1:.2f}, Q3={Q3:.2f}, IQR={IQR:.2f} | Outliers count: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")

    # 5. Core KPIs Summary
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    profit_margin = (total_profit / total_sales) * 100
    total_orders = df['Order ID'].nunique()
    total_customers = df['Customer ID'].nunique()
    aov = total_sales / total_orders
    avg_discount = df['Discount'].mean() * 100

    print("\n--- 4. EXECUTIVE SUMMARY KEY METRICS ---")
    print(f"Total Sales:         ${total_sales:,.2f}")
    print(f"Total Profit:        ${total_profit:,.2f}")
    print(f"Overall Margin:      {profit_margin:.2f}%")
    print(f"Total Orders:        {total_orders:,}")
    print(f"Total Customers:     {total_customers:,}")
    print(f"Average Order Value: ${aov:.2f}")
    print(f"Average Discount:    {avg_discount:.2f}%")

    # 6. Customer & Segment Analysis
    print("\n--- 5. CUSTOMER ANALYSIS ---")
    cust_orders = df.groupby('Customer ID').agg(
        Order_Count=('Order ID', 'nunique'),
        Total_Spend=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum')
    )
    repeat_customers = cust_orders[cust_orders['Order_Count'] > 1]
    repeat_rate = (len(repeat_customers) / total_customers) * 100
    print(f"Repeat Customer Rate: {repeat_rate:.2f}% ({len(repeat_customers)} out of {total_customers})")

    # Top 5 Customers by Spend
    top_cust = cust_orders.sort_values(by='Total_Spend', ascending=False).head(5)
    print("Top 5 Customers by Spend:")
    print(top_cust)

    # 7. Category & Sub-Category Performance
    print("\n--- 6. PRODUCT CATEGORY ANALYSIS ---")
    cat_summary = df.groupby('Product Category').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Discount=('Discount', 'mean'),
        Units_Sold=('Quantity', 'sum')
    )
    cat_summary['Profit_Margin_%'] = (cat_summary['Total_Profit'] / cat_summary['Total_Sales']) * 100
    print(cat_summary)

    # 8. Regional Performance
    print("\n--- 7. REGIONAL PERFORMANCE ---")
    reg_summary = df.groupby('Region').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Order_Count=('Order ID', 'nunique')
    )
    reg_summary['Profit_Margin_%'] = (reg_summary['Total_Profit'] / reg_summary['Total_Sales']) * 100
    print(reg_summary)

    # 9. Correlation Analysis
    print("\n--- 8. CORRELATION ANALYSIS ---")
    corr = df[numeric_cols].corr()
    print(corr.round(3))

    # =========================================================
    # VISUALIZATIONS GENERATION (MATPLOTLIB)
    # =========================================================

    # Chart 1: Monthly Sales & Profit Trend
    plt.figure(figsize=(12, 5))
    monthly_trend = df.groupby(df['Order Date'].dt.to_period('M')).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly_trend['Period'] = monthly_trend['Order Date'].astype(str)

    plt.plot(monthly_trend['Period'], monthly_trend['Sales'] / 1000, label='Sales ($K)', color='#1f77b4', linewidth=2.5, marker='o', markersize=4)
    plt.plot(monthly_trend['Period'], monthly_trend['Profit'] / 1000, label='Profit ($K)', color='#2ca02c', linewidth=2.5, marker='s', markersize=4)
    
    plt.title('Monthly Sales & Profit Trend (2023 - 2025)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Year-Month', fontsize=11)
    plt.ylabel('Amount ($ Thousands)', fontsize=11)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(frameon=True, facecolor='#FFFFFF', edgecolor='#DDDDDD')
    plt.tight_layout()
    plt.savefig('images/monthly_sales_trend.png', dpi=300)
    plt.close()

    # Chart 2: Category Sales & Profit Margin Comparison
    plt.figure(figsize=(10, 5))
    sub_summary = df.groupby(['Product Category', 'Sub Category']).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    sub_summary = sub_summary.sort_values(by='Sales', ascending=True)

    y_pos = np.arange(len(sub_summary))
    width = 0.4

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    bars = ax1.barh(y_pos - width/2, sub_summary['Sales'] / 1000, width, label='Sales ($K)', color='#2b5c8f')
    bars2 = ax1.barh(y_pos + width/2, sub_summary['Profit'] / 1000, width, label='Profit ($K)', color='#e05d5d')

    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(sub_summary['Sub Category'])
    ax1.set_xlabel('Amount ($ Thousands)', fontsize=11, fontweight='bold')
    ax1.set_title('Sub-Category Sales vs Profit Performance', fontsize=14, fontweight='bold', pad=15)
    ax1.grid(True, linestyle=':', alpha=0.6, axis='x')
    ax1.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig('images/category_profitability.png', dpi=300)
    plt.close()

    # Chart 3: Regional Sales & Profit Split
    plt.figure(figsize=(9, 5))
    reg_plot = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    x = np.arange(len(reg_plot))
    width = 0.35

    plt.bar(x - width/2, reg_plot['Sales'] / 1000, width, label='Sales ($K)', color='#3498db')
    plt.bar(x + width/2, reg_plot['Profit'] / 1000, width, label='Profit ($K)', color='#2ecc71')

    plt.xlabel('Region', fontsize=11, fontweight='bold')
    plt.ylabel('Amount ($ Thousands)', fontsize=11, fontweight='bold')
    plt.title('Regional Performance Comparison (Sales vs Profit)', fontsize=13, fontweight='bold', pad=15)
    plt.xticks(x, reg_plot['Region'], fontsize=11)
    plt.legend(frameon=True)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig('images/regional_performance.png', dpi=300)
    plt.close()

    # Chart 4: Discount vs Profit Margin Analysis
    plt.figure(figsize=(9, 5))
    disc_summary = df.groupby('Discount').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    disc_summary['Profit Margin %'] = (disc_summary['Profit'] / disc_summary['Sales']) * 100

    colors = ['#27ae60' if m > 10 else '#f39c12' if m > 0 else '#c0392b' for m in disc_summary['Profit Margin %']]
    
    plt.bar(disc_summary['Discount'].astype(str), disc_summary['Profit Margin %'], color=colors, edgecolor='#333333', linewidth=0.5)
    plt.axhline(0, color='black', linewidth=1, linestyle='--')
    plt.xlabel('Discount Rate', fontsize=11, fontweight='bold')
    plt.ylabel('Profit Margin (%)', fontsize=11, fontweight='bold')
    plt.title('Impact of Discount Rate on Profit Margin (%)', fontsize=13, fontweight='bold', pad=15)
    plt.grid(axis='y', linestyle=':', alpha=0.7)
    plt.tight_layout()
    plt.savefig('images/discount_impact_analysis.png', dpi=300)
    plt.close()

    # Chart 5: Customer Spend Tier Segmentation
    plt.figure(figsize=(8, 5))
    cust_spend = df.groupby('Customer ID')['Sales'].sum()
    labels = ['Low Spend (<$2k)', 'Medium Spend ($2k-$5k)', 'High Spend ($5k-$10k)', 'VIP Spend (>$10k)']
    bins = [0, 2000, 5000, 10000, np.inf]
    tiers = pd.cut(cust_spend, bins=bins, labels=labels)
    tier_counts = tiers.value_counts().reindex(labels)

    plt.pie(tier_counts, labels=tier_counts.index, autopct='%1.1f%%', startangle=140, colors=['#95a5a6', '#3498db', '#9b59b6', '#f1c40f'], explode=[0, 0, 0.05, 0.1])
    plt.title('Customer Tier Breakdown by Lifetime Value (LTV)', fontsize=13, fontweight='bold')
    plt.tight_layout()
    plt.savefig('images/customer_segmentation.png', dpi=300)
    plt.close()

    print("\nVisualizations successfully generated and saved to 'images/' folder!")

if __name__ == "__main__":
    run_full_analysis()
