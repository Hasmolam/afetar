# Afetar Backend - Kurulum ve Çalıştırma Kılavuzu

## 📋 Gereksinimler
- Python 3.8+
- PostgreSQL 12+ (veya Supabase gibi cloud PostgreSQL servisi)
- pip (Python paket yöneticisi)

## 🚀 Hızlı Başlangıç

### 1. Sanal Ortam Oluşturma ve Aktivasyon
```bash
cd backend

# Sanal ortam oluştur
python3 -m venv venv

# Sanal ortamı aktif et
source venv/bin/activate  # Linux/Mac
# veya
venv\Scripts\activate  # Windows
```

### 2. Bağımlılıkları Yükleme
```bash
pip install -r requirements.txt
```

### 3. Ortam Değişkenlerini Ayarlama
`.env.example` dosyasını `.env` olarak kopyalayın ve değerleri düzenleyin:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:
```bash
# Gerekli alanlar
SECRET_KEY=cok-guclu-ve-rastgele-bir-anahtar-buraya-yazin
JWT_SECRET_KEY=jwt-icin-ayri-bir-guclu-anahtar  # JWT authentication için
DATABASE_URL=postgresql://kullanici_adi:sifre@host:5432/veritabani_adi
FLASK_ENV=development
```

**JWT Authentication Notları:**
- `JWT_SECRET_KEY` mutlaka güçlü ve rastgele olmalı (en az 32 karakter önerilir)
- Production'da `SECRET_KEY` ve `JWT_SECRET_KEY` farklı olmalı
- Token süreleri: Access Token 1 saat, Refresh Token 30 gün

#### Supabase Kullanıyorsanız:
Supabase projenizden PostgreSQL bağlantı bilgilerini alın:
1. Supabase Dashboard → Settings → Database
2. Connection String (URI) seçeneğini kopyalayın
3. `DATABASE_URL` değerine yapıştırın

### 4. Veritabanı Migration'ları

Migration sistemi hazır durumda. Migration komutlarını kullanmak için:

#### Kolay Yol (Önerilen):
```bash
# Migration helper script'ini kullan
bash scripts/migrate.sh help          # Tüm komutları göster
bash scripts/migrate.sh current       # Mevcut durumu göster
bash scripts/migrate.sh upgrade       # Migration'ları uygula
bash scripts/migrate.sh create "msg"  # Yeni migration oluştur
```

#### Manuel Yol:
```bash
# Migration'ları uygula
flask db upgrade

# Yeni migration oluşturmak için (model değişikliklerinde)
flask db migrate -m "Açıklama mesajı"

# Migration durumunu kontrol et
flask db current

# Migration geçmişini görüntüle
flask db history
```

**Not:** Detaylı migration rehberi için [docs/MIGRATIONS.md](docs/MIGRATIONS.md) dosyasına bakın.

### 5. Uygulamayı Çalıştırma
```bash
# Sanal ortamın aktif olduğundan emin olun
source venv/bin/activate  # Linux/Mac

# Uygulamayı başlat
python run.py
```

Uygulama `http://localhost:5000` adresinde çalışacaktır.

## 📡 API Endpoint'leri

**37+ endpoint** ile eksiksiz REST API! 

### 🔗 Hızlı Linkler
- **[Detaylı API Dokümantasyonu](docs/API_DOCUMENTATION.md)** - Tüm endpoint'ler, örnekler ve açıklamalar
- **[Özellik Özeti](docs/FEATURES_SUMMARY.md)** - MVP özellikleri ve teknik detaylar
- **[Endpoint Listesi](scripts/list_endpoints.py)** - Script ile tüm endpoint'leri görüntüle

### 📋 Hızlı Genel Bakış

#### 🔐 Authentication & Authorization
- JWT token bazlı kimlik doğrulama
- Access token (1 saat) ve Refresh token (30 gün)
- Kullanıcı bazlı yetkilendirme
- 16 korumalı endpoint, 21 public endpoint

#### Kullanıcı Yönetimi (7 endpoint)
- Kullanıcı CRUD işlemleri
- Gönüllü modu aktivasyonu (🔒 Protected)
- Profil yönetimi (🔒 Protected)
- Acil durum kişileri (🔒 Protected)

#### Yardım Talepleri - SOS (8 endpoint)
- ✅ **SOS Butonu** - Tek dokunuşla yardım çağrısı (🔒 Protected)
- ✅ **Durum Takibi** - Real-time güncelleme
- ✅ **Yakınlık Arama** - Coğrafi konum bazlı
- ✅ **Gönüllü Atama** - Otomatik eşleştirme (🔒 Protected)

