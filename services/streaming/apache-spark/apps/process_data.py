from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, udf, when, lit, to_date, regexp_replace, trim
)
from pyspark.sql.types import StringType
import json
import datetime

# Google Cloud configuration
BQ_PROJECT = 'your-gcp-project'
BQ_DATASET = 'your_dataset'
BQ_BUCKET = 'tc4a-backet'
date_suffix = datetime.datetime.now().strftime("%Y%m%d")

# Kafka configuration
KAFKA_BROKER = "localhost:9092" 
KAFKA_TOPIC = "your_topic_name"

# Initialize Spark session with BigQuery support
spark = SparkSession.builder \
    .appName("TC4A Data Transformation from Kafka to BigQuery") \
    .config("spark.jars", "/opt/spark-apps/jars/spark-sql-kafka-0-10_2.12-3.2.1.jar") \
    .getOrCreate()

def standardize_country_name(country_name):
    if country_name:
        return country_name.strip().title()
    return None

def sanitize_gender(gender):
    if not gender or gender.strip() == '':
        return 'Other'
    gender = gender.strip().capitalize()
    return gender if gender in ['Male', 'Female'] else 'Other'

def sanitize_field_name(name):
    return name.replace(' ', '_').replace('/', '_').replace('-', '_').replace('?', '') \
        .replace('.', '').replace('(', '').replace(')', '').replace(',', '_').lower()

@udf(StringType())
def extract_json_to_columns(other_info):
    if other_info:
        try:
            other_info = other_info.replace("'", '"')
            other_info_dict = json.loads(other_info)
            return json.dumps({sanitize_field_name(k): v for k, v in other_info_dict.items()})
        except json.JSONDecodeError:
            return None
    return None

# Function to read data from Kafka
def read_from_kafka():
    # Read Kafka stream data
    df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", KAFKA_BROKER).option("subscribe", KAFKA_TOPIC).load()

    # Convert the Kafka data (in bytes) into a readable format (string or JSON)
    df = df.selectExpr("CAST(value AS STRING) AS json_data")

    # Parse JSON data
    df = df.selectExpr("json_data", "from_json(json_data, 'organization_name STRING, event_title STRING, first_name STRING, last_name STRING, email STRING, gender STRING, country_region_name STRING, other_info STRING') AS parsed_data") \
        .select("parsed_data.*")
    
    return df

# Transformations
def transform_data(df):
    # Extract JSON to columns
    df = df.withColumn("other_info_json", extract_json_to_columns(col("other_info")))

    # Sanitize gender
    df = df.withColumn("gender", when(col("gender").isNotNull(), sanitize_gender(col("gender"))).otherwise(lit("Other")))

    # Standardize country names
    df = df.withColumn("country_region_name", when(col("country_region_name").isNotNull(), 
                                                   standardize_country_name(col("country_region_name"))))
    df = df.withColumn("country", when(col("country").isNotNull(), standardize_country_name(col("country"))))

    # Drop unnecessary fields
    fields_to_drop = ['other_info', 'can_your_email_be_used_for_future_communications', 'is_guest', 'join_time', 'leave_time']
    for field in fields_to_drop:
        if field in df.columns:
            df = df.drop(field)

    return df

# Save DataFrame to BigQuery
def save_to_bigquery(df, entity):
    table_name = f"{BQ_PROJECT}.{BQ_DATASET}.{entity}_transformed_data_{date_suffix}"

    df.writeStream \
        .format("bigquery") \
        .option("checkpointLocation", f"/tmp/{entity}_checkpoint") \
        .option("table", table_name) \
        .outputMode("append") \
        .start()

    print(f"Data streaming to BigQuery: {table_name}")

# Main process
def process_entity(category, entity_name):
    print(f"Processing data for category: {category}")
    df = read_from_kafka()  # Read data from Kafka
    transformed_df = transform_data(df)  # Apply transformations
    save_to_bigquery(transformed_df, entity_name)  # Save data to BigQuery

if __name__ == "__main__":
    entities = {
        "hospital": "hospital",
        "ngo": "ngo",
        "pharma": "pharma",
        "association": "association",
        "Avenue Healthcare": "avenue",
        "CCARE E-LEARNING PORTAL": "ccare"
    }

    for category, entity_name in entities.items():
        process_entity(category, entity_name)

    spark.streams.awaitAnyTermination()
