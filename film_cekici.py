import requests
from bs4 import BeautifulSoup

def veri_cek(url, secici):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=15)
        res.raise_for_status()
        return BeautifulSoup(res.text, "html.parser").select(secici)
    except:
        return []

def film_tara():
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    # 1. Kaynak Denemesi
    print("1. Kaynak deneniyor...")
    items = veri_cek("https://www.fullhdfilmizlesene.live/yil/2026-filmleri-izle", ".film-item")
    
    # Eğer 1. kaynak boşsa 2. Kaynağı dene
    if not items:
        print("1. Kaynak basarisiz, 2. Kaynak deneniyor...")
        items = veri_cek("https://www.hdfilmcehennemi.nl/kategori/2026-filmleri/", ".poster")

    for film in items[:40]:
        a = film.select_one("a")
        img = film.select_one("img")
        if a and img:
            isim = (img.get('alt') or a.get('title') or "Film").strip()
            link = a['href']
            afis = img.get('data-src') or img.get('src') or ""
            liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{isim}\n{link}')

    # Dosyaya yaz (Sadece liste doluysa yaz ki eski veriyi silmesin)
    if len(liste) > 1:
        with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(liste))
        print(f"Islem TAMAM! {len(liste)-1} film eklendi.")
    else:
        print("HATA: Iki kaynak da veri vermedi!")

if __name__ == "__main__":
    film_tara()
