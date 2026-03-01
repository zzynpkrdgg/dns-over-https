import streamlit as st
import socket
import requests
import time
import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Sayfa yapılandırması
st.set_page_config(
    page_title="DNS Karşılaştırma Testi",
    page_icon="🌐",
    layout="wide"
)

JSON_DOSYA_ADI = "siteler.json"
DOH_URL = "https://cloudflare-dns.com/dns-query"

# Session state başlatma
if 'test_results' not in st.session_state:
    st.session_state.test_results = []
if 'test_running' not in st.session_state:
    st.session_state.test_running = False
if 'progress' not in st.session_state:
    st.session_state.progress = {'current': 0, 'total': 0}

def siteleri_yukle():
    """JSON dosyasından site listesini okur"""
    try:
        with open(JSON_DOSYA_ADI, 'r', encoding='utf-8') as f:
            siteler = json.load(f)
            return siteler
    except FileNotFoundError:
        st.error(f"❌ HATA: {JSON_DOSYA_ADI} dosyası bulunamadı!")
        return []
    except json.JSONDecodeError:
        st.error(f"❌ HATA: {JSON_DOSYA_ADI} dosyası geçersiz JSON formatında!")
        return []

def test_classic_dns(domain):
    """Klasik DNS çözümleme testi"""
    try:
        start = time.time()
        socket.gethostbyname(domain)
        return (time.time() - start) * 1000
    except:
        return None

def test_doh(domain):
    """DNS over HTTPS testi"""
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

def test_domains(domains):
    """Domain'leri test et ve sonuçları session state'e kaydet"""
    st.session_state.test_results = []
    st.session_state.progress = {'current': 0, 'total': len(domains)}
    
    for i, domain in enumerate(domains, 1):
        if not st.session_state.test_running:
            break
            
        # Testleri çalıştır
        dns_time = test_classic_dns(domain)
        doh_time = test_doh(domain)
        
        # Sonuçları kaydet
        if dns_time and doh_time:
            fark = doh_time - dns_time
            result = {
                'domain': domain,
                'dns_time': dns_time,
                'doh_time': doh_time,
                'fark': fark,
                'timestamp': datetime.now()
            }
            st.session_state.test_results.append(result)
        
        # İlerlemeyi güncelle
        st.session_state.progress = {'current': i, 'total': len(domains)}

