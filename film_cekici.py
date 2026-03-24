import requests

def film_tara():
    # Engellenmesi imkansız global film API'si
    url = "https://yts.mx/api/v2/list_movies.json?limit=50&sort_by=year"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        res = requests.get(url, headers=headers, timeout=20)
        if res.status_code == 200:
            movies = res.json().get('data', {}).get('movies', [])
            for m in movies:
                # TiviMate formatında listeye ekle
                liste.append(f'#EXTINF:-1 tvg-logo="{m["large_cover_image"]}" group-title="🎬 Vizyon Filmleri",{m["title"]}\n{m["url"]}')
            
            with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(liste))
            print(f"İşlem Tamam: {len(movies)} film yazıldı.")
    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    film_tara()
