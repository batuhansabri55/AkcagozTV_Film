import requests

def film_cek_cehennem_tarzi():
    # Bu adres, film sitelerinin kullandığı ana veri merkezidir.
    # 'hdfilmcehennemi' de filmleri buradan listeler.
    url = "https://api.themoviedb.org/3/discover/movie?api_key=50e2669788f8d6729a73887d1a580a6b&language=tr-TR&sort_by=primary_release_date.desc&page=1"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    
    try:
        print("HD Cehennemi tarzı güncel filmler taranıyor...")
        res = requests.get(url, headers=headers, timeout=20)
        
        if res.status_code == 200:
            movies = res.json().get('results', [])
            for m in movies:
                isim = m.get('title')
                afis = f"https://image.tmdb.org/t/p/w500{m.get('poster_path')}"
                puan = m.get('vote_average')
                
                # Bu link TiviMate'te filmi açmanı sağlar
                film_link = f"https://www.themoviedb.org/movie/{m.get('id')}"
                
                liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 HD Cehennemi Güncel",{isim} (IMDB: {puan})\n{film_link}')
            
            with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
                f.write("\n".join(liste))
            print(f"BAŞARILI! {len(movies)} film listeye eklendi.")
        else:
            print(f"Hata: {res.status_code}")
            
    except Exception as e:
        print(f"Hata oluştu: {e}")

if __name__ == "__main__":
    film_cek_cehennem_tarzi()
