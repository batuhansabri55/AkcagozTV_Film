import requests

def film_arsivi_olustur():
    # Bu kaynaklar IPTV dünyasının en sağlam veri havuzlarıdır
    kaynaklar = [
        "https://api.themoviedb.org/3/trending/movie/day?api_key=50e2669788f8d6729a73887d1a580a6b&language=tr-TR",
        "https://api.themoviedb.org/3/movie/popular?api_key=50e2669788f8d6729a73887d1a580a6b&language=tr-TR&page=1"
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    liste = ["#EXTM3U\n#EXT-X-SESSION-DATA:ID='AkcagozTV'"]
    film_sayisi = 0

    print("Film arşivi taranıyor...")

    for url in kaynaklar:
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code == 200:
                veriler = res.json().get('results', [])
                for f in veriler:
                    isim = f.get('title')
                    yil = f.get('release_date', '2026').split('-')[0]
                    afis = f"https://image.tmdb.org/t/p/w500{f.get('poster_path')}"
                    puan = f.get('vote_average')
                    
                    # TiviMate'te filmi açacak link yapısı
                    link = f"https://www.themoviedb.org/movie/{f.get('id')}"
                    
                    liste.append(f'#EXTINF:-1 tvg-logo="{afis}" group-title="🎬 Güncel Filmler (HD Cehennemi Arşivi)",{isim} ({yil}) - Puan: {puan}\n{link}')
                    film_sayisi += 1
        except:
            continue

    if film_sayisi > 0:
        with open("FilmDizi.m3u", "w", encoding="utf-8") as f:
            f.write("\n".join(liste))
        print(f"BAŞARILI! {film_sayisi} film listeye eklendi.")
    else:
        print("HATA: Kaynaklara bağlanılamadı.")

if __name__ == "__main__":
    film_arsivi_olustur()
