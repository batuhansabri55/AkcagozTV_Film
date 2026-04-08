import requests
import re

def film_makinesi_cek():
    dosya_adi = "FilmDizi.m3u"
    site_url = "https://www.filmmakinesi.net/"
    headers = {'User-Agent': 'Mozilla/5.0'}

    try:
        # 1. Sitenin ana sayfasını indir
        print("Film Makinesi taranıyor...")
        r = requests.get(site_url, headers=headers, timeout=15)
        
        # 2. Film linklerini ve isimlerini ayıkla (Regex ile)
        # Sitedeki <a href="..." title="..."> yapısını yakalıyoruz
        filmler = re.findall(r'class="movie-title"><a href="(https://www.filmmakinesi.net/[^"]+)" title="([^"]+)"', r.text)

        if not filmler:
            print("Film bulunamadı, site yapısı değişmiş olabilir.")
            return

        with open(dosya_adi, "a", encoding="utf-8") as f:
            f.write("\n\n# --- SEYİRTÜRK: FİLM MAKİNESİ GÜNCEL --- \n")
            
            for link, isim in filmler[:20]: # Son 20 filmi al
                # TiviMate için jilet gibi format
                temiz_link = link if link.endswith("/") else link + "/"
                final_url = f"{temiz_link}#/MOVIES/"
                
                f.write(f'#EXTINF:-1 group-title="SEYİRTÜRK FİLMLER", {isim}\n')
                f.write(f'{final_url}\n')

        print(f"{len(filmler[:20])} adet yeni film listenin sonuna eklendi usta!")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    film_makinesi_cek()
