from flask import Flask
from config import Config
from app.extentions import db, migrate
from dotenv import load_dotenv

def create_app(config_class=Config):
    """
    Flask uygulaması oluşturan factory fonksiyonu.
    Bu pattern sayesinde test ve production ortamları için farklı konfigürasyonlar kullanılabilir.
    """
    load_dotenv()
    # Flask uygulaması oluştur
    app = Flask(__name__)
    
    # Konfigürasyonu yükle
    app.config.from_object(config_class)
    
    # Eklentileri uygulamaya bağla
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Modelleri import et (migration'lar için gerekli)
    from app import models
    
    # API route'larını kaydet
    from app.api import routes
    app.register_blueprint(routes.api_bp)
    
    # Ana sayfa route'u
    @app.route('/')
    def index():
        return {
            'message': 'Afetar API\'ye hoş geldiniz!',
            'version': '1.0',
            'status': 'active'
        }
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200
    
    return app
