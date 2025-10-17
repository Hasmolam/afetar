# Ürün Gereksinimleri Dokümanı (PRD): AFETAR

**Sürüm:** 1.0
**Tarih:** 17.10.2025

---

### **1. Giriş ve Amaç**

* **1.1. Proje Adı:** AFETAR
* **1.2. Vizyon:** AFETAR, afet anında yardıma ihtiyaç duyan kişilerle onlara en yakın konumdaki gönüllüleri anında eşleştiren bir mobil uygulamadır.
* **1.3. Çözülen Problem:** Afet ve acil durum anlarında, yardıma muhtaç kişilerin konumlarını hızlı ve etkin bir şekilde yardım edebilecek kişilere bildirmesi kritik bir sorundur. AFETAR, tek bir tuşla anlık konum bilgisini kullanarak yardım çağrısı oluşturmayı ve bu çağrıyı en yakındaki gönüllüye yönlendirerek müdahale süresini en aza indirmeyi hedefler.
* **1.4. Hackathon Temasıyla Uyumluluk:** Proje, "Afet" temasıyla doğrudan uyumludur ve afet yönetimi süreçlerine teknolojik bir çözüm sunmaktadır.

---

### **2. Hedef Kitle ve Kullanıcı Personaları**

* **2.1. Kullanıcı Personası 1: Yardım İsteyen (Afetzede)**
    * **Temel Amaç:** En hızlı ve en basit şekilde yardım çağrısı başlatmak.
    * **Zorluklar:** Zayıf internet, azalan şarj, panik durumu.
    * **İhtiyaçlar:** Çağrının alındığına ve birinin yolda olduğuna dair net geri bildirim.

* **2.2. Kullanıcı Personası 2: Gönüllü (Yardım Eden)**
    * **Temel Amaç:** Yakınındaki gerçek bir yardım ihtiyacına hızlıca müdahale etmek.
    * **İhtiyaçlar:** Afetzedenin net konumu.
    * **Endişeler:** Sahte ihbarlar ve kendi güvenliği.

---

### **3. Ürün Özellikleri (MVP)**

* **Ö-1: Tek Dokunuşla Yardım Çağrısı (SOS Butonu):** Ana ekranda, anında konum gönderen büyük bir yardım butonu.
* **Ö-2: Çağrı Durumu Geri Bildirimi:** Afetzede için "Çağrı Alındı", "Gönüllü Yola Çıktı" gibi durum güncellemeleri.
* **Ö-3: Gönüllü Modu Aktivasyonu:** Gönüllülerin bildirim almak için aktif hale getireceği bir mod.
* **Ö-4: Yakındaki Çağrıları Haritada Görme:** Gönüllüler için yakındaki aktif yardım çağrılarını gösteren bir harita.
* **Ö-5: Çağrıyı Üstlenme ve Navigasyon:** Gönüllünün bir çağrıyı kabul etme ve afetzedenin konumuna rota çizme butonu.
* **Ö-6: Proaktif Bildirim Sistemi:** Gönüllünün yakınına bir çağrı düştüğünde anlık bildirim gönderme.

---

### **4. Başarı Hedefi ve Demo Senaryosu**

Projenin başarısı, aşağıdaki demo akışının sorunsuz çalışmasıyla ölçülecektir:

1.  **Çağrı Başlatma:** Afetzede tek tuşla yardım ister.
2.  **Anında Bildirim:** Gönüllünün telefonuna 10 saniye içinde bildirim düşer.
3.  **Görevi Üstlenme:** Gönüllü, haritada çağrıyı görür ve görevi kabul eder.
4.  **Durum Güncellemesi:** Afetzedenin ekranında "Bir gönüllü yola çıktı!" mesajı anında belirir.

---

### **5. Teknik Gereksinimler ve Kapsam**

* **5.1. Teknoloji Yığını:**
    * Frontend: React Native (Expo)
    * Backend: Flask (Python)
    * Veritabanı: PostgreSQL

* **5.2. Harici API ve Servisler:**
    * Harita/Konum Servisi (Belirlenecek)
    * Anlık Bildirim Servisi (Belirlenecek)

* **5.3. Kapsam Dışı Bırakılanlar:**
    * Detaylı kullanıcı profilleri.
    * Uygulama içi anlık mesajlaşma (chat).
    * Gönüllü değerlendirme ve puanlama sistemi.
    * Geçmiş aktivite kaydı.