import requests
import re
import os

# --- AYARLAR ---
CIKIS_DOSYASI = "FilmDizi.m3u"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Referer": "https://www.google.com/"
}

class AkcagozFilmCekici:
    def __init__(self):
        self.icerik_listesi = []

    def filmmakinesi_tara(self):
        """Parser.js'deki filmmakinesi mantığına göre ana sayfayı tarar"""
        print("🔎 Film Makinesi taranıyor...")
        url = "https://www.filmmakinesi.pw"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            # Film kartlarındaki Link, Başlık ve Poster bilgilerini regex ile söküyoruz
            pattern = r'<div class="poster">.*?<a href="(.*?)" title="(.*?)">.*?<img src="(.*?)"'
            matches = re.findall(pattern, r.text, re.S)
            for link, baslik, poster in matches:
                self.icerik_listesi.append({
                    "ad": baslik,
                    "url": link,
                    "logo": poster,
                    "grup": "FİLM MAKİNESİ"
                })
        except Exception as e:
            print(f"❌ Film Makinesi hatası: {e}")

    def filmmodu_tara(self):
        """Parser.js'deki filmmodu mantığına göre tarar"""
        print("🔎 FilmModu taranıyor...")
        url = "https://www.filmmodu.org"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            pattern = r'<div class="movie-post">.*?<a href="(.*?)".*?title="(.*?)".*?<img src="(.*?)"'
            matches = re.findall(pattern, r.text, re.S)
            for link, baslik, poster in matches:
                if not link.startswith('http'): link = url + link
                self.icerik_listesi.append({
                    "ad": baslik,
                    "url": link,
                    "logo": poster,
                    "grup": "FİLM MODU"
                })
        except Exception as e:
            print(f"❌ FilmModu hatası: {e}")

    def dosyaya_yaz(self):
        print(f"💾 {len(self.icerik_listesi)} içerik dosyaya yazılıyor...")
        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for item in self.icerik_listesi:
                f.write(f'#EXTINF:-1 tvg-logo="{item["logo"]}" group-title="{item["grup"]}",{item["ad"]}\n')
                f.write(f'{item["url"]}\n\n')
        print(f"✅ {CIKIS_DOSYASI} başarıyla güncellendi.")

if __name__ == "__main__":
    bot = AkcagozFilmCekici()
    
    # Parser mantığındaki siteleri tara
    bot.filmmakinesi_tara()
    bot.filmmodu_tara()
    
    # Sonucu depoya kaydet
    if bot.icerik_listesi:
        bot.dosyaya_yaz()
    else:
        print("⚠️ Hiç içerik bulunamadı, tarayıcı patternlerini kontrol et!")
