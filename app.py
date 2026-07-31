import os
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(
    page_title="Executive Business Intelligence Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Compact & Premium KPI Cards
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 8px;
        padding: 10px 14px;
        border-left: 4px solid #3B82F6;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
        margin-bottom: 10px;
    }
    .metric-title {
        color: #94A3B8;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 1.85rem;
        font-weight: 800;
        line-height: 1.2;
        margin-top: 2px;
    }
    .metric-sub {
        font-size: 0.75rem;
        font-weight: 500;
        margin-top: 2px;
    }
    .footer-text {
        text-align: center;
        color: #64748B;
        font-size: 0.85rem;
        padding: 20px 0;
        border-top: 1px solid #334155;
        margin-top: 30px;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    csv_path = os.path.join("dataset", "sales_data.csv")
    df = pd.read_csv(csv_path)
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.strftime('%Y-%m')
    return df

df_raw = load_data()

# ---------------------------------------------------------
# Sidebar Slicers & Filters
# ---------------------------------------------------------
st.sidebar.title("⚙️ Dashboard Controls")
st.sidebar.markdown("Filter enterprise sales metrics:")

years = ["All"] + sorted(list(df_raw['Year'].unique()))
selected_year = st.sidebar.selectbox("Select Year", years, index=0)

regions = ["All"] + sorted(list(df_raw['Region'].unique()))
selected_region = st.sidebar.selectbox("Select Region", regions, index=0)

categories = ["All"] + sorted(list(df_raw['Product Category'].unique()))
selected_category = st.sidebar.selectbox("Select Category", categories, index=0)

payments = ["All"] + sorted(list(df_raw['Payment Mode'].unique()))
selected_payment = st.sidebar.selectbox("Select Payment Mode", payments, index=0)

# Filter Dataframe
df = df_raw.copy()
if selected_year != "All":
    df = df[df['Year'] == selected_year]
if selected_region != "All":
    df = df[df['Region'] == selected_region]
if selected_category != "All":
    df = df[df['Product Category'] == selected_category]
if selected_payment != "All":
    df = df[df['Payment Mode'] == selected_payment]

# ---------------------------------------------------------
# Title & Subtitle Branding
# ---------------------------------------------------------
st.title("📊 Global Retail Sales Analytics")
st.markdown("### Executive Business Intelligence Dashboard | Retail Sales Performance (2023–2025)")

# Informative Banner for Negative Profit scenario if triggered by heavy filtering
total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
margin_pct = (total_profit / total_sales * 100) if total_sales > 0 else 0

if total_profit < 0:
    st.warning(f"⚠️ **Filter Scenario Alert**: The selected filter combination currently results in a net loss (${total_profit:,.2f}, Margin: {margin_pct:.2f}%). This reflects discount erosion (>20% discount rates) and elevated freight overhead in specific segments.")

# ---------------------------------------------------------
# Expanded Recruiters KPI Cards Grid (Consistent Semantic Colors)
# ---------------------------------------------------------
total_orders = df['Order ID'].nunique()
total_customers = df['Customer ID'].nunique()
total_products = df['Product ID'].nunique()
avg_quantity = df['Quantity'].mean()

# Repeat Customer Retention Rate calculation
cust_counts = df.groupby('Customer ID')['Order ID'].nunique()
repeat_cust = (cust_counts > 1).sum()
retention_rate = (repeat_cust / total_customers * 100) if total_customers > 0 else 0

# Format Values for Scanning
sales_str = f"${total_sales/1e6:.2f}M" if total_sales >= 1e6 else f"${total_sales/1e3:.1f}K"
profit_str = f"${total_profit/1e6:.2f}M" if total_profit >= 1e6 else f"${total_profit/1e3:.1f}K" if total_profit >= 0 else f"-${abs(total_profit)/1e3:.1f}K"

profit_color = "#10B981" if total_profit >= 0 else "#EF4444" # Green if positive, Red if negative
margin_color = "#10B981" if margin_pct >= 10 else "#F59E0B" if margin_pct >= 0 else "#EF4444"

# Row 1 KPIs
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #3B82F6;">
        <div class="metric-title">Total Revenue</div>
        <div class="metric-value" style="color: #3B82F6;">{sales_str}</div>
        <div class="metric-sub" style="color: #94A3B8;">Gross Sales ($13.36M Total)</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {profit_color};">
        <div class="metric-title">Total Profit</div>
        <div class="metric-value" style="color: {profit_color};">{profit_str}</div>
        <div class="metric-sub" style="color: #94A3B8;">Net Earnings</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {margin_color};">
        <div class="metric-title">Profit Margin</div>
        <div class="metric-value" style="color: {margin_color};">{margin_pct:.1f}%</div>
        <div class="metric-sub" style="color: #94A3B8;">Target: > 10.0%</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #8B5CF6;">
        <div class="metric-title">Total Orders</div>
        <div class="metric-value" style="color: #8B5CF6;">{total_orders:,}</div>
        <div class="metric-sub" style="color: #94A3B8;">Transactions Count</div>
    </div>
    """, unsafe_allow_html=True)

# Row 2 KPIs
c5, c6, c7, c8 = st.columns(4)
with c5:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #14B8A6;">
        <div class="metric-title">Total Customers</div>
        <div class="metric-value" style="color: #14B8A6;">{total_customers:,}</div>
        <div class="metric-sub" style="color: #94A3B8;">Active Buyer Base</div>
    </div>
    """, unsafe_allow_html=True)

