import requests
import re

CIKIS_DOSYASI = "FilmDizi.m3u"
VOD_TAG = "#/movies/" # Boşluksuz bitişik
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
                # Satır satır tara: Hem etiketi (group-title dahil) hem URL'yi al
                bloklar = re.findall(r'(#EXTINF:.*?)\n(http.*)', r.text)
                
                for etiket, link in bloklar:
                    # Linkin sonundaki boşluğu sil ve VOD takısını yapıştır
                    temiz_link = f"{link.strip()}{VOD_TAG}"
                    
                    f.write(f"{etiket.strip()}\n")
                    f.write(f"{temiz_link}\n\n")
            except:
                continue

if __name__ == "__main__":
    film_cek()
