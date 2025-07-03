import os
from werkzeug.security import generate_password_hash

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'you-will-never-guess')
    ADMIN_PASSWORD_HASH = os.environ.get(
        'ADMIN_PASSWORD_HASH',
        generate_password_hash('yourpassword')
    )
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///recipes.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    S3_ENDPOINT_URL = os.environ.get('S3_ENDPOINT_URL', 'http://minio:9000')
    S3_ACCESS_KEY = os.environ.get('S3_ACCESS_KEY', 'your-access-key')
    S3_SECRET_KEY = os.environ.get('S3_SECRET_KEY', 'your-secret-key')
    S3_BUCKET_NAME = os.environ.get('S3_BUCKET_NAME', 'recipes')
    S3_REGION = os.environ.get('S3_REGION', 'us-east-1')
    S3_SECURE = os.environ.get('S3_SECURE', 'False').lower() == 'true'