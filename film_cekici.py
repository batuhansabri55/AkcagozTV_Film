import requests
import re
import os
import datetime

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# IMAGE_E7AD98 VE IMAGE_E7B0DD GÖRÜNTÜLERİNDEKİ GERÇEK DOSYA YOLLARI
VOD_KAYNAKLAR = [
    # Ana Arşivler
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/best/all.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/turkey.m3u8",
    # image_e7ad98'de görülen tekil m3u8 dosyaları
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/baskatv-kick.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/bizimbergamatv.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/serhattv.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/teleon.m3u8"
]

def main():
    print("🎬 VOD Avcısı 4.0 Başlatıldı...")
    toplam_vod = []

    for url in VOD_KAYNAKLAR:
        try:
            print(f"🔎 Arşiv taranıyor: {url}")
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                # Regex'i en basit hale getirdik: #EXTINF ile başlayıp http ile biten her şeyi al
                icerikler = re.findall(r"(#EXTINF:[^\n]+\n+http[^\s\n]+)", r.text)
                if icerikler:
                    toplam_vod.extend(icerikler)
                    print(f"✅ {len(icerikler)} içerik çekildi.")
        except:
            pass

    # DOSYAYA YAZMA
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        # Tekrar edenleri temizle (Duplicate)
        benzersiz_vod = list(set(toplam_vod))
        for icerik in benzersiz_vod:
            f.write(icerik.strip() + "\n")

    print(f"🚀 OPERASYON TAMAM! {len(benzersiz_vod)} Film/Dizi eklendi.")

if __name__ == "__main__":
    main()
