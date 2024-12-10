import json
import boto3
import os  # Import the 'os' module for path handling

# Construct the file path to the JSON configuration file in the "mclass" sub-directory
config_file_path = os.path.join("/home/KIPPNashvilleData/mclass", "config_mclass.json")

# Load AWS credentials from the JSON file
aws_config = json.load(open(config_file_path))["awss3"]
access_key_id = aws_config["access_key_id"]
access_secret_key = aws_config["access_secret_key"]
bucket_name = aws_config["bucket_name"]

s3 = boto3.resource('s3', aws_access_key_id=access_key_id,
                    aws_secret_access_key=access_secret_key,
                   )
s3.meta.client.upload_file('/home/KIPPNashvilleData/mclass/mclass_pm.csv', "kippnashville", "mclass/mclass_pm.csv")
s3.meta.client.upload_file('/home/KIPPNashvilleData/mclass/mclass_bm.csv', "kippnashville", "mclass/mclass_bm.csv")

print("CSVs moved to S3 bucket")
