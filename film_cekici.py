import requests

def film_tara():
    # Bu kaynak (YTS API) GitHub Actions'tan asla engellenmez.
    url = "https://yts.mx/api/v2/list_movies.json?limit=50&sort_by=year"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # Başlık kısmını ekliyoruz
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        print("Film veritabanına bağlanılıyor...")
        res = requests.get(url, headers=headers, timeout=30)
        
        if res.status_code == 200:
            data = res.json()
            movies = data.get('data', {}).get('movies', [])
            
            if not movies:
                print("Hata: Film verisi boş geldi!")
                return

            for m in movies:
                # TiviMate ve IPTV oynatıcılar için tam uyumlu format
                isim = m.get('title', 'Film')
                link = m.get('url', '')
                afis = m.get('large_cover_image', '')
                yil = m.get('year', '')
                
                # Listeye ekle
                liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 Yeni Filmler ({yil})",{isim}\n{link}')
            
            # Dosyaya kaydet
            with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(liste))
            print(f"BAŞARILI! {len(movies)} adet film eklendi.")
        else:
            print(f"API Hatası: {res.status_code}")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    film_tara()
