#!/usr/bin/env python
"""
Flask uygulamasını başlatmak için ana dosya
"""
import os
from dotenv import load_dotenv

# .env dosyasını yükle (import'lardan önce)
load_dotenv()

from app import create_app

# Uygulamayı oluştur
app = create_app()

if __name__ == '__main__':
    # Development modunda çalıştır
    # Production'da gunicorn veya benzeri bir WSGI server kullanılmalı
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
