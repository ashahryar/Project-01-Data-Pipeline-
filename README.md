# ☁️ AWS Cloud Data Engineering – End-to-End Data Pipeline

![AWS](https://img.shields.io/badge/AWS-Cloud-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-PySpark-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-Athena-A855F7?style=for-the-badge&logo=amazon&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-00FF88?style=for-the-badge)

---

## 📌 Project Overview

This project demonstrates a **complete end-to-end cloud data pipeline** built on AWS. Raw sales transaction data from Kaggle is ingested, cleaned, transformed, stored, queried analytically, and visualized in an interactive dashboard.

**Dataset:** RFM Sales Transactions — 30,000 records  
**Domain:** Retail / E-Commerce Sales Analytics  
**Tools:** Amazon S3, AWS Glue, Amazon Athena, Google Looker Studio

---

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────────┐     ┌─────────────┐     ┌─────────────────┐
│   Kaggle    │────▶│  Amazon S3   │────▶│   AWS Glue    │────▶│   Amazon S3      │────▶│   Amazon    │────▶│ Google Looker   │
│  CSV File   │     │  /raw-data/  │     │  ETL PySpark  │     │ /processed-data/ │     │   Athena    │     │    Studio       │
│ 30K Records │     │              │     │               │     │                  │     │  5 Queries  │     │  Dashboard      │
└─────────────┘     └──────────────┘     └───────────────┘     └──────────────────┘     └─────────────┘     └─────────────────┘
    STEP 1               STEP 2               STEP 3                  STEP 3                STEP 4               STEP 5
```

---

## 📂 Project Structure

```
aws-data-pipeline/
│
├── 📁 data/
│   ├── raw_rfm_sales_transactions_30000.csv     # Original Kaggle dataset
│   └── processed_sales_data.csv                 # Cleaned & transformed data
│
├── 📁 scripts/
│   ├── glue_etl_script.py                       # AWS Glue PySpark ETL job
│   └── athena_sql_queries.sql                   # All 5 Athena SQL queries
│
├── 📁 diagrams/
│   └── architecture_aws_icons.drawio            # Architecture diagram
│
├── 📁 screenshots/
│   ├── s3_bucket.png                            # S3 bucket setup
│   ├── glue_job_success.png                     # Glue ETL job succeeded
│   ├── athena_query_1.png                       # Total Records
│   ├── athena_query_2.png                       # Total Revenue
│   ├── athena_query_3.png                       # Top 5 Products
│   ├── athena_query_4.png                       # Monthly Sales Summary
│   ├── athena_query_5.png                       # Average Order Value
│   └── dashboard.png                            # Looker Studio Dashboard
│
├── 📄 Architecture_Report.docx                  # 2-page architecture explanation
└── 📄 README.md                                 # This file
```

---

## 🚀 Step-by-Step Implementation

### ✅ Step 1 — Dataset Selection

- **Source:** Kaggle
- **Dataset:** RFM Sales Transactions
- **File:** `raw_rfm_sales_transactions_30000.csv`
- **Records:** 30,000 transactions
- **Columns:** Transaction ID, Date, Product ID, Product Name, Product Category, Quantity, PPU (Price), Amount

---

### ✅ Step 2 — Data Storage (Amazon S3)

**Bucket Name:** `bootcamp4.00`

| Folder | Purpose |
|--------|---------|
| `/raw-data/` | Original unmodified CSV file |
| `/processed-data/` | Cleaned and transformed output |
| `/athena-results/` | Athena SQL query results |

**Steps performed:**
1. Created S3 bucket `bootcamp4.00`
2. Created folder structure `/raw-data/` and `/processed-data/`
3. Uploaded raw CSV to `/raw-data/`

---

### ✅ Step 3 — Data Processing (AWS Glue ETL)

**Job Type:** PySpark (AWS Glue Spark Job)  
**Script:** `scripts/glue_etl_script.py`

#### Transformations Applied:

| # | Transformation | Details |
|---|---------------|---------|
| 1 | **Remove Junk Rows** | Filtered rows where Transaction ID doesn't start with 'T' |
| 2 | **Standardize Column Names** | Lowercase + underscores (e.g. `Product Name` → `product_name`) |
| 3 | **Remove Null Values** | `dropna()` removed 100 incomplete records |
| 4 | **Convert Date Format** | `DD.MM.YYYY` → `YYYY-MM-DD` standard format |
| 5 | **Clean Numeric Fields** | Removed commas from price/amount strings (`380,000` → `380000`) |
| 6 | **Create Calculated Column** | `total_sales = quantity × price` |
| 7 | **Add Time Columns** | `order_year`, `order_month`, `order_month_name` |

**Input:** `s3://bootcamp4.00/raw-data/raw_rfm_sales_transactions_30000.csv`  
**Output:** `s3://bootcamp4.00/processed-data/`  
**Result:** 30,000 clean records ✅

---

### ✅ Step 4 — Data Warehouse (Amazon Athena)

**Database:** `sales_db`  
**Table:** `sales_data`  
**Script:** `scripts/athena_sql_queries.sql`

#### SQL Queries & Results:

**Query 1 — Total Records**
```sql
SELECT COUNT(*) AS total_records
FROM sales_db.sales_data;
```
> Result: **30,000 records**

---

**Query 2 — Total Revenue**
```sql
SELECT ROUND(SUM(total_sales), 2) AS total_revenue
FROM sales_db.sales_data;
```
> Result: **74,052,929,500 PKR**

---

**Query 3 — Top 5 Products**
```sql
SELECT product_name,
       CAST(SUM(quantity) AS BIGINT) AS total_units_sold,
       ROUND(SUM(total_sales), 2) AS total_revenue
FROM sales_db.sales_data
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 5;
```
> Result: 27-inch 4K Monitor ranked #1

---

**Query 4 — Monthly Sales Summary**
```sql
SELECT order_year, order_month, order_month_name,
       COUNT(*) AS total_orders,
       ROUND(SUM(total_sales), 2) AS monthly_revenue
FROM sales_db.sales_data
GROUP BY order_year, order_month, order_month_name
ORDER BY order_year, order_month;
```
> Result: Monthly breakdown January–June 2025

---

**Query 5 — Average Order Value**
```sql
SELECT ROUND(AVG(total_sales), 2) AS avg_order_value,
       ROUND(MIN(total_sales), 2) AS min_order_value,
       ROUND(MAX(total_sales), 2) AS max_order_value
FROM sales_db.sales_data;
```
> Result: Average order value calculated ✅

---

### ✅ Step 5 — Visualization (Google Looker Studio)

**Tool:** Google Looker Studio (free alternative to Amazon QuickSight)  
**Connected to:** Processed CSV data

#### Dashboard Charts:

| Chart | Type | Fields Used |
|-------|------|------------|
| Top Products by Revenue | Bar Chart | `product_name` × `total_sales` |
| Sales by Category | Donut Pie Chart | `product_category` × `total_sales` |
| Monthly Sales Trend | Line Chart | `order_month_name` × `total_sales` |
| Total Revenue KPI | Scorecard | `total_sales` SUM |
| Total Orders KPI | Scorecard | `Record Count` |
| Total Units Sold KPI | Scorecard | `quantity` SUM |

#### Dashboard Insights:
- 📊 **Electronics** dominates with **66.2%** of total revenue
- 🛋️ **Furniture** accounts for **31.7%** of revenue
- 📉 Sales trend shows **decline from January to June 2025**
- 🏆 **27-inch 4K Monitor** is the top selling product

---

## 💰 Cost Analysis

| AWS Service | Usage | Cost |
|-------------|-------|------|
| Amazon S3 | < 1MB storage | **Free** (5GB free tier) |
| AWS Glue | 1 ETL job (~3 min) | **Free** (1M DPU-seconds/month) |
| Amazon Athena | 5 SQL queries | **~$0.00** |
| Google Looker Studio | Dashboard | **Free** |
| **Total** | **Complete Pipeline** | **~$0.00** ✅ |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| **Amazon S3** | Data Lake — raw & processed storage |
| **AWS Glue (PySpark)** | ETL — data cleaning & transformation |
| **Amazon Athena** | Serverless SQL data warehouse |
| **AWS Glue Data Catalog** | Metadata & schema management |
| **Google Looker Studio** | Business intelligence dashboard |
| **Python / PySpark** | ETL scripting language |
| **SQL** | Analytical querying |

---

## 📊 Dataset Details

| Field | Value |
|-------|-------|
| Source | Kaggle |
| Records | 30,000 |
| Time Period | January 2025 – June 2025 |
| Categories | Electronics, Furniture, Office Supplies |
| Products | 10 unique products |
| Total Revenue | 74,052,929,500 PKR |

---

## 🔧 How to Reproduce

### Prerequisites
- AWS Account (free tier)
- Python 3.x
- Draw.io (for architecture diagram)

### Steps

**1. Clone this repository**
```bash
git clone https://github.com/ashahryar/aws-data-pipeline.git
cd aws-data-pipeline
```

**2. Upload to S3**
```bash
# Create bucket and folders in AWS Console
# Upload data/raw_rfm_sales_transactions_30000.csv to /raw-data/
```

**3. Run Glue ETL Job**
```bash
# Go to AWS Glue → ETL Jobs → Script Editor
# Paste scripts/glue_etl_script.py
# Change BUCKET_NAME = "your-bucket-name"
# Click Save → Run
```

**4. Run Athena Queries**
```bash
# Go to Amazon Athena → Query Editor
# Run scripts/athena_sql_queries.sql queries one by one
```

**5. View Dashboard**
```
https://lookerstudio.google.com
# Connect processed CSV → Build charts
```

---

## 👨‍💻 Author

**ShahryarAhmed**  
AWS Cloud Data Engineering — Practical Assignment  
Batch: 2025

---

## 📄 License

This project is for educational purposes only.

---

⭐ **If you found this helpful, please give it a star!**
