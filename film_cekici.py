import requests
from bs4 import BeautifulSoup

def hdfilm_kazı():
    # Güncel adresini buraya sabitledik
    url = "https://www.hdfilmcehennemi.nl/"
    
    # Gerçek bir kullanıcı gibi görünmek için detaylı başlıklar
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com/'
    }
    
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        print(f"{url} adresi taranıyor...")
        session = requests.Session()
        res = session.get(url, headers=headers, timeout=30)
        res.encoding = 'utf-8'
        
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            # Sitedeki film kartlarını buluyoruz
            filmler = soup.find_all('div', class_='poster-container')
            
            for film in filmler:
                link_etiketi = film.find('a')
                resim_etiketi = film.find('img')
                
                if link_etiketi and resim_etiketi:
                    # Film adını al
                    isim = resim_etiketi.get('alt') or "Film"
                    # Film sayfa linkini al
                    link = link_etiketi['href']
                    if not link.startswith('http'):
                        link = "https://www.hdfilmcehennemi.nl" + link
                    
                    # Film afişini al
                    afis = resim_etiketi.get('data-src') or resim_etiketi.get('src') or ""
                    
                    # M3U formatına ekle
                    liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="HD Cehennemi (Yeni)",{isim}\n{link}')
            
            # Dosyayı yazdır
            if len(liste) > 1:
                with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                    f.write("\n".join(liste))
                print(f"BAŞARILI! {len(liste)-1} adet film listeye eklendi.")
            else:
                print("Hata: Sitede film yapısı bulunamadı (Tasarım değişmiş olabilir).")
        else:
            print(f"Siteye erişilemedi. Hata kodu: {res.status_code}")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    hdfilm_kazı()
