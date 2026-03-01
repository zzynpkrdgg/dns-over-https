#Bu dosya, en çok gecikme yaşanan sitelerdeki UDP (Klasik DNS) ve TCP/TLS (DoH) farkını somutlaştırır

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

try:
    df = pd.read_csv('dns_karsilastirma_sonuclari.csv')
    df['Klasik DNS (ms)'] = pd.to_numeric(df['Klasik DNS (ms)'], errors='coerce')
    df['DoH (ms)'] = pd.to_numeric(df['DoH (ms)'], errors='coerce')
    
    # En yavaş 10 siteyi seç
    top_10 = df.nlargest(10, 'DoH (ms)')

    plt.figure(figsize=(12, 8))
    y = np.arange(len(top_10))
    width = 0.35

    plt.barh(y - width/2, top_10['Klasik DNS (ms)'], width, label='Klasik DNS (UDP)', color='#3498db')
    plt.barh(y + width/2, top_10['DoH (ms)'], width, label='DoH (TCP/TLS)', color='#e67e22')

    plt.yticks(y, top_10['Domain'])
    plt.xlabel('Gecikme (ms)')
    plt.title('En Yüksek Gecikmeli 10 Sitede UDP vs TCP/TLS Farkı')
    plt.legend()
    plt.tight_layout()
    plt.savefig('protokol_kiyaslama.png')
    print("Protokol kıyaslama grafiği 'protokol_kiyaslama.png' olarak kaydedildi.")
    plt.show()
except Exception as e:
    print(f"Hata: {e}")