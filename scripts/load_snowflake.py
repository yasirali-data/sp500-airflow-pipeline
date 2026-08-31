import json
import os

import boto3
import snowflake.connector


BUCKET_NAME = "sp500-airflow-pipeline-data"


def load_to_snowflake(s3_key):
    # -------------------------
    # Environment variables
    # -------------------------
    account = os.getenv("SNOWFLAKE_ACCOUNT")
    user = os.getenv("SNOWFLAKE_USER")
    password = os.getenv("SNOWFLAKE_PASSWORD")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
    database = os.getenv("SNOWFLAKE_DATABASE")
    schema = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")
    role = os.getenv("SNOWFLAKE_ROLE")

    required = {
        "SNOWFLAKE_ACCOUNT": account,
        "SNOWFLAKE_USER": user,
        "SNOWFLAKE_PASSWORD": password,
        "SNOWFLAKE_WAREHOUSE": warehouse,
        "SNOWFLAKE_DATABASE": database,
        "SNOWFLAKE_SCHEMA": schema,
        "SNOWFLAKE_ROLE": role,
    }

    missing = [key for key, value in required.items() if not value]

    if missing:
        raise ValueError(
            f"Missing Snowflake environment variables: {missing}"
        )

    # -------------------------
    # Read JSON from S3
    # -------------------------
    print(f"Reading data from s3://{BUCKET_NAME}/{s3_key}")

    s3 = boto3.client("s3")

    response = s3.get_object(
        Bucket=BUCKET_NAME,
        Key=s3_key,
    )

    data = json.loads(
        response["Body"].read().decode("utf-8")
    )

    if not data:
        raise ValueError("No stock profile data found in S3")

    print(f"Loaded {len(data)} records from S3")

    # -------------------------
    # Snowflake connection
    # -------------------------
    conn = snowflake.connector.connect(
        account=account,
        user=user,
        password=password,
        database=database,
        schema=schema,
        role=role,
    )

    cursor = conn.cursor()

    try:
        cursor.execute(f'USE WAREHOUSE "{warehouse}"')
        cursor.execute(f'USE DATABASE "{database}"')
        cursor.execute(f'USE SCHEMA "{schema}"')

        # -------------------------
        # Create table
        # -------------------------
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS STOCK_PROFILES (
                SYMBOL VARCHAR,
                COMPANY_NAME VARCHAR,
                PRICE FLOAT,
                MARKET_CAP FLOAT,
                SECTOR VARCHAR,
                INDUSTRY VARCHAR,
                EXCHANGE VARCHAR,
                DESCRIPTION VARCHAR
            )
            """
        )

        # -------------------------
        # MERGE records
        # Prevent duplicates
        # -------------------------
        for record in data:
            cursor.execute(
                """
                MERGE INTO STOCK_PROFILES AS target
                USING (
                    SELECT
                        %s AS SYMBOL,
                        %s AS COMPANY_NAME,
                        %s AS PRICE,
                        %s AS MARKET_CAP,
                        %s AS SECTOR,
                        %s AS INDUSTRY,
                        %s AS EXCHANGE,
                        %s AS DESCRIPTION
                ) AS source
                ON target.SYMBOL = source.SYMBOL

                WHEN MATCHED THEN UPDATE SET
                    COMPANY_NAME = source.COMPANY_NAME,
                    PRICE = source.PRICE,
                    MARKET_CAP = source.MARKET_CAP,
                    SECTOR = source.SECTOR,
                    INDUSTRY = source.INDUSTRY,
                    EXCHANGE = source.EXCHANGE,
                    DESCRIPTION = source.DESCRIPTION

                WHEN NOT MATCHED THEN INSERT (
                    SYMBOL,
                    COMPANY_NAME,
                    PRICE,
                    MARKET_CAP,
                    SECTOR,
                    INDUSTRY,
                    EXCHANGE,
                    DESCRIPTION
                )
                VALUES (
                    source.SYMBOL,
                    source.COMPANY_NAME,
                    source.PRICE,
                    source.MARKET_CAP,
                    source.SECTOR,
                    source.INDUSTRY,
                    source.EXCHANGE,
                    source.DESCRIPTION
                )
                """,
                (
                    record.get("symbol"),
                    record.get("companyName"),
                    record.get("price"),
                    record.get("marketCap"),
                    record.get("sector"),
                    record.get("industry"),
                    record.get("exchange"),
                    record.get("description"),
                ),
            )

        conn.commit()

        print(
            f"Successfully loaded {len(data)} records into "
            f"{database}.{schema}.STOCK_PROFILES"
        )

    finally:
        cursor.close()
        conn.close()
