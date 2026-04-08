import requests
import re

# --- AYARLAR ---
CIKIS_DOSYASI = "FilmDizi.m3u"
# Boşluksuz bitişik VOD takısı
VOD_TAG = "#/movies/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

class AkcagozFilmBotu:
    def __init__(self):
        self.liste = []
        # Senin verdiğin güncel kaynaklar
        self.kaynaklar = [
            {"ad": "Power Cinema", "url": "https://tinyurl.com/power-cinema", "grup": "POWER SİNEMA"},
            {"ad": "Film Arşiv 1", "url": "https://tinyurl.com/2bhf2qox", "grup": "FİLM ARŞİV"},
            {"ad": "Film Arşiv 2", "url": "https://tinyurl.com/2ao2rans", "grup": "DİZİ ARŞİV"}
        ]

    def veri_topla(self):
        print("🚀 TiviMate VOD (Boşluksuz) İçerikler Toplanıyor...")
        for kaynak in self.kaynaklar:
            try:
                print(f"🔎 Tarama: {kaynak['ad']}")
                r = requests.get(kaynak['url'], headers=HEADERS, timeout=25, allow_redirects=True)
                
                # M3U içindeki isim ve URL yapısını yakala
                bulunanlar = re.findall(r'#EXTINF:.*?,(.*?)\n(http.*)', r.text)
                
                for ad, url in bulunanlar:
                    # ham_url.strip() ile baştaki ve sondaki tüm gizli boşlukları siliyoruz
                    ham_url = url.strip()
                    # Arada kesinlikle boşluk bırakmadan birleştiriyoruz
                    vod_url = f"{ham_url}{VOD_TAG}"
                    
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
            print("🛑 Veri çekilemedi, liste boş!")
            return

        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for item in self.liste:
                # TiviMate VOD kütüphanesi için jilet gibi format
                f.write(f'#EXTINF:-1 tvg-logo="{item["logo"]}" group-title="{item["grup"]}",{item["ad"]}\n')
                f.write(f'{item["url"]}\n\n')
        
        print(f"✅ Bitti! {len(self.liste)} içerik boşluksuz şekilde {CIKIS_DOSYASI} dosyasına yazıldı.")

if __name__ == "__main__":
    bot = AkcagozFilmBotu()
    bot.veri_topla()
    bot.m3u_kaydet()
