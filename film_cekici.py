import requests
import re
import os
import datetime

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
}

# SENİN VERDİĞİN YENİ VE GÜÇLÜ VOD KAYNAKLARI
VOD_KAYNAKLAR = [
    "https://tinyurl.com/2ys5fe3h",
    "https://tinyurl.com/2ao2rans",
    "https://tinyurl.com/power-cinema"
]

def main():
    print("🎬 VOD Avcısı 5.0 (Power Cinema) Başlatıldı...")
    toplam_vod = []

    for index, url in enumerate(VOD_KAYNAKLAR, 1):
        try:
            print(f"🔎 Kaynak taranıyor ({index}/3): {url}")
            # Redirect (yönlendirme) takibi için allow_redirects=True yapıyoruz
            r = requests.get(url, headers=HEADERS, timeout=45, allow_redirects=True)
            
            if r.status_code == 200:
                # Regex: #EXTINF satırından başlar, linkin sonuna kadar her şeyi alır
                # Özellikle tvg-logo (afiş) ve group-title (kategori) kısımlarını korur
                icerikler = re.findall(r"(#EXTINF:[^\n]+\n+http[^\s\n]+)", r.text, re.IGNORECASE)
                
                if icerikler:
                    toplam_vod.extend(icerikler)
                    print(f"✅ {len(icerikler)} film/dizi çekildi.")
                else:
                    print("⚠️ İçerik formatı uymadı, ham metin kontrol ediliyor...")
                    # Eğer format farklıysa daha esnek bir arama yap
                    esnek_icerik = re.findall(r"#EXTINF:.*?\n+.*?http.*", r.text)
                    toplam_vod.extend(esnek_icerik)
        except Exception as e:
            print(f"❌ Bağlantı hatası ({url}): {str(e)}")

    # DOSYAYA YAZMA
    with open(VOD_FILE, 'w', encoding='utf-8') as f:
        f.write("#EXTM3U\n")
        
        # Tekrar eden linkleri temizle (duplicate engelleme)
        benzersiz_list = list(dict.fromkeys(toplam_vod))
        
        for madde in benzersiz_list:
            f.write(madde.strip() + "\n")

    zaman = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')
    print(f"🚀 OPERASYON TAMAM! Toplam {len(benzersiz_list)} Film/Dizi eklendi. ({zaman})")

if __name__ == "__main__":
    main()
