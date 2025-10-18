# 🆘 AFETAR - Afet Gönüllü Eşleştirme Platformu

<div align="center">

**Afet anında yardıma ihtiyaç duyan kişilerle onlara en yakın konumdaki gönüllüleri anında eşleştiren bir mobil uygulama.**

[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-12+-blue.svg)](https://www.postgresql.org/)
[![React Native](https://img.shields.io/badge/React_Native-Expo-blue.svg)](https://reactnative.dev/)

</div>

---

## 📖 Proje Hakkında

AFETAR, afet ve acil durum anlarında yardıma ihtiyaç duyan kişilerin tek bir tuşla yardım çağrısı yapabilmelerini ve bu çağrının en yakındaki gönüllüye anında iletilmesini sağlayan bir mobil uygulamadır.

### 🎯 Temel Özellikler

- **🚨 Tek Dokunuşla SOS:** Afetzedeler tek tuşla anlık konum bilgisiyle yardım çağrısı gönderebilir
- **📍 Konum Tabanlı Eşleştirme:** Sistem, en yakındaki aktif gönüllüyü otomatik olarak bulur
- **🔔 Anlık Bildirimler:** Gönüllüler yakınlarındaki yardım çağrılarından anında haberdar olur
- **🗺️ Harita Entegrasyonu:** Yardım taleplerinin ve güvenli bölgelerin harita üzerinde görüntülenmesi
- **👥 Gönüllü Modu:** Kullanıcılar aktif olarak gönüllü olup yardım edebilirler
- **🏥 Sağlık Profili:** Kan grubu, alerji ve kronik hastalık bilgilerinin saklanması
- **📱 Acil Durum Kontakları:** Kullanıcının yakınlarına otomatik bildirim gönderimi
- **📊 İhtiyaç Takibi:** Gıda, su, ilaç gibi spesifik ihtiyaçların belirtilmesi

---

## 🏗️ Teknoloji Altyapısı

### Backend
- **Framework:** Flask 2.3+
- **Veritabanı:** PostgreSQL 12+
- **ORM:** SQLAlchemy
- **Migration:** Flask-Migrate (Alembic)
- **Ortam Yönetimi:** python-dotenv

### Frontend (Planlanan)
- **Framework:** React Native (Expo)
- **Harita:** Mapbox / Google Maps
- **Bildirimler:** Firebase Cloud Messaging
- **State Management:** Redux / Context API

### Dağıtım (Planlanan)
- **Backend:** Railway / Render / AWS
- **Veritabanı:** Supabase / AWS RDS
- **Frontend:** Expo Application Services (EAS)

---

## 📂 Proje Yapısı

```
afetar/
├── backend/                 # Flask API Backend
│   ├── app/
│   │   ├── __init__.py     # Flask factory
│   │   ├── models.py       # SQLAlchemy modelleri
│   │   ├── extentions.py   # Flask eklentileri
│   │   └── api/            # API endpoint'leri
│   ├── migrations/         # Veritabanı migration'ları
│   ├── .env.example        # Örnek ortam değişkenleri
│   ├── config.py           # Konfigürasyon
│   ├── requirements.txt    # Python bağımlılıkları
│   ├── run.py             # Uygulama başlangıcı
│   └── README.md          # Backend dokümantasyonu
├── frontend/               # React Native Mobile App (Geliştirilecek)
├── dbmodel.txt            # Veritabanı şeması
├── PRD.md                 # Ürün Gereksinimleri Dokümanı
└── README.md              # Bu dosya
```

---

## 🚀 Hızlı Başlangıç

### Önkoşullar

- Python 3.8 veya üzeri
- PostgreSQL 12 veya üzeri (veya Supabase)
- pip (Python paket yöneticisi)
- Git

### Backend Kurulumu

1. **Repoyu klonlayın:**
```bash
git clone https://github.com/Hasmolam/afetar.git
cd afetar/backend
```

2. **Sanal ortam oluşturun ve aktif edin:**
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

3. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

4. **Ortam değişkenlerini ayarlayın:**
```bash
cp .env.example .env
# .env dosyasını düzenleyin ve gerekli değerleri girin
```

5. **Veritabanı migration'larını uygulayın:**
```bash
flask db upgrade
```

6. **Uygulamayı başlatın:**
```bash
python run.py
```

Backend artık `http://localhost:5000` adresinde çalışıyor! 🎉

Detaylı kurulum talimatları için [Backend README](backend/README.md) dosyasına bakın.

---

## 📊 Veritabanı Şeması

Proje aşağıdaki temel modelleri içerir:

- **User:** Kullanıcı kimlik doğrulama ve temel bilgiler
- **UserProfile:** Sağlık bilgileri, kan grubu, alerji bilgileri
- **EmergencyContact:** Acil durum iletişim kişileri
- **HelpRequest:** SOS yardım talepleri
- **LocationPoint:** Güvenli bölgeler, toplanma alanları
- **NeedType:** İhtiyaç kategorileri (gıda, su, barınak, vb.)
- **RequestedNeed:** Talep edilen spesifik ihtiyaçlar

Detaylı veritabanı şeması için [dbmodel.txt](dbmodel.txt) dosyasına bakın.

---

## 🔌 API Endpoint'leri

### Temel Endpoint'ler
```
GET  /                          # API bilgisi
GET  /health                    # Health check
```

### Kullanıcı İşlemleri
```
GET    /api/v1/users           # Kullanıcıları listele
POST   /api/v1/users           # Yeni kullanıcı oluştur
GET    /api/v1/users/<id>      # Kullanıcı detayı
PUT    /api/v1/users/<id>      # Kullanıcı güncelle
DELETE /api/v1/users/<id>      # Kullanıcı sil
```

### Yardım Talepleri (SOS)
```
GET    /api/v1/help-requests         # Tüm talepleri listele
POST   /api/v1/help-requests         # Yeni SOS talebi oluştur
GET    /api/v1/help-requests/<id>    # Talep detayı
PUT    /api/v1/help-requests/<id>    # Talep durumunu güncelle
GET    /api/v1/help-requests/nearby  # Yakındaki talepleri getir
```

### Konum Noktaları
```
GET    /api/v1/locations              # Onaylanmış konumları listele
POST   /api/v1/locations              # Yeni konum bildir
GET    /api/v1/locations/type/<type>  # Tipe göre konumları getir
```

### İhtiyaç Tipleri
```
GET    /api/v1/need-types    # İhtiyaç kategorilerini listele
POST   /api/v1/need-types    # Yeni kategori ekle
```

Detaylı API dokümantasyonu için [Backend README](backend/README.md) dosyasına bakın.

---

## 🎯 Kullanım Senaryoları

### Senaryo 1: Afetzede Yardım İster
1. Kullanıcı uygulamayı açar
2. Ana ekrandaki büyük SOS butonuna basar
3. İhtiyaçlarını seçer (gıda, su, ilaç, vb.)
4. Sistem konumunu otomatik alır ve yardım talebi oluşturur
5. En yakın aktif gönüllüye bildirim gönderilir
6. Kullanıcı "Yardım yolda!" mesajı alır

### Senaryo 2: Gönüllü Yardım Eder
1. Gönüllü "Gönüllü Modu"nu aktif eder
2. Yakınında bir SOS çağrısı geldiğinde bildirim alır
3. Haritada çağrıyı görür ve kabul eder
4. Navigasyon ile afetzedenin konumuna yönlendirilir
5. Yardımı tamamladıktan sonra durumu "Tamamlandı" olarak işaretler

---

## 🛠️ Geliştirme Yol Haritası

### ✅ Tamamlanan
- [x] Backend proje yapısı ve konfigürasyonu
- [x] Veritabanı modellerinin oluşturulması
- [x] Temel API endpoint'lerinin hazırlanması
- [x] PostgreSQL entegrasyonu

### 🔄 Devam Eden
- [ ] Kullanıcı kimlik doğrulama (JWT)
- [ ] Telefon numarası doğrulama (SMS)
- [ ] Konum tabanlı sorgulama optimizasyonu
- [ ] Real-time bildirim sistemi

### 📋 Planlanıyor
- [ ] React Native frontend uygulaması
- [ ] Harita entegrasyonu
- [ ] Push notification servisi
- [ ] Admin paneli
- [ ] Test senaryolarının yazılması
- [ ] CI/CD pipeline kurulumu
- [ ] Production deployment

---

## 🤝 Katkıda Bulunma

Bu proje açık kaynaklıdır ve katkılara açıktır! Katkıda bulunmak için:

1. Bu repoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik: Açıklama'`)
4. Branch'inizi push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

---

## 📄 Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.

---

## 👥 Ekip

- **Hasmolam** - Proje Sahibi ve Geliştirici

---

## 📞 İletişim

Sorularınız veya önerileriniz için:
- GitHub Issues: [github.com/Hasmolam/afetar/issues](https://github.com/Hasmolam/afetar/issues)
- Email: [İletişim bilgisi eklenecek]

---

## 🌟 Destekleyin

Bu projeyi faydalı bulduysanız ⭐ vermeyi unutmayın!

---

<div align="center">

**Afetlere Karşı Hazırlıklı Olalım, Birlikte Güçlüyüz! 💪**

Made with ❤️ for a safer world

</div>
