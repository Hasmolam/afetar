# JWT Authentication Sistemi

## Genel Bakış

AFETAR API'si JWT (JSON Web Token) tabanlı kimlik doğrulama kullanmaktadır. Kullanıcılar sisteme kayıt olup giriş yaparak access token ve refresh token alırlar.

## Token Yapısı

### Access Token
- **Süre**: 1 saat
- **Kullanım**: API isteklerinde kimlik doğrulama için
- **Header**: `Authorization: Bearer <access_token>`

### Refresh Token
- **Süre**: 30 gün
- **Kullanım**: Access token'ın yenilenmesi için
- **Endpoint**: `/api/auth/refresh`

## Authentication Endpoints

### 1. Kayıt Ol (Register)
```http
POST /api/auth/register
Content-Type: application/json

{
    "phone_number": "5551234567",
    "password": "güvenli_şifre",
    "full_name": "Ahmet Yılmaz"
}
```

**Yanıt:**
```json
{
    "message": "Kullanıcı başarıyla oluşturuldu",
    "user_id": 1,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 2. Giriş Yap (Login)
```http
POST /api/auth/login
Content-Type: application/json

{
    "phone_number": "5551234567",
    "password": "güvenli_şifre"
}
```

**Yanıt:**
```json
{
    "message": "Giriş başarılı",
    "user_id": 1,
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 3. Token Yenile (Refresh)
```http
POST /api/auth/refresh
Authorization: Bearer <refresh_token>
```

**Yanıt:**
```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### 4. Mevcut Kullanıcı (Current User)
```http
GET /api/auth/me
Authorization: Bearer <access_token>
```

**Yanıt:**
```json
{
    "user_id": 1,
    "phone_number": "5551234567",
    "is_volunteer_mode_active": false,
    "created_at": "2024-01-15T10:30:00"
}
```

## Korumalı Endpoint'ler

### 🔒 Authentication Gerektiren Endpoint'ler

#### Kullanıcı İşlemleri
- `POST /users/<user_id>/volunteer-mode` - Gönüllü modu aç/kapat
- `GET /users/<user_id>/profile` - Profil görüntüle
- `POST /users/<user_id>/profile` - Profil oluştur/güncelle
- `PUT /users/<user_id>/profile` - Profil güncelle

#### Acil Durum Kişileri
- `GET /users/<user_id>/emergency-contacts` - Kişileri listele
- `POST /users/<user_id>/emergency-contacts` - Kişi ekle
- `PUT /emergency-contacts/<contact_id>` - Kişi güncelle
- `DELETE /emergency-contacts/<contact_id>` - Kişi sil

#### Yardım Talepleri
- `POST /help-requests` - Yeni talep oluştur (SOS butonu)
- `POST /help-requests/<request_id>/assign` - Gönüllü olarak üstlen
- `POST /help-requests/<request_id>/complete` - Talebi tamamla
- `POST /help-requests/<request_id>/cancel` - Talebi iptal et

#### Konum Bildirimi
- `POST /locations` - Yeni konum bildir
- `PUT /locations/<location_id>` - Konum güncelle

### 🔓 Public Endpoint'ler (Authentication Gerektirmeyen)

#### Kullanıcı Bilgileri
- `GET /users` - Kullanıcı listesi
- `POST /users` - Yeni kullanıcı oluştur (deprecated, /auth/register kullanın)
- `GET /users/<user_id>` - Kullanıcı bilgisi

#### Yardım Talepleri (Görüntüleme)
- `GET /help-requests` - Talep listesi
- `GET /help-requests/<request_id>` - Talep detayı
- `GET /help-requests/nearby` - Yakındaki talepler (harita için)

#### Konum Noktaları (Görüntüleme)
- `GET /locations` - Konum listesi
- `GET /locations/<location_id>` - Konum detayı
- `GET /locations/type/<point_type>` - Tip bazında konumlar

#### İhtiyaç Tipleri
- `GET /need-types` - Tip listesi
- `GET /need-types/<need_type_id>` - Tip detayı
- `POST /need-types` - Yeni tip ekle (gelecekte admin kontrolü eklenebilir)
- `PUT /need-types/<need_type_id>` - Tip güncelle (gelecekte admin kontrolü eklenebilir)
- `DELETE /need-types/<need_type_id>` - Tip sil (gelecekte admin kontrolü eklenebilir)

## Yetkilendirme (Authorization) Kuralları

### Kullanıcı Bazlı Kısıtlamalar

1. **Kendi Verisini Değiştirme**
   - Kullanıcılar sadece kendi profillerini düzenleyebilir
   - Kullanıcılar sadece kendi acil durum kişilerini yönetebilir
   - Kullanıcılar sadece kendi adlarına yardım talebi oluşturabilir

2. **Gönüllü İşlemleri**
   - Gönüllüler sadece kendilerini taleplere atayabilir
   - Gönüllü modu aktif olmalıdır

3. **Talep Yönetimi**
   - Talebi oluşturan veya üstlenen gönüllü tamamlayabilir
   - Sadece talebi oluşturan iptal edebilir

4. **Konum Bildirimi**
   - Kullanıcılar sadece kendi bildirdikleri konumları güncelleyebilir

## Hata Kodları

### 401 Unauthorized
```json
{
    "msg": "Missing Authorization Header"
}
```
Token gönderilmemiş.

### 403 Forbidden
```json
{
    "error": "Yetkiniz yok"
}
```
Kullanıcı bu işlemi yapmaya yetkili değil.

### 422 Unprocessable Entity
```json
{
    "msg": "Signature verification failed"
}
```
Token geçersiz veya süresi dolmuş.

## Kullanım Örnekleri

### Python ile İstek Gönderme

```python
import requests

# 1. Giriş yap
login_response = requests.post('http://localhost:5000/api/auth/login', json={
    'phone_number': '5551234567',
    'password': 'şifre'
})
tokens = login_response.json()
access_token = tokens['access_token']

# 2. Korumalı endpoint'e istek gönder
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

profile_response = requests.get(
    'http://localhost:5000/api/users/1/profile',
    headers=headers
)
print(profile_response.json())

# 3. Token yenile (gerekirse)
refresh_token = tokens['refresh_token']
refresh_headers = {
    'Authorization': f'Bearer {refresh_token}'
}
new_token_response = requests.post(
    'http://localhost:5000/api/auth/refresh',
    headers=refresh_headers
)
new_access_token = new_token_response.json()['access_token']
```

### JavaScript (Fetch API) ile İstek

```javascript
// 1. Giriş yap
const loginResponse = await fetch('http://localhost:5000/api/auth/login', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        phone_number: '5551234567',
        password: 'şifre'
    })
});
const tokens = await loginResponse.json();

