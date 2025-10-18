from datetime import datetime
from app.extentions import db


class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_phone_verified = db.Column(db.Boolean, nullable=False, default=False)
    is_volunteer_mode_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # İlişkiler
    profile = db.relationship('UserProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    emergency_contacts = db.relationship('EmergencyContact', backref='user', cascade='all, delete-orphan')
    reported_locations = db.relationship('LocationPoint', backref='reporter', foreign_keys='LocationPoint.reported_by_user_id')
    help_requests = db.relationship('HelpRequest', backref='requester', foreign_keys='HelpRequest.requester_id')
    volunteered_requests = db.relationship('HelpRequest', backref='volunteer', foreign_keys='HelpRequest.volunteer_id')
    
    def __repr__(self):
        return f'<User {self.phone_number}>'


class UserProfile(db.Model):
    __tablename__ = 'user_profile'
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    full_name = db.Column(db.String(100))
    blood_type = db.Column(db.String(3))  # Örn: 'A+', 'B-', 'AB+'
    chronic_diseases = db.Column(db.Text)  # Kronik hastalıklar
    medications = db.Column(db.Text)  # Düzenli kullanılan ilaçlar
    allergies = db.Column(db.Text)  # Bilinen alerjiler
    home_address_text = db.Column(db.Text)  # Opsiyonel adres bilgisi
    
    def __repr__(self):
        return f'<UserProfile {self.full_name}>'


class EmergencyContact(db.Model):
    __tablename__ = 'emergency_contact'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contact_name = db.Column(db.String(100), nullable=False)
    contact_phone_number = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'<EmergencyContact {self.contact_name}>'


class LocationPoint(db.Model):
    __tablename__ = 'location_point'
    
    id = db.Column(db.Integer, primary_key=True)
    point_type = db.Column(db.String(50), nullable=False)  # 'toplanma_alani', 'dagitim_noktasi', 'guvenli_bolge', 'mobil_hastane'
    name = db.Column(db.String(200), nullable=False)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='onay_bekliyor')  # 'onay_bekliyor', 'onaylandi', 'hizmet_disi'
    reported_by_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<LocationPoint {self.name}>'


class HelpRequest(db.Model):
    __tablename__ = 'help_request'
    
    id = db.Column(db.Integer, primary_key=True)
    requester_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    latitude = db.Column(db.Numeric(10, 8), nullable=False)
    longitude = db.Column(db.Numeric(11, 8), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='bekliyor')  # 'bekliyor', 'gönüllü_atandı', 'tamamlandı', 'iptal_edildi'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    requested_needs = db.relationship('RequestedNeed', backref='help_request', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<HelpRequest {self.id} - {self.status}>'


class NeedType(db.Model):
    __tablename__ = 'need_type'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    
    # İlişkiler
    requested_needs = db.relationship('RequestedNeed', backref='need_type')
    
    def __repr__(self):
        return f'<NeedType {self.name}>'


class RequestedNeed(db.Model):
    __tablename__ = 'requested_need'
    
    id = db.Column(db.Integer, primary_key=True)
    help_request_id = db.Column(db.Integer, db.ForeignKey('help_request.id'), nullable=False)
    need_type_id = db.Column(db.Integer, db.ForeignKey('need_type.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='bekleniyor')  # 'bekleniyor', 'yolda', 'teslim_edildi'
    quantity = db.Column(db.Integer, nullable=False, default=1)
    notes = db.Column(db.Text)  # Ek detaylar, örn: 'Bebek maması 0-6 ay için'
    
    def __repr__(self):
        return f'<RequestedNeed {self.id} - {self.status}>'
