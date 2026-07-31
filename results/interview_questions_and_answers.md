# 💬 25 Data Analyst Interview Questions & Answers (Project-Based)

---

### 🔹 Section 1: SQL & Database Queries (Q1 – Q8)

#### Q1: How did you write a query to find the Top 10 Customers by total spend using Window Functions?
**Answer**: I used a Common Table Expression (CTE) combining `SUM(sales)` and `DENSE_RANK() OVER (ORDER BY SUM(sales) DESC)`. Using `DENSE_RANK()` ensures no rank numbers are skipped if two customers have identical spend. Filtered `WHERE spend_rank <= 10`.

#### Q2: What is the difference between `RANK()`, `DENSE_RANK()`, and `ROW_NUMBER()` in MySQL?
**Answer**:
- `ROW_NUMBER()` assigns a unique incremental integer to every row regardless of ties (1, 2, 3, 4).
- `RANK()` assigns identical ranks to ties but skips subsequent rank numbers (1, 2, 2, 4).
- `DENSE_RANK()` assigns identical ranks to ties without skipping subsequent numbers (1, 2, 2, 3).

#### Q3: How did you calculate a Running Total of sales in SQL?
**Answer**: I used the window aggregate function: `SUM(sales) OVER (ORDER BY order_date ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW)`.

#### Q4: How do you calculate Month-over-Month (MoM) sales growth in SQL?
**Answer**: I aggregated monthly sales in a CTE, then used `LAG(monthly_sales, 1) OVER (ORDER BY year_month ASC)` to pull the previous month's revenue. MoM % was calculated as `((Current - Prev) / Prev) * 100`.

#### Q5: How did you structure your SQL Views, and why are Views preferred over raw tables for Power BI?
**Answer**: I created views like `vw_executive_kpis` and `vw_category_profitability`. Views encapsulate complex join and aggregation logic on the database side, reduce data transfer payload, ensure consistent metric definitions across teams, and allow Power BI to use direct query or scheduled import efficiently.

#### Q6: How do you identify repeat customers versus new customers in SQL?
**Answer**: I found each customer's first purchase date using `MIN(order_date) GROUP BY customer_id` in a CTE, then joined back to transaction records. Orders matching `MIN(order_date)` were flagged as 'New', while later orders were flagged as 'Repeat'.

#### Q7: Why did you add indexes on `order_date`, `customer_id`, and `region` in MySQL?
**Answer**: Indexing B-tree keys speeds up filter filtering (`WHERE order_date BETWEEN ...`), join lookups, and `GROUP BY` operations significantly on large tables, reducing execution time from full table scans to index range scans.

#### Q8: How did you handle loss-leader detection in SQL?
**Answer**: I queried sub-categories where `SUM(profit) < 0` or profit margin % was below target thresholds, ordering by `SUM(profit) ASC` using `RANK()`.

---

### 🔹 Section 2: Python Data Science & EDA (Q9 – Q15)

#### Q9: How did you detect and handle outliers in Python?
**Answer**: I calculated Interquartile Range (IQR) for numeric variables (`Q3 - Q1`). Outliers were identified outside `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]`. I retained valid edge transactions (like bulk tech purchases) for actual revenue reporting but evaluated trimmed datasets during regression modeling.

#### Q10: How did you check data quality and handle missing values in Pandas?
**Answer**: Used `df.isnull().sum()` and `df.duplicated().sum()`. The synthetic dataset maintained high integrity; for missing fields in standard workflows, numeric fields are imputed using median, categorical fields with mode, or dropped if missing rate > 30%.

#### Q11: What insights did you gain from the Correlation Analysis?
**Answer**: Unit Price correlated strongly with Sales (0.734) and Profit (0.565), while Discount showed a negative correlation with Profit (-0.287), confirming high discounts directly penalize margins.

#### Q12: Why did you choose Matplotlib over Seaborn for your exported graphics?
**Answer**: Matplotlib provides granular control over figure axes, tick labels, custom color palettes, and legend coordinates, ensuring exact pixel-perfect chart formatting exported at 300 DPI for GitHub and report embedding.