// 2. Korumalı endpoint'e istek gönder
const profileResponse = await fetch('http://localhost:5000/api/users/1/profile', {
    headers: {
        'Authorization': `Bearer ${tokens.access_token}`
    }
});
const profile = await profileResponse.json();

// 3. Token'ı localStorage'a kaydet
localStorage.setItem('access_token', tokens.access_token);
localStorage.setItem('refresh_token', tokens.refresh_token);
```

### cURL ile İstek

```bash
# 1. Giriş yap
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"5551234567","password":"şifre"}'

# 2. Korumalı endpoint'e istek (token'ı değiştirin)
curl -X GET http://localhost:5000/api/users/1/profile \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."

# 3. Token yenile
curl -X POST http://localhost:5000/api/auth/refresh \
  -H "Authorization: Bearer <refresh_token>"
```

## Güvenlik Notları

1. **Token Güvenliği**
   - Access token'ları güvenli bir yerde saklayın (localStorage, secure cookies)
   - Token'ları URL parametresi olarak göndermeyin
   - HTTPS kullanın (production ortamında zorunlu)

2. **Şifre Güvenliği**
   - Şifreler Werkzeug ile hash'lenir (PBKDF2-SHA256)
   - Şifreler veritabanında açık metin olarak saklanmaz
   - Minimum 6 karakter önerilir

3. **Rate Limiting**
   - Gelecekte eklenecek
   - Login endpoint'inde brute-force saldırılarına karşı

4. **JWT Secret Key**
   - Production'da güçlü ve rastgele bir key kullanın
   - Environment variable olarak saklayın
   - Asla kodda hardcode etmeyin

## Gelecek Geliştirmeler

- [ ] Role-based access control (Admin, Moderator, User)
- [ ] Email doğrulama
- [ ] SMS doğrulama (2FA)
- [ ] Rate limiting
- [ ] IP bazlı engelleme
- [ ] Token blacklist (logout için)
- [ ] Session yönetimi
- [ ] Activity logging
