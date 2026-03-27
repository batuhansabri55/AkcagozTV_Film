import requests
import re
import os
import datetime

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# EKRAN GÖRÜNTÜLERİNDEKİ GERÇEK VE DOĞRULANMIŞ LİNKLER
VOD_KAYNAKLAR = [
    # 1. UzunMuhalefet yayinlar/streams klasörü altındaki dosyalar (image_e7ad98 tabanlı)
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/best/all.m3u8",
    
    # 2. Legal-IPTV/lists klasörü (image_e7b0dd tabanlı)
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/turkey.m3u8",
    
    # 3. Genel Film ve Dizi Havuzları
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/lists/movies.m3u",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/lists/series.m3u"
]

def main():
    print("🎬 VOD Avcısı 3.0 Başlatıldı...")
    toplam_vod = []

    for url in VOD_KAYNAKLAR:
        try:
            print(f"🔎 Arşiv taranıyor: {url}")
            r = requests.get(url, headers=HEADERS, timeout=35)
            if r.status_code == 200:
                # Regex: #EXTINF ile başlayan ve link ile biten blokları yakalar
                # Film afişlerini (tvg-logo) ve isimlerini kaçırmaz
                icerikler = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                if icerikler:
                    toplam_vod.extend(icerikler)
                    print(f"✅ {len(icerikler)} içerik bulundu.")
                else:
                    # Alternatif basit yakalama (eğer format farklıysa)
                    basit_icerik = re.findall(r"#EXTINF:[^\n]+\n+http[^\s\n]+", r.text)
                    if basit_icerik:
                        toplam_vod.extend(basit_icerik)
                        print(f"✅ {len(basit_icerik)} içerik (basit mod) bulundu.")
        except:
            print(f"❌ Bağlantı kurulamadı: {url}")

    # DOSYAYI OLUŞTUR
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        count = 0
        for icerik in toplam_vod:
            f.write(icerik.strip() + "\n")
            count += 1

    zaman = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    print(f"🚀 BİTTİ! Toplam {count} içerik listenize eklendi. ({zaman})")

if __name__ == "__main__":
    main()