def create_live_chart():
    """Canlı grafik oluştur"""
    if not st.session_state.test_results:
        return None
    
    df = pd.DataFrame(st.session_state.test_results)
    
    # Grafik oluştur
    fig = go.Figure()
    
    # Klasik DNS çizgisi
    fig.add_trace(go.Scatter(
        x=list(range(len(df))),
        y=df['dns_time'],
        mode='lines+markers',
        name='Klasik DNS',
        line=dict(color='#1f77b4', width=2),
        marker=dict(size=4)
    ))
    
    # DoH çizgisi
    fig.add_trace(go.Scatter(
        x=list(range(len(df))),
        y=df['doh_time'],
        mode='lines+markers',
        name='DNS over HTTPS',
        line=dict(color='#ff7f0e', width=2),
        marker=dict(size=4)
    ))
    
    fig.update_layout(
        title='DNS Karşılaştırma Testi - Canlı Grafik',
        xaxis_title='Test Sırası',
        yaxis_title='Yanıt Süresi (ms)',
        hovermode='x unified',
        height=500,
        template='plotly_white',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

def create_comparison_chart():
    """Karşılaştırma grafiği oluştur"""
    if not st.session_state.test_results:
        return None
    
    df = pd.DataFrame(st.session_state.test_results)
    
    # Ortalama değerler
    avg_dns = df['dns_time'].mean()
    avg_doh = df['doh_time'].mean()
    
    fig = go.Figure(data=[
        go.Bar(name='Klasik DNS', x=['Ortalama'], y=[avg_dns], marker_color='#1f77b4'),
        go.Bar(name='DNS over HTTPS', x=['Ortalama'], y=[avg_doh], marker_color='#ff7f0e')
    ])
    
    fig.update_layout(
        title='Ortalama Yanıt Süreleri Karşılaştırması',
        yaxis_title='Yanıt Süresi (ms)',
        barmode='group',
        height=400,
        template='plotly_white'
    )
    
    return fig

def create_scatter_chart():
    """Dağılım grafiği oluştur"""
    if not st.session_state.test_results:
        return None
    
    df = pd.DataFrame(st.session_state.test_results)
    
    fig = px.scatter(
        df,
        x='dns_time',
        y='doh_time',
        hover_data=['domain'],
        labels={'dns_time': 'Klasik DNS (ms)', 'doh_time': 'DNS over HTTPS (ms)'},
        title='DNS vs DoH Yanıt Süreleri Dağılımı',
        color='fark',
        color_continuous_scale='RdYlGn_r',
        height=500
    )
    
    # Diyagonal çizgi ekle (eşitlik çizgisi)
    max_val = max(df['dns_time'].max(), df['doh_time'].max())
    fig.add_trace(go.Scatter(
        x=[0, max_val],
        y=[0, max_val],
        mode='lines',
        name='Eşitlik Çizgisi',
        line=dict(color='gray', dash='dash'),
        showlegend=True
    ))
    
    return fig

# Ana başlık
st.title("🌐 DNS Karşılaştırma Testi")
st.markdown("---")

# Sidebar - Kontroller
with st.sidebar:
    st.header("⚙️ Kontroller")
    
    # Site sayısı seçici
    domains_all = siteleri_yukle()
    total_sites = len(domains_all) if domains_all else 0
    
    if total_sites > 0:
        st.subheader("📊 Test Ayarları")
        max_sites = st.slider(
            "Test Edilecek Site Sayısı",
            min_value=1,
            max_value=total_sites,
            value=min(50, total_sites),  # Varsayılan olarak 50 veya toplam site sayısı
            step=1,
            disabled=st.session_state.test_running,
            help=f"Toplam {total_sites} site mevcut. Kaç tanesini test etmek istediğinizi seçin."
        )
        st.caption(f"📌 Toplam {total_sites} site mevcut")
    else:
        max_sites = 0
        st.warning("⚠️ Site listesi yüklenemedi!")
    
    st.markdown("---")
    
    if st.button("🚀 Testi Başlat", disabled=st.session_state.test_running or max_sites == 0, use_container_width=True):
        if domains_all and max_sites > 0:
            # Seçilen sayı kadar siteyi al
            selected_domains = domains_all[:max_sites]
            st.session_state.test_running = True
            st.session_state.test_results = []
            st.session_state.test_started = False
            st.session_state.progress = {'current': 0, 'total': len(selected_domains)}
            st.session_state.selected_domains = selected_domains
            st.rerun()
    
    if st.button("⏹️ Testi Durdur", disabled=not st.session_state.test_running, use_container_width=True):
        st.session_state.test_running = False
        if 'selected_domains' in st.session_state:
            del st.session_state.selected_domains
        st.rerun()
    
    if st.button("🗑️ Sonuçları Temizle", disabled=st.session_state.test_running, use_container_width=True):
        st.session_state.test_results = []
        if 'selected_domains' in st.session_state:
            del st.session_state.selected_domains
        st.rerun()
    
    st.markdown("---")
    st.header("ℹ️ Bilgi")
    st.info("""
    Bu uygulama klasik DNS ve DNS over HTTPS (DoH) 
    çözümleme sürelerini karşılaştırır.
    
    **Test Adımları:**
    1. 'Testi Başlat' butonuna tıklayın
    2. Grafikler canlı olarak güncellenecek
    3. Sonuçları tabloda görebilirsiniz
    """)

# Ana içerik alanı
if st.session_state.test_running:
    # Seçilen domain listesini kullan
    if 'selected_domains' in st.session_state:
        domains = st.session_state.selected_domains
    else:
        domains = siteleri_yukle()
    
    if domains:
        # İlerleme çubuğu ve durum metni
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Progress'i başlat (eğer henüz başlatılmadıysa)
        if st.session_state.progress['total'] == 0:
            st.session_state.progress = {'current': 0, 'total': len(domains)}
        
        # Testi çalıştır (her yenilemede bir domain test et)
        if st.session_state.progress['current'] < st.session_state.progress['total']:
            current_idx = st.session_state.progress['current']
            if current_idx < len(domains):
                domain = domains[current_idx]
                
                # Testleri çalıştır
                dns_time = test_classic_dns(domain)
                doh_time = test_doh(domain)
                
                # Sonuçları kaydet
                if dns_time and doh_time:
                    fark = doh_time - dns_time
                    result = {
                        'domain': domain,
                        'dns_time': dns_time,
                        'doh_time': doh_time,
                        'fark': fark,
                        'timestamp': datetime.now()
                    }
                    st.session_state.test_results.append(result)
                
                # İlerlemeyi güncelle
                st.session_state.progress['current'] += 1
                
                # UI güncellemesi
                if st.session_state.progress['total'] > 0:
                    progress = st.session_state.progress['current'] / st.session_state.progress['total']
                    progress_bar.progress(progress)
                    status_text.text(
                        f"Test ediliyor: {domain} ({st.session_state.progress['current']}/{st.session_state.progress['total']})"
                    )
                
                # Kısa bekleme ve yenileme
                time.sleep(0.1)
                st.rerun()
            else:
                # Test tamamlandı
                st.session_state.test_running = False
                if 'selected_domains' in st.session_state:
                    del st.session_state.selected_domains
                status_text.text("✅ Test tamamlandı!")
                progress_bar.progress(1.0)
        else:
            # Test tamamlandı
            st.session_state.test_running = False
            if 'selected_domains' in st.session_state:
                del st.session_state.selected_domains
            status_text.text("✅ Test tamamlandı!")
            progress_bar.progress(1.0)

# Grafikler
if st.session_state.test_results:
    st.header("📊 Grafikler")
    
    # Canlı grafik
    fig_live = create_live_chart()
    if fig_live:
        st.plotly_chart(fig_live, use_container_width=True)
    
    # İki sütunlu grafikler
    col1, col2 = st.columns(2)
    
    with col1:
        fig_comp = create_comparison_chart()
        if fig_comp:
            st.plotly_chart(fig_comp, use_container_width=True)
    
    with col2:
        fig_scatter = create_scatter_chart()
        if fig_scatter:
            st.plotly_chart(fig_scatter, use_container_width=True)
    
    # İstatistikler
    st.header("📈 İstatistikler")
    df = pd.DataFrame(st.session_state.test_results)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Toplam Test", len(df))
    
    with col2:
        avg_dns = df['dns_time'].mean()
        st.metric("Ortalama Klasik DNS", f"{avg_dns:.2f} ms")
    
    with col3:
        avg_doh = df['doh_time'].mean()
        st.metric("Ortalama DoH", f"{avg_doh:.2f} ms")
    
    with col4:
        avg_fark = df['fark'].mean()
        st.metric("Ortalama Fark", f"{avg_fark:.2f} ms")
    
    # Sonuçlar tablosu
    st.header("📋 Test Sonuçları")
    df_display = df.copy()
    df_display['dns_time'] = df_display['dns_time'].round(2)
    df_display['doh_time'] = df_display['doh_time'].round(2)
    df_display['fark'] = df_display['fark'].round(2)
    df_display = df_display.rename(columns={
        'domain': 'Domain',
        'dns_time': 'Klasik DNS (ms)',
        'doh_time': 'DoH (ms)',
        'fark': 'Fark (ms)'
    })
    st.dataframe(df_display, use_container_width=True, height=400)
    
    # CSV indirme
    csv = df_display.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 Sonuçları CSV Olarak İndir",
        data=csv,
        file_name=f"dns_test_sonuclari_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv"
    )


