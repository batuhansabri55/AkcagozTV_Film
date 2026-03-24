import requests
from bs4 import BeautifulSoup

def film_tara():
    # FullHDFilmIzlesene 2026 Listesi
    url = "https://www.fullhdfilmizlesene.live/yil/2026-filmleri-izle"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        filmler = []
        
        # Film kutularını tek tek gezer
        for film in soup.select(".film-item"): 
            isim = film.select_one(".title").text.strip()
            link = film.select_one("a")["href"]
            afis = film.select_one("img")["src"]
            
            # M3U formatına çevirir
            filmler.append(f"#EXTINF:-1 tvg-logo='{afis}' group-title='2026 FILMLER',{isim}\n{link}")
        
        # FilmDizi.m3u dosyasını günceller
        if filmler:
            with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                f.write("#EXTM3U\n" + "\n".join(filmler))
            print(f"Basarili: {len(filmler)} film eklendi.")
            
    except Exception as e:
        print(f"Hata olustu: {e}")

if __name__ == "__main__":
    film_tara()
