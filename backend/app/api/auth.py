"""
Authentication helper functions
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models import User


def admin_required():
    """
    Admin yetkisi gerektiren endpoint'ler için decorator
    Gelecekte User modeline role field eklendiğinde kullanılacak
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            # Şimdilik basit bir kontrol, gelecekte role kontrolü eklenebilir
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def get_current_user():
    """
    JWT token'dan mevcut kullanıcıyı döndürür
    """
    user_id = get_jwt_identity()
    return User.query.get(user_id)
