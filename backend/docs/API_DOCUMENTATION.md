# AFETAR API Endpoint'leri Dokümantasyonu

## 📡 Base URL
```
http://localhost:5000/api/v1
```

---

## 🎯 Genel Endpoint'ler

### Test Endpoint'i
**GET** `/test`

API'nin çalışıp çalışmadığını test eder.

**Response:**
```json
{
  "message": "API çalışıyor!",
  "endpoint": "/api/v1/test"
}
```

---

## 👤 Kullanıcı (User) Endpoint'leri

### Tüm Kullanıcıları Listele
**GET** `/users`

**Response:**
```json
{
  "count": 2,
  "users": [
    {
      "id": 1,
      "phone_number": "+905551234567"
    }
  ]
}
```

### Kullanıcı Detayı
**GET** `/users/<user_id>`

**Response:**
```json
{
  "id": 1,
  "phone_number": "+905551234567",
  "is_phone_verified": true,
  "is_volunteer_mode_active": false,
  "created_at": "2025-10-18T12:00:00"
}
```

### Yeni Kullanıcı Oluştur (Kayıt)
**POST** `/users`

**Request Body:**
```json
{
  "phone_number": "+905551234567",
  "password": "securepassword123",
  "is_phone_verified": false
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "phone_number": "+905551234567",
  "is_phone_verified": false,
  "is_volunteer_mode_active": false,
  "created_at": "2025-10-18T12:00:00"
}
```

### Kullanıcı Güncelle
**PUT** `/users/<user_id>`

**Request Body:**
```json
{
  "is_phone_verified": true,
  "is_volunteer_mode_active": true
}
```

### Kullanıcı Sil
**DELETE** `/users/<user_id>`

**Response:**
```json
{
  "message": "Kullanıcı silindi"
}
```

### Gönüllü Modunu Aç/Kapat (Ö-3)
**POST** `/users/<user_id>/volunteer-mode`

**Request Body:**
```json
{
  "is_active": true
}
```

**Response:**
```json
{
  "user_id": 1,
  "is_volunteer_mode_active": true,
  "message": "Gönüllü modu güncellendi"
}
```

---

## 📝 Kullanıcı Profili (UserProfile) Endpoint'leri

### Profil Getir
**GET** `/users/<user_id>/profile`

**Response:**
```json
{
  "user_id": 1,
  "full_name": "Ahmet Yılmaz",
  "blood_type": "A+",
  "chronic_diseases": "Astım",
  "medications": "İnhaler",
  "allergies": "Fıstık",
  "home_address_text": "İstanbul, Kadıköy"
}
```

### Profil Oluştur veya Güncelle
**POST/PUT** `/users/<user_id>/profile`

**Request Body:**
```json
{
  "full_name": "Ahmet Yılmaz",
  "blood_type": "A+",
  "chronic_diseases": "Astım",
  "medications": "İnhaler",
  "allergies": "Fıstık",
  "home_address_text": "İstanbul, Kadıköy"
}
```

---

## 🚨 Acil Durum Kişileri (EmergencyContact) Endpoint'leri

### Acil Durum Kişilerini Listele
**GET** `/users/<user_id>/emergency-contacts`

**Response:**
```json
{
  "count": 2,
  "contacts": [
    {
      "id": 1,
      "contact_name": "Anne",
      "contact_phone_number": "+905559876543"
    }
  ]
}
```

### Acil Durum Kişisi Ekle
**POST** `/users/<user_id>/emergency-contacts`

**Request Body:**
```json
{
  "contact_name": "Anne",
  "contact_phone_number": "+905559876543"
}
```

**Response:** `201 Created`

### Acil Durum Kişisi Güncelle
**PUT** `/emergency-contacts/<contact_id>`

### Acil Durum Kişisi Sil
**DELETE** `/emergency-contacts/<contact_id>`

---

## 🆘 Yardım Talepleri (HelpRequest) Endpoint'leri

### Tüm Yardım Taleplerini Listele
**GET** `/help-requests`

**Query Parameters:**
- `status` (optional): 'bekliyor', 'gönüllü_atandı', 'tamamlandı', 'iptal_edildi'

**Response:**
```json
{
  "count": 5,
  "requests": [
    {
      "id": 1,
      "requester_id": 1,
      "volunteer_id": null,
      "status": "bekliyor",
      "latitude": 41.0082,
      "longitude": 28.9784,
      "created_at": "2025-10-18T12:00:00",
      "updated_at": "2025-10-18T12:00:00",
      "needs": [
        {
          "need_type_id": 1,
          "need_name": "Gıda",
          "quantity": 2,
          "status": "bekleniyor",
          "notes": "Acil gıda"
        }
      ]
    }
  ]
}
```

