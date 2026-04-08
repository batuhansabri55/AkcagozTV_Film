import requests

def guncelle():
    dosya = "FilmDizi.m3u"
    
    # 1. Power Cinema'yı al
    try:
        power = requests.get("https://tinyurl.com/power-cinema", timeout=10).text
    except:
        power = ""

    # 2. Dosyayı oku ve her linkin sonunu sadece #/movies/ yap
    with open(dosya, "r", encoding="utf-8") as f:
        satirlar = f.readlines()

    temiz_liste = []
    for s in satirlar:
        satir = s.strip()
        if satir.startswith("http"):
            # Linkin sonundaki her şeyi temizle, sadece küçük harf ekle
            link = satir.split("#")[0].rstrip("/")
            temiz_liste.append(f"{link}/#/movies/\n")
        else:
            temiz_liste.append(s if s.endswith("\n") else s + "\n")

    # 3. Power Cinema'yı da aynı formatta sona ekle
    power_ekle = "\n# --- POWER CINEMA ---\n"
    for p_satir in power.splitlines():
        ps = p_satir.strip()
        if ps.startswith("http"):
            p_link = ps.split("#")[0].rstrip("/")
            power_ekle += f"{p_link}/#/movies/\n"
        else:
            power_ekle += ps + "\n"

    # 4. Dosyayı kaydet
    with open(dosya, "w", encoding="utf-8") as f:
        f.writelines(temiz_liste)
        f.write(power_ekle)

if __name__ == "__main__":
    guncelle()
