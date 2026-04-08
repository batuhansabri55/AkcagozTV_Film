def movies_etiketi_ekle():
    dosya_adi = "FilmDizi.m3u"
    
    with open(dosya_adi, "r", encoding="utf-8") as f:
        satirlar = f.readlines()

    yeni_satirlar = []
    for satir in satirlar:
        link = satir.strip()
        # Eğer satır bir linkse ve sonunda henüz MOVIES yoksa ekle
        if link.startswith("http") and "#/MOVIES/" not in link:
            # Linkin sonu / ile bitmiyorsa ekle, sonra etiketi yapıştır
            if not link.endswith("/"):
                link += "/"
            yeni_satirlar.append(link + "#/MOVIES/\n")
        else:
            yeni_satirlar.append(satir)

    # Dosyayı tamamen güncellenmiş haliyle tekrar yaz
    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.writelines(yeni_satirlar)
    
    print("Tüm listeye #/MOVIES/ etiketi çakıldı usta!")

if __name__ == "__main__":
    movies_etiketi_ekle()
