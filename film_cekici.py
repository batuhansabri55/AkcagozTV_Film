import requests
import re

CIKIS_DOSYASI = "FilmDizi.m3u"
VOD_TAG = "#/movies/" 
HEADERS = {"User-Agent": "Mozilla/5.0"}

def film_cek():
    kaynaklar = [
        "https://tinyurl.com/power-cinema",
        "https://tinyurl.com/2bhf2qox",
        "https://tinyurl.com/2ao2rans"
    ]
    
    with open(CIKIS_DOSYASI, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        
        for url in kaynaklar:
            try:
                r = requests.get(url, headers=HEADERS, timeout=15)
                # Resimde gördüğün tüm o uzun etiket satırını ve altındaki URL'yi beraber yakalar
                bloklar = re.findall(r'(#EXTINF:.*?)\n(http.*)', r.text)
                
                for etiket, link in bloklar:
                    # Mevcut kategoriye (group-title) dokunma, sadece linkin sonundaki boşluğu sil
                    temiz_link = f"{link.strip()}{VOD_TAG}"
                    
                    f.write(f"{etiket.strip()}\n")
                    f.write(f"{temiz_link}\n\n")
            except:
                continue

if __name__ == "__main__":
    film_cek()
