import requests

def guncelle():
    dosya = "FilmDizi.m3u"
    
    # 1. Kaynak URL'leri
    kaynaklar = {
        "POWER CINEMA": "https://tinyurl.com/power-cinema",
        "ZERK FILM": "https://raw.githubusercontent.com/Zerk1903/zerkfilm/refs/heads/main/Filmler.m3u"
    }

    # 2. Mevcut dosyayı oku ve temizle
    try:
        with open(dosya, "r", encoding="utf-8") as f:
            satirlar = f.readlines()
    except FileNotFoundError:
        satirlar = ["#EXTM3U\n"]

    temiz_liste = []
    for s in satirlar:
        satir = s.strip()
        if not satir: continue
        if satir.startswith("http"):
            link = satir.split("#")[0].rstrip("/")
            temiz_liste.append(f"{link}/#/movies/\n")
        else:
            temiz_liste.append(satir + "\n")

    # 3. Dış kaynakları çek ve formatla ekle
    ek_icerik = ""
    for isim, url in kaynaklar.items():
        try:
            print(f"{isim} çekiliyor...")
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                ek_icerik += f"\n# --- {isim} ---\n"
                for p_satir in response.text.splitlines():
                    ps = p_satir.strip()
                    if not ps: continue
                    if ps.startswith("http"):
                        p_link = ps.split("#")[0].rstrip("/")
                        ek_icerik += f"{p_link}/#/movies/\n"
                    else:
                        # #EXTINF satırlarını olduğu gibi ama temiz al
                        ek_icerik += ps + "\n"
        except Exception as e:
            print(f"{isim} alınırken hata oluştu: {e}")

    # 4. Dosyayı kaydet
    with open(dosya, "w", encoding="utf-8") as f:
        f.writelines(temiz_liste)
        f.write(ek_icerik)
    
    print("Güncelleme başarıyla tamamlandı usta.")

if __name__ == "__main__":
    guncelle()