#### Konum & İhtiyaç Yönetimi (15+ endpoint)
- Toplanma alanları, dağıtım noktaları
- İhtiyaç tipleri ve takibi
- Durum yönetimi

### 🎯 MVP Özellikleri - Tamamlandı!
Tüm Product Requirement Document (PRD) özellikleri uygulandı:
- ✅ Ö-1: Tek Dokunuşla Yardım Çağrısı
- ✅ Ö-2: Çağrı Durumu Geri Bildirimi
- ✅ Ö-3: Gönüllü Modu Aktivasyonu
- ✅ Ö-4: Yakındaki Çağrıları Haritada Görme
- ✅ Ö-5: Çağrıyı Üstlenme ve Navigasyon
- 🔨 Ö-6: Proaktif Bildirim (Backend hazır, Push servis gerekli)
- ✅ **JWT Authentication** - Güvenli kimlik doğrulama ve yetkilendirme

**Detaylar için:** 
- [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) - Tüm endpoint'ler
- [docs/JWT_AUTHENTICATION.md](docs/JWT_AUTHENTICATION.md) - Authentication rehberi

## 📁 Proje Yapısı
```
backend/
├── app/                           # 🐍 Ana uygulama kodu
│   ├── __init__.py               # Flask factory fonksiyonu
│   ├── extentions.py             # Flask eklentileri (db, migrate)
│   ├── models.py                 # SQLAlchemy veritabanı modelleri (7 tablo)
│   └── api/
│       ├── __init__.py
│       └── routes.py             # API endpoint'leri (791 satır, 37 endpoint)
│
├── docs/                          # 📚 Dokümantasyon dosyaları
│   ├── README.md                 # Dokümantasyon indeksi
│   ├── API_DOCUMENTATION.md      # Detaylı API referansı (800+ satır)
│   ├── JWT_AUTHENTICATION.md     # JWT authentication rehberi (400+ satır)
│   ├── JWT_IMPLEMENTATION_SUMMARY.md # JWT implementasyon özeti
│   ├── FEATURES_SUMMARY.md       # Özellik özeti ve teknik detaylar
│   ├── DEVELOPMENT_COMPLETE.md   # Geliştirme tamamlama raporu
│   ├── MIGRATIONS.md             # Kapsamlı migration rehberi
│   ├── MIGRATION_QUICKREF.md     # Hızlı referans kartı
│   └── MIGRATION_SETUP_SUMMARY.md # Migration kurulum özeti
│
├── scripts/                       # 🛠️ Yardımcı scriptler
│   ├── test_api.py               # API test script'i
│   ├── test_jwt_auth.py          # JWT authentication test script'i
│   ├── list_endpoints.py         # Endpoint listesi
│   ├── migrate.sh                # Migration script
│   └── migration-quickstart.sh   # Hızlı migration kurulumu
│   ├── test_api.py               # Otomatik API test scripti
│   ├── list_endpoints.py         # Endpoint listesi görüntüleyici
│   ├── migrate.sh                # Migration helper script
│   └── migration-quickstart.sh   # Hızlı başlangıç scripti
│
├── migrations/                    # 📦 Alembic veritabanı migration'ları
├── instance/                      # 🔐 Instance-specific dosyalar
├── venv/                         # 🐍 Python sanal ortamı (git'e eklenmez)
│
├── .env                          # 🔑 Ortam değişkenleri (git'e eklenmez)
├── .env.example                  # Örnek ortam değişkenleri dosyası
├── config.py                     # ⚙️ Uygulama konfigürasyonu
├── requirements.txt              # 📋 Python bağımlılıkları
├── run.py                        # 🚀 Uygulama giriş noktası
└── README.md                     # 📖 Bu dosya (kurulum rehberi)
```

## 🗄️ Veritabanı Modelleri

### User (Kullanıcı)
Kullanıcı kimlik doğrulama ve temel bilgiler.

### UserProfile (Kullanıcı Profili)
Sağlık bilgileri, kan grubu, ilaç ve alerji bilgileri.

### EmergencyContact (Acil Durum İletişim)
Kullanıcının acil durum iletişim kişileri.

### HelpRequest (Yardım Talebi)
SOS butonu ile oluşturulan yardım çağrıları.

### LocationPoint (Konum Noktası)
Toplanma alanları, dağıtım noktaları, güvenli bölgeler.

### NeedType (İhtiyaç Tipi)
Gıda, su, barınak, ilaç gibi ihtiyaç kategorileri.

### RequestedNeed (Talep Edilen İhtiyaç)
Yardım taleplerinde belirtilen spesifik ihtiyaçlar.

## 🛠️ Geliştirme Notları

### Database Migrations

Veritabanı şemasında değişiklik yaparken migration sistemi kullanılmalıdır.