### Yardım Talebi Detayı
**GET** `/help-requests/<request_id>`

### Yeni Yardım Talebi Oluştur (Ö-1: SOS Butonu)
**POST** `/help-requests`

**Request Body:**
```json
{
  "requester_id": 1,
  "latitude": 41.0082,
  "longitude": 28.9784,
  "needs": [
    {
      "need_type_id": 1,
      "quantity": 2,
      "notes": "Acil gıda gerekli"
    },
    {
      "need_type_id": 2,
      "quantity": 5,
      "notes": "Su bidonu"
    }
  ]
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "requester_id": 1,
  "status": "bekliyor",
  "latitude": 41.0082,
  "longitude": 28.9784,
  "created_at": "2025-10-18T12:00:00",
  "message": "Yardım çağrısı oluşturuldu"
}
```

### Yardım Talebini Güncelle (Ö-2: Durum Güncellemesi)
**PUT** `/help-requests/<request_id>`

**Request Body:**
```json
{
  "status": "gönüllü_atandı",
  "volunteer_id": 2
}
```

### Gönüllü Ata (Ö-5: Çağrıyı Üstlenme)
**POST** `/help-requests/<request_id>/assign`

**Request Body:**
```json
{
  "volunteer_id": 2
}
```

**Response:**
```json
{
  "id": 1,
  "volunteer_id": 2,
  "status": "gönüllü_atandı",
  "message": "Gönüllü atandı"
}
```

### Yardım Talebini Tamamla
**POST** `/help-requests/<request_id>/complete`

**Response:**
```json
{
  "id": 1,
  "status": "tamamlandı",
  "message": "Yardım talebi tamamlandı"
}
```

### Yardım Talebini İptal Et
**POST** `/help-requests/<request_id>/cancel`

### Yakındaki Yardım Taleplerini Getir (Ö-4: Haritada Görme)
**GET** `/help-requests/nearby`

**Query Parameters:**
- `latitude` (required): Gönüllünün enlemi
- `longitude` (required): Gönüllünün boylamı
- `radius` (optional, default=10): Yarıçap (km)

**Response:**
```json
{
  "count": 3,
  "radius_km": 10,
  "requests": [
    {
      "id": 1,
      "requester_id": 1,
      "latitude": 41.0082,
      "longitude": 28.9784,
      "status": "bekliyor",
      "created_at": "2025-10-18T12:00:00",
      "needs": [
        {
          "need_name": "Gıda",
          "quantity": 2
        }
      ]
    }
  ]
}
```

---

## 📍 Konum Noktaları (LocationPoint) Endpoint'leri

### Konum Noktalarını Listele
**GET** `/locations`

**Query Parameters:**
- `status` (optional, default='onaylandi'): 'onay_bekliyor', 'onaylandi', 'hizmet_disi'
- `type` (optional): 'toplanma_alani', 'dagitim_noktasi', 'guvenli_bolge', 'mobil_hastane'

**Response:**
```json
{
  "count": 10,
  "locations": [
    {
      "id": 1,
      "name": "Merkez Toplanma Alanı",
      "type": "toplanma_alani",
      "latitude": 41.0082,
      "longitude": 28.9784,
      "status": "onaylandi",
      "reported_by_user_id": null,
      "created_at": "2025-10-18T12:00:00"
    }
  ]
}
```

### Konum Noktası Detayı
**GET** `/locations/<location_id>`

### Yeni Konum Noktası Bildir
**POST** `/locations`

**Request Body:**
```json
{
  "name": "Yeni Toplanma Alanı",
  "point_type": "toplanma_alani",
  "latitude": 41.0082,
  "longitude": 28.9784,
  "reported_by_user_id": 1
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "name": "Yeni Toplanma Alanı",
  "type": "toplanma_alani",
  "status": "onay_bekliyor",
  "message": "Konum noktası bildirildi, onay bekliyor"
}
```

### Konum Noktası Güncelle
**PUT** `/locations/<location_id>`

### Konum Noktası Sil
**DELETE** `/locations/<location_id>`

### Tipe Göre Konum Noktalarını Getir
**GET** `/locations/type/<point_type>`

