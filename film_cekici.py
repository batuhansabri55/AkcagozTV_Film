import requests
from bs4 import BeautifulSoup
import os

def film_cek():
    url = "https://www.hdfilmcehennemi.nl/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Siteye erişilemedi: {response.status_code}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Film kartlarını seçiyoruz
        filmler = soup.find_all('div', class_='poster-container')
        
        m3u_icerik = "#EXTM3U\n"
        
        for film in filmler:
            baslik_etiketi = film.find('h2') or film.find('img', alt=True)
            link_etiketi = film.find('a')
            
            if baslik_etiketi and link_etiketi:
                baslik = baslik_etiketi.get('alt') if baslik_etiketi.name == 'img' else baslik_etiketi.text.strip()
                link = link_etiketi.get('href')
                if not link.startswith('http'):
                    link = f"https://www.hdfilmcehennemi.nl{link}"
                
                # M3U formatına ekle (Logonuz varsa tvg-logo ekleyebilirsiniz)
                m3u_icerik += f'#EXTINF:-1 tvg-name="{baslik}" tvg-logo="", {baslik}\n{link}\n'

        # Dosyaya kaydet
        with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
            f.write(m3u_icerik)
            
        print("FilmDizi.m3u başarıyla güncellendi.")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    film_cek()
