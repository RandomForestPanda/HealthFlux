
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when

# Set JAVA_HOME for Spark
os.environ["JAVA_HOME"] = "/opt/homebrew/Cellar/openjdk@11/11.0.27/libexec/openjdk.jdk/Contents/Home"
os.environ["SPARK_LOCAL_IP"] = "192.168.1.77"

# Initialize Spark session
try:
    spark = SparkSession.builder.appName("HealthcareAnalytics").config("spark.driver.memory", "4g").getOrCreate()
    print("Spark session initialized")
except Exception as e:
    print(f"Error initializing Spark: {e}")
    exit()

# Load dataset and print columns for debugging
try:
    df = spark.read.csv("healthcare_dataset.csv", header=True, inferSchema=True)
    # Normalize column names: lowercase and replace spaces with underscores
    df = df.select([col(c).alias(c.lower().replace(' ', '_')) for c in df.columns])
    print("CSV columns:", df.columns)
    df.createOrReplaceTempView("healthcare")
    print("Dataset loaded successfully")
except Exception as e:
    print(f"Error loading dataset: {e}")
    spark.stop()
    exit()

# Analytics 1: Top 5 diagnoses
try:
    top_diagnoses = spark.sql("""
        SELECT medical_condition AS diagnosis, COUNT(*) AS count
        FROM healthcare
        GROUP BY medical_condition
        ORDER BY count DESC
        LIMIT 5
    """)
    top_diagnoses.show()
    top_diagnoses.write.mode("overwrite").json("top_diagnoses.json")
    print("Top diagnoses saved")
except Exception as e:
    print(f"Error in top diagnoses query: {e}")

# Analytics 2: Readmission rate (patients with multiple admissions)
try:
    readmissions = spark.sql("""
        SELECT name, COUNT(*) AS admission_count
        FROM healthcare
        GROUP BY name
        HAVING COUNT(*) > 1
        ORDER BY admission_count DESC
        LIMIT 10
    """)
    readmissions.show()
    readmissions.write.mode("overwrite").json("readmissions.json")
    print("Readmissions saved")
except Exception as e:
    print(f"Error in readmissions query: {e}")

# Stop Spark session
spark.stop()
print("Analytics completed and results saved")
