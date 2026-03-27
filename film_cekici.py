import requests
import re

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

# 1. VIP KAYNAK (Senin verdiğin ve Konuşanlar olan link)
VIP_KAYNAK = "http://electranextssp.xyz:8080/get.php?username=DenizTurkan2&password=de7mdR8q&type=m3u_plus"

# 2. DİĞER SABİT ARŞİV KAYNAKLARI
VOD_KAYNAKLAR = [
    VIP_KAYNAK,
    "https://tinyurl.com/2ys5fe3h",
    "https://tinyurl.com/2ao2rans",
    "https://tinyurl.com/power-cinema"
]

def karakter_onari(metin):
    """Bozuk karakterleri senin sözlüğüne göre düzeltir"""
    sozluk = {
        "Гü": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş",
        "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö",
        "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ"
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    return metin

def dinamik_link_avla():
    """Deathless kanalından günün sürpriz linkini de getirir"""
    target_url = "https://telemetr.io/en/channels/1571593743-WyjV90VuVbs5YTFk"
    try:
        r = requests.get(target_url, headers=HEADERS, timeout=10)
        if r.ok:
            found = re.findall(r'https://bit.ly/[\w-]+', r.text)
            if found: return found[0]
    except: pass
    return None

def main():
    print("🚀 VIP Operasyon Başladı...")
    
    # Telegram'dan gelen taze linki de havuzun sonuna ekleyelim
    taze_ekstra = dinamik_link_avla()
    if taze_ekstra:
        VOD_KAYNAKLAR.append(taze_ekstra)

    m3u_output = "#EXTM3U\n"
    eklenen_urller = set()
    sayac = 0

    for kaynak in VOD_KAYNAKLAR:
        try:
            print(f"📡 taranıyor: {kaynak[:30]}...")
            r = requests.get(kaynak, headers=HEADERS, timeout=20)
            if not r.ok: continue
            
            lines = r.text.split("\n")
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    info = karakter_onari(lines[i])
                    url = lines[i+1].strip() if (i+1) < len(lines) else ""
                    
                    if url and url.startswith("http") and url not in eklenen_urller:
                        # Eğer VIP kaynaktaysak, 'Konuşanlar' gibi kelimeleri öne çıkarabiliriz
                        m3u_output += f"{info}\n{url}\n"
                        eklenen_urller.add(url)
                        sayac += 1
        except:
            continue

    with open(VOD_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_output)
    
    print(f"✅ İşlem Tamam! {sayac} adet içerik listeye eklendi.")

if __name__ == "__main__":
    main()
