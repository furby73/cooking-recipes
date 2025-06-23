import os

class Config:
    SECRET_KEY = os.environ.get('SECTET_KEY') or 'you-will-never-guess'