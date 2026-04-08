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
        self.kategorize_liste = {}  # Kategorilere göre sözlük yapısı
        self.kaynaklar = [
            {"ad": "Power Cinema", "url": "https://tinyurl.com/power-cinema", "grup": "POWER SİNEMA"},
            {"ad": "Film Arşiv 1", "url": "https://tinyurl.com/2bhf2qox", "grup": "FİLM ARŞİV"},
            {"ad": "Film Arşiv 2", "url": "https://tinyurl.com/2ao2rans", "grup": "DİZİ ARŞİV"}
        ]

    def veri_topla(self):
        print("🚀 TiviMate VOD Kategorizasyon Başlatıldı...")
        for kaynak in self.kaynaklar:
            try:
                print(f"🔎 Tarama: {kaynak['ad']}")
                r = requests.get(kaynak['url'], headers=HEADERS, timeout=25, allow_redirects=True)
                bulunanlar = re.findall(r'#EXTINF:.*?,(.*?)\n(http.*)', r.text)
                
                if kaynak['grup'] not in self.kategorize_liste:
                    self.kategorize_liste[kaynak['grup']] = []

                for ad, url in bulunanlar:
                    # Linkin sonundaki boşlukları strip() ile siliyoruz, sonra takıyı ekliyoruz
                    vod_url = f"{url.strip()}{VOD_TAG}"
                    
                    self.kategorize_liste[kaynak['grup']].append({
                        "ad": ad.strip(),
                        "url": vod_url,
                        "logo": "https://via.placeholder.com/300x450?text=" + ad.strip().replace(" ", "+")
                    })
            except Exception as e:
                print(f"❌ {kaynak['ad']} hatası: {e}")

    def m3u_kaydet(self):
        if not self.kategorize_liste:
            print("🛑 Veri bulunamadı!")
            return

        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            # Her grubu kendi içinde yazdırarak TiviMate'in kategorileri tanımasını sağlıyoruz
            for grup_adi, filmler in self.kategorize_liste.items():
                print(f"📦 {grup_adi} grubu yazılıyor ({len(filmler)} içerik)...")
                for film in filmler:
                    f.write(f'#EXTINF:-1 tvg-logo="{film["logo"]}" group-title="{grup_adi}",{film["ad"]}\n')
                    f.write(f'{film["url"]}\n\n')
        
        print(f"✅ İşlem bitti. {CIKIS_DOSYASI} jilet gibi hazır.")

if __name__ == "__main__":
    bot = AkcagozFilmBotu()
    bot.veri_topla()
    bot.m3u_kaydet()
