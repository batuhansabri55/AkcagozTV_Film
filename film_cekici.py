import requests
from bs4 import BeautifulSoup
import random
import time

def film_tara():
    # En taze 2026 kaynakları
    kaynaklar = [
        {"url": "https://www.hdfilmcehennemi.nl/kategori/2026-filmleri/", "sc": ".poster"},
        {"url": "https://www.fullhdfilmizlesene.live/yil/2026-filmleri-izle", "sc": ".film-item"}
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    for site in kaynaklar:
        try:
            print(f"{site['url']} taranıyor...")
            # Siteyi yormamak ve bot olduğumuzu belli etmemek için rastgele bekleme
            time.sleep(random.randint(2, 5))
            
            res = requests.get(site['url'], headers=headers, timeout=20)
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, "html.parser")
                items = soup.select(site['sc'])
                
                for film in items[:20]:
                    a = film.select_one("a")
                    img = film.select_one("img")
                    if a and img:
                        isim = (img.get('alt') or a.get('title') or "Film").strip()
                        link = a['href']
                        afis = img.get('data-src') or img.get('src') or ""
                        if not afis.startswith('http'): afis = "https:" + afis if afis.startswith('//') else afis
                        
                        liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{isim}\n{link}')
        except Exception as e:
            print(f"Hata oluştu: {e}")
            continue

    if len(liste) > 1:
        with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(liste))
        print(f"BAŞARILI! {len(liste)-1} film dosyaya yazıldı.")
    else:
        print("KRİTİK HATA: Hiçbir siteden veri çekilemedi!")

if __name__ == "__main__":
    film_tara()
