import os
import boto3
from dotenv import load_dotenv

print(' Connecting to AWS... ')
load_dotenv()

s3_client = boto3.client('s3')
bucket_name = os.environ['AWS_BUCKET_NAME']

print(' Inspecting S3 Bucket... ')

try:
    response = s3_client.list_objects(Bucket=bucket_name)

    if 'Contents' in response:
        print(f'\n {'File Path / Key':<50} | {'Size(Bytes)':<15} | {'Last Modified'}')
        print('-' * 85)

        total_size = 0
        file_count = 0

        for obj in response['Contents']:
            file_key = obj['Key']
            file_size = obj['Size']
            last_modified = obj['LastModified']

            total_size += file_size
            file_count += 1

            print(f'\n {file_key:50} | {file_size:<15} | {str(last_modified)} ')

        print('-' * 85)
        print(f'\n Summary: Found {file_count} files totaling {total_size} bytes')
    else:
        print('\n The bucket is currently empty')

except Exception as e:
    print(f' Error connecting to S3 or listing bucket contents: {e}')
