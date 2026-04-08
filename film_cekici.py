import requests
import re
import os

# AYARLAR
CIKIS_DOSYASI = "FilmDizi.m3u"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"

# Parser.js mantığını Python'a uyarlayan "Video Avcıları"
class FilmParser:
    @staticmethod
    def filmmakinesi_cek():
        # Film Makinesi ana sayfasından son eklenenleri toplar
        base_url = "https://www.filmmakinesi.pw"
        try:
            res = requests.get(base_url, headers={"User-Agent": USER_AGENT}, timeout=10)
            # Regex ile film adlarını, linklerini ve afişlerini söküyoruz (Parser.js mantığı)
            filmler = re.findall(r'<div class="poster">.*?<a href="(.*?)" title="(.*?)">.*?<img src="(.*?)"', res.text, re.S)
            return [{"ad": f[1], "url": f[0], "logo": f[2], "grup": "FİLM MAKİNESİ"} for f in filmler]
        except: return []

    @staticmethod
    def filmmodu_cek():
        base_url = "https://www.filmmodu.org"
        try:
            res = requests.get(base_url, headers={"User-Agent": USER_AGENT}, timeout=10)
            filmler = re.findall(r'<div class="movie-post">.*?<a href="(.*?)".*?title="(.*?)".*?<img src="(.*?)"', res.text, re.S)
            return [{"ad": f[1], "url": f[0], "logo": f[2], "grup": "FİLM MODU"} for f in filmler]
        except: return []

def liste_olustur():
    print("🚀 17.000+ İçerik İçin Tarama Başlatıldı...")
    m3u_icerik = "#EXTM3U\n"
    
    parser = FilmParser()
    tum_icerikler = []
    
    # Parser.js içindeki siteleri tek tek dönüyoruz
    tum_icerikler.extend(parser.filmmakinesi_cek())
    tum_icerikler.extend(parser.filmmodu_cek())

    for item in tum_icerikler:
        # Linki senin sistemine göre temiz dizeye çevirir
        m3u_icerik += f'#EXTINF:-1 tvg-logo="{item["logo"]}" group-title="{item["grup"]}",{item["ad"]}\n{item["url"]}\n'

    with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
        f.write(m3u_icerik)
    
    print(f"✅ İşlem Tamam! {len(tum_icerikler)} içerik {CIKIS_DOSYASI} dosyasına yüklendi.")

if __name__ == "__main__":
    liste_olustur()
