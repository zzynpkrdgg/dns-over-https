#Bu dosya, klasik DNS'in hız stabilitesi ile DoH'un gecikme değişkenliğini karşılaştıran bir histogram oluşturur
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

try:
    df = pd.read_csv('dns_karsilastirma_sonuclari.csv')
    dns_col = 'Klasik DNS (ms)'
    doh_col = 'DoH (ms)'

    plt.figure(figsize=(10, 6))
    sns.histplot(pd.to_numeric(df[dns_col], errors='coerce').dropna(), color="skyblue", label="Klasik DNS", kde=True)
    sns.histplot(pd.to_numeric(df[doh_col], errors='coerce').dropna(), color="salmon", label="DoH (HTTPS)", kde=True)
    
    plt.title('DNS vs DoH Gecikme Süreleri Dağılımı')
    plt.xlabel('Gecikme (ms)')
    plt.ylabel('Frekans (Site Sayısı)')
    plt.legend()
    plt.xlim(0, 1000)
    plt.savefig('gecikme_dagilimi.png')
    print("Gecikme dağılımı grafiği 'gecikme_dagilimi.png' olarak kaydedildi.")
    plt.show()
except Exception as e:
    print(f"Hata: {e}")