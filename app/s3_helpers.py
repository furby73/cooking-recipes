import os
import uuid
import boto3
from botocore.exceptions import ClientError
from werkzeug.utils import secure_filename
from app import app

def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=app.config['S3_ENDPOINT_URL'],
        aws_access_key_id=app.config['S3_ACCESS_KEY'],
        aws_secret_access_key=app.config['S3_SECRET_KEY'],
        region_name=app.config['S3_REGION'],
        verify=app.config['S3_SECURE']
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
            except ClientError as ce:
                app.logger.error(f"Error creating bucket: {ce}")
                raise
        else:
            app.logger.error(f"S3 bucket check error: {e}")
            raise

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
        
        if app.config['S3_ENDPOINT_URL']:
            return f"{app.config['S3_ENDPOINT_URL']}/{app.config['S3_BUCKET_NAME']}/{object_name}"
        else:
            return f"https://{app.config['S3_BUCKET_NAME']}.s3.{app.config['S3_REGION']}.amazonaws.com/{object_name}"
    except ClientError as e:
        app.logger.error(f"S3 upload error: {e}")
        return None

def delete_file(url):
    if not url or not app.config['S3_BUCKET_NAME'] in url:
        return False
    
    try:
        s3 = get_s3_client()
        object_name = url.split(f"{app.config['S3_BUCKET_NAME']}/")[1]
        s3.delete_object(
            Bucket=app.config['S3_BUCKET_NAME'],
            Key=object_name
        )
        return True
    except ClientError as e:
        app.logger.error(f"S3 delete error: {e}")
        return False