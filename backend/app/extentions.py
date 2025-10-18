# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Henüz uygulamaya bağlamadan eklenti nesnelerini oluşturuyoruz
db = SQLAlchemy()
migrate = Migrate()