with c6:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #6366F1;">
        <div class="metric-title">Total Products</div>
        <div class="metric-value" style="color: #6366F1;">{total_products}</div>
        <div class="metric-sub" style="color: #94A3B8;">Active SKU Count</div>
    </div>
    """, unsafe_allow_html=True)

with c7:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #F97316;">
        <div class="metric-title">Avg Quantity / Order</div>
        <div class="metric-value" style="color: #F97316;">{avg_quantity:.2f}</div>
        <div class="metric-sub" style="color: #94A3B8;">Units per Basket</div>
    </div>
    """, unsafe_allow_html=True)

with c8:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #06B6D4;">
        <div class="metric-title">Customer Retention</div>
        <div class="metric-value" style="color: #06B6D4;">{retention_rate:.1f}%</div>
        <div class="metric-sub" style="color: #94A3B8;">Repeat Buyer Rate</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tabs Navigation & Interactive Charts
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Executive Trends", 
    "💰 Profitability & Discounts", 
    "👥 Customer Analytics", 
    "📦 Product Portfolio", 
    "🌍 Regional Performance"
])

with tab1:
    st.subheader("Monthly Sales & Profit Velocity (2023 - 2025)")
    monthly = df.groupby('Month').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#1E293B')
    
    ax.plot(monthly['Month'], monthly['Sales'] / 1000, label='Sales ($K)', color='#3B82F6', linewidth=2.5, marker='o')
    ax.plot(monthly['Month'], monthly['Profit'] / 1000, label='Profit ($K)', color='#10B981', linewidth=2.5, marker='s')
    
    ax.set_xticklabels(monthly['Month'], rotation=45, ha='right', color='#94A3B8')
    ax.tick_params(colors='#94A3B8')
    ax.grid(True, linestyle='--', alpha=0.2)
    ax.legend(facecolor='#1E293B', edgecolor='#334155', labelcolor='#F8FAFC')
    st.pyplot(fig)

with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Discount Rate Toxicity Threshold")
        disc = df.groupby('Discount').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
        disc['Margin %'] = (disc['Profit'] / disc['Sales']) * 100
        
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#1E293B')
        
        colors = ['#10B981' if m > 10 else '#F59E0B' if m > 0 else '#EF4444' for m in disc['Margin %']]
        ax.bar(disc['Discount'].astype(str), disc['Margin %'], color=colors)
        ax.axhline(0, color='#94A3B8', linestyle='--', linewidth=1)
        ax.set_xlabel("Discount Rate", color="#F8FAFC")
        ax.set_ylabel("Profit Margin (%)", color="#F8FAFC")
        ax.tick_params(colors='#94A3B8')
        st.pyplot(fig)
        
    with col_b:
        st.subheader("Sub-Category Net Profit Driver Breakdown")
        sub_cat = df.groupby('Sub Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index().sort_values(by='Profit')
        
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#1E293B')
        
        colors = ['#EF4444' if p < 0 else '#3B82F6' for p in sub_cat['Profit']]
        ax.barh(sub_cat['Sub Category'], sub_cat['Profit'] / 1000, color=colors)
        ax.set_xlabel("Profit ($ Thousands)", color="#F8FAFC")
        ax.tick_params(colors='#94A3B8')
        st.pyplot(fig)

with tab3:
    st.subheader("Top 10 High-Value Spenders & RFM Segmentation")
    cust = df.groupby(['Customer ID', 'Customer Name', 'Gender']).agg(
        Orders=('Order ID', 'nunique'),
        Total_Spend=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum')
    ).reset_index().sort_values(by='Total_Spend', ascending=False)
    
    st.dataframe(cust.head(10).style.format({'Total_Spend': '${:,.2f}', 'Total_Profit': '${:,.2f}'}), use_container_width=True)

with tab4:
    st.subheader("Category Sales vs Profit Comparison")
    cat_df = df.groupby('Product Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    st.bar_chart(cat_df.set_index('Product Category')[['Sales', 'Profit']])

with tab5:
    st.subheader("Regional Sales & Profit Distribution")
    reg_df = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    st.dataframe(reg_df.style.format({'Sales': '${:,.2f}', 'Profit': '${:,.2f}'}), use_container_width=True)

# ---------------------------------------------------------
# Portfolio Dashboard Footer
# ---------------------------------------------------------
st.markdown(f"""
    <div class="footer-text">
        <strong>Last Updated:</strong> 31 Jul 2026 &nbsp;|&nbsp; 
        <strong>Data Source:</strong> Global Retail Sales Dataset (10,000 Records) &nbsp;|&nbsp; 
        <strong>Developed by:</strong> Anubhuti Kaushik
    </div>
""", unsafe_allow_html=True)
