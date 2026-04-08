import requests

def film_listesini_guncelle():
    # 1. AYARLAR
    dosya_adi = "FilmDizi.m3u"
    worker_url = "https://atv-switch.huseyinakcagoz.workers.dev" # Senin görseldeki worker adresin
    
    # SeyirTur listesindeki en popüler film kaynakları
    kaynaklar = [
        {"ad": "POWER CINEMA", "url": "https://tinyurl.com/power-cinema"},
        # Buraya o görseldeki diğer m3u kaynaklarını ekleyebilirsin
    ]

    try:
        # Mevcut dosyanı korumak için önce temiz bir başlangıç (isteğe bağlı) 
        # veya 'a' ile sona ekleme yapıyoruz.
        with open(dosya_adi, "a", encoding="utf-8") as f:
            
            for kaynak in kaynaklar:
                print(f"{kaynak['ad']} çekiliyor...")
                try:
                    r = requests.get(kaynak['url'], timeout=15)
                    if r.status_code == 200:
                        f.write(f"\n\n# --- {kaynak['ad']} --- \n")
                        f.write(r.text)
                except:
                    print(f"{kaynak['ad']} alınamadı, atlanıyor.")

            # 2. ÖZEL SEYİRTUR SİTELERİ İÇİN ŞABLON EKLEME
            # Bu kısım o görseldeki 'TÜMÜ' dediğin siteleri TiviMate'e ekler
            f.write("\n\n# --- SEYIRTUR FILM SITELERI --- \n")
            
            siteler = [
                {"isim": "Film Makinesi", "slug": "filmmakinesi"},
                {"isim": "Film Modu", "slug": "filmmodu"},
                {"isim": "720p İzle", "slug": "izle720p"},
                {"isim": "Dizibox", "slug": "dizibox"}
            ]
            
            for site in siteler:
                # Bu linkler tıklandığında senin Worker'ına gider ve o 2438 satırlık kod çalışır
                f.write(f'#EXTINF:-1 group-title="SEYIRTUR", {site["isim"]}\n')
                f.write(f'{worker_url}/{site["slug"]}\n')

        print(f"İşlem tamam! {dosya_adi} güncellendi.")

    except Exception as e:
        print(f"Hata: {e}")

if __name__ == "__main__":
    film_listesini_guncelle()
