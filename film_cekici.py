import requests
import re

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

KAYNAKLAR = [
    {"ad": "Filmmodu", "url": "https://www.filmmodu.org", "tip": "web"},
    {"ad": "Filmmakinesi", "url": "https://www.filmmakinesi.net", "tip": "web"},
    {"ad": "Fanatik", "url": "https://tinyurl.com/FanatikplayFilm", "tip": "m3u"},
    {"ad": "Power", "url": "https://tinyurl.com/power-cinema", "tip": "m3u"}
]

def karakter_onari(metin):
    sozluk = {"Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş", "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö", "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ"}
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    return metin

def m3u_tara(url):
    veriler = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=30)
        lines = r.text.splitlines()
        temp_inf = ""
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF:"):
                temp_inf = karakter_onari(line)
            elif line.startswith("http") and temp_inf:
                # 1. DİZİ TESPİTİ
                is_series = re.search(r'(S\d{1,2}|E\d{1,2}|Bölüm|Sezon|\d\.\s*Bölüm|Part|Cilt)', temp_inf, re.I)
                clean_name = temp_inf.split(',')[-1].strip()

                if is_series:
                    # TiviMate'in dizi kütüphanesi için S01E01 yapısı şarttır
                    if not re.search(r'S\d{1,2}|E\d{1,2}', clean_name, re.I):
                        clean_name = f"{clean_name} S01 E01"
                    
                    # tvg-type="series" ve Kategori isminde 'Series' veya 'TV Shows' geçmeli
                    new_inf = f'#EXTINF:-1 tvg-type="series" group-title="SERIES (Dizi)",' + clean_name
                    new_line = f"{line}#.mkv"
                else:
                    # FİLMLER İÇİN:
                    new_inf = f'#EXTINF:-1 tvg-type="movie" group-title="MOVIES (Film)",' + clean_name
                    new_line = f"{line}#.mp4"

                veriler.append(f"{new_inf}\n{new_line}")
                temp_inf = ""
    except: pass
    return veriler

def web_tara(site_ad, url):
    filmler = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        matches = re.findall(r'<a href="(/film/[^"]+)" title="([^"]+)">', r.text)
        for link, isim in matches:
            full_url = f"{url}{link}" if not link.startswith("http") else link
            temiz_isim = karakter_onari(isim)
            # Webden gelenleri film (Movie) bölümüne at
            entry = f'#EXTINF:-1 tvg-type="movie" group-title="MOVIES | {site_ad.upper()}",{temiz_isim}\n{full_url}#.mp4'
            filmler.append(entry)
    except: pass
    return filmler

def main():
    output = []
    for kaynak in KAYNAKLAR:
        if kaynak["tip"] == "web":
            output.extend(web_tara(kaynak["ad"], kaynak["url"]))
        else:
            output.extend(m3u_tara(kaynak["url"]))

    with open(VOD_FILE, "w", encoding="utf-8") as f:
        # TiviMate'e bu listenin bir VOD listesi olduğunu X-TIVIMATE-VOD ile bildiriyoruz
        f.write('#EXTM3U x-tvg-url=""\n')
        for entry in output:
            f.write(entry + "\n")
    print("✅ TiviMate Zorlayıcı Format Hazır!")

if __name__ == "__main__":
    main()
