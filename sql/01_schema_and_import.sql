-- =============================================================================
-- Database: sales_analytics_db
-- Description: Table schema, index optimizations, and data ingestion pipeline
-- Author: Senior Data Analyst
-- =============================================================================

CREATE DATABASE IF NOT EXISTS sales_analytics_db;
USE sales_analytics_db;

-- Drop table if already exists
DROP TABLE IF EXISTS sales_transactions;

-- Table Creation
CREATE TABLE sales_transactions (
    order_id VARCHAR(30) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE NOT NULL,
    customer_id VARCHAR(20) NOT NULL,
    customer_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    age INT NOT NULL,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    region VARCHAR(20) NOT NULL,
    product_id VARCHAR(30) NOT NULL,
    product_category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    product_name VARCHAR(150) NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount DECIMAL(4,2) NOT NULL,
    sales DECIMAL(12,2) NOT NULL,
    profit DECIMAL(12,2) NOT NULL,
    shipping_cost DECIMAL(10,2) NOT NULL,
    payment_mode VARCHAR(30) NOT NULL,
    order_priority VARCHAR(20) NOT NULL,
    PRIMARY KEY (order_id, product_id)
);

-- Indexing for High-Performance Queries
CREATE INDEX idx_order_date ON sales_transactions(order_date);
CREATE INDEX idx_customer_id ON sales_transactions(customer_id);
CREATE INDEX idx_region_state ON sales_transactions(region, state);
CREATE INDEX idx_category_sub ON sales_transactions(product_category, sub_category);
CREATE INDEX idx_payment_mode ON sales_transactions(payment_mode);

-- Data Import Command (MySQL Server / Workbench)
-- NOTE: Modify the file path below to your local directory path
/*
LOAD DATA INFILE 'c:/Users/garvi/Documents/Data Science Projects/Sales and Business Data Analysis/dataset/sales_data.csv'
INTO TABLE sales_transactions
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(order_id, order_date, ship_date, customer_id, customer_name, gender, age, city, state, region, product_id, product_category, sub_category, product_name, quantity, unit_price, discount, sales, profit, shipping_cost, payment_mode, order_priority);
*/
