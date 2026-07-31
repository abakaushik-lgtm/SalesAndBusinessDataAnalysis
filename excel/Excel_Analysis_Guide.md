# 📊 Excel Data Analysis & Financial Modeling Guide

This document details the Excel methodology, preprocessing steps, advanced formulas, and Pivot Table architecture used in building the enterprise financial model (`excel/sales_analysis_model.xlsx`).

---

## 🛠️ 1. Data Cleaning & Preprocessing in Excel
Before performing analysis, the raw transactional data (10,000 records) underwent the following preprocessing workflow:

1. **Duplicate Removal**:
   - Navigation: `Data Tab -> Remove Duplicates -> Select Order ID & Product ID`.
   - Verified 0 duplicate order lines across 10,000 transactions.
2. **Data Type Standardization**:
   - `Order Date` & `Ship Date`: Formatted as Short Date (`YYYY-MM-DD`).
   - `Sales`, `Profit`, `Unit Price`, `Shipping Cost`: Formatted as Currency (`$#,##0.00`).
   - `Discount`: Formatted as Percentage (`0.00%`).
   - `Quantity`, `Age`: Formatted as Whole Number (`#,##0`).
3. **Handling Missing & Blank Values**:
   - Filtered all columns using `Ctrl + Shift + L` to inspect for blanks. Verified 100% complete data fields.

---

## 🧮 2. Advanced Excel Formulas & Modeling

### Core Aggregation Formulas
- **Total Revenue**: `=SUM(Raw_Data!R2:R10001)`
- **Total Profit**: `=SUM(Raw_Data!S2:S10001)`
- **Overall Profit Margin %**: `=E5/C5` (Profit / Revenue)
- **Total Order Volume**: `=COUNTA(Raw_Data!A2:A10001)`
- **Average Order Value (AOV)**: `=C5/I5` (Revenue / Total Orders)
- **Average Discount Rate**: `=AVERAGE(Raw_Data!Q2:Q10001)`

### Category & Regional Aggregations (`SUMIFS` & `AVERAGEIFS`)
- **Category Gross Revenue**:
  ```excel
  =SUMIFS(Raw_Data!R2:R10001, Raw_Data!L2:L10001, "Technology")
  ```
- **Category Net Profit**:
  ```excel
  =SUMIFS(Raw_Data!S2:S10001, Raw_Data!L2:L10001, "Technology")
  ```
- **Category Average Discount**:
  ```excel
  =AVERAGEIFS(Raw_Data!Q2:Q10001, Raw_Data!L2:L10001, "Technology")
  ```

### Advanced Lookup Formulas (`XLOOKUP` & `INDEX/MATCH`)
- **Customer Lookup via XLOOKUP**:
  ```excel
  =XLOOKUP("CUST-0093", Raw_Data!D2:D10001, Raw_Data!E2:E10001, "Not Found")
  ```
- **Product Price Retrieval via INDEX/MATCH**:
  ```excel
  =INDEX(Raw_Data!P2:P10001, MATCH("PROD-TEC-1001", Raw_Data!K2:K10001, 0))
  ```

---

## 📊 3. Pivot Tables & Dynamic Dashboard Setup

### Pivot Table 1: Category & Sub-Category Financial Breakdown
- **Rows**: `Product Category` -> `Sub Category`
- **Values**: 
  - `Sum of Sales` (Formatted as `$#,##0.00`)
  - `Sum of Profit` (Formatted as `$#,##0.00`)
  - `Calculated Field (Profit Margin %)`: `= Profit / Sales` (Formatted as `0.00%`)

### Pivot Table 2: Monthly Revenue Velocity & Seasonality
- **Rows**: `Order Date` (Grouped by Years & Months)
- **Columns**: `Region` (West, East, Central, South)
- **Values**: `Sum of Sales`
- **Visual**: Inserted 2D Clustered Column Chart to display Q4 seasonal surges.

### Pivot Table 3: Discount Erosion & Loss Leader Matrix
- **Rows**: `Discount` (0%, 5%, 10%, 15%, 20%, 25%, 30%, 35%, 40%, 50%)
- **Values**: `Sum of Sales`, `Sum of Profit`, `Average Profit Margin %`
- **Conditional Formatting**: Highlighted cells where `Profit Margin % < 0%` in Soft Red (`#FCA5A5`) to immediately flag high-discount toxicity.
