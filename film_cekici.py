import requests
import re

# --- AYARLAR ---
# TiviMate'in içeriği Film/Dizi sekmesine alması için /movies/ takısı şarttır
WORKER_BASE_URL = "https://atv-switch.huseyinakcagoz.workers.dev/movies/"
CIKIS_DOSYASI = "FilmDizi.m3u"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

class AkcagozFilmBotu:
    def __init__(self):
        self.liste = []
        # Sn. Latte ve Power Cinema kaynakları
        self.kaynaklar = [
            {"ad": "Power Cinema", "url": "https://tinyurl.com/power-cinema", "grup": "POWER SİNEMA"},
            {"ad": "Film Arşiv 1", "url": "https://tinyurl.com/2bhf2qox", "grup": "FİLM ARŞİV"},
            {"ad": "Film Arşiv 2", "url": "https://tinyurl.com/2ao2rans", "grup": "DİZİ ARŞİV"}
        ]

    def veri_topla(self):
        print("🚀 TiviMate VOD uyumlu içerikler toplanıyor...")
        for kaynak in self.kaynaklar:
            try:
                print(f"🔎 Tarama: {kaynak['ad']}")
                r = requests.get(kaynak['url'], headers=HEADERS, timeout=25, allow_redirects=True)
                
                # M3U içindeki isim ve URL yapısını yakalıyoruz
                bulunanlar = re.findall(r'#EXTINF:.*?,(.*?)\n(http.*)', r.text)
                
                for ad, url in bulunanlar:
                    ham_url = url.strip()
                    # KRİTİK: TiviMate VOD bölümü için link yapısını düzenliyoruz
                    vod_url = f"{WORKER_BASE_URL}{ham_url}"
                    
                    self.liste.append({
                        "ad": ad.strip(),
                        "url": vod_url,
                        "logo": "https://via.placeholder.com/300x450?text=" + ad.strip().replace(" ", "+"),
                        "grup": kaynak['grup']
                    })
            except Exception as e:
                print(f"❌ {kaynak['ad']} hatası: {e}")

    def m3u_kaydet(self):
        if not self.liste:
            print("🛑 Veri çekilemedi, patternleri kontrol et!")
            return

        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for item in self.liste:
                # TiviMate v5.2 için grup ve logo bilgilerini basıyoruz
                f.write(f'#EXTINF:-1 tvg-logo="{item["logo"]}" group-title="{item["grup"]}",{item["ad"]}\n')
                f.write(f'{item["url"]}\n\n')
        print(f"✅ {len(self.liste)} içerik {CIKIS_DOSYASI} dosyasına jilet gibi dizildi.")

if __name__ == "__main__":
    bot = AkcagozFilmBotu()
    bot.veri_topla()
    bot.m3u_kaydet()
