import requests
import re
import os
import datetime

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

# UZUNMUHALEFET'İN GERÇEK VOD KLASÖRLERİNDEN GELEN GÜNCEL LİNKLER
VOD_KAYNAKLAR = [
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/lists/movies.m3u", # Ana film listesi
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/lists/series.m3u", # Ana dizi listesi
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/movies.m3u8", # Alternatif film
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/best/movies.m3u8" # En iyi kalite klasörü
]

def main():
    print("🎬 VOD Avcısı 2.0 Başlatıldı...")
    toplam_vod = []

    for url in VOD_KAYNAKLAR:
        try:
            print(f"🔎 Arşiv taranıyor: {url}")
            r = requests.get(url, headers=HEADERS, timeout=35)
            if r.status_code == 200:
                # Regex: #EXTINF satırından başlayıp altındaki linkin sonuna kadar her şeyi (boşluk dahil) yakalar
                icerikler = re.findall(r"(#EXTINF:[^\n]+\n+http[^\s\n]+)", r.text)
                if icerikler:
                    toplam_vod.extend(icerikler)
                    print(f"✅ {len(icerikler)} içerik çekildi.")
                else:
                    print("⚠️ Bu linkte uygun formatta içerik bulunamadı.")
        except Exception as e:
            print(f"❌ Bağlantı hatası: {str(e)}")

    # DOSYAYA YAZMA (M3U FORMATINDA)
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        for icerik in toplam_vod:
            f.write(icerik.strip() + "\n")

    zaman = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    print(f"🚀 OPERASYON TAMAM! {len(toplam_vod)} Film/Dizi listenize eklendi. ({zaman})")

if __name__ == "__main__":
    main()
