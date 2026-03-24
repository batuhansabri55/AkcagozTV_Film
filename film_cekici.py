import cloudscraper
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def film_tara():
    # Cloudscraper ile bot korumasini asiyoruz
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    
    rss_url = "https://www.hdfilmcehennemi.nl/feed/"
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        print("RSS verisi profesyonel yontemle cekiliyor...")
        response = scraper.get(rss_url, timeout=30)
        
        if response.status_code == 200:
            # XML verisini ayikla
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            for item in items[:50]:
                title = item.find('title').text
                link = item.find('link').text
                
                # Afis ayiklama
                desc = item.find('description').text
                afis = ""
                if desc:
                    soup = BeautifulSoup(desc, "html.parser")
                    img = soup.find('img')
                    if img:
                        afis = img.get('src', '')
                        if afis.startswith('//'): afis = "https:" + afis

                liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{title}\n{link}')
            
            # Dosyaya yazma islemi
            if len(liste) > 1:
                with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                    f.write("\n".join(liste))
                print(f"ISLEM BASARILI! {len(liste)-1} film eklendi.")
            else:
                print("HATA: RSS icerigi bos geldi.")
        else:
            print(f"HATA: Siteye giris reddedildi (Kod: {response.status_code})")
            
    except Exception as e:
        print(f"KRITIK HATA: {e}")

if __name__ == "__main__":
    film_tara()
