import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Veriyi Oku
try:
    # Dosyayı oku
    df = pd.read_csv('dns_karsilastirma_sonuclari.csv')
    
    # Senin verdiğin sütun isimlerini değişkenlere atayalım
    dns_col = 'Klasik DNS (ms)'
    doh_col = 'DoH (ms)'

    # 2. Ortalama Performansı Hesapla (Sayısal olmayan verileri temizleyerek)
    # Bazı satırlar 'Hata' veya boş olabilir, onları sayıya çevirip hatalıları yok sayıyoruz
    df[dns_col] = pd.to_numeric(df[dns_col], errors='coerce')
    df[doh_col] = pd.to_numeric(df[doh_col], errors='coerce')
    
    avg_dns = df[dns_col].mean()
    avg_doh = df[doh_col].mean()

    print(f"Grafik Hazırlanıyor...")
    print(f"Ortalama Klasik DNS: {avg_dns:.2f} ms")
    print(f"Ortalama DoH: {avg_doh:.2f} ms")

    # 3. Görselleştirme
    plt.figure(figsize=(10, 7))
    sns.set_style("whitegrid")
    
    # Sütun grafiği oluştur
    ax = sns.barplot(x=['Klasik DNS (Port 53)', 'DoH (HTTPS - Port 443)'], 
                     y=[avg_dns, avg_doh], 
                     palette=['#3498db', '#e74c3c']) # Mavi ve Kırmızı tonları
    
    plt.title('DNS vs DoH: Ortalama Yanıt Süresi Karşılaştırması', fontsize=15, fontweight='bold')
    plt.ylabel('Gecikme Süresi (Milisaniye)', fontsize=12)
    plt.ylim(0, max(avg_dns, avg_doh) * 1.2) # Tepede biraz boşluk bırak
    
    # Değerleri sütunların üzerine yazdır
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.2f} ms', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha='center', va='center', 
                    xytext=(0, 10), 
                    textcoords='offset points',
                    fontsize=12, fontweight='bold')

    # Grafiği dosyaya kaydet
    plt.savefig('performans_analizi_final.png')
    print("BAŞARILI: 'performans_analizi_final.png' dosyası oluşturuldu.")
    
    # Grafiği ekranda göster
    plt.show()

except Exception as e:
    print(f"Hata oluştu: {e}")
    print("Lütfen csv dosyasındaki sütun isimlerinin 'Klasik DNS (ms)' ve 'DoH (ms)' olduğundan emin olun.")