**Örnek:** `/locations/type/toplanma_alani`

---

## 📦 İhtiyaç Tipleri (NeedType) Endpoint'leri

### Tüm İhtiyaç Tiplerini Listele
**GET** `/need-types`

**Response:**
```json
{
  "count": 4,
  "need_types": [
    {
      "id": 1,
      "name": "Gıda",
      "description": "Temel gıda maddeleri"
    },
    {
      "id": 2,
      "name": "Su",
      "description": "İçme suyu"
    }
  ]
}
```

### İhtiyaç Tipi Detayı
**GET** `/need-types/<need_type_id>`

### Yeni İhtiyaç Tipi Ekle
**POST** `/need-types`

**Request Body:**
```json
{
  "name": "Gıda",
  "description": "Temel gıda maddeleri"
}
```

**Response:** `201 Created`

### İhtiyaç Tipi Güncelle
**PUT** `/need-types/<need_type_id>`

### İhtiyaç Tipi Sil
**DELETE** `/need-types/<need_type_id>`

---

## 📋 Talep Edilen İhtiyaçlar (RequestedNeed) Endpoint'leri

### Yardım Talebinin İhtiyaçlarını Listele
**GET** `/help-requests/<request_id>/needs`

**Response:**
```json
{
  "help_request_id": 1,
  "count": 2,
  "needs": [
    {
      "id": 1,
      "need_type_id": 1,
      "need_name": "Gıda",
      "quantity": 2,
      "status": "bekleniyor",
      "notes": "Acil gıda"
    }
  ]
}
```

### Yardım Talebine İhtiyaç Ekle
**POST** `/help-requests/<request_id>/needs`

**Request Body:**
```json
{
  "need_type_id": 1,
  "quantity": 3,
  "notes": "Bebek maması"
}
```

**Response:** `201 Created`

### Talep Edilen İhtiyacı Güncelle
**PUT** `/requested-needs/<need_id>`

**Request Body:**
```json
{
  "quantity": 5,
  "status": "yolda",
  "notes": "Güncellenmiş not"
}
```

### Talep Edilen İhtiyacı Sil
**DELETE** `/requested-needs/<need_id>`

---

## 🎯 MVP Özellikleri ve Karşılık Gelen Endpoint'ler

### Ö-1: Tek Dokunuşla Yardım Çağrısı (SOS Butonu)
- `POST /help-requests` - Yeni yardım talebi oluşturur

### Ö-2: Çağrı Durumu Geri Bildirimi
- `GET /help-requests/<request_id>` - Talep durumunu sorgular
- `PUT /help-requests/<request_id>` - Durumu günceller

### Ö-3: Gönüllü Modu Aktivasyonu
- `POST /users/<user_id>/volunteer-mode` - Gönüllü modunu açar/kapatır

### Ö-4: Yakındaki Çağrıları Haritada Görme
- `GET /help-requests/nearby?latitude=X&longitude=Y&radius=Z` - Yakındaki talepleri getirir

### Ö-5: Çağrıyı Üstlenme ve Navigasyon
- `POST /help-requests/<request_id>/assign` - Gönüllüyü atar

### Ö-6: Proaktif Bildirim Sistemi
- Backend tarafında WebSocket veya Push Notification servisi ile entegre edilmeli
- `/help-requests/nearby` endpoint'i bildirim tetikleyici olarak kullanılabilir

---

## ⚠️ Hata Kodları

- **200 OK**: İstek başarılı
- **201 Created**: Kaynak başarıyla oluşturuldu
- **400 Bad Request**: Geçersiz istek (eksik parametreler)
- **404 Not Found**: Kaynak bulunamadı
- **409 Conflict**: Çakışma (örn: telefon numarası zaten kayıtlı)
- **500 Internal Server Error**: Sunucu hatası

---

## 📝 Notlar

1. Tüm tarih-saat değerleri ISO 8601 formatındadır (örn: `2025-10-18T12:00:00`)
2. Koordinatlar ondalık derece formatındadır (örn: `41.0082`)
3. Telefon numaraları uluslararası formattadır (örn: `+905551234567`)
4. Durum (status) değerleri string olarak döner
5. Tüm POST/PUT endpoint'leri `Content-Type: application/json` header'ı gerektirir

---

## 🔐 Güvenlik

- Production ortamında JWT authentication eklenmeli
- Rate limiting uygulanmalı
- HTTPS kullanılmalı
- CORS ayarları production domain'e göre yapılandırılmalı
