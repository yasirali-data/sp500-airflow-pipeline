import os
import json
import snowflake.connector


def load_to_snowflake():

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

    file_path = "/opt/airflow/scripts/stock_profiles_final.json"

    with open(file_path, "r") as file:
        data = json.load(file)

    if not data:
        raise ValueError("No stock profile data found")

    print(f"Loading {len(data)} records into Snowflake...")
    print(f"Database: {database}")
    print(f"Schema: {schema}")
    print(f"Warehouse: {warehouse}")
    print(f"Role: {role}")

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
        # Select warehouse explicitly
        cursor.execute(f'USE WAREHOUSE "{warehouse}"')

        # Select database explicitly
        cursor.execute(f'USE DATABASE "{database}"')

        # Select schema explicitly
        cursor.execute(f'USE SCHEMA "{schema}"')

        # Create table
        cursor.execute("""
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
        """)

        # Insert records
        for record in data:
            cursor.execute(
                """
                INSERT INTO STOCK_PROFILES (
                    SYMBOL,
                    COMPANY_NAME,
                    PRICE,
                    MARKET_CAP,
                    SECTOR,
                    INDUSTRY,
                    EXCHANGE,
                    DESCRIPTION
                )
                SELECT %s, %s, %s, %s, %s, %s, %s, %s
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


if __name__ == "__main__":
    load_to_snowflake()
