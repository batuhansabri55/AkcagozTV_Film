import requests
from bs4 import BeautifulSoup

def film_tara():
    # 2026'nın en sağlam linki
    url = "https://www.fullhdfilmizlesene.live/yil/2026-filmleri-izle"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Dosyayı sıfırdan oluşturuyoruz (Hata vermemesi için)
        liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
        
        # İlk 30 filmi çek
        for film in soup.select(".film-item")[:30]:
            a = film.select_one("a")
            img = film.select_one("img")
            if a and img:
                isim = a.get('title') or img.get('alt')
                link = a['href']
                afis = img.get('src') or img.get('data-src') or ""
                liste.append(f'#EXTINF:-1 type="movie" tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{isim}\n{link}')
        
        # Dosyayı tertemiz kaydet
        with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(liste))
        print("Bitti! Liste artik doldu.")
            
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    film_tara()