#### Hızlı Komutlar (migrate.sh ile):
```bash
bash scripts/migrate.sh create "Add new field to User"  # Yeni migration oluştur
bash scripts/migrate.sh upgrade                          # Migration'ları uygula
bash scripts/migrate.sh current                          # Durumu kontrol et
bash scripts/migrate.sh history                          # Geçmişi görüntüle
bash scripts/migrate.sh downgrade                        # Son migration'ı geri al
```

#### Manuel Komutlar:
```bash
# Model değişikliklerinden sonra:
flask db migrate -m "Değişiklik açıklaması"
flask db upgrade

# Migration durumunu kontrol et:
flask db current

# Migration geçmişini göster:
flask db history

# Son migration'ı geri al:
flask db downgrade
```

**Önemli:** Detaylı migration rehberi ve best practices için [docs/MIGRATIONS.md](docs/MIGRATIONS.md) dosyasını okuyun.

### Migration Oluşturma
Model değişikliklerinden sonra:
```bash
flask db migrate -m "Değişiklik açıklaması"
flask db upgrade
```

### Veritabanını Sıfırlama
```bash
# Tüm migration'ları geri al
flask db downgrade base

# Migration'ları tekrar uygula
flask db upgrade
```

### Test Verisi Ekleme
Geliştirme ortamında test verisi eklemek için:
```python
# Python shell'i aç
flask shell

# Örnek kullanıcı oluştur
from app.models import User, NeedType
from app.extentions import db

user = User(phone_number='+905551234567', password_hash='hashed_password')
db.session.add(user)
db.session.commit()
```

## 🐛 Sık Karşılaşılan Hatalar

### RuntimeError: SQLALCHEMY_DATABASE_URI must be set
**Çözüm:** `.env` dosyasında `DATABASE_URL` değişkeninin ayarlı olduğundan emin olun.

### ModuleNotFoundError: No module named 'dotenv'
**Çözüm:** Sanal ortamı aktif edin ve `pip install -r requirements.txt` komutunu çalıştırın.

### İzin hatası veya "Böyle bir dosya yok"
**Çözüm:** Backend dizininde olduğunuzdan ve sanal ortamın aktif olduğundan emin olun:
```bash
cd backend
source venv/bin/activate
python run.py
```

## 🔒 Güvenlik Notları

- **Production'da:** `SECRET_KEY` ve `JWT_SECRET_KEY` değerlerini güçlü, rastgele değerlerle değiştirin.
- **Production'da:** `DEBUG=False` ve `FLASK_ENV=production` ayarlayın.
- **Production'da:** HTTPS kullanın ve CORS ayarlarını production domain'inizle sınırlayın.
- **Production'da:** Gunicorn veya uWSGI gibi bir production WSGI server kullanın.
- **Production'da:** Nginx gibi bir reverse proxy arkasında çalıştırın.
- Veritabanı şifrelerini ve API anahtarlarını asla git'e commit etmeyin.
- `.env` dosyasını `.gitignore`'a eklediğinizden emin olun.

## 📚 Ek Kaynaklar

### Proje Dokümantasyonu
- **[Dokümantasyon İndeksi](docs/README.md)** - Tüm dökümanlara erişim
- **[API Referansı](docs/API_DOCUMENTATION.md)** - Detaylı endpoint rehberi
- **[Özellik Özeti](docs/FEATURES_SUMMARY.md)** - Teknik detaylar ve mimari
- **[Migration Rehberi](docs/MIGRATIONS.md)** - Database yönetimi

### Test ve Araçlar
- **[API Test Script](scripts/test_api.py)** - Otomatik test scripti
- **[Endpoint Listesi](scripts/list_endpoints.py)** - Tüm endpoint'leri görüntüle
- **[Migration Helper](scripts/migrate.sh)** - Migration yardımcı script

### Dış Kaynaklar
- [Flask Dokümantasyonu](https://flask.palletsprojects.com/)
- [SQLAlchemy Dokümantasyonu](https://docs.sqlalchemy.org/)
- [Flask-Migrate Dokümantasyonu](https://flask-migrate.readthedocs.io/)
- [PostgreSQL Dokümantasyonu](https://www.postgresql.org/docs/)
- [Supabase Dokümantasyonu](https://supabase.com/docs)

## 💬 Destek

Sorularınız için issue açabilir veya proje sahipleriyle iletişime geçebilirsiniz.

---

**Not:** 
- Backend dokümantasyonu için [docs/](docs/) klasörüne bakın
- Ana proje dokümantasyonu için [Ana README](../README.md) dosyasına bakın
- API test etmek için: `python scripts/test_api.py`
- Endpoint'leri listelemek için: `python scripts/list_endpoints.py`
