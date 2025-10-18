# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

# Henüz uygulamaya bağlamadan eklenti nesnelerini oluşturuyoruz
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()