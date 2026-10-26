# Geliştirme Yol Haritası (Roadmap)

Her gün sıradaki bekleyen madde birim testleriyle birlikte geliştirilip commit atılır.

- [x] Temel veri modelleri: `Product`, `PriceSnapshot`, `AlertRule` (`src/models.py`)
- [x] Veritabanı katmanı: SQLite tablo oluşturma ve bağlantı yöneticisi (`src/db.py`)
- [x] Veri erişim katmanı (Repository): Ürün ekleme ve fiyat geçmişi sorgulama (`src/repository.py`)
- [x] Fiyat ayrıştırıcı (Parser): Fiyat metinlerinden sayısal değerleri çıkarma (`src/parser.py`)
- [ ] HTTP istek modülü: Özel User-Agent ve zaman aşımı destekli hafif `urllib` istemcisi (`src/fetcher.py`)
- [ ] Fiyat karşılaştırma motoru: Fiyatın eşik değerin altına inip inmediğini kontrol etme (`src/comparator.py`)
- [ ] Konsol bildirici: Terminalde renkli/biçimli fiyat düşüş uyarıları (`src/notifiers/console.py`)
- [ ] Webhook bildirici: Discord / Telegram / genel webhook bildirim gönderimi (`src/notifiers/webhook.py`)
- [ ] CLI komutları: Ürün ekleme, takip listesi ve anlık kontrol (`src/cli.py`)
- [ ] Dışa aktarma modülü: Fiyat geçmişini JSON / CSV olarak kaydetme (`src/exporter.py`)
