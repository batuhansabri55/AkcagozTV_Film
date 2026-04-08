import requests

def sadece_power_ve_movies():
    dosya = "FilmDizi.m3u"
    
    # 1. Power Cinema'yı al
    power = requests.get("https://tinyurl.com/power-cinema").text

    # 2. Mevcut dosyadaki linkleri temizle (Fazlalıkları sil, tek format yap)
    with open(dosya, "r", encoding="utf-8") as f:
        satirlar = f.readlines()

    yeni_liste = []
    for s in satirlar:
        if s.startswith("http"):
            link = s.split("#")[0].strip().rstrip("/")
            yeni_liste.append(f"{link}/#/MOVIES/\n")
        else:
            yeni_liste.append(s)

    # 3. Power Cinema'yı da aynı formatta sona ekle
    power_temiz = ""
    for satir in power.splitlines():
        if satir.startswith("http"):
            l = satir.split("#")[0].strip().rstrip("/")
            power_temiz += f"{l}/#/MOVIES/\n"
        else:
            power_temiz += satir + "\n"

    # 4. Dosyayı jilet gibi yaz
    with open(dosya, "w", encoding="utf-8") as f:
        f.writelines(yeni_liste)
        f.write("\n# --- POWER CINEMA ---\n")
        f.write(power_temiz)

if __name__ == "__main__":
    sadece_power_ve_movies()
