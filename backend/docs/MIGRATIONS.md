# Database Migrations Rehberi

Bu proje Flask-Migrate kullanarak veritabanı şemasını yönetir. Flask-Migrate, Alembic'in Flask için bir wrapper'ıdır.

## Migrations Sistemi Kurulumu

Migrations sistemi başarıyla kurulmuştur ve kullanıma hazırdır.

## Temel Komutlar

### 1. Yeni Migration Oluşturma

Model değişikliklerinden sonra yeni bir migration oluşturmak için:

```bash
cd backend
source venv/bin/activate
flask db migrate -m "Açıklayıcı mesaj"
```

Bu komut, model değişikliklerini otomatik olarak algılar ve `migrations/versions/` klasörüne yeni bir migration dosyası oluşturur.

### 2. Migration'ları Uygulama

Bekleyen migration'ları veritabanına uygulamak için:

```bash
flask db upgrade
```

Tüm migration'ları uygulamak için:

```bash
flask db upgrade head
```

### 3. Migration'ları Geri Alma

Son migration'ı geri almak için:

```bash
flask db downgrade
```

Belirli bir revision'a geri dönmek için:

```bash
flask db downgrade <revision_id>
```

### 4. Migration Geçmişini Görüntüleme

Mevcut migration durumunu görmek için:

```bash
flask db current
```

Tüm migration geçmişini görmek için:

```bash
flask db history
```

### 5. Veritabanını Belirli Bir Duruma İşaretleme

Mevcut veritabanı durumunu belirli bir revision olarak işaretlemek için:

```bash
flask db stamp <revision_id>
```

En son revision olarak işaretlemek için:

```bash
flask db stamp head
```

## Migration İş Akışı

### Yeni Model Ekleme veya Mevcut Modeli Değiştirme

1. `app/models.py` dosyasında değişikliklerinizi yapın
2. Yeni migration oluşturun:
   ```bash
   flask db migrate -m "Add new field to User model"
   ```
3. Oluşturulan migration dosyasını kontrol edin (`migrations/versions/` klasöründe)
4. Migration'ı uygulayın:
   ```bash
   flask db upgrade
   ```

### Migration Dosyasını Manuel Düzenleme

Otomatik oluşturulan migration dosyaları her zaman mükemmel olmayabilir. Özellikle:
- Veri dönüşümleri gerektiğinde
- Karmaşık ilişki değişikliklerinde
- Özel index veya constraint'ler eklerken

Migration dosyasını `migrations/versions/` klasöründen açıp düzenleyebilirsiniz.

## Mevcut Veritabanı Şeması

### Tablolar

1. **user** - Kullanıcı bilgileri
   - Telefon numarası ile kimlik doğrulama
   - Gönüllü modu
   - Telefon doğrulama durumu

2. **user_profile** - Kullanıcı profil detayları
   - Sağlık bilgileri (kan grubu, kronik hastalıklar, ilaçlar, alerjiler)
   - Kişisel bilgiler (ad soyad, adres)

3. **emergency_contact** - Acil durum kişileri
   - Her kullanıcının birden fazla acil durum kişisi olabilir

4. **location_point** - Konum noktaları
   - Afet bölgelerinin haritada işaretlenmesi
   - Kategori ve durum bilgisi

5. **help_request** - Yardım talepleri
   - Talep eden ve gönüllü eşleşmesi
   - Durum takibi
   - Konum bilgisi

6. **need_type** - İhtiyaç tipleri (Yiyecek, Su, Barınak vb.)

7. **requested_need** - Talep edilen ihtiyaçlar
   - Help request ile ilişkili
   - Miktar bilgisi

## Önemli Notlar

### Production Ortamında

1. **Yedekleme**: Migration öncesi mutlaka veritabanı yedeği alın
2. **Test**: Önce test/staging ortamında deneyin
3. **Downtime**: Bazı migration'lar downtime gerektirebilir, bunu planlayın
4. **Geri Alma Planı**: Her zaman bir rollback planı hazırlayın

### Development Ortamında

1. Migration dosyalarını git'e commit edin
2. Takım arkadaşlarınız da aynı migration'ları uygulamalı
3. Çakışma durumunda migration'ları merge etmek yerine yeniden oluşturun

## Sorun Giderme

### "Target database is not up to date" Hatası

```bash
flask db stamp head
flask db migrate -m "Your message"
flask db upgrade
```

### Migration Çakışması

```bash
flask db heads  # Mevcut head'leri göster
flask db merge <revision1> <revision2> -m "Merge migrations"
```

### Veritabanını Sıfırlama (Dikkat: Tüm veri silinir!)

```bash
flask db downgrade base
flask db upgrade head
```

## Kaynaklar

- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
