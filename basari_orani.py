import pandas as pd
import matplotlib.pyplot as plt

try:
    df = pd.read_csv('dns_karsilastirma_sonuclari.csv')
    
    # Senin terminal çıktılarından bildiğimiz toplam site sayısı
    TOPLAM_HEDEF_SITE = 496
    # CSV'ye kaydedilen başarılı satır sayısı
    basarili_sayisi = len(df) 
    # Aradaki fark başarısız olanlardır
    basarisiz_sayisi = TOPLAM_HEDEF_SITE - basarili_sayisi

    print(f"Toplam Hedef: {TOPLAM_HEDEF_SITE}")
    print(f"CSV'deki Başarılı Kayıt: {basarili_sayisi}")
    print(f"Hesaplanan Başarısız: {basarisiz_sayisi}")

    # Grafik Verileri
    veriler = [basarili_sayisi, basarisiz_sayisi]
    etiketler = [f'Başarılı ({basarili_sayisi})', f'Başarısız/Pas ({basarisiz_sayisi})']
    renkler = ['#2ecc71', '#e74c3c']

    plt.figure(figsize=(8, 8))
    plt.pie(veriler, labels=etiketler, autopct='%1.1f%%', 
            colors=renkler, startangle=140, explode=(0.05, 0), shadow=True)
    
    plt.title('DNS over HTTPS Testi Genel Başarı Analizi', fontsize=14, fontweight='bold')
    
    # Not ekle
    plt.annotate(f'Toplam site havuzu: {TOPLAM_HEDEF_SITE}', (0,0), xytext=(-1,-1.1), fontsize=10, fontstyle='italic')

    plt.savefig('basari_orani_final.png')
    plt.show()

except Exception as e:
    print(f"Hata oluştu: {e}")