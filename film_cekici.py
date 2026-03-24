import requests

def film_tara():
    # Bu kaynak GitHub Actions sunucularını engellemez
    api_url = "https://yts.mx/api/v2/list_movies.json?limit=50&sort_by=year&order_by=desc"
    
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        print("Film verileri çekiliyor...")
        res = requests.get(api_url, timeout=20)
        
        if res.status_code == 200:
            data = res.json()
            movies = data.get('data', {}).get('movies', [])
            
            for m in movies:
                isim = m.get('title', 'Bilinmeyen Film')
                link = m.get('url', '')
                afis = m.get('large_cover_image', '')
                
                # TiviMate ve diğerleri için formatlıyoruz
                liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 Vizyon Filmleri",{isim}\n{link}')
            
            # Dosyayı yaz
            with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(liste))
            
            print(f"BAŞARILI: {len(movies)} film listeye eklendi.")
        else:
            print(f"HATA: API yanıt vermedi, kod: {res.status_code}")
            
    except Exception as e:
        print(f"Kritik Hata Oluştu: {e}")

if __name__ == "__main__":
    film_tara()
