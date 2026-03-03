
CREATE DATABASE sales_db;

CREATE EXTERNAL TABLE sales_db.sales_data (
    transaction_id   STRING,
    "date"           DATE,
    product_id       STRING,
    product_name     STRING,
    product_category STRING,
    quantity         DOUBLE,
    price            DOUBLE,
    amount           DOUBLE,
    total_sales      DOUBLE,
    order_year       INT,
    order_month      INT,
    order_month_name STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\""
)
STORED AS TEXTFILE
LOCATION 's3://my-data-pipeline-yourname/processed-data/'
TBLPROPERTIES ('skip.header.line.count' = '1');

-- ⚠️ Replace 'my-data-pipeline-yourname' with your actual bucket name


-- -------------------------------------------------------
-- QUERY 2: Total Records
-- -------------------------------------------------------
SELECT 
    COUNT(*) AS total_records
FROM sales_db.sales_data;


-- -------------------------------------------------------
-- QUERY 3: Total Revenue
-- -------------------------------------------------------
SELECT 
    ROUND(SUM(total_sales), 2) AS total_revenue
FROM sales_db.sales_data;


-- -------------------------------------------------------
-- QUERY 4: Top 5 Products by Revenue
-- -------------------------------------------------------
SELECT 
    product_name,
    product_category,
    CAST(SUM(quantity) AS BIGINT)      AS total_units_sold,
    ROUND(SUM(total_sales), 2)         AS total_revenue
FROM sales_db.sales_data
GROUP BY product_name, product_category
ORDER BY total_revenue DESC
LIMIT 5;


-- -------------------------------------------------------
-- QUERY 5: Monthly Sales Summary
-- -------------------------------------------------------
SELECT 
    order_year,
    order_month,
    order_month_name,
    COUNT(*)                           AS total_transactions,
    CAST(SUM(quantity) AS BIGINT)      AS total_units_sold,
    ROUND(SUM(total_sales), 2)         AS monthly_revenue,
    ROUND(AVG(total_sales), 2)         AS avg_sale_per_transaction
FROM sales_db.sales_data
GROUP BY order_year, order_month, order_month_name
ORDER BY order_year, order_month;


-- -------------------------------------------------------
-- QUERY 6: Average Order Value
-- -------------------------------------------------------
SELECT 
    ROUND(AVG(total_sales), 2) AS avg_order_value,
    ROUND(MIN(total_sales), 2) AS min_order_value,
    ROUND(MAX(total_sales), 2) AS max_order_value,
    COUNT(*)                   AS total_orders
FROM sales_db.sales_data;
