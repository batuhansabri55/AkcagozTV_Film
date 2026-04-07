import requests
import re

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

KAYNAKLAR = [
    {"ad": "Filmmodu", "url": "https://www.filmmodu.org", "tip": "web"},
    {"ad": "Filmmakinesi", "url": "https://www.filmmakinesi.net", "tip": "web"},
    {"ad": "Fanatik", "url": "https://tinyurl.com/FanatikplayFilm", "tip": "m3u"},
    {"ad": "Power", "url": "https://tinyurl.com/power-cinema", "tip": "m3u"}
]

def karakter_onari(metin):
    sozluk = {
        "Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş", "Д±": "ı", "Д°": "İ",
        "Г¶": "ö", "Г–": "Ö", "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ", "Д\x9e": "Ğ",
        "Ð": "Ğ", "Ý": "İ", "þ": "ş", "ý": "ı", "ð": "ğ"
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    return metin

def web_tara(site_ad, url):
    filmler = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        matches = re.findall(r'<a href="(/film/[^"]+)" title="([^"]+)">', r.text)
        for link, isim in matches:
            full_url = f"{url}{link}" if not link.startswith("http") else link
            temiz_isim = karakter_onari(isim)
            # Webden gelenler genellikle film olduğu için direkt film etiketi ekliyoruz
            entry = f'#EXTINF:-1 tvg-type="movie" group-title="SİNEMA | {site_ad.upper()}",{temiz_isim}\n{full_url}#.mp4'
            filmler.append(entry)
    except: pass
    return filmler

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
                # Dizi tespiti (Sezon, Bölüm veya S01E01 gibi ifadeler)
                is_series = re.search(r'(S\d{1,2}|E\d{1,2}|Bölüm|Sezon|\d\.\s*Bölüm)', temp_inf, re.I)
                
                g_match = re.search(r'group-title="([^"]+)"', temp_inf)
                mevcut_g = g_match.group(1) if g_match else "Genel"
                
                stream_link = line
                if is_series:
                    # DİZİ ETİKETİ: tvg-type="series" ekliyoruz
                    temp_inf = re.sub(r'#EXTINF:(-1|0)', '#EXTINF:-1 tvg-type="series"', temp_inf)
                    temp_inf = re.sub(r'group-title="([^"]+)"', f'group-title="DİZİ | {mevcut_g}"', temp_inf)
                    if not any(stream_link.endswith(ext) for ext in [".mp4", ".mkv", ".m3u8"]):
                        stream_link = f"{stream_link}#.mkv"
                else:
                    # FİLM ETİKETİ: tvg-type="movie" ekliyoruz
                    temp_inf = re.sub(r'#EXTINF:(-1|0)', '#EXTINF:-1 tvg-type="movie"', temp_inf)
                    temp_inf = re.sub(r'group-title="([^"]+)"', f'group-title="SİNEMA | {mevcut_g}"', temp_inf)
                    if not any(stream_link.endswith(ext) for ext in [".mp4", ".mkv", ".m3u8"]):
                        stream_link = f"{stream_link}#.mp4"
                
                veriler.append(f"{temp_inf}\n{stream_link}")
                temp_inf = ""
    except: pass
    return veriler

def main():
    print("🚀 AkçagözTV VOD & Dizi Ayırıcı Başlatıldı...")
    output = []

    for kaynak in KAYNAKLAR:
        print(f"🔎 {kaynak['ad']} taranıyor...")
        if kaynak["tip"] == "web":
            output.extend(web_tara(kaynak["ad"], kaynak["url"]))
        else:
            output.extend(m3u_tara(kaynak["url"]))

    with open(VOD_FILE, "w", encoding="utf-8") as f:
        # TiviMate'in listeyi VOD olarak tanıması için header'a x-tvg-url ekliyoruz
        f.write("#EXTM3U x-tvg-url=\"\"\n")
        for entry in output:
            f.write(entry + "\n")

    print(f"✅ Bitti! {len(output)} içerik kategorize edildi.")

if __name__ == "__main__":
    main()
