# config.py
import os
from datetime import timedelta

class Config:
    # Flask uygulamaları için güvenlik anahtarı
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Veritabanı bağlantı adresi
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # SQLAlchemy'nin olay sistemini devre dışı bırakarak performansı artırır
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_IDENTITY_CLAIM = 'sub'  # JWT standard claim
    JWT_ERROR_MESSAGE_KEY = 'msg'  # Error message key