import requests
import re
import os

# --- AYARLAR ---
VOD_FILE = "FilmDizi.m3u"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}

# Sabit, kemikleşmiş kaynakların
VOD_KAYNAKLAR = [
    "https://tinyurl.com/2ys5fe3h",
    "https://tinyurl.com/2ao2rans",
    "https://tinyurl.com/power-cinema"
]

def karakter_onari(metin):
    """Görseldeki sözlük mantığıyla isimleri düzeltir"""
    sozluk = {
        "Гј": "ü", "Гњ": "Ü", "Еџ": "ş", "Ећ": "Ş",
        "Д±": "ı", "Д°": "İ", "Г¶": "ö", "Г–": "Ö",
        "Г§": "ç", "Г‡": "Ç", "Дџ": "ğ", "Д4": "Ğ"
    }
    for bozuk, duzgun in sozluk.items():
        metin = metin.replace(bozuk, duzgun)
    return metin

def dinamik_link_avla():
    """Telemetr üzerinden her gün değişen o 'On Numara' linki yakalar"""
    print("🔍 Güncel link avlanıyor...")
    target_url = "https://telemetr.io/en/channels/1571593743-WyjV90VuVbs5YTFk"
    try:
        r = requests.get(target_url, headers=HEADERS, timeout=15)
        if r.ok:
            # Sayfadaki bit.ly kısaltmalarını bulur (image_f6353a.png'deki gibi)
            found = re.findall(r'https://bit.ly/[\w-]+', r.text)
            if found:
                # En güncel linki (ilk sıradaki) döndürür
                print(f"✅ Av Başarılı! Yeni Kaynak: {found[0]}")
                return found[0]
    except:
        print("⚠️ Kanal sayfasına ulaşılamadı, sabit listelerle devam ediliyor.")
    return None

def main():
    print("🚀 Operasyon Başladı...")
    
    # Her sabah değişen taze linki listeye ekle
    taze_link = dinamik_link_avla()
    if taze_link:
        VOD_KAYNAKLAR.insert(0, taze_link) # En başa ekle ki öncelikli olsun

    toplam_icerik = 0
    m3u_output = "#EXTM3U\n"
    eklenen_urller = set()

    for kaynak in VOD_KAYNAKLAR:
        try:
            r = requests.get(kaynak, headers=HEADERS, timeout=20)
            if not r.ok: continue
            
            lines = r.text.split("\n")
            for i in range(len(lines)):
                if lines[i].startswith("#EXTINF"):
                    info = karakter_onari(lines[i])
                    url = lines[i+1].strip() if (i+1) < len(lines) else ""
                    
                    if url and url.startswith("http") and url not in eklenen_urller:
                        # "Konuşanlar", "Hayrettin" gibi özel serileri ayırabiliriz
                        m3u_output += f"{info}\n{url}\n"
                        eklenen_urller.add(url)
                        toplam_icerik += 1
        except:
            continue

    with open(VOD_FILE, "w", encoding="utf-8") as f:
        f.write(m3u_output)
    
    print(f"✅ Bitti! Toplam {toplam_icerik} içerik hazırlandı.")

if __name__ == "__main__":
    main()
