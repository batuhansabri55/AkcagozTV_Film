import requests
from bs4 import BeautifulSoup
import os

def film_tara():
    # Güncel 2026 Film Linkleri
    siteler = [
        {"url": "https://www.fullhdfilmizlesene.live/yil/2026-filmleri-izle", "kat": "🎬 01 Vizyon Filmleri"},
        {"url": "https://www.hdfilmcehennemi.nl/kategori/2026-filmleri/", "kat": "🎬 01 Vizyon Filmleri"},
        {"url": "https://sinemaizle.org/yil/2026-filmleri/", "kat": "🎬 01 Vizyon Filmleri"}
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    yeni_filmler = []

    for site in siteler:
        try:
            print(f"Taraniyor: {site['url']}")
            res = requests.get(site["url"], headers=headers, timeout=15)
            soup = BeautifulSoup(res.text, "html.parser")
            
            # 2026 siteleri için en geniş kapsamlı arama seçicileri
            items = soup.find_all(['div', 'article'], class_=['film-item', 'poster', 'movie-item', 'post-column'])
            
            for film in items[:15]: 
                a_tag = film.find('a')
                img_tag = film.find('img')
                
                if a_tag and a_tag.get('href'):
                    isim = (a_tag.get('title') or img_tag.get('alt') or a_tag.text).strip()
                    link = a_tag['href']
                    afis = img_tag.get('src') or img_tag.get('data-src') or ""
                    
                    if not afis.startswith('http'): afis = "https:" + afis if afis.startswith('//') else afis
                    
                    yeni_filmler.append(f'#EXTINF:-1 type="movie" tvg-logo="{afis}" group-title="{site["kat"]}",{isim}\n{link}')
        except Exception as e:
            print(f"Hata: {site['url']} -> {e}")

    if yeni_filmler:
        dosya = "FilmDizi.m3u"
        eski_icerik = ""
        if os.path.exists(dosya):
            with open(dosya, "r", encoding="utf-8") as f:
                eski_icerik = f.read().replace("#EXTM3U", "").strip()
        
        with open(dosya, "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(yeni_filmler) + "\n" + eski_icerik)
        print(f"Basarili: {len(yeni_filmler)} yeni film eklendi.")
    else:
        print("Uyari: Hic film bulunamadi, seciciler kontrol edilmeli.")

if __name__ == "__main__":
    film_tara()
