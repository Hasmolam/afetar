# config.py
import os

class Config:
    # Flask uygulamaları için güvenlik anahtarı
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'cok-guclu-bir-anahtar-girmelisin'
    
    # Veritabanı bağlantı adresi
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://kullanici_adi:sifre@localhost/afetar_db'
    
    # SQLAlchemy'nin olay sistemini devre dışı bırakarak performansı artırır
    SQLALCHEMY_TRACK_MODIFICATIONS = False