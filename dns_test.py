import socket
import requests
import time
import csv
import json  


JSON_DOSYA_ADI = "siteler.json"
DOH_URL = "https://cloudflare-dns.com/dns-query"
CIKTI_DOSYASI = "dns_karsilastirma_sonuclari.csv"

def siteleri_yukle():
    """JSON dosyasından site listesini okur"""
    try:
        with open(JSON_DOSYA_ADI, 'r') as f:
            siteler = json.load(f)
            print(f"{len(siteler)} adet site yüklendi.")
            return siteler
    except FileNotFoundError:
        print(f"HATA: {JSON_DOSYA_ADI} dosyası bulunamadı!")
        return []

def test_classic_dns(domain):
    try:
        start = time.time()
        socket.gethostbyname(domain)
        return (time.time() - start) * 1000
    except:
        return None

def test_doh(domain):
    headers = {"accept": "application/dns-json"}
    params = {"name": domain, "type": "A"}
    try:
        start = time.time()
        response = requests.get(DOH_URL, headers=headers, params=params, timeout=5)
        if response.status_code == 200:
            return (time.time() - start) * 1000
        return None
    except:
        return None


domains = siteleri_yukle() 

if domains:
    print("Test başlıyor... (Çok fazla site varsa işlem uzun sürebilir)")
    
    with open(CIKTI_DOSYASI, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Domain", "Klasik DNS (ms)", "DoH (ms)", "Fark (ms)"])
        
       
        for i, domain in enumerate(domains, 1):
            dns_time = test_classic_dns(domain)
            doh_time = test_doh(domain)
            
            if dns_time and doh_time:
                fark = doh_time - dns_time
                writer.writerow([domain, f"{dns_time:.2f}", f"{doh_time:.2f}", f"{fark:.2f}"])
                print(f"[{i}/{len(domains)}] {domain}: DNS={dns_time:.0f}ms | DoH={doh_time:.0f}ms")
            else:
                print(f"[{i}/{len(domains)}] {domain}: Başarısız (Pas geçildi)")

    print(f"\nBitti! Sonuçlar '{CIKTI_DOSYASI}' dosyasına kaydedildi.")