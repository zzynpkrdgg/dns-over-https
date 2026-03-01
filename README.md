# DNSoverHTTPs - Web Arayüzlü DNS Karşılaştırma Testi

Bu proje, klasik DNS ve DNS over HTTPS (DoH) çözümleme sürelerini karşılaştıran ve sonuçları canlı grafiklerle gösteren bir web uygulamasıdır.

## 🚀 Özellikler

- **Web Arayüzü**: Streamlit tabanlı modern ve kullanıcı dostu arayüz
- **Canlı Grafikler**: Test sonuçları gerçek zamanlı olarak grafiklerde gösterilir
- **Çoklu Grafik Görünümü**: 
  - Canlı zaman serisi grafiği
  - Ortalama karşılaştırma grafiği
  - Dağılım grafiği
- **Detaylı İstatistikler**: Ortalama süreler ve farklar
- **CSV İndirme**: Test sonuçlarını CSV formatında indirme

## 📋 Gereksinimler

- Python 3.7 veya üzeri
- Gerekli Python paketleri (requirements.txt dosyasında listelenmiştir)

## 🔧 Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

## 🎯 Kullanım

1. Uygulamayı başlatın:
```bash
streamlit run app.py
```

2. Tarayıcınızda otomatik olarak açılacak web arayüzünde:
   - **"Testi Başlat"** butonuna tıklayın
   - Test sonuçları canlı olarak grafiklerde görünecektir
   - İstediğiniz zaman **"Testi Durdur"** ile testi durdurabilirsiniz
   - **"Sonuçları Temizle"** ile sonuçları sıfırlayabilirsiniz

## 📊 Grafikler

- **Canlı Grafik**: Test sırasında her domain için klasik DNS ve DoH yanıt süreleri gösterilir
- **Karşılaştırma Grafiği**: Ortalama yanıt sürelerinin karşılaştırması
- **Dağılım Grafiği**: DNS ve DoH yanıt süreleri arasındaki ilişki

## 📁 Dosya Yapısı

- `app.py`: Ana Streamlit uygulaması
- `dns_test.py`: Orijinal komut satırı scripti
- `siteler.json`: Test edilecek domain listesi
- `requirements.txt`: Gerekli Python paketleri

## 🔍 Test Edilen DNS Servisleri

- **Klasik DNS**: Sistem DNS ayarları kullanılır
- **DNS over HTTPS**: Cloudflare DoH servisi kullanılır (https://cloudflare-dns.com/dns-query)

## 📝 Notlar

- Test sırasında internet bağlantısı gereklidir
- Çok sayıda domain test edilirken işlem uzun sürebilir
- Test sonuçları tarayıcı oturumu boyunca saklanır
