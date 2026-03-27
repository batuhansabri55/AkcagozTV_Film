import requests
import re
import os
import datetime

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# TARANACAK DEV FİLM ARŞİVLERİ
VOD_KAYNAKLAR = [
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/movies.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/Legal-IPTV/main/lists/movies.m3u8",
    "https://raw.githubusercontent.com/UzunMuhalefet/yayinlar/main/streams/series.m3u8"
]

def main():
    print("🎬 VOD Avcısı Başlatıldı...")
    toplam_vod = []

    for url in VOD_KAYNAKLAR:
        try:
            print(f"🔎 Film aranıyor: {url}")
            r = requests.get(url, headers=HEADERS, timeout=30)
            if r.status_code == 200:
                # Film bloğunu yakala (Afiş, İsim ve Link)
                # re.DOTALL ile satır atlamalarını da okur
                icerikler = re.findall(r"(#EXTINF:.*?\n+http.*?)(?=#EXTINF|$)", r.text, re.DOTALL)
                toplam_vod.extend(icerikler)
                print(f"✅ {len(icerikler)} içerik bulundu.")
        except:
            print(f"❌ Kaynağa ulaşılamadı: {url}")

    # DOSYAYA YAZMA
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        for icerik in toplam_vod:
            # TiviMate'in film olarak tanıması için temizlik ve düzenleme
            temiz_icerik = icerik.strip()
            # Eğer içerikte grup yoksa "GENEL FİLMLER" yapalım
            if 'group-title="' not in temiz_icerik:
                temiz_icerik = temiz_icerik.replace('#EXTINF:', '#EXTINF:-1 group-title="YENİ FİLMLER",')
            
            f.write(temiz_icerik + "\n")

    zaman = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    print(f"🚀 BİTTİ! Toplam {len(toplam_vod)} Film/Dizi listenize eklendi. ({zaman})")

if __name__ == "__main__":
    main()
