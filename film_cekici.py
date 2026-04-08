import requests
import re

# --- AYARLAR ---
CIKIS_DOSYASI = "FilmDizi.m3u"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}

class AkcagozFilmBotu:
    def __init__(self):
        self.liste = []
        self.kaynaklar = [
            {"ad": "Power Cinema", "url": "https://tinyurl.com/power-cinema", "grup": "POWER SİNEMA"},
            {"ad": "Film Kaynak 1", "url": "https://tinyurl.com/2bhf2qox", "grup": "FİLM ARŞİV"},
            {"ad": "Film Kaynak 2", "url": "https://tinyurl.com/2ao2rans", "grup": "DİZİ ARŞİV"}
        ]

    def veri_topla(self):
        print("🚀 Film ve Dizi içerikleri çekiliyor...")
        for kaynak in self.kaynaklar:
            try:
                print(f"🔎 Tarama: {kaynak['ad']}")
                r = requests.get(kaynak['url'], headers=HEADERS, timeout=20, allow_redirects=True)
                
                # Sitedeki film/dizi linklerini ve isimlerini yakalayan genel parser
                # Sn. Latte'nin yapısına ve Power Cinema patternine uygundur
                bulunanlar = re.findall(r'#EXTINF:.*?,(.*?)\n(http.*)', r.text)
                
                if bulunanlar:
                    for ad, url in bulunanlar:
                        self.liste.append({
                            "ad": ad.strip(),
                            "url": url.strip(),
                            "logo": "https://via.placeholder.com/300x450?text=" + ad.replace(" ", "+"),
                            "grup": kaynak['grup']
                        })
                else:
                    # Eğer doğrudan link ise veya farklı bir yapıdaysa yedek tarama
                    print(f"⚠️ {kaynak['ad']} için özel tarama yapılıyor...")
                    # HTML içinden link sökme mantığı
                    links = re.findall(r'href="(.*?)"', r.text)
                    for l in links:
                        if ".m3u8" in l or ".mp4" in l:
                            self.liste.append({
                                "ad": kaynak['ad'],
                                "url": l,
                                "logo": "",
                                "grup": kaynak['grup']
                            })
            except Exception as e:
                print(f"❌ {kaynak['ad']} hatası: {e}")

    def m3u_kaydet(self):
        if not self.liste:
            print("🛑 Hiç içerik çekilemedi, liste oluşturulmadı!")
            return

        print(f"💾 {len(self.liste)} içerik dosyaya yazılıyor...")
        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for item in self.liste:
                f.write(f'#EXTINF:-1 tvg-logo="{item["logo"]}" group-title="{item["grup"]}",{item["ad"]}\n')
                f.write(f'{item["url"]}\n\n')
        print(f"✅ {CIKIS_DOSYASI} hazır usta!")

if __name__ == "__main__":
    bot = AkcagozFilmBotu()
    bot.veri_topla()
    bot.m3u_kaydet()
