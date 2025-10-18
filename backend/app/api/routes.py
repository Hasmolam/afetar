from flask import Blueprint, jsonify, request
from app.extentions import db
from app.models import User, UserProfile, EmergencyContact, LocationPoint, HelpRequest, NeedType, RequestedNeed
from datetime import datetime
from sqlalchemy import func, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, create_refresh_token, 
    jwt_required, get_jwt_identity
)

# API Blueprint oluştur
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')


@api_bp.route('/test')
def test():
    """API test endpoint'i"""
    return jsonify({
        'message': 'API çalışıyor!',
        'endpoint': '/api/v1/test'
    })


# Authentication endpoint'leri
@api_bp.route('/auth/register', methods=['POST'])
def register():
    """Yeni kullanıcı kaydı (JWT token ile)"""
    data = request.get_json()
    
    if not data or not data.get('phone_number') or not data.get('password'):
        return jsonify({'error': 'Telefon numarası ve şifre gereklidir'}), 400
    
    # Kullanıcı zaten var mı kontrol et
    existing_user = User.query.filter_by(phone_number=data['phone_number']).first()
    if existing_user:
        return jsonify({'error': 'Bu telefon numarası zaten kayıtlı'}), 409
    
    # Yeni kullanıcı oluştur
    new_user = User(
        phone_number=data['phone_number'],
        password_hash=generate_password_hash(data['password']),
        is_phone_verified=data.get('is_phone_verified', False),
        is_volunteer_mode_active=data.get('is_volunteer_mode_active', False)
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    # JWT token'ları oluştur (identity string olmalı)
    access_token = create_access_token(identity=str(new_user.id))
    refresh_token = create_refresh_token(identity=str(new_user.id))
    
    return jsonify({
        'message': 'Kullanıcı başarıyla oluşturuldu',
        'user': {
            'id': new_user.id,
            'phone_number': new_user.phone_number,
            'is_phone_verified': new_user.is_phone_verified,
            'is_volunteer_mode_active': new_user.is_volunteer_mode_active,
            'created_at': new_user.created_at.isoformat() if new_user.created_at else None
        },
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 201


@api_bp.route('/auth/login', methods=['POST'])
def login():
    """Kullanıcı girişi (JWT token alır)"""
    data = request.get_json()
    
    if not data or not data.get('phone_number') or not data.get('password'):
        return jsonify({'error': 'Telefon numarası ve şifre gereklidir'}), 400
    
    # Kullanıcıyı bul
    user = User.query.filter_by(phone_number=data['phone_number']).first()
    
    # Kullanıcı yok veya şifre yanlış
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Telefon numarası veya şifre hatalı'}), 401
    
    # JWT token'ları oluştur (identity string olmalı)
    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))
    
    return jsonify({
        'message': 'Giriş başarılı',
        'user': {
            'id': user.id,
            'phone_number': user.phone_number,
            'is_phone_verified': user.is_phone_verified,
            'is_volunteer_mode_active': user.is_volunteer_mode_active
        },
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200


@api_bp.route('/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh token ile yeni access token al"""
    current_user_id = int(get_jwt_identity())
    new_access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'access_token': new_access_token
    }), 200


@api_bp.route('/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Mevcut kullanıcının bilgilerini getir (JWT korumalı)"""
    current_user_id = int(get_jwt_identity())  # String'den int'e çevir
    user = User.query.get_or_404(current_user_id)
    
    return jsonify({
        'id': user.id,
        'phone_number': user.phone_number,
        'is_phone_verified': user.is_phone_verified,
        'is_volunteer_mode_active': user.is_volunteer_mode_active,
        'created_at': user.created_at.isoformat() if user.created_at else None
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


@api_bp.route('/users', methods=['POST'])
def create_user():
    """Yeni kullanıcı oluştur (kayıt)"""
    data = request.get_json()
    
    if not data or not data.get('phone_number') or not data.get('password'):
        return jsonify({'error': 'Telefon numarası ve şifre gereklidir'}), 400
    
    # Kullanıcı zaten var mı kontrol et
    existing_user = User.query.filter_by(phone_number=data['phone_number']).first()
    if existing_user:
        return jsonify({'error': 'Bu telefon numarası zaten kayıtlı'}), 409
    
    # Yeni kullanıcı oluştur
    new_user = User(
        phone_number=data['phone_number'],
        password_hash=generate_password_hash(data['password']),
        is_phone_verified=data.get('is_phone_verified', False),
        is_volunteer_mode_active=data.get('is_volunteer_mode_active', False)
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'id': new_user.id,
        'phone_number': new_user.phone_number,
        'is_phone_verified': new_user.is_phone_verified,
        'is_volunteer_mode_active': new_user.is_volunteer_mode_active,
        'created_at': new_user.created_at.isoformat() if new_user.created_at else None
    }), 201


@api_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Kullanıcı bilgilerini güncelle"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'is_phone_verified' in data:
        user.is_phone_verified = data['is_phone_verified']
    if 'is_volunteer_mode_active' in data:
        user.is_volunteer_mode_active = data['is_volunteer_mode_active']
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    
    db.session.commit()
    
    return jsonify({
        'id': user.id,
        'phone_number': user.phone_number,
        'is_phone_verified': user.is_phone_verified,
        'is_volunteer_mode_active': user.is_volunteer_mode_active
    })


@api_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Kullanıcıyı sil"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'Kullanıcı silindi'}), 200


@api_bp.route('/users/<int:user_id>/volunteer-mode', methods=['POST'])
@jwt_required()
def toggle_volunteer_mode(user_id):
    """Gönüllü modunu aç/kapat (Ö-3: Gönüllü Modu Aktivasyonu)"""
    current_user_id = int(get_jwt_identity())
    
    # Kullanıcı sadece kendi bilgilerini güncelleyebilir
    if current_user_id != user_id:
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    user.is_volunteer_mode_active = data.get('is_active', not user.is_volunteer_mode_active)
    db.session.commit()
    
    return jsonify({
        'user_id': user.id,
        'is_volunteer_mode_active': user.is_volunteer_mode_active,
        'message': 'Gönüllü modu güncellendi'
    })


# Kullanıcı profili endpoint'leri
@api_bp.route('/users/<int:user_id>/profile', methods=['GET'])
@jwt_required()
def get_user_profile(user_id):
    """Kullanıcı profilini getir"""
    current_user_id = int(get_jwt_identity())
    
    # Kullanıcı sadece kendi profilini görebilir
    if current_user_id != user_id:
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    profile = UserProfile.query.get_or_404(user_id)
    return jsonify({
        'user_id': profile.user_id,
        'full_name': profile.full_name,
        'blood_type': profile.blood_type,
        'chronic_diseases': profile.chronic_diseases,
        'medications': profile.medications,
        'allergies': profile.allergies,
        'home_address_text': profile.home_address_text
    })


@api_bp.route('/users/<int:user_id>/profile', methods=['POST', 'PUT'])
@jwt_required()
def create_or_update_profile(user_id):
    """Kullanıcı profili oluştur veya güncelle"""
    current_user_id = int(get_jwt_identity())
    
    # Kullanıcı sadece kendi profilini güncelleyebilir
    if current_user_id != user_id:
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    profile = UserProfile.query.get(user_id)
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.session.add(profile)
    
    profile.full_name = data.get('full_name', profile.full_name)
    profile.blood_type = data.get('blood_type', profile.blood_type)
    profile.chronic_diseases = data.get('chronic_diseases', profile.chronic_diseases)
    profile.medications = data.get('medications', profile.medications)
    profile.allergies = data.get('allergies', profile.allergies)
    profile.home_address_text = data.get('home_address_text', profile.home_address_text)
    
    db.session.commit()
    
    return jsonify({
        'user_id': profile.user_id,
        'full_name': profile.full_name,
        'blood_type': profile.blood_type,
        'message': 'Profil güncellendi'
    })


# Acil durum iletişim endpoint'leri
@api_bp.route('/users/<int:user_id>/emergency-contacts', methods=['GET'])
@jwt_required()
def get_emergency_contacts(user_id):
    """Kullanıcının acil durum kişilerini getir"""
    current_user_id = int(get_jwt_identity())
    
    # Kullanıcı sadece kendi kişilerini görebilir
    if current_user_id != user_id:
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    user = User.query.get_or_404(user_id)
    contacts = EmergencyContact.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'count': len(contacts),
        'contacts': [{
            'id': c.id,
            'contact_name': c.contact_name,
            'contact_phone_number': c.contact_phone_number
        } for c in contacts]
    })


@api_bp.route('/users/<int:user_id>/emergency-contacts', methods=['POST'])
@jwt_required()
def add_emergency_contact(user_id):
    """Yeni acil durum kişisi ekle"""
    current_user_id = int(get_jwt_identity())
    
    # Kullanıcı sadece kendi listesine ekleyebilir
    if current_user_id != user_id:
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if not data.get('contact_name') or not data.get('contact_phone_number'):
        return jsonify({'error': 'İsim ve telefon numarası gereklidir'}), 400
    
    contact = EmergencyContact(
        user_id=user_id,
        contact_name=data['contact_name'],
        contact_phone_number=data['contact_phone_number']
    )
    
    db.session.add(contact)
    db.session.commit()
    
    return jsonify({
        'id': contact.id,
        'contact_name': contact.contact_name,
        'contact_phone_number': contact.contact_phone_number,
        'message': 'Acil durum kişisi eklendi'
    }), 201


@api_bp.route('/emergency-contacts/<int:contact_id>', methods=['PUT'])
@jwt_required()
def update_emergency_contact(contact_id):
    """Acil durum kişisini güncelle"""
    contact = EmergencyContact.query.get_or_404(contact_id)
    current_user_id = int(get_jwt_identity())
    
    # Kullanıcı sadece kendi kişisini güncelleyebilir
    if contact.user_id != current_user_id:
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    data = request.get_json()
    
    contact.contact_name = data.get('contact_name', contact.contact_name)
    contact.contact_phone_number = data.get('contact_phone_number', contact.contact_phone_number)
    
    db.session.commit()
    
    return jsonify({
        'id': contact.id,
        'contact_name': contact.contact_name,
        'contact_phone_number': contact.contact_phone_number,
        'message': 'Kişi güncellendi'
    })


@api_bp.route('/emergency-contacts/<int:contact_id>', methods=['DELETE'])
@jwt_required()
def delete_emergency_contact(contact_id):
    """Acil durum kişisini sil"""
    contact = EmergencyContact.query.get_or_404(contact_id)
    current_user_id = int(get_jwt_identity())
    
    # Kullanıcı sadece kendi kişisini silebilir
    if contact.user_id != current_user_id:
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    db.session.delete(contact)
    db.session.commit()
    
    return jsonify({'message': 'Acil durum kişisi silindi'}), 200


# Yardım talepleri endpoint'leri
@api_bp.route('/help-requests', methods=['GET'])
def get_help_requests():
    """Tüm yardım taleplerini listele"""
    status_filter = request.args.get('status')
    
    query = HelpRequest.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    requests = query.order_by(HelpRequest.created_at.desc()).all()
    
    return jsonify({
        'count': len(requests),
        'requests': [{
            'id': r.id,
            'requester_id': r.requester_id,
            'volunteer_id': r.volunteer_id,
            'status': r.status,
            'latitude': float(r.latitude) if r.latitude else None,
            'longitude': float(r.longitude) if r.longitude else None,
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'updated_at': r.updated_at.isoformat() if r.updated_at else None,
            'needs': [{
                'need_type_id': need.need_type_id,
                'need_name': need.need_type.name,
                'quantity': need.quantity,
                'status': need.status,
                'notes': need.notes
            } for need in r.requested_needs]
        } for r in requests]
    })


@api_bp.route('/help-requests/<int:request_id>', methods=['GET'])
def get_help_request(request_id):
    """Belirli bir yardım talebini getir"""
    help_request = HelpRequest.query.get_or_404(request_id)
    
    return jsonify({
        'id': help_request.id,
        'requester_id': help_request.requester_id,
        'volunteer_id': help_request.volunteer_id,
        'status': help_request.status,
        'latitude': float(help_request.latitude),
        'longitude': float(help_request.longitude),
        'created_at': help_request.created_at.isoformat() if help_request.created_at else None,
        'updated_at': help_request.updated_at.isoformat() if help_request.updated_at else None,
        'needs': [{
            'id': need.id,
            'need_type_id': need.need_type_id,
            'need_name': need.need_type.name,
            'quantity': need.quantity,
            'status': need.status,
            'notes': need.notes
        } for need in help_request.requested_needs]
    })


@api_bp.route('/help-requests', methods=['POST'])
@jwt_required()
def create_help_request():
    """Yeni yardım talebi oluştur (Ö-1: SOS Butonu)"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not data.get('requester_id') or not data.get('latitude') or not data.get('longitude'):
        return jsonify({'error': 'requester_id, latitude ve longitude gereklidir'}), 400
    
    # Kullanıcı sadece kendi adına talep oluşturabilir
    if current_user_id != data.get('requester_id'):
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    # Yardım talebini oluştur
    help_request = HelpRequest(
        requester_id=data['requester_id'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        status='bekliyor'
    )
    
    db.session.add(help_request)
    db.session.flush()  # ID'yi almak için
    
    # İhtiyaçları ekle
    if data.get('needs'):
        for need_data in data['needs']:
            requested_need = RequestedNeed(
                help_request_id=help_request.id,
                need_type_id=need_data['need_type_id'],
                quantity=need_data.get('quantity', 1),
                notes=need_data.get('notes', '')
            )
            db.session.add(requested_need)
    
    db.session.commit()
    
    return jsonify({
        'id': help_request.id,
        'requester_id': help_request.requester_id,
        'status': help_request.status,
        'latitude': float(help_request.latitude),
        'longitude': float(help_request.longitude),
        'created_at': help_request.created_at.isoformat(),
        'message': 'Yardım çağrısı oluşturuldu'
    }), 201


@api_bp.route('/help-requests/<int:request_id>', methods=['PUT'])
def update_help_request(request_id):
    """Yardım talebini güncelle (Ö-2: Durum Güncellemesi)"""
    help_request = HelpRequest.query.get_or_404(request_id)
    data = request.get_json()
    
    if 'status' in data:
        help_request.status = data['status']
    if 'volunteer_id' in data:
        help_request.volunteer_id = data['volunteer_id']
    
    help_request.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'id': help_request.id,
        'status': help_request.status,
        'volunteer_id': help_request.volunteer_id,
        'updated_at': help_request.updated_at.isoformat(),
        'message': 'Yardım talebi güncellendi'
    })


@api_bp.route('/help-requests/<int:request_id>/assign', methods=['POST'])
@jwt_required()
def assign_volunteer(request_id):
    """Gönüllüyü yardım talebine ata (Ö-5: Çağrıyı Üstlenme)"""
    current_user_id = int(get_jwt_identity())
    help_request = HelpRequest.query.get_or_404(request_id)
    data = request.get_json()
    
    if not data.get('volunteer_id'):
        return jsonify({'error': 'volunteer_id gereklidir'}), 400
    
    # Kullanıcı sadece kendini atayabilir
    if current_user_id != data.get('volunteer_id'):
        return jsonify({'error': 'Sadece kendinizi atayabilirsiniz'}), 403
    
    # Gönüllünün var olduğunu ve gönüllü modunun aktif olduğunu kontrol et
    volunteer = User.query.get_or_404(data['volunteer_id'])
    if not volunteer.is_volunteer_mode_active:
        return jsonify({'error': 'Gönüllü modu aktif değil'}), 400
    
    # Talebin zaten atanmış olup olmadığını kontrol et
    if help_request.volunteer_id and help_request.status == 'gönüllü_atandı':
        return jsonify({'error': 'Bu talep zaten bir gönüllüye atanmış'}), 409
    
    help_request.volunteer_id = data['volunteer_id']
    help_request.status = 'gönüllü_atandı'
    help_request.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'id': help_request.id,
        'volunteer_id': help_request.volunteer_id,
        'status': help_request.status,
        'message': 'Gönüllü atandı'
    })


@api_bp.route('/help-requests/<int:request_id>/complete', methods=['POST'])
@jwt_required()
def complete_help_request(request_id):
    """Yardım talebini tamamla"""
    current_user_id = int(get_jwt_identity())
    help_request = HelpRequest.query.get_or_404(request_id)
    
    # Kullanıcı sadece kendi talebi veya atandığı talebi tamamlayabilir
    if current_user_id != help_request.requester_id and current_user_id != help_request.volunteer_id:
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    help_request.status = 'tamamlandı'
    help_request.updated_at = datetime.utcnow()
    
    # Tüm ihtiyaçları teslim edildi olarak işaretle
    for need in help_request.requested_needs:
        need.status = 'teslim_edildi'
    
    db.session.commit()
    
    return jsonify({
        'id': help_request.id,
        'status': help_request.status,
        'message': 'Yardım talebi tamamlandı'
    })


@api_bp.route('/help-requests/<int:request_id>/cancel', methods=['POST'])
@jwt_required()
def cancel_help_request(request_id):
    """Yardım talebini iptal et"""
    current_user_id = int(get_jwt_identity())
    help_request = HelpRequest.query.get_or_404(request_id)
    
    # Kullanıcı sadece kendi talebini iptal edebilir
    if current_user_id != help_request.requester_id:
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    help_request.status = 'iptal_edildi'
    help_request.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    return jsonify({
        'id': help_request.id,
        'status': help_request.status,
        'message': 'Yardım talebi iptal edildi'
    })


@api_bp.route('/help-requests/nearby', methods=['GET'])
def get_nearby_help_requests():
    """Yakındaki yardım taleplerini getir (Ö-4: Haritada Görme, Ö-6: Bildirim için)"""
    latitude = request.args.get('latitude', type=float)
    longitude = request.args.get('longitude', type=float)
    radius = request.args.get('radius', default=10, type=float)  # km cinsinden
    
    if not latitude or not longitude:
        return jsonify({'error': 'latitude ve longitude gereklidir'}), 400
    
    # Basit mesafe hesaplama (Haversine formülü yerine yaklaşık hesap)
    # Gerçek üretimde PostGIS veya daha gelişmiş hesaplama kullanılmalı
    # 1 derece yaklaşık 111 km
    lat_range = radius / 111.0
    lon_range = radius / (111.0 * func.cos(func.radians(latitude)))
    
    nearby_requests = HelpRequest.query.filter(
        and_(
            HelpRequest.status == 'bekliyor',
            HelpRequest.latitude.between(latitude - lat_range, latitude + lat_range),
            HelpRequest.longitude.between(longitude - lon_range, longitude + lon_range)
        )
    ).order_by(HelpRequest.created_at.desc()).all()
    
    return jsonify({
        'count': len(nearby_requests),
        'radius_km': radius,
        'requests': [{
            'id': r.id,
            'requester_id': r.requester_id,
            'latitude': float(r.latitude),
            'longitude': float(r.longitude),
            'status': r.status,
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'needs': [{
                'need_name': need.need_type.name,
                'quantity': need.quantity
            } for need in r.requested_needs]
        } for r in nearby_requests]
    })


# Konum noktaları endpoint'leri
@api_bp.route('/locations', methods=['GET'])
def get_locations():
    """Tüm konum noktalarını listele"""
    status_filter = request.args.get('status', 'onaylandi')
    point_type = request.args.get('type')
    
    query = LocationPoint.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if point_type:
        query = query.filter_by(point_type=point_type)
    
    locations = query.all()
    
    return jsonify({
        'count': len(locations),
        'locations': [{
            'id': loc.id,
            'name': loc.name,
            'type': loc.point_type,
            'latitude': float(loc.latitude) if loc.latitude else None,
            'longitude': float(loc.longitude) if loc.longitude else None,
            'status': loc.status,
            'reported_by_user_id': loc.reported_by_user_id,
            'created_at': loc.created_at.isoformat() if loc.created_at else None
        } for loc in locations]
    })


@api_bp.route('/locations', methods=['POST'])
@jwt_required()
def create_location():
    """Yeni konum noktası bildir"""
    current_user_id = int(get_jwt_identity())
    data = request.get_json()
    
    if not all(k in data for k in ['name', 'point_type', 'latitude', 'longitude']):
        return jsonify({'error': 'name, point_type, latitude ve longitude gereklidir'}), 400
    
    location = LocationPoint(
        name=data['name'],
        point_type=data['point_type'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        reported_by_user_id=data.get('reported_by_user_id'),
        status='onay_bekliyor'
    )
    
    db.session.add(location)
    db.session.commit()
    
    return jsonify({
        'id': location.id,
        'name': location.name,
        'type': location.point_type,
        'status': location.status,
        'message': 'Konum noktası bildirildi, onay bekliyor'
    }), 201


@api_bp.route('/locations/<int:location_id>', methods=['GET'])
def get_location(location_id):
    """Belirli bir konum noktasını getir"""
    location = LocationPoint.query.get_or_404(location_id)
    
    return jsonify({
        'id': location.id,
        'name': location.name,
        'type': location.point_type,
        'latitude': float(location.latitude),
        'longitude': float(location.longitude),
        'status': location.status,
        'reported_by_user_id': location.reported_by_user_id,
        'created_at': location.created_at.isoformat() if location.created_at else None
    })


@api_bp.route('/locations/<int:location_id>', methods=['PUT'])
@jwt_required()
def update_location(location_id):
    """Konum noktasını güncelle"""
    current_user_id = int(get_jwt_identity())
    location = LocationPoint.query.get_or_404(location_id)
    
    # Kullanıcı sadece kendi bildirdiği konumu güncelleyebilir
    if location.reported_by_user_id and current_user_id != location.reported_by_user_id:
        return jsonify({'error': 'Yetkiniz yok'}), 403
    
    data = request.get_json()
    
    if 'name' in data:
        location.name = data['name']
    if 'point_type' in data:
        location.point_type = data['point_type']
    if 'status' in data:
        location.status = data['status']
    if 'latitude' in data:
        location.latitude = data['latitude']
    if 'longitude' in data:
        location.longitude = data['longitude']
    
    db.session.commit()
    
    return jsonify({
        'id': location.id,
        'name': location.name,
        'status': location.status,
        'message': 'Konum noktası güncellendi'
    })


@api_bp.route('/locations/<int:location_id>', methods=['DELETE'])
def delete_location(location_id):
    """Konum noktasını sil"""
    location = LocationPoint.query.get_or_404(location_id)
    db.session.delete(location)
    db.session.commit()
    
    return jsonify({'message': 'Konum noktası silindi'}), 200


@api_bp.route('/locations/type/<point_type>', methods=['GET'])
def get_locations_by_type(point_type):
    """Belirli tipteki konumları getir"""
    locations = LocationPoint.query.filter_by(
        point_type=point_type,
        status='onaylandi'
    ).all()
    
    return jsonify({
        'count': len(locations),
        'point_type': point_type,
        'locations': [{
            'id': loc.id,
            'name': loc.name,
            'latitude': float(loc.latitude),
            'longitude': float(loc.longitude)
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


@api_bp.route('/need-types', methods=['POST'])
def create_need_type():
    """Yeni ihtiyaç tipi ekle"""
    data = request.get_json()
    
    if not data.get('name'):
        return jsonify({'error': 'name gereklidir'}), 400
    
    # Aynı isimde ihtiyaç tipi var mı kontrol et
    existing = NeedType.query.filter_by(name=data['name']).first()
    if existing:
        return jsonify({'error': 'Bu ihtiyaç tipi zaten mevcut'}), 409
    
    need_type = NeedType(
        name=data['name'],
        description=data.get('description', '')
    )
    
    db.session.add(need_type)
    db.session.commit()
    
    return jsonify({
        'id': need_type.id,
        'name': need_type.name,
        'description': need_type.description,
        'message': 'İhtiyaç tipi eklendi'
    }), 201


@api_bp.route('/need-types/<int:need_type_id>', methods=['GET'])
def get_need_type(need_type_id):
    """Belirli bir ihtiyaç tipini getir"""
    need_type = NeedType.query.get_or_404(need_type_id)
    
    return jsonify({
        'id': need_type.id,
        'name': need_type.name,
        'description': need_type.description
    })


@api_bp.route('/need-types/<int:need_type_id>', methods=['PUT'])
def update_need_type(need_type_id):
    """İhtiyaç tipini güncelle"""
    need_type = NeedType.query.get_or_404(need_type_id)
    data = request.get_json()
    
    if 'name' in data:
        need_type.name = data['name']
    if 'description' in data:
        need_type.description = data['description']
    
    db.session.commit()
    
    return jsonify({
        'id': need_type.id,
        'name': need_type.name,
        'description': need_type.description,
        'message': 'İhtiyaç tipi güncellendi'
    })


@api_bp.route('/need-types/<int:need_type_id>', methods=['DELETE'])
def delete_need_type(need_type_id):
    """İhtiyaç tipini sil"""
    need_type = NeedType.query.get_or_404(need_type_id)
    db.session.delete(need_type)
    db.session.commit()
    
    return jsonify({'message': 'İhtiyaç tipi silindi'}), 200


# Talep edilen ihtiyaçlar endpoint'leri
@api_bp.route('/help-requests/<int:request_id>/needs', methods=['GET'])
def get_request_needs(request_id):
    """Yardım talebinin ihtiyaçlarını listele"""
    help_request = HelpRequest.query.get_or_404(request_id)
    
    return jsonify({
        'help_request_id': request_id,
        'count': len(help_request.requested_needs),
        'needs': [{
            'id': need.id,
            'need_type_id': need.need_type_id,
            'need_name': need.need_type.name,
            'quantity': need.quantity,
            'status': need.status,
            'notes': need.notes
        } for need in help_request.requested_needs]
    })


@api_bp.route('/help-requests/<int:request_id>/needs', methods=['POST'])
def add_request_need(request_id):
    """Yardım talebine ihtiyaç ekle"""
    help_request = HelpRequest.query.get_or_404(request_id)
    data = request.get_json()
    
    if not data.get('need_type_id'):
        return jsonify({'error': 'need_type_id gereklidir'}), 400
    
    requested_need = RequestedNeed(
        help_request_id=request_id,
        need_type_id=data['need_type_id'],
        quantity=data.get('quantity', 1),
        notes=data.get('notes', ''),
        status='bekleniyor'
    )
    
    db.session.add(requested_need)
    db.session.commit()
    
    return jsonify({
        'id': requested_need.id,
        'need_type_id': requested_need.need_type_id,
        'quantity': requested_need.quantity,
        'status': requested_need.status,
        'message': 'İhtiyaç eklendi'
    }), 201


@api_bp.route('/requested-needs/<int:need_id>', methods=['PUT'])
def update_requested_need(need_id):
    """Talep edilen ihtiyacı güncelle"""
    requested_need = RequestedNeed.query.get_or_404(need_id)
    data = request.get_json()
    
    if 'quantity' in data:
        requested_need.quantity = data['quantity']
    if 'status' in data:
        requested_need.status = data['status']
    if 'notes' in data:
        requested_need.notes = data['notes']
    
    db.session.commit()
    
    return jsonify({
        'id': requested_need.id,
        'quantity': requested_need.quantity,
        'status': requested_need.status,
        'message': 'İhtiyaç güncellendi'
    })


@api_bp.route('/requested-needs/<int:need_id>', methods=['DELETE'])
def delete_requested_need(need_id):
    """Talep edilen ihtiyacı sil"""
    requested_need = RequestedNeed.query.get_or_404(need_id)
    db.session.delete(requested_need)
    db.session.commit()
    
    return jsonify({'message': 'İhtiyaç silindi'}), 200


# Hata yakalama
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Kaynak bulunamadı'}), 404


@api_bp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Sunucu hatası'}), 500
