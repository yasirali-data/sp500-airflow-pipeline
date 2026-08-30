import boto3
from datetime import date


BUCKET_NAME = "sp500-airflow-pipeline-data"
LOCAL_FILE = "stock_profiles_final.json"


def upload_to_s3():

    s3 = boto3.client("s3")

    today = date.today().isoformat()

    s3_key = f"raw/{today}/stock_profiles.json"

    s3.upload_file(
        LOCAL_FILE,
        BUCKET_NAME,
        s3_key
    )

    print(f"Uploaded to s3://{BUCKET_NAME}/{s3_key}")


if __name__ == "__main__":
    upload_to_s3()