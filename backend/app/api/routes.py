from flask import Blueprint, jsonify, request
from app.extentions import db
from app.models import User, UserProfile, EmergencyContact, LocationPoint, HelpRequest, NeedType, RequestedNeed

# API Blueprint oluştur
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/test')
def test():
    """API test endpoint'i"""
    return jsonify({
        'message': 'API çalışıyor!',
        'endpoint': '/api/v1/test'
    })


# Kullanıcı endpoint'leri
@api_bp.route('/users', methods=['GET'])
def get_users():
    """Tüm kullanıcıları listele"""
    users = User.query.all()
    return jsonify({
        'count': len(users),
        'users': [{'id': u.id, 'phone_number': u.phone_number} for u in users]
    })


@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Belirli bir kullanıcıyı getir"""
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'phone_number': user.phone_number,
        'is_phone_verified': user.is_phone_verified,
        'is_volunteer_mode_active': user.is_volunteer_mode_active,
        'created_at': user.created_at.isoformat() if user.created_at else None
    })


# Yardım talepleri endpoint'leri
@api_bp.route('/help-requests', methods=['GET'])
def get_help_requests():
    """Tüm yardım taleplerini listele"""
    requests = HelpRequest.query.all()
    return jsonify({
        'count': len(requests),
        'requests': [{
            'id': r.id,
            'status': r.status,
            'latitude': float(r.latitude) if r.latitude else None,
            'longitude': float(r.longitude) if r.longitude else None,
            'created_at': r.created_at.isoformat() if r.created_at else None
        } for r in requests]
    })


# Konum noktaları endpoint'leri
@api_bp.route('/locations', methods=['GET'])
def get_locations():
    """Tüm konum noktalarını listele"""
    locations = LocationPoint.query.filter_by(status='onaylandi').all()
    return jsonify({
        'count': len(locations),
        'locations': [{
            'id': loc.id,
            'name': loc.name,
            'type': loc.point_type,
            'latitude': float(loc.latitude) if loc.latitude else None,
            'longitude': float(loc.longitude) if loc.longitude else None,
            'status': loc.status
        } for loc in locations]
    })


# İhtiyaç tipleri endpoint'leri
@api_bp.route('/need-types', methods=['GET'])
def get_need_types():
    """Tüm ihtiyaç tiplerini listele"""
    need_types = NeedType.query.all()
    return jsonify({
        'count': len(need_types),
        'need_types': [{
            'id': nt.id,
            'name': nt.name,
            'description': nt.description
        } for nt in need_types]
    })


# Hata yakalama
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Kaynak bulunamadı'}), 404


@api_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Sunucu hatası'}), 500
