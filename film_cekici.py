import requests
import re

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.google.com/'
}

# parsers.js'deki en popüler kaynaklar
KAYNAKLAR = [
    {"ad": "Filmmodu", "url": "https://www.filmmodu.org", "tip": "web"},
    {"ad": "Filmmakinesi", "url": "https://www.filmmakinesi.net", "tip": "web"},
    {"ad": "Fanatik", "url": "https://tinyurl.com/FanatikplayFilm", "tip": "m3u"},
    {"ad": "Power", "url": "https://tinyurl.com/power-cinema", "tip": "m3u"}
]

def karakter_onari(metin):
    """Parsers.js'deki bozuk karakter temizleme mantığı"""
    sozluk = {
        "Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş", "Д±": "ı", "Д°": "İ",
        "Г¶": "ö", "Г–": "Ö", "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ", "Д\x9e": "Ğ",
        "Ð": "Ğ", "Ý": "İ", "þ": "ş", "ý": "ı", "ð": "ğ"
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    return metin

def web_tara(site_ad, url):
    """parsers.js içindeki regex mantığıyla siteleri tarar"""
    filmler = []
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        # Sitedeki film linklerini yakala (parsers.js regex'i gibi)
        matches = re.findall(r'<a href="(/film/[^"]+)" title="([^"]+)">', r.text)
        
        for link, isim in matches:
            full_url = f"{url}{link}" if not link.startswith("http") else link
            temiz_isim = karakter_onari(isim)
            entry = f'#EXTINF:-1 group-title="SİNEMA | {site_ad.upper()}",{temiz_isim}\n{full_url}'
            filmler.append(entry)
    except: pass
    return filmler

def m3u_tara(url):
    """Mevcut m3u linklerini kategorize eder"""
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
                # Dizi/Film ayrımı
                is_series = re.search(r'(S\d{1,2}|E\d{1,2}|Bölüm|Sezon)', temp_inf, re.I)
                g_match = re.search(r'group-title="([^"]+)"', temp_inf)
                mevcut_g = g_match.group(1) if g_match else "Genel"
                prefix = "DİZİ" if is_series else "SİNEMA"
                
                temp_inf = re.sub(r'group-title="([^"]+)"', f'group-title="{prefix} | {mevcut_g}"', temp_inf)
                veriler.append(f"{temp_inf}\n{line}")
                temp_inf = ""
    except: pass
    return veriler

def main():
    print("🚀 AkçagözTV VOD Avcısı Başlatıldı...")
    output = []

    for kaynak in KAYNAKLAR:
        print(f"🔎 {kaynak['ad']} taranıyor...")
        if kaynak["tip"] == "web":
            output.extend(web_tara(kaynak["ad"], kaynak["url"]))
        else:
            output.extend(m3u_tara(kaynak["url"]))

    # Sonuçları Kaydet
    with open(VOD_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for entry in output:
            f.write(entry + "\n")

    print(f"✅ Bitti! {len(output)} film/dizi listelendi.")

if __name__ == "__main__":
    main()
