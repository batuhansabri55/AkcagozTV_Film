import requests
from bs4 import BeautifulSoup
import time

def film_tara():
    # 2026'nin en guncel ve acik sitesi
    url = "https://www.hdfilmcehennemi.nl/kategori/2026-filmleri/"
    
    # Gercek bir tarayici gibi gorunmek icin gelismis basliklar
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com/"
    }
    
    try:
        print("Siteye baglaniliyor...")
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        
        liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
        
        # Sitedeki film kutularini bul (2026 guncel secicisi)
        items = soup.select(".poster") # Bu site icin en garanti secici
        
        found_count = 0
        for film in items[:40]: # Ilk 40 filmi al
            a = film.select_one("a")
            img = film.select_one("img")
            
            if a and img:
                isim = (img.get('alt') or a.get('title') or "Adsiz Film").strip()
                link = a['href']
                afis = img.get('data-src') or img.get('src') or ""
                
                # Linkleri TiviMate'in sevecegi formata sok
                if not afis.startswith('http'): afis = "https:" + afis if afis.startswith('//') else afis
                
                liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{isim}\n{link}')
                found_count += 1
        
        if found_count > 0:
            with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(liste))
            print(f"Basarili! {found_count} film listeye eklendi.")
        else:
            print("Hata: Hic film bulunamadi, site yapisi degismis olabilir.")
            
    except Exception as e:
        print(f"Baglanti Hatasi: {e}")

if __name__ == "__main__":
    film_tara()
