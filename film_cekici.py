import requests

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

# Senin görselde gösterdiğin o "On Numara" kaynak
VIP_KAYNAK = "http://electranextssp.xyz:8080/get.php?username=DenizTurkan2&password=de7mdR8q&type=m3u_plus"

# Arşiv kaynakların
DIGER_KAYNAKLAR = [
    "https://tinyurl.com/2ys5fe3h",
    "https://tinyurl.com/2ao2rans"
]

def karakter_onari(metin):
    """Bozuk karakterleri senin sözlüğüne göre düzeltir"""
    sozluk = {"Гü": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş", "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö", "Г§": "ç"}
    for b, d in sozluk.items(): metin = metin.replace(b, d)
    return metin

def main():
    m3u_output = "#EXTM3U\n"
    eklenen_urller = set()
    butun_kaynaklar = [VIP_KAYNAK] + DIGER_KAYNAKLAR

    for kaynak in butun_kaynaklar:
        try:
            print(f"📡 Kaynak taranıyor: {kaynak[:40]}...")
            r = requests.get(kaynak, headers=HEADERS, timeout=20)
            if not r.ok: continue
            
            lines = r.text.split("\n")
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    info = karakter_onari(lines[i])
                    url = lines[i+1].strip() if (i+1) < len(lines) else ""
                    
                    if url and url.startswith("http") and url not in eklenen_urller:
                        # "Konuşanlar" gibi içerikleri grubuna göre işaretleyebiliriz
                        if "Konusanlar" in info:
                            info = info.replace("group-title=\"", "group-title=\"🌟 ÖZEL GÜNCEL|")
                        
                        m3u_output += f"{info}\n{url}\n"
                        eklenen_urller.add(url)
        except: continue

    with open(VOD_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_output)
    print("✅ Operasyon Tamam! TiviMate'i yenileyebilirsin.")

if __name__ == "__main__":
    main()
