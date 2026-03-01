import re
import json


GIRIS_DOSYASI = "download.htm"  
CIKTI_DOSYASI = "siteler.json"

def html_den_site_cek(dosyayolu):
    try:
        with open(dosyayolu, "r", encoding="utf-8") as f:
            icerik = f.read()
            
      
        pattern = r'\b[a-zA-Z0-9-]+\.[a-z]{2,}\b'
        
        bulunanlar = re.findall(pattern, icerik)
        
       
        yasakli_uzantilar = ['css', 'js', 'png', 'jpg', 'html', 'htm', 'xml']
        temiz_liste = []
        
        for site in bulunanlar:
            uzanti = site.split('.')[-1]
           
            if uzanti not in yasakli_uzantilar and site not in temiz_liste:
                temiz_liste.append(site)
                
        return temiz_liste

    except FileNotFoundError:
        print(f"HATA: '{dosyayolu}' dosyası bulunamadı! Dosya adını kontrol et.")
        return []

print("HTML taranıyor...")
siteler = html_den_site_cek(GIRIS_DOSYASI)

if siteler:
    with open(CIKTI_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(siteler, f, indent=4)
    print(f"BAŞARILI! {len(siteler)} adet site bulundu ve '{CIKTI_DOSYASI}' dosyasına kaydedildi.")
    print("İlk 5 site örneği:", siteler[:5])
else:
    print("Hiç site bulunamadı. HTML dosyasının formatı çok karışık olabilir.")