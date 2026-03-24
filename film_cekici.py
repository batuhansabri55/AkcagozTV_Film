import requests

def film_tara():
    # Global film API'si (Bloklanma riski yok)
    url = "https://yts.mx/api/v2/list_movies.json?limit=50&sort_by=year"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            data = res.json()
            movies = data.get('data', {}).get('movies', [])
            
            for m in movies:
                isim = m.get('title', 'Bilinmeyen Film')
                link = m.get('url', '')
                afis = m.get('large_cover_image', '')
                # TiviMate formatı
                liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 Vizyon Filmleri",{isim}\n{link}')
            
            with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(liste))
            print(f"BASARILI: {len(movies)} film yazildi.")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    film_tara()
