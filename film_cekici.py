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
                # DİZİ TESPİTİ
                is_series = re.search(r'(S\d{1,2}|E\d{1,2}|Bölüm|Sezon|\d\.\s*Bölüm)', temp_inf, re.I)
                clean_name = temp_inf.split(',')[-1].strip()

                if is_series:
                    # KRİTİK: TiviMate'e bu kanalın bir "Dizi" (TV Show) olduğunu zorla öğretiyoruz
                    # 'type="series"' ve 'group-id' ekliyoruz
                    new_inf = f'#EXTINF:-1 tvg-id="dizi" tvg-type="series" group-title="SERIES",' + clean_name
                    # Linkin sonuna sanal mkv (oynatıcıyı dizi moduna sokar)
                    new_line = f"{line}#.mkv"
                else:
                    new_inf = f'#EXTINF:-1 tvg-id="film" tvg-type="movie" group-title="MOVIES",' + clean_name
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
        # EN ÖNEMLİ SATIR: TiviMate'e listenin tipini M3U olarak bırakmasını söylüyoruz
        f.write("#EXTM3U\n")
        for entry in output:
            f.write(entry + "\n")
    print("✅ TiviMate için grup başlıkları 'SERIES' ve 'MOVIES' olarak güncellendi.")

if __name__ == "__main__":
    main()
