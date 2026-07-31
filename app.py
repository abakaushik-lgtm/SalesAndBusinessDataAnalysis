import os
import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt

# Page Config
st.set_page_config(
    page_title="Sales & Business Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Executive Dashboard Styling
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
    }
    .metric-card {
        background-color: #1E293B;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #3B82F6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-title {
        color: #94A3B8;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #F8FAFC;
        font-size: 1.8rem;
        font-weight: 700;
    }
    .metric-sub {
        color: #10B981;
        font-size: 0.8rem;
        font-weight: 500;
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
st.sidebar.title("🔍 Interactive Dashboard Filters")
st.sidebar.markdown("Filter enterprise sales records in real time:")

years = ["All"] + sorted(list(df_raw['Year'].unique()))
selected_year = st.sidebar.selectbox("Select Year", years)

regions = ["All"] + sorted(list(df_raw['Region'].unique()))
selected_region = st.sidebar.selectbox("Select Region", regions)

categories = ["All"] + sorted(list(df_raw['Product Category'].unique()))
selected_category = st.sidebar.selectbox("Select Category", categories)

payments = ["All"] + sorted(list(df_raw['Payment Mode'].unique()))
selected_payment = st.sidebar.selectbox("Select Payment Mode", payments)

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
# Main Header & Executive Metrics
# ---------------------------------------------------------
st.title("📈 Global Retail Corp - Sales & Business Analytics")
st.markdown("##### Real-Time Executive KPI Dashboard & Decision Support System")

total_sales = df['Sales'].sum()
total_profit = df['Profit'].sum()
margin_pct = (total_profit / total_sales * 100) if total_sales > 0 else 0
total_orders = df['Order ID'].nunique()
aov = total_sales / total_orders if total_orders > 0 else 0
avg_discount = df['Discount'].mean() * 100

col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Revenue</div>
        <div class="metric-value">${total_sales:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #10B981;">
        <div class="metric-title">Total Profit</div>
        <div class="metric-value">${total_profit:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    color = "#10B981" if margin_pct > 10 else "#F59E0B" if margin_pct > 0 else "#EF4444"
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: {color};">
        <div class="metric-title">Profit Margin</div>
        <div class="metric-value">{margin_pct:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #8B5CF6;">
        <div class="metric-title">Total Orders</div>
        <div class="metric-value">{total_orders:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #06B6D4;">
        <div class="metric-title">Avg Order Value</div>
        <div class="metric-value">${aov:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #EC4899;">
        <div class="metric-title">Avg Discount</div>
        <div class="metric-value">{avg_discount:.2f}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------------------------------------------------
# Tabs Navigation
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Executive Trends", 
    "💰 Profitability & Discounts", 
    "👥 Customer Analytics", 
    "📦 Product Portfolio", 
    "🌍 Regional Performance"
])

# ---------------------------------------------------------
# Tab 1: Executive Trends
# ---------------------------------------------------------
with tab1:
    st.subheader("Monthly Sales & Profit Velocity")
    monthly = df.groupby('Month').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    
    fig, ax = plt.subplots(figsize=(12, 4))
    fig.patch.set_facecolor('#0E1117')
    ax.set_facecolor('#1E293B')
    
    ax.plot(monthly['Month'], monthly['Sales'] / 1000, label='Sales ($K)', color='#38BDF8', linewidth=2.5, marker='o')
    ax.plot(monthly['Month'], monthly['Profit'] / 1000, label='Profit ($K)', color='#34D399', linewidth=2.5, marker='s')
    
    ax.set_xticklabels(monthly['Month'], rotation=45, ha='right', color='#94A3B8')
    ax.tick_params(colors='#94A3B8')
    ax.grid(True, linestyle='--', alpha=0.2)
    ax.legend(facecolor='#1E293B', edgecolor='#334155', labelcolor='#F8FAFC')
    st.pyplot(fig)

# ---------------------------------------------------------
# Tab 2: Profitability & Discounts
# ---------------------------------------------------------
with tab2:
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Discount Toxicity Matrix")
        disc = df.groupby('Discount').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
        disc['Margin %'] = (disc['Profit'] / disc['Sales']) * 100
        
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#1E293B')
        
        colors = ['#34D399' if m > 10 else '#FBBF24' if m > 0 else '#F87171' for m in disc['Margin %']]
        ax.bar(disc['Discount'].astype(str), disc['Margin %'], color=colors)
        ax.axhline(0, color='#94A3B8', linestyle='--', linewidth=1)
        ax.set_xlabel("Discount Rate", color="#F8FAFC")
        ax.set_ylabel("Profit Margin (%)", color="#F8FAFC")
        ax.tick_params(colors='#94A3B8')
        st.pyplot(fig)
        
    with col_b:
        st.subheader("Sub-Category Profitability Drivers")
        sub_cat = df.groupby('Sub Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index().sort_values(by='Profit')
        
        fig, ax = plt.subplots(figsize=(6, 4))
        fig.patch.set_facecolor('#0E1117')
        ax.set_facecolor('#1E293B')
        
        colors = ['#F87171' if p < 0 else '#38BDF8' for p in sub_cat['Profit']]
        ax.barh(sub_cat['Sub Category'], sub_cat['Profit'] / 1000, color=colors)
        ax.set_xlabel("Profit ($ Thousands)", color="#F8FAFC")
        ax.tick_params(colors='#94A3B8')
        st.pyplot(fig)

# ---------------------------------------------------------
# Tab 3: Customer Analytics
# ---------------------------------------------------------
with tab3:
    st.subheader("Top 10 Spenders & Customer RFM Tiers")
    cust = df.groupby(['Customer ID', 'Customer Name', 'Gender']).agg(
        Orders=('Order ID', 'nunique'),
        Total_Spend=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum')
    ).reset_index().sort_values(by='Total_Spend', ascending=False)
    
    st.dataframe(cust.head(10).style.format({'Total_Spend': '${:,.2f}', 'Total_Profit': '${:,.2f}'}), use_container_width=True)

# ---------------------------------------------------------
# Tab 4: Product Portfolio
# ---------------------------------------------------------
with tab4:
    st.subheader("Category Sales vs Profit Comparison")
    cat_df = df.groupby('Product Category').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    st.bar_chart(cat_df.set_index('Product Category')[['Sales', 'Profit']])

# ---------------------------------------------------------
# Tab 5: Regional Performance
# ---------------------------------------------------------
with tab5:
    st.subheader("Regional Sales & Profit Distribution")
    reg_df = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    st.dataframe(reg_df.style.format({'Sales': '${:,.2f}', 'Profit': '${:,.2f}'}), use_container_width=True)

st.markdown("---")
st.markdown("📌 **Sales & Business Analytics System** | Developed with Python, Streamlit, SQL & Matplotlib")