#### Q13: How did you group dates by month in Pandas?
**Answer**: Converted `Order Date` to datetime (`pd.to_datetime`), then used `df['Order Date'].dt.to_period('M')` or `df.resample('M', on='Order Date').sum()`.

#### Q14: Explain the Customer Lifetime Value (LTV) segmentation logic you wrote in Python.
**Answer**: Grouped by `Customer ID`, calculated total spend, and categorized clients using `pd.cut()` into 4 tiers: VIP (>$10k), Tier 2 ($5k-$10k), Tier 3 ($2k-$5k), and Tier 4 (<$2k).

#### Q15: How did you analyze price elasticity in Python?
**Answer**: Plotted Quantity Sold against Unit Price and Discount levels, evaluating how unit sales volume responded to price shifts across different categories.

---

### 🔹 Section 3: Power BI & DAX Modeling (Q16 – Q21)

#### Q16: Explain the difference between `CALCULATE` and `FILTER` in DAX.
**Answer**: `CALCULATE` evaluates an expression in a modified filter context. `FILTER` is an iterator function that returns a table filtered row-by-row. `FILTER` is typically passed as a table argument inside `CALCULATE`.

#### Q17: How did you create the YoY Sales Growth DAX measure?
**Answer**: Created `PY Sales = CALCULATE([Total Sales], SAMEPERIODLASTYEAR('Calendar'[Date]))`, then computed `DIVIDE([Total Sales] - [PY Sales], [PY Sales], 0)`.

#### Q18: Why use `DIVIDE()` instead of `/` in DAX?
**Answer**: `DIVIDE()` automatically handles division-by-zero scenarios without throwing errors, allowing a user-defined fallback value (e.g., `0` or `BLANK()`).

#### Q19: What is the purpose of establishing a dedicated Calendar Date Table in Power BI?
**Answer**: Time Intelligence functions (`TOTALYTD`, `SAMEPERIODLASTYEAR`) require a contiguous date table marked as a Date Table without gaps to compute temporal shifts accurately.

#### Q20: How did you configure cross-filtering between visuals?
**Answer**: Used Power BI's Edit Interactions toolbar to set visual relationships to 'Filter' or 'None', ensuring slicers update card metrics and regional maps seamlessly.

#### Q21: What DAX function did you use to rank products or customers?
**Answer**: `RANKX(ALL(sales_transactions[Customer Name]), [Total Sales], , DESC, Dense)`. `ALL()` ignores context filters on individual table rows to calculate relative global rank.

---

### 🔹 Section 4: Business Sense & Strategic Problem Solving (Q22 – Q25)

#### Q22: If Furniture has high sales ($3.67M) but low profit ($92.9K), would you recommend discontinuing it?
**Answer**: No. Discontinuing Furniture would lose $3.67M in top-line revenue and potential cross-selling opportunities (e.g., pairing office desks with laptops). Instead, I recommend capping discounts at 20%, adjusting freight surcharges, and renegotiating supplier costs to lift margin from 2.53% to 10%+.

#### Q23: Why do discounts above 30% erode profits so drastically?
**Answer**: Base profit margins range between 15%–25%. A 30%+ discount exceeds the profit margin cushion and fails to cover fixed shipping overhead, turning transactions net-negative.

#### Q24: How would you present these findings to a non-technical C-suite executive?
**Answer**: Focus on business impact rather than technical jargon: highlight the top-line numbers ($13.36M revenue, $1.44M profit), present the 3 core visual takeaways (Tech drives profit, Furniture needs margin fixing, Discounts >30% destroy money), and deliver 3 clear actionable recommendations with estimated ROI.

#### Q25: How would you scale this project if transaction volume grew from 10,000 to 10,000,000 rows?
**Answer**: Migrate storage from local MySQL to a cloud data warehouse (Snowflake / BigQuery), implement Star Schema data modeling (Fact and Dimension tables), utilize PySpark for distributed data processing, and implement Power BI DirectQuery / Aggregation Tables for real-time dashboard performance.
