import sys
import os

spark_path = '/usr/lib/spark2'
sys.path.append(spark_path + "/python/lib/pyspark.zip")
sys.path.append(spark_path + "/python/lib/py4j-0.10.6-src.zip")

os.environ["HADOOP_USER_NAME"] = "wix"

from pyspark.sql import SparkSession
from wixspark import SqlLoader


# Create a spark session
spark = SparkSession \
    .builder \
    .appName("HED_Test") \
    .master("yarn") \
    .getOrCreate()


# editor_headers = load 'wix_html_editor' using SqlQueryLoader(
#     'select site_id, more_data from site_headers
#         where date_updated >= $START_DATE and date_updated < $STOP_DATE
#         and more_data like "%wixCodeAppData%"
#     ', 'true'
# );


df = SqlLoader(spark,"wix_html_editor").load_table("site_headers",
                                                  predicates=[
                                                      'more_data like "%wixCodeAppData%"',
                                                      "date_updated >= BETWEEN '2018-06-01' AND '2018-06-02'"
                                                  ])

df.createOrReplaceTempView("test")
spark.sql("select * from test")


for row in df.rdd.collect():
    print ('--' + str(row))