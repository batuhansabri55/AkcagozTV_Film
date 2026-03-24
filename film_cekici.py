import requests
from bs4 import BeautifulSoup
import os

def film_tara():
    url = "https://www.fullhdfilmizlesene.live/yil/2026-filmleri-izle"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    kategori_adi = "🎬 01 Vizyon Filmleri"
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")
        yeni_filmler = []
        
        for film in soup.select(".film-item"): 
            isim = film.select_one(".title").text.strip()
            link = film.select_one("a")["href"]
            afis = film.select_one("img")["src"]
            
            # İstediğin formatta ve kategoride satırı hazırlar
            yeni_filmler.append(f'#EXTINF:-1 type="movie" tvg-logo="{afis}" group-title="{kategori_adi}",{isim}\n{link}')
        
        if yeni_filmler:
            dosya_yolu = "FilmDizi.m3u"
            mevcut_icerik = ""
            
            # Eğer dosya zaten varsa eski filmleri oku
            if os.path.exists(dosya_yolu):
                with open(dosya_yolu, "r", encoding="utf-8") as f:
                    mevcut_icerik = f.read()
            
            # Dosya başlığını (M3U) ve yeni filmleri en üste koy, sonra eskileri ekle
            # #EXTM3U satırı zaten varsa onu ayıklarız
            icerik_temiz = mevcut_icerik.replace("#EXTM3U", "").strip()
            tam_liste = "#EXTM3U\n" + "\n".join(yeni_filmler) + "\n" + icerik_temiz
            
            with open(dosya_yolu, "w", encoding="utf-8") as f:
                f.write(tam_liste.strip())
                
            print(f"Basarili: {len(yeni_filmler)} film listenin en basina, {kategori_adi} grubuna eklendi.")
            
    except Exception as e:
        print(f"Hata olustu: {e}")

if __name__ == "__main__":
    film_tara()
