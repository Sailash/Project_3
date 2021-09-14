# How many Big data Meetup Events events scheduled in each country?

# To start pyspark shell
# ./pyspark --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2

# To Create output topic
# ./kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic bigDataMeetingOutput

# To run using spark submit
# ./spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 /home/flash/Desktop/rev/activeCities/activeCities.py

# To get data from terminal using kafka consumer
# ./kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic activeCitiesInUsOutput --from-beginning

# Import Required Libraries
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode, to_json, struct, count
from pyspark.sql.types import *

# Created spark session
spark = SparkSession \
    .builder \
    .appName("bigDataMeeting") \
    .getOrCreate()

# Created kafka consumer using spark readStream
raw_df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "meetUpProducer") \
    .option("startingOffsets", "latest") \
    .load() \
    .selectExpr("CAST(value AS STRING)")

# Created Schema for Structured Streaming
schema = StructType(
    [
        StructField("venue", StructType([
            StructField("venue_name", StringType()),
            StructField("lon", FloatType()),
            StructField("lat", FloatType()),
            StructField("venue_id", IntegerType())]
        )), 
        StructField("visibility", StringType()),
        StructField("response", StringType()),
        StructField("guests", IntegerType()),
        StructField("member", StructType([
            StructField("member_id", IntegerType()),
            StructField("photo", StringType()),
            StructField("member_name", StringType()),]
        )),
        StructField("rsvp_id", IntegerType()),
        StructField("mtime", TimestampType()),
        StructField("event", StructType([
            StructField("event_name", StringType()),
            StructField("event_id", StringType()),
            StructField("time", TimestampType()),
            StructField("event_url", StringType()),]
        )),

        StructField("group", StructType([
            StructField("group_topics", ArrayType(
                StructType([
                    StructField("urlkey", StringType()),
                    StructField("topic_name", StringType()),]
                )
            )),
            StructField("group_city", StringType()),
            StructField("group_country", StringType()),
            StructField("group_id", IntegerType()),
            StructField("group_name", StringType()),
            StructField("group_lon", FloatType()),
            StructField("group_urlname", StringType()),
            StructField("group_lat", FloatType()),  
        ])),              
    ]
)

# Applied schema on data
schema_df = raw_df.select(from_json(raw_df.value, schema).alias("data"))

# Selecting the group country and topic array and splitting into separate rows and 
df = schema_df.select(explode(col("data.group.group_topics.urlkey")).alias("topic"), col("data.group.group_country").alias("country"))

# Group by country where topic is big data and get count by country
output = df.filter(col("topic").like("big-data")).groupBy(col("country")).agg(count("*").alias("country_count"))

# Converted the table records to json and changed table the name to "values"
output_df = output.select(to_json(struct(col("*"))).alias("value"))

# Sending the data to kafka brocker
query = output_df.writeStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("checkpointLocation", "/tmp/checkpoint3").outputMode("complete").option("topic", "bigDataMeetingOutput").start()

# Waits for the termination signal from user
query.awaitTermination()
