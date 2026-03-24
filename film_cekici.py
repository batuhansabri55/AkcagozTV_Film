import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

def film_tara():
    # RSS beslemesi bot korumasina takilmaz
    rss_url = "https://www.hdfilmcehennemi.nl/feed/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        print("RSS verisi cekiliyor...")
        res = requests.get(rss_url, headers=headers, timeout=20)
        
        if res.status_code == 200:
            # XML verisini ayikla
            root = ET.fromstring(res.content)
            items = root.findall('.//item')
            
            for item in items[:40]:
                title = item.find('title').text
                link = item.find('link').text
                
                # Afis genelde aciklama (description) icinde img tagi olarak bulunur
                desc = item.find('description').text
                afis = ""
                if desc:
                    soup = BeautifulSoup(desc, "html.parser")
                    img = soup.find('img')
                    if img:
                        afis = img.get('src', '')

                liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{title}\n{link}')
            
            if len(liste) > 1:
                with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                    f.write("\n".join(liste))
                print(f"BASARILI! {len(liste)-1} film RSS ile eklendi.")
            else:
                print("Hata: RSS icinde film bulunamadi.")
        else:
            print(f"Hata: RSS servisi {res.status_code} dondu.")
            
    except Exception as e:
        print(f"RSS Hatasi: {e}")

if __name__ == "__main__":
    film_tara()
