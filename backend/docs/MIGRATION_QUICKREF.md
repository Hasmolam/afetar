# 🗂️ Database Migration - Hızlı Başvuru Kartı

## En Çok Kullanılan Komutlar

### 1️⃣ Model Değiştirdim - Ne Yapmalıyım?

```bash
# Adım 1: Yeni migration oluştur
./migrate.sh create "Açıklayıcı mesaj yazın"

# Adım 2: Migration dosyasını kontrol et
cat migrations/versions/[yeni_dosya_adı].py

# Adım 3: Migration'ı uygula
./migrate.sh upgrade

# Adım 4: Durumu kontrol et
./migrate.sh current
```

### 2️⃣ Yeni Model Ekledim

```bash
# app/models.py dosyasında yeni model tanımladıktan sonra:
./migrate.sh create "Add [ModelAdı] model"
./migrate.sh upgrade
```

### 3️⃣ Mevcut Modelde Alan Değiştirdim

```bash
# Alan ekledim/sildim/değiştirdim:
./migrate.sh create "Update [ModelAdı]: [değişiklik açıklaması]"
./migrate.sh upgrade
```

### 4️⃣ Hata Yaptım - Geri Almak İstiyorum

```bash
# Son migration'ı geri al:
./migrate.sh downgrade

# Değişikliği düzelt ve tekrar oluştur:
./migrate.sh create "Fix [sorun açıklaması]"
./migrate.sh upgrade
```

### 5️⃣ Durumu Kontrol Etmek İstiyorum

```bash
# Mevcut durum:
./migrate.sh current

# Tüm geçmiş:
./migrate.sh history
```

---

## 📝 Migration Mesaj Örnekleri

**İyi Örnekler:**
- ✅ `"Add email field to User model"`
- ✅ `"Create Notification model with user relationship"`
- ✅ `"Update HelpRequest: add priority field"`
- ✅ `"Remove deprecated status field from LocationPoint"`

**Kötü Örnekler:**
- ❌ `"update"` (çok genel)
- ❌ `"fix"` (ne düzeltildi?)
- ❌ `"changes"` (hangi değişiklikler?)
- ❌ `"asdf"` (anlamsız)

---

## ⚠️ Production Ortamında

```bash
# 1. MUTLAKA yedek alın!
pg_dump -h host -U user -d database > backup_$(date +%Y%m%d_%H%M%S).sql

# 2. Migration durumunu kontrol edin
./migrate.sh current

# 3. Migration'ları uygulayın
./migrate.sh upgrade

# 4. Veritabanını test edin
python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.extentions import db; print('Connection OK' if db.engine.connect() else 'Connection FAILED')"
```

---

## 🆘 Sorun Giderme

### "Target database is not up to date"
```bash
./migrate.sh stamp
./migrate.sh upgrade
```

### "Can't locate revision identified by..."
```bash
# Veritabanı ve migration dosyaları senkronize değil
./migrate.sh history
# Sorunu bulun ve düzeltin
```

### Migration çakışması
```bash
flask db heads  # Birden fazla head varsa
flask db merge <rev1> <rev2> -m "Merge migrations"
```

### Tüm migration'ları temizlemek (DİKKAT - Development only!)
```bash
./migrate.sh reset
./migrate.sh upgrade
```

---

## 🔗 İlgili Dosyalar

- 📘 Detaylı rehber: [MIGRATIONS.md](MIGRATIONS.md)
- 📗 Genel README: [README.md](README.md)
- 🗂️ Migration klasörü: `migrations/versions/`
- ⚙️ Helper script: `migrate.sh`

---

## 💡 İpuçları

1. **Sık commit edin**: Her migration'dan sonra git commit yapın
2. **Açıklayıcı olun**: Migration mesajları gelecekte size yardımcı olacak
3. **Test edin**: Production'a göndermeden önce test ortamında deneyin
4. **Yedek alın**: Önemli migration'lardan önce mutlaka yedek alın
5. **Takım çalışması**: Migration'ları git'e ekleyin, herkes aynı durumda olsun

---

**Son güncelleme:** 18 Ekim 2025
