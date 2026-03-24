import cloudscraper
from bs4 import BeautifulSoup
import time

def film_tara():
    # Cloudscraper, standart requests'in asamadigi engelleri asar
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    
    url = "https://www.hdfilmcehennemi.nl/kategori/2026-filmleri/"
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        print("Site korumasi asiliyor...")
        response = scraper.get(url, timeout=30)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Sitedeki film kutularini buluyoruz
            items = soup.select(".poster")
            
            for film in items[:40]:
                a = film.select_one("a")
                img = film.select_one("img")
                if a and img:
                    isim = (img.get('alt') or a.get('title') or "Film").strip()
                    link = a['href']
                    afis = img.get('data-src') or img.get('src') or ""
                    # Afis linkini duzelt
                    if afis.startswith('//'): afis = "https:" + afis
                    
                    liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{isim}\n{link}')
            
            if len(liste) > 1:
                with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                    f.write("\n".join(liste))
                print(f"ISLEM TAMAM! {len(liste)-1} film eklendi.")
            else:
                print("Hata: Siteye girildi ama film kutulari bulunamadi.")
        else:
            print(f"Hata: Site {response.status_code} koduyla reddetti.")
            
    except Exception as e:
        print(f"Kritik Hata: {e}")

if __name__ == "__main__":
    film_tara()
