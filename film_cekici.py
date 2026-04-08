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
        print("🔎 Film Makinesi taranıyor...")
        url = "https://www.filmmakinesi.pw"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            # Parser.js mantığı: Poster, Link ve Başlık avı
            pattern = r'<div class="poster">.*?<a href="(.*?)" title="(.*?)">.*?<img src="(.*?)"'
            matches = re.findall(pattern, r.text, re.S)
            for link, baslik, poster in matches:
                self.icerik_listesi.append({"ad": baslik, "url": link, "logo": poster, "grup": "FİLM MAKİNESİ"})
        except: pass

    def filmmodu_tara(self):
        print("🔎 FilmModu taranıyor...")
        url = "https://www.filmmodu.org"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            pattern = r'<div class="movie-post">.*?<a href="(.*?)".*?title="(.*?)".*?<img src="(.*?)"'
            matches = re.findall(pattern, r.text, re.S)
            for link, baslik, poster in matches:
                l = link if link.startswith('http') else url + link
                self.icerik_listesi.append({"ad": baslik, "url": l, "logo": poster, "grup": "FİLM MODU"})
        except: pass

    def fullhdfilm_tara(self):
        print("🔎 FullHDFilmIzlesene (Power) taranıyor...")
        url = "https://www.fullhdfilmizlesene.pw"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            # Sitedeki film bloklarını yakalayan güncel pattern
            pattern = r'<div class="poster">.*?<a href="(.*?)" title="(.*?)">.*?<img.*?src="(.*?)"'
            matches = re.findall(pattern, r.text, re.S)
            for link, baslik, poster in matches:
                self.icerik_listesi.append({"ad": baslik, "url": link, "logo": poster, "grup": "FULL HD FİLM"})
        except: pass

    def 720pizle_tara(self):
        print("🔎 720pIzle taranıyor...")
        url = "https://720pizle.pw"
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            pattern = r'<div class="movie-data">.*?<a href="(.*?)" title="(.*?)">.*?<img src="(.*?)"'
            matches = re.findall(pattern, r.text, re.S)
            for link, baslik, poster in matches:
                self.icerik_listesi.append({"ad": baslik, "url": link, "logo": poster, "grup": "720P İZLE"})
        except: pass

    def dosyaya_yaz(self):
        print(f"💾 {len(self.icerik_listesi)} içerik M3U'ya yazılıyor...")
        with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n")
            for item in self.icerik_listesi:
                # TiviMate v5.2 için en temiz format
                f.write(f'#EXTINF:-1 tvg-logo="{item["logo"]}" group-title="{item["grup"]}",{item["ad"]}\n')
                f.write(f'{item["url"]}\n\n')
        print(f"✅ {CIKIS_DOSYASI} depoya yüklendi!")

if __name__ == "__main__":
    bot = AkcagozFilmCekici()
    bot.filmmakinesi_tara()
    bot.filmmodu_tara()
    bot.fullhdfilm_tara()
    bot.720pizle_tara()
    
    if bot.icerik_listesi:
        bot.dosyaya_yaz()
    else:
        print("⚠️ Hata: Hiçbir siteden veri çekilemedi. Patternleri kontrol et!")
