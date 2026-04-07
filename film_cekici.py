import requests
import re

VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def m3u_tara(url):
    veriler = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        lines = r.text.splitlines()
        temp_inf = ""
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF:"):
                temp_inf = line
            elif line.startswith("http") and temp_inf:
                # 1. DİZİ TESPİTİ (S01, Sezon, Bölüm kelimeleri)
                is_series = re.search(r'(S\d{1,2}|E\d{1,2}|Bölüm|Sezon|\d\.\s*Bölüm)', temp_inf, re.I)
                clean_name = temp_inf.split(',')[-1].strip()

                if is_series:
                    # TiviMate'in dizi kütüphanesine girmesi için 'tvg-type' ve 'S01 E01' şart
                    if not re.search(r'S\d{1,2}|E\d{1,2}', clean_name, re.I):
                        clean_name = f"{clean_name} S01 E01"
                    
                    # 'Series' etiketi TiviMate'i 'Diziler' sekmesine yönlendirir
                    new_inf = f'#EXTINF:-1 tvg-type="series" group-title="SERIES",' + clean_name
                    new_line = f"{line}#.mkv"
                else:
                    # Filmler için standart etiket
                    new_inf = f'#EXTINF:-1 tvg-type="movie" group-title="MOVIES",' + clean_name
                    new_line = f"{line}#.mp4"

                veriler.append(f"{new_inf}\n{new_line}")
                temp_inf = ""
    except: pass
    return veriler

def main():
    kaynaklar = ["https://tinyurl.com/FanatikplayFilm", "https://tinyurl.com/power-cinema"]
    output = []
    for k in kaynaklar:
        output.extend(m3u_tara(k))

    with open(VOD_FILE, "w", encoding="utf-8") as f:
        # --- BURASI KRİTİK: TiviMate'i VOD/SERIES moduna sokan başlık ---
        f.write('#EXTM3U x-tvg-url="" x-tivimate-vod="1"\n')
        for entry in output:
            f.write(entry + "\n")
    print("✅ TiviMate kütüphane modu aktif edildi.")

if __name__ == "__main__":
    main()
