import org.apache.spark.sql.{Dataset, SaveMode, SparkSession}
import org.apache.spark.sql.functions._

object Team09 extends App {
  val spark = SparkSession.builder()
    //    .master("local[*]")
    //    .config("hive.metastore.uris", "thrift://master3:3306")
    .enableHiveSupport()
    .getOrCreate()

  import org.apache.spark.sql.{Dataset, SaveMode, SparkSession}
  import org.apache.spark.sql.types._

  val df2 = spark.
    readStream.
    format("kafka").
    option("kafka.bootstrap.servers", "13.124.248.100:19094,13.124.248.100:29094,13.124.248.100:39094").
    option("subscribe", "kfk-pollution").
    load()

  val schema2 = StructType(Array(
    StructField("date", StringType),
    StructField("hour", StringType),
    StructField("spot", StringType),
    StructField("PM10", StringType),
    StructField("PM25", StringType),
    StructField("O3", StringType),
    StructField("NO2", StringType),
    StructField("CO", StringType),
    StructField("SO2", StringType)
  ))

  val streamDf2 = df2.
    withColumn("value", from_json(col("value").cast("string"), schema2)).
    select(col("value.*")).
    withColumn("ymd", col("date")).
    withColumn("pm10", col("PM10")).
    withColumn("pm25", col("PM25")).
    withColumn("o3", col("O3")).
    withColumn("no2", col("NO2")).
    withColumn("co", col("CO")).
    withColumn("so2", col("SO2")).
    select(col("ymd"), col("hour"), col("spot"), col("pm10"), col("pm25"), col("o3"), col("no2"), col("co"), col("so2"))

  streamDf2.writeStream.outputMode("append").format("console").start()

  spark.sql("CREATE TABLE if not exists pollution (ymd STRING, hour STRING, spot STRING, pm10 STRING, pm25 STRING, o3 STRING, no2 STRING, co STRING, so2 STRING) STORED AS ORC LOCATION '/user/ubuntu/hive/pollution'")

  val query2 = streamDf2.writeStream.foreachBatch((batchDs: Dataset[_], batchId: Long) => {
    batchDs
      .write
      .mode(SaveMode.Append)
      .insertInto("pollution");
  }).start()


  val df = spark.
    readStream.
    format("kafka").
    option("kafka.bootstrap.servers", "13.124.248.100:19094,13.124.248.100:29094,13.124.248.100:39094").
    option("subscribe", "kfk-traffic").
    load()

  val schema = StructType(Array(
    StructField("date", StringType),
    StructField("hour", StringType),
    StructField("spot", StringType),
    StructField("vol", StringType),
  ))

  val streamDf = df.
    withColumn("value", from_json(col("value").cast("string"), schema)).
    select(col("value.*")).
    withColumn("ymd", col("date")).
    select(col("ymd"), col("hour"), col("spot"), col("vol"))

  streamDf.writeStream.outputMode("append").format("console").start()

  spark.sql("CREATE TABLE if not exists traffic (ymd STRING, hour STRING, spot STRING, vol STRING) STORED AS ORC LOCATION '/user/ubuntu/hive/traffic'")

  val query = streamDf.writeStream.foreachBatch((batchDs: Dataset[_], batchId: Long) => {
    batchDs
      .write
      .mode(SaveMode.Append)
      .insertInto("traffic");
  }).start()

  query2.awaitTermination()
  query.awaitTermination()
}
