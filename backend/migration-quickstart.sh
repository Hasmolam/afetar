#!/bin/bash
# Migration Hızlı Başlangıç - İlk Kullanım

echo "═══════════════════════════════════════════════════════"
echo "  🚀 Migration Sistemi - Hızlı Başlangıç Rehberi"
echo "═══════════════════════════════════════════════════════"
echo ""

echo "✅ Migration sistemi kuruldu ve kullanıma hazır!"
echo ""

echo "📚 Dökümanlar:"
echo "  • MIGRATIONS.md           - Detaylı rehber (tüm komutlar ve açıklamalar)"
echo "  • MIGRATION_QUICKREF.md   - Hızlı başvuru kartı (en çok kullanılanlar)"
echo "  • MIGRATION_SETUP_SUMMARY.md - Kurulum özeti"
echo ""

echo "🛠️  En Çok Kullanacağınız Komutlar:"
echo ""
echo "  1️⃣  Model değiştirdikten sonra:"
echo "      ./migrate.sh create \"Açıklama mesajı\""
echo "      ./migrate.sh upgrade"
echo ""
echo "  2️⃣  Durumu kontrol etmek için:"
echo "      ./migrate.sh current"
echo ""
echo "  3️⃣  Geçmişi görmek için:"
echo "      ./migrate.sh history"
echo ""
echo "  4️⃣  Geri almak için:"
echo "      ./migrate.sh downgrade"
echo ""
echo "  5️⃣  Tüm komutları görmek için:"
echo "      ./migrate.sh help"
echo ""

echo "💡 İpuçları:"
echo "  • Her migration'dan sonra git commit yapın"
echo "  • Açıklayıcı mesajlar kullanın"
echo "  • Production'da mutlaka yedek alın"
echo "  • Migration dosyalarını kontrol edin"
echo ""

echo "📖 Örnek Kullanım:"
echo ""
echo "  # User modeline email alanı ekledim"
echo "  ./migrate.sh create \"Add email field to User model\""
echo "  ./migrate.sh upgrade"
echo "  git add migrations/"
echo "  git commit -m \"Add email field to User model\""
echo ""

echo "═══════════════════════════════════════════════════════"
echo ""

# Mevcut durumu göster
echo "📊 Mevcut Migration Durumu:"
echo ""
source venv/bin/activate
flask db current
echo ""

echo "✨ Hazırsınız! İyi kodlamalar!"
echo ""
