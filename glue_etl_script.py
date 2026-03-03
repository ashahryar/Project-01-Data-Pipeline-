

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from pyspark.sql.types import *

BUCKET_NAME = "my-data-pipeline-yourname"        
INPUT_FILE  = "raw_rfm_sales_transactions_30000.csv"  

INPUT_PATH  = f"s3://{BUCKET_NAME}/raw-data/{INPUT_FILE}"
OUTPUT_PATH = f"s3://{BUCKET_NAME}/processed-data/"


# Initialize Glue
sc         = SparkContext()
glueContext = GlueContext(sc)
spark      = glueContext.spark_session
job        = Job(glueContext)

print("=" * 50)
print("🚀 ETL Job Started")
print(f"📂 Reading from: {INPUT_PATH}")
print("=" * 50)


# STEP 1: Read Raw CSV from S3

df = spark.read \
    .option("header", "true") \
    .option("inferSchema", "true") \
    .csv(INPUT_PATH)

print(f"✅ Raw rows loaded: {df.count()}")

# ----------------------------------------------------------
# STEP 2: Remove junk rows (rows where Transaction ID does NOT start with 'T' — e.g. customer header rows)

df = df.filter(col("`Transaction ID`").startswith("T"))
print(f"✅ After removing junk rows: {df.count()}")


# STEP 3: Standardize Column Names 
# ------------------------------------------------------
for c in df.columns:
    new = c.lower().strip().replace(" ", "_").replace("-", "_")
    df  = df.withColumnRenamed(c, new)

print(f"✅ Standardized columns: {df.columns}")


# STEP 4: Remove Null Values

df = df.dropna()
print(f"✅ Rows after removing nulls: {df.count()}")


# STEP 5: Rename ppu → price for clarity

df = df.withColumnRenamed("ppu", "price")


# STEP 6: Clean numeric columns (remove commas from strings)

df = df.withColumn("price",    regexp_replace(col("price"),    ",", "").cast(DoubleType()))
df = df.withColumn("amount",   regexp_replace(col("amount"),   ",", "").cast(DoubleType()))
df = df.withColumn("quantity", col("quantity").cast(DoubleType()))


# STEP 7: Convert Date Format

df = df.withColumn("date", to_date(col("date"), "dd.MM.yyyy"))

# Add helper columns for time-based analysis

df = df.withColumn("order_year",       year(col("date")))
df = df.withColumn("order_month",      month(col("date")))
df = df.withColumn("order_month_name", date_format(col("date"), "MMMM"))

print("✅ Date converted to YYYY-MM-DD format")

# STEP 8: Create Calculated Column   Total_Sales = Quantity × Price


df = df.withColumn("total_sales", round(col("quantity") * col("price"), 2))
print("✅ total_sales column created (Quantity × Price)")


# STEP 9: Show sample of processed data
# ----------------------------------------------------------
print("\n=== Sample of Processed Data ===")
df.show(5, truncate=False)
print(f"📊 Final Row Count : {df.count()}")
print(f"📋 Final Columns   : {df.columns}")


# STEP 10: Save Processed Data to S3 /processed-data/
# ----------------------------------------------------------
df.write \
  .mode("overwrite") \
  .option("header", "true") \
  .csv(OUTPUT_PATH)

print(f"\n✅ Processed data saved to: {OUTPUT_PATH}")
print("🎉 ETL Job Completed Successfully!")

job.commit()
