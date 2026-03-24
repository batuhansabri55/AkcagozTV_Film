import requests
from bs4 import BeautifulSoup

def film_tara():
    # Sadece FullHDFilmIzlesene 2026 (En hızlı ve garantisi bu)
    url = "https://www.fullhdfilmizlesene.live/yil/2026-filmleri-izle"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        yeni_filmler = ["#EXTM3U"]
        
        # Sitedeki ilk 20 filmi alalım
        items = soup.select(".film-item")
        for film in items[:20]:
            a_tag = film.select_one("a")
            img_tag = film.select_one("img")
            if a_tag and img_tag:
                isim = a_tag.get('title') or img_tag.get('alt')
                link = a_tag['href']
                afis = img_tag.get('src') or img_tag.get('data-src')
                yeni_filmler.append(f'#EXTINF:-1 type="movie" tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{isim}\n{link}')
        
        # Mevcut büyük dosyayı okumadan, sıfırdan küçük ve hızlı bir dosya yazar
        with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(yeni_filmler))
        print("Sifir dosya olusturuldu, filmler eklendi!")
            
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    film_tara()
