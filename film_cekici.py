import requests

def film_tara():
    # Engellenmesi imkansiz, dogrudan API uzerinden veri cekiyoruz
    api_url = "https://www.hdfilmcehennemi.nl/api/v1/movies?category=2026-filmleri&limit=50"
    # Eger yukaridaki API calismazsa alternatif (Genel veri)
    fallback_url = "https://www.hdfilmcehennemi.nl/kategori/2026-filmleri/page/1/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        print("Veri motoruna baglaniliyor...")
        # Ilk olarak standart sayfa istegi (Cookie almak icin)
        session = requests.Session()
        session.get("https://www.hdfilmcehennemi.nl/", headers=headers, timeout=10)
        
        # Simdi veriyi cek
        res = session.get(fallback_url, headers=headers, timeout=15)
        
        if res.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(res.text, "html.parser")
            items = soup.select(".poster")
            
            for film in items:
                a = film.select_one("a")
                img = film.select_one("img")
                if a and img:
                    isim = img.get('alt', 'Film').strip()
                    link = a['href']
                    afis = img.get('data-src') or img.get('src') or ""
                    if afis.startswith('//'): afis = "https:" + afis
                    
                    liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{isim}\n{link}')
            
            if len(liste) > 1:
                with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                    f.write("\n".join(liste))
                print(f"BINGO! {len(liste)-1} film dosyaya yazildi.")
            else:
                print("Hata: Site icerigi hala bos donuyor.")
        else:
            print(f"Hata: Baglanti reddedildi. Kod: {res.status_code}")
            
    except Exception as e:
        print(f"Hata detayi: {e}")

if __name__ == "__main__":
    film_tara()
