# Power BI DAX Measures Library

This document contains the complete repository of DAX (Data Analysis Expressions) measures created for the **Sales & Business Data Analysis Power BI Dashboard**.

---

## 1. Core Financial & KPI Measures

### Total Sales
```dax
Total Sales = SUM(sales_transactions[Sales])
```

### Total Profit
```dax
Total Profit = SUM(sales_transactions[Profit])
```

### Profit Margin %
```dax
Profit Margin % = 
DIVIDE(
    [Total Profit], 
    [Total Sales], 
    0
)
```

### Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE(
    [Total Sales], 
    [Total Orders], 
    0
)
```

### Total Orders
```dax
Total Orders = DISTINCTCOUNT(sales_transactions[Order ID])
```

### Total Customers
```dax
Total Customers = DISTINCTCOUNT(sales_transactions[Customer ID])
```

### Average Discount Rate %
```dax
Average Discount = AVERAGE(sales_transactions[Discount])
```

### Total Shipping Cost
```dax
Total Shipping Cost = SUM(sales_transactions[Shipping Cost])
```

---

## 2. Time Intelligence & Trend Measures

### Prior Year Sales (PY Sales)
```dax
PY Sales = 
CALCULATE(
    [Total Sales], 
    SAMEPERIODLASTYEAR('Calendar'[Date])
)
```

### Year-over-Year (YoY) Sales Growth %
```dax
YoY Sales Growth % = 
DIVIDE(
    [Total Sales] - [PY Sales], 
    [PY Sales], 
    0
)
```

### Running Total Sales (YTD)
```dax
Running Total Sales = 
TOTALYTD(
    [Total Sales], 
    'Calendar'[Date]
)
```

### Month-over-Month (MoM) Growth %
```dax
MoM Sales Growth % = 
VAR PrevMonthSales = CALCULATE([Total Sales], DATEADD('Calendar'[Date], -1, MONTH))
RETURN
DIVIDE([Total Sales] - PrevMonthSales, PrevMonthSales, 0)
```

---

## 3. Customer & Segmentation Measures

### Repeat Customer Rate %
```dax
Repeat Customer Rate % = 
VAR TotalCust = [Total Customers]
VAR RepeatCust = 
    COUNTROWS(
        FILTER(
            SUMMARIZE(sales_transactions, sales_transactions[Customer ID], "OrderCount", DISTINCTCOUNT(sales_transactions[Order ID])),
            [OrderCount] > 1
        )
    )
RETURN
DIVIDE(RepeatCust, TotalCust, 0)
```

### High-Value VIP Customer Revenue
```dax
VIP Revenue = 
CALCULATE(
    [Total Sales],
    FILTER(
        sales_transactions,
        [Total Sales] >= 10000
    )
)
```

---

## 4. Advanced Ranking & Conditional Measures

### Customer Sales Rank
```dax
Customer Sales Rank = 
RANKX(
    ALL(sales_transactions[Customer Name]),
    [Total Sales],
    ,
    DESC,
    Dense
)
```

### Product Profit Rank
```dax
Product Profit Rank = 
RANKX(
    ALL(sales_transactions[Product Name]),
    [Total Profit],
    ,
    DESC,
    Skip
)
```

### Margin Status Alert (KPI Formatting)
```dax
Margin Status Color = 
SWITCH(
    TRUE(),
    [Profit Margin %] >= 0.15, "#27AE60", -- Green
    [Profit Margin %] >= 0.05, "#F39C12", -- Orange
    "#E74C3C"                             -- Red Alert
)
```
