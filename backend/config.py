# config.py
import os

class Config:
    # Flask uygulamaları için güvenlik anahtarı
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Veritabanı bağlantı adresi
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # SQLAlchemy'nin olay sistemini devre dışı bırakarak performansı artırır
    SQLALCHEMY_TRACK_MODIFICATIONS = False