from pyspark.sql import SparkSession


def main():

    spark = SparkSession.builder \
        .appName("CustomerIdentityResolution") \
        .getOrCreate()


    customer_data = [
        (101, "John", "john@test.com"),
        (102, "David", "david@test.com"),
        (103, "Alex", "alex@test.com")
    ]


    customer_df = spark.createDataFrame(
        customer_data,
        ["contact_id", "name", "email"]
    )


    print("Customer Golden Dataset")

    customer_df.show()


    spark.stop()


if __name__ == "__main__":
    main()
