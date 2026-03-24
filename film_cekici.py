import requests
from bs4 import BeautifulSoup

def film_tara():
    # En stabil calisan kaynak
    url = "https://www.fullhdfilmizlesene.live/yil/2026-filmleri-izle"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        
        # Dosya baslangici
        liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
        
        # Sitedeki ilk 30 filmi çek
        items = soup.select(".film-item")
        for film in items[:30]:
            a = film.select_one("a")
            img = film.select_one("img")
            if a and img:
                isim = a.get('title') or img.get('alt')
                link = a['href']
                afis = img.get('src') or img.get('data-src') or ""
                # Tam senin istedigin kategori ve format
                liste.append(f'#EXTINF:-1 type="movie" tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{isim}\n{link}')
        
        # Dosyayi sifirdan tertemiz yazar (Hata vermez, hızlıdır)
        with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(liste))
        print("Liste basariyla guncellendi!")
            
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    film_tara()
