#!/bin/bash
# Database Migration Helper Script
# Bu script veritabanı migration işlemlerini kolaylaştırır

# Renk kodları
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Virtual environment'ı aktif et
source venv/bin/activate

# Komut fonksiyonları
function show_help {
    echo -e "${GREEN}Database Migration Helper${NC}"
    echo ""
    echo "Kullanım: ./migrate.sh [komut]"
    echo ""
    echo "Komutlar:"
    echo "  init           - Migration sistemini başlat (sadece ilk kez)"
    echo "  create <msg>   - Yeni migration oluştur"
    echo "  upgrade        - Bekleyen migration'ları uygula"
    echo "  downgrade      - Son migration'ı geri al"
    echo "  current        - Mevcut migration durumunu göster"
    echo "  history        - Migration geçmişini göster"
    echo "  stamp          - Veritabanını head olarak işaretle"
    echo "  reset          - Tüm migration'ları geri al ve sıfırla (DİKKAT!)"
    echo ""
}

function create_migration {
    if [ -z "$1" ]; then
        echo -e "${RED}Hata: Migration mesajı gerekli${NC}"
        echo "Kullanım: ./migrate.sh create \"Migration mesajınız\""
        exit 1
    fi
    
    echo -e "${YELLOW}Yeni migration oluşturuluyor: $1${NC}"
    flask db migrate -m "$1"
    echo -e "${GREEN}✓ Migration oluşturuldu${NC}"
}

function upgrade_db {
    echo -e "${YELLOW}Migration'lar uygulanıyor...${NC}"
    flask db upgrade
    echo -e "${GREEN}✓ Migration'lar başarıyla uygulandı${NC}"
}

function downgrade_db {
    echo -e "${YELLOW}Son migration geri alınıyor...${NC}"
    read -p "Emin misiniz? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        flask db downgrade
        echo -e "${GREEN}✓ Migration geri alındı${NC}"
    else
        echo -e "${YELLOW}İşlem iptal edildi${NC}"
    fi
}

function show_current {
    echo -e "${YELLOW}Mevcut migration durumu:${NC}"
    flask db current
}

function show_history {
    echo -e "${YELLOW}Migration geçmişi:${NC}"
    flask db history
}

function stamp_head {
    echo -e "${YELLOW}Veritabanı head olarak işaretleniyor...${NC}"
    flask db stamp head
    echo -e "${GREEN}✓ İşlem tamamlandı${NC}"
}

function reset_db {
    echo -e "${RED}DİKKAT: Bu işlem tüm migration'ları geri alır!${NC}"
    read -p "Devam etmek istediğinizden emin misiniz? (yes/no) " -r
    echo
    if [[ $REPLY == "yes" ]]; then
        echo -e "${YELLOW}Veritabanı sıfırlanıyor...${NC}"
        flask db downgrade base
        echo -e "${GREEN}✓ Veritabanı sıfırlandı${NC}"
    else
        echo -e "${YELLOW}İşlem iptal edildi${NC}"
    fi
}

# Ana komut işleyici
case "$1" in
    init)
        echo -e "${YELLOW}Migration sistemi başlatılıyor...${NC}"
        flask db init
        echo -e "${GREEN}✓ Migration sistemi başlatıldı${NC}"
        ;;
    create)
        create_migration "$2"
        ;;
    upgrade|up)
        upgrade_db
        ;;
    downgrade|down)
        downgrade_db
        ;;
    current|status)
        show_current
        ;;
    history|log)
        show_history
        ;;
    stamp)
        stamp_head
        ;;
    reset)
        reset_db
        ;;
    help|--help|-h|"")
        show_help
        ;;
    *)
        echo -e "${RED}Geçersiz komut: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
