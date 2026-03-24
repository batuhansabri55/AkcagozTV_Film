import requests

def film_tara():
    # Bot koruması olmayan, daha stabil bir veri kaynağı
    # Bu sefer doğrudan film veritabanı API simülasyonu yapıyoruz
    url = "https://yts.mx/api/v2/list_movies.json?sort_by=year&order_by=desc&limit=50"
    
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        print("Film veritabanına bağlanılıyor...")
        res = requests.get(url, timeout=20)
        
        if res.status_code == 200:
            data = res.json()
            movies = data.get('data', {}).get('movies', [])
            
            for film in movies:
                isim = film.get('title_long', 'Bilinmeyen Film')
                link = film.get('url', '')
                afis = film.get('large_cover_image', '')
                yil = film.get('year', '')
                
                # Sadece güncel filmleri (2025-2026) listeye al
                if yil >= 2025:
                    liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 01 Vizyon Filmleri",{isim}\n{link}')
            
            if len(liste) > 1:
                with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                    f.write("\n".join(liste))
                print(f"BAŞARILI! {len(liste)-1} yeni vizyon filmi eklendi.")
            else:
                print("HATA: Kriterlere uygun film bulunamadı.")
        else:
            print(f"HATA: Servis yanıt vermedi. Kod: {res.status_code}")
            
    except Exception as e:
        print(f"Kritik Hata: {e}")

if __name__ == "__main__":
    film_tara()
