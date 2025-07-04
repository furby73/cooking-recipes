import os
import uuid
import json  # Added missing import
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
from app import app
from botocore.client import Config

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=app.config['S3_ENDPOINT_URL'],
        aws_access_key_id=app.config['S3_ACCESS_KEY'],
        aws_secret_access_key=app.config['S3_SECRET_KEY'],
        config=Config(
            signature_version='s3v4',
            s3={'addressing_style': 'path'}
        ),
        verify=False
    )

def create_bucket_if_not_exists():
    s3 = get_s3_client()
    try:
        s3.head_bucket(Bucket=app.config['S3_BUCKET_NAME'])
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == '404':
            try:
                s3.create_bucket(Bucket=app.config['S3_BUCKET_NAME'])
                s3.put_bucket_policy(
                    Bucket=app.config['S3_BUCKET_NAME'],
                    Policy=json.dumps({
                        "Version": "2012-10-17",
                        "Statement": [{
                            "Effect": "Allow",
                            "Principal": "*",
                            "Action": "s3:GetObject",
                            "Resource": f"arn:aws:s3:::{app.config['S3_BUCKET_NAME']}/*"
                        }]
                    })
                )
                app.logger.info(f"Created bucket: {app.config['S3_BUCKET_NAME']}")
            except ClientError as ce:
                app.logger.error(f"Error creating bucket: {ce}")
        else:
            app.logger.error(f"Error checking bucket: {e}")

def upload_file(file_stream, filename, folder):
    s3 = get_s3_client()
    secure_name = secure_filename(filename)
    object_name = f"{folder}/{uuid.uuid4().hex}_{secure_name}"
    
    try:
        s3.upload_fileobj(
            Fileobj=file_stream,
            Bucket=app.config['S3_BUCKET_NAME'],
            Key=object_name
        )
        return f"{app.config['S3_PUBLIC_URL']}/{app.config['S3_BUCKET_NAME']}/{object_name}"
    except ClientError as e:
        app.logger.error(f"S3 upload error: {e}")
        return None

def delete_file(url):
    if not url or app.config['S3_BUCKET_NAME'] not in url:
        return False
    try:
        s3 = get_s3_client()
        object_name = url.split(f"{app.config['S3_BUCKET_NAME']}/", 1)[1]
        s3.delete_object(
            Bucket=app.config['S3_BUCKET_NAME'],
            Key=object_name
        )
        return True
    except (ClientError, IndexError) as e:
        app.logger.error(f"S3 delete error: {e}")
        